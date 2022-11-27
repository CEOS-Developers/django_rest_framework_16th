#!/bin/sh

python manage.py collectstatic --no-input
python manage.py makemigrations api
python manage.py migrate

exec "$@"