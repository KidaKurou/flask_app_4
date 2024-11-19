from prometheus_flask_exporter import PrometheusMetrics
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache
import logging
import os
logging.basicConfig(level = logging.DEBUG)

app = Flask(__name__)
POSTGRES_HOST = os.getenv('POSTGRES_HOST', '127.0.0.1')
POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', '5432'))
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://user:password@{POSTGRES_HOST}:{POSTGRES_PORT}/flask_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] = os.getenv('REDIS_HOST', '127.0.0.1')
app.config['CACHE_REDIS_PORT'] = int(os.getenv('REDIS_PORT', '6379'))
app.config['CACHE_REDIS_DB'] = 0
app.config['CACHE_REDIS_URL'] = f"redis://{app.config['CACHE_REDIS_HOST']}:{app.config['CACHE_REDIS_PORT']}/0"

cache = Cache(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db) # Инициализация Flask-Migrate
metrics = PrometheusMetrics(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    def __repr__(self):
        return f'<User {self.username}>'

# Создание нового пользователя
@app.route('/users', methods=['POST'])
def create_user():
    cache.clear()
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'})
# Получение всех пользователей
@app.route('/users', methods=['GET'])
@cache.cached(timeout = 60)
def get_users():
    users = User.query.all()
    users_list = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
    return jsonify(users_list)
# Обновление пользователя
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    data = request.get_json()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    cache.clear()
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})
# Удаление пользователя
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    cache.clear()
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})
# healthcheck
@app.route('/health')
def health_check():
    return jsonify(status = 'OK'), 200

# if __name__ == '__main__':
#     app.run(host = '0.0.0.0', port = 5000)
