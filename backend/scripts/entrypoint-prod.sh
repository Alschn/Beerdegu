#!/bin/bash
python3 backend/manage.py makemigrations --no-input
python3 backend/manage.py migrate --no-input

cd backend
daphne -b 0.0.0.0 -p $PORT core.asgi:application -v2
