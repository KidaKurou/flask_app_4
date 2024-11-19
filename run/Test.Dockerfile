FROM python:3.9-alpine AS test

RUN mkdir -p /app/src/ /app/log/

WORKDIR /app/src/

COPY ../src/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ../src/ .

CMD ["pytest", "tests/"]