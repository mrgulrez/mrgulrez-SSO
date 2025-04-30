#!/bin/bash
cd app_project
python manage.py makemigrations main_app
python manage.py migrate
python manage.py runserver 8001