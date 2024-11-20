FROM python:3.9-alpine AS test

RUN mkdir -p /app/src/ /app/log/

RUN adduser -D user

WORKDIR /app/src/

COPY ../src/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ../src/ .

RUN chown -R user:user /app
USER user

ENV PYTHONPATH=/app/src

CMD ["pytest", "tests"]