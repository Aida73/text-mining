#!/bin/sh

#until cd /app
# do
#     echo "Waiting for server volume..."
# done


# until python manage.py migrate
# do
#     echo "Waiting for db to be ready..."
#     sleep 2
# done


python /app/manage.py collectstatic --noinput

# python manage.py createsuperuser --noinput

gunicorn dq_project.wsgi --bind 0.0.0.0:8000 --workers 4 --threads 4

# for debug
python /app/manage.py runserver 0.0.0.0:8000