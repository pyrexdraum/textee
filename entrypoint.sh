#!/bin/sh
set -e

python manage.py collectstatic --no-input
python manage.py migrate --no-input
gunicorn config.wsgi -b 0:8000 --workers 2

exec "$@"