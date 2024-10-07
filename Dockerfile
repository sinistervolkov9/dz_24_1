FROM python

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

RUN apt-get update && apt-get install -y redis-server

EXPOSE 8000

CMD ["sh", "-c", "redis-server & celery -A config beat -l info & celery -A config worker -l info -P gevent & python manage.py runserver 0.0.0.0:8000"]
