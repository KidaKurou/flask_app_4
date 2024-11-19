FROM python:3.9-alpine AS test

RUN mkdir -p /app/src/
RUN mkdir -p /app/log/

WORKDIR /app/src/
COPY src/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src/test.py test.py
COPY src/app.py app.py
# CMD ["pytest", "test_user_service.py"]
