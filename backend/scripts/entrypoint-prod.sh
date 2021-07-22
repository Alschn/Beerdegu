#!/bin/bash
cd backend
python3 manage.py makemigrations --no-input
python3 manage.py migrate --no-input

script="
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD');
    print('Superuser created.');
else:
    print('Superuser creation skipped.');
"
printf "$script" | python manage.py shell

daphne -b 0.0.0.0 -p $PORT core.asgi:application -v2
