FROM python:3.11-slim

RUN mkdir app
WORKDIR app

COPY requirements /app/requirements
RUN pip install -r requirements/prod.txt

COPY . /app/

CMD python manage.py makemigrations \
    && python manage.py migrate \
    && python scripts/create_superuser.py \
    && python manage.py collectstatic --noinput \
    && gunicorn blog.wsgi:application --env DJANGO_SETTINGS_MODULE=blog.settings.prod --bind 0.0.0.0:8000 \
    --access-logfile - --error-logfile -
