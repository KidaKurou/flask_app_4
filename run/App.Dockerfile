FROM python:3.9-alpine AS production

# Создаем рабочий каталог
RUN mkdir -p /app/src/ /app/log/

# Добавляем пользователя
RUN adduser -D user

# Устанавливаем рабочий каталог
WORKDIR /app/src/

# Копируем зависимости
COPY ../src/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем приложение
COPY ../src/ .

# Передаем права на выполнение
RUN chown -R user:user /app
USER user

# Запускаем приложение через Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app", "--timeout", "120"]
