<div align="center" style="padding-bottom: 20px">
    <h1>Beerdegu</h1>
    <img src="https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white" alt=""/>
    <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt=""/>
    <img src="https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white" alt=""/>
    <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt=""/>
    <img src="https://img.shields.io/badge/Vite-B73BFE?style=for-the-badge&logo=vite&logoColor=FFD62E" alt=""/>    
    <img src="https://img.shields.io/badge/Sass-CC6699?style=for-the-badge&logo=sass&logoColor=white" alt=""/>
    <img src="https://img.shields.io/badge/MUI-0081CB?style=for-the-badge&logo=mui&logoColor=white" alt=""/>
    <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt=""/>
    <img src="https://img.shields.io/badge/Redis-%23DD0031.svg?&style=for-the-badge&logo=redis&logoColor=white" alt=""/>
    <img src="https://img.shields.io/badge/Docker-008FCC?style=for-the-badge&logo=docker&logoColor=white" alt=""/>
    <img src="https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white" alt=""/>    
    <img src="https://img.shields.io/badge/Fly.io-7B36ED?style=for-the-badge&logo=fly.io&logoColor=white" alt=""/>&nbsp;
</div>

Beerdegu is a real-time web application meant for beer tasting sessions, when
you and your friends are rating every consumed beer (color, smell, taste etc.).

Built with Django Channels, Django Rest Framework, React with Typescript,
Postgres, Redis in a Dockerized environment
with an option to deploy to Heroku. Running development setup
without docker-compose is also possible.

### Tools, libraries, frameworks:

This setup has been tested with Python 3.10 and Node 16.

### Backend

- Django 4.2 + Django Rest Framework : `django` `djangorestframework`
- Django Channels 4 : `channels`- handling websockets backend
- `django-extensions` - django utilities
- `django-cors-headers` - handling cross-origin requests
- `django-filter` - filter backend for drf views
- `django-q` - async task queue
- `django-import-export` - data import/export in admin panel
- `django-allauth`, `dj-rest-auth`, `djangorestframework-simplejwt` - authentication (jwt, google)
- `django-sesame` - websockets token authentication
- `openpyxl` - excel reports generation
- `drf-spectacular` - OpenAPI schema generation
- `coverage` - for code coverage reports and running unit tests
- `mypy` + `djangorestframework-stubs` - for better typing experience
- `psycopg2` - needed to use Postgres (in Docker container)
- `channels_redis`, `redis` - connection to Redis database service
- `whitenoise` - building static files
- `daphne` - production asgi server

### Frontend (deprecated)

- React 18
- Typescript
- `react-use-websocket` - websocket client, connects with ws backend
- `@mui/material`, `@mui/icons-material`, `@mui/lab`, - Material UI library
- `sass` - enables scss/sass support
- `axios` - http client
- `@tanstack/react-query` - client-side data fetching and caching
- `react-infinite-scroll-component` - infinite scroll
- `react-toastify` - toast notifications
- `vitest`, `@testing-library/react` + other packages - unit testing
- `msw` - mocking http requests in tests

# Development setup

## Without Docker

### Backend

Create a virtual environment from cmd (or do it in Pycharm manually)

```shell script
cd backend

python -m pip install --upgrade pip

pipenv install

pipenv shell
```

Run django application from cmd (or add new Django configuration if using Pycharm)

```shell script
python manage.py runserver
```

Preparing (if there are any changes to db schema) and running migrations

```shell script
python manage.py makemigrations

python manage.py migrate
```

Create superuser

```shell script
python manage.py createsuper user
```

### Frontend

You need to provide `VITE_WEBSOCKET_URL` and `VITE_BACKEND_URL` environment variables.

Install node dependencies.

```shell script
cd frontend

yarn install
```

Run development server in second terminal

```shell script
yarn dev
```

### Backend tests coverage

```shell script
cd backend
```

Run tests using Coverage instead of `python manage.py test`

```shell script
coverage run manage.py test
```

Get report from coverage:

```shell script
coverage report -m
```

## With Docker

First create `env` folder in **root directory** with following env files:

`env/postgres.env`

```dotenv
# credentials to postgres database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
```

`env/backend.env`

```dotenv
DJANGO_SETTINGS_MODULE=core.settings.dev
SECRET_KEY=...
# same values as in postgres.env
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
# same as in docker-compose.yml
DB_HOST=postgres_db
DB_PORT=5432
# same as in docker-compose.yml
REDIS_HOST=redis_db
REDIS_PORT=6379
# if you want to use mailing functionality e.g with smtp backend
EMAIL_HOST=...
EMAIL_PORT=...
EMAIL_USER=...
EMAIL_PASSWORD=...
# Google auth - configured in Google Cloud Platform
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
GOOGLE_CLIENT_REDIRECT_URI=...
# Site object's name in Django admin - needed for building links to frontend
# e.g. when sending email with password reset link or activation link
FRONTEND_SITE_NAME=beerdegu
```

`env/redis.env`

```dotenv
TZ=Europe/Warsaw
```

`env/frontend.env`

```dotenv
# required for hot reloading to work in docker
CHOKIDAR_USEPOLLING=true
WATCHPACK_POLLING=true

NODE_ENV=development

# in format:  PROTOCOL://HOST:PORT without trailing slash!
# variable names have to be prefixed with VITE_
VITE_WEBSOCKET_URL=ws://127.0.0.1:8000
VITE_BACKEND_URL=http://127.0.0.1:8000
```

Make sure Docker Engine is running.

While in **root directory**, build docker images and run them with docker-compose. This might take up to few minutes.
Rebuilding image is crucial after installing new packages via pip or npm.

```shell script
docker-compose up --build
```

Application should be up and running: backend `127.0.0.1:8000`, frontend `127.0.0.1:3000`.

If images had been installed and **no additional packages have been installed**, just run to start containers:

```shell script
docker-compose up
```

Bringing down containers with **optional** -v flag removes **all** attached volumes and invalidates caches.

```shell script
docker-compose down
```

To run commands in active container:

```shell script
docker exec -it CONTAINER_ID bash
```

Rebuilding individual containers instead of all of them

```shell
docker-compose build CONTAINER_NAME
```

If there are problems caused by caching, then you can use optional flag to build container without Docker's cache

```shell
docker-compose build CONTAINER_NAME --no-cache
```

## Accessing backend from mobile app (BeerdeguMobile):

Add your local ip4 address to existing `ALLOWED_HOSTS` list in `backend/core/settings/dev.py` file.
You can retrieve it by running `ipconfig` in terminal and looking for `IPv4 Address`.

```python
ALLOWED_HOSTS = ["backend", "localhost", "127.0.0.1", "YOUR_IP_ADDRESS"]
```

# Production Deployment

## Fly.io

Launch a new app

```shell
fly launch
```

Set secrets: `PRODUCTION_HOST`, `SECRET_KEY`, `REDIS_URL`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USER`, `EMAIL_PASSWORD`,
`GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_CLIENT_REDIRECT_URI`, `FRONTEND_SITE_NAME`

```shell
fly secrets set KEY=VALUE
```

Create postgres and redis addons

```shell
fly pg create
```

```shell
fly redis create
```

Attach postgres instance to the app (it will automatically set `DATABASE_URL` env variable)

```shell
fly pg attach -a <postgres_app_name>
```

Deploy the app

Include `API_URL`, `WEBSOCKETS_URL` build args to make frontend work

```shell
fly deploy --build-arg API_URL=https://beerdegu.fly.dev --build-arg WEBSOCKETS_URL=wss://beerdegu.fly.dev
```

Connecting to app instance (e.g to create superuser)

```shell
fly ssh console
```

## Heroku (deprecated)

1) [Create Heroku Account](https://signup.heroku.com/dc)
2) [Download/Install/Setup Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install)
    - After install, log into Heroku CLI: `heroku login`
3) Run: `heroku create <app name>` to create the Heroku application
4) Set your environment variables for your production environment by running:
   ```bash
   heroku config:set KEY=VALUE
   ```
   Or in the Heroku dashboard, go to Settings > Config Vars and add the variables there.  
   Variables to set: `DJANGO_SETTINGS_MODULE=core.settings.prod` `DJANGO_SUPERUSER_EMAIL`,
   `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_PASSWORD`, `PRODUCTION_HOST=<app name>.herokuapp.com`,
   `SECRET_KEY`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USER`, `EMAIL_PASSWORD`
5) Run: `heroku stack:set container` so Heroku knows this is a containerized application
6) Run: `heroku addons:create heroku-postgresql:hobby-dev` which creates the postgres add-on for Heroku
7) Run: `heroku addons:create heroku-redis:hobby-dev` which creates the redis add-on for Heroku
8) Deploy app by running: `git push heroku master`,  
   *or* manually in Heroku dashboard  
   *or* by pushing to your github repository, having Automatic Deploys set up
9) Go to `<app name>.herokuapp.com` to see the published website.

## CI

This repository uses Github Actions to run test pipeline.  
`tests.yml` - runs backend and frontend as separate jobs in one workflow

# To do list (backend)

- [ ] User profile with list of past beer tasting sessions and statistics
- [ ] Test async db utils and consumer
- [ ] Task queue with Django Q - e.g. removing inactive users in rooms
- [ ] Improve xlsx reports (headers styling, better formatting, etc.)
