#!/usr/bin/env bash

set -e

rm -f db.sqlite3
rm -r main/migrations
python manage.py makemigrations main
python manage.py migrate
python manage.py createsuperuser
python manage.py db_seed
