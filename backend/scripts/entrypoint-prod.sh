#!/bin/bash
cd backend

python3 manage.py migrate --no-input

script="
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD');
    print('Superuser created!');
else:
    print('Superuser creation skipped!');
"

printf "$script" | python manage.py shell
