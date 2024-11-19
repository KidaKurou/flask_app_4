import json

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hello' in response.data

def test_data_page(client):
    response = client.get('/data')
    assert response.status_code == 200
    assert b'This is some data!' in response.data

# Check cache clear
def test_clear_cache(client):
    response = client.post('/users/cache/clear', json={'user_id': 1})
    assert response.status_code == 200
    assert response.json == {'message': 'Cache cleared'}

# Check create new user
def test_create_user(client):
    user = client.get('/users/1')
    if user.status_code == 404:
        response = client.post('/users', json={'username': 'test', 'email': 'L5eG8@example.com'})
        assert response.status_code == 201
        assert response.json == {'username': 'test', 'email': 'L5eG8@example.com'}

def test_get_users(client):
    response = client.get('/users')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list) # Проверяем, что ответ является списком

def test_user_not_found(client):
    response = client.get('/users/999')
    assert response.status_code == 404
    assert response.json == {'error': 'Not Found'}
