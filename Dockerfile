FROM python:3.11-slim

RUN mkdir app
WORKDIR app

ADD requirements.txt /app/
RUN pip install -r requirements.txt

ADD . /app/
ADD .env.docker /app/.env

CMD python manage.py collectstatic \
    && gunicorn blog.wsgi:application -b 0.0.0.0:8000