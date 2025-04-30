#!/bin/bash
cd auth_project
python manage.py makemigrations authentication
python manage.py migrate
python manage.py runserver 8000