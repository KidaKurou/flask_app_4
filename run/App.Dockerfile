FROM python:3.9-alpine AS production

RUN mkdir -p /app/src/
RUN mkdir -p /app/log/
RUN adduser -D user

WORKDIR /app/src/
COPY src/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src/run.py run.py
RUN chown -R user:user /app
USER user

CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]
