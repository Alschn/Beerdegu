#!/bin/bash
python3 backend/manage.py makemigrations --no-input
python3 backend/manage.py migrate --no-input

daphne -b 0.0.0.0 -p 8001 backend.core.asgi:application
