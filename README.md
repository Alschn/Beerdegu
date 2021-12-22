
<div align="center" style="padding-bottom: 20px">
    <h1>Beerdegu</h1>
    <img src="https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white" alt=""/>
    <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt=""/>
    <img src="https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white" alt=""/>
    <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt=""/>
    <img src="https://img.shields.io/badge/Sass-CC6699?style=for-the-badge&logo=sass&logoColor=white" alt=""/>
    <img src="https://img.shields.io/badge/MUI-0081CB?style=for-the-badge&logo=mui&logoColor=white" alt=""/>
    <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt=""/>
    <img src="https://img.shields.io/badge/Redis-%23DD0031.svg?&style=for-the-badge&logo=redis&logoColor=white" alt=""/>
    <img src="https://img.shields.io/badge/Docker-008FCC?style=for-the-badge&logo=docker&logoColor=white" alt=""/>
    <img src="https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white" alt=""/>
</div>

Beerdegu is a real-time web application meant for beer tasting sessions, when
you and your friends are rating every consumed beer (color, smell, taste etc.).  
 
Built with Django Channels, Django Rest Framework, React with Typescript, 
Postgres, Redis in a Dockerized environment 
with an option to deploy to Heroku. Running development setup
without docker-compose is also possible.

### Tools, libraries, frameworks:
This setup has been tested with Python 3.8/3.9 and Node 12/14.

### Backend
- Django + Django Rest Framework : `django` `djangorestframework`
- Django Channels 3 : `channels`- handling websockets backend
- `django-cors-headers` - handling cross origin requests
- `django-filter` - filter backend for drf views
- `coverage` - for code coverage reports and running unit tests
- `mypy` + `djangorestframework-stubs` - for better typing experience
- `psycopg2` - needed to use Postgres (in Docker container)
- `channels_redis` - connection to Redis database service
- `whitenoise` - building static files
- `daphne` - production asgi server


### Frontend
- React
- Typescript
- `react-use-websocket` - websocket client, connects with ws backend
- `html2canvas`, `jspdf` - converting html to canvas and saving to pdf
- `@mui/material`, `@mui/icons-material`, `@mui/lab`, `@mui/styles` - Material UI library
- `node-sass` - enables scss/sass support
- `axios` - for making http requests

# Development setup

## Without Docker
### Backend
Create a virtual environment from cmd (or do it in Pycharm manually)
```shell script
cd backend

py -3 -m venv venv

venv/Scripts/Activate

python -m pip install --upgrade pip

pip install -r requirements.txt
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
Install node dependencies.
```shell script
cd frontend

npm i
```
Run development server in second terminal
```shell script
npm start
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
In case it does not work, try:
```shell script
docker exec -it CONTAINER_ID /bin/sh
```

# Production Deployment  
   1) [Create Heroku Account](https://signup.heroku.com/dc)  
   2) [Download/Install/Setup Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install)  
    - After install, log into Heroku CLI: `heroku login`  
   3) Run: `heroku create <app name>` to create the Heroku application    
   4) Set your environment variables for your production environment by running:  
    ```
    heroku config:set VARIABLE=value
    ```  
    Variables to set: `DJANGO_SETTINGS_MODULE=core.settings.prod` `DJANGO_SUPERUSER_EMAIL`,
    `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_PASSWORD`, `PRODUCTION_HOST=<app name>.herokuapp.com`, 
    `SECRET_KEY`,
   5) Run: `heroku stack:set container` so Heroku knows this is a containerized application  
   6) Run: `heroku addons:create heroku-postgresql:hobby-dev` which creates the postgres add-on for Heroku 
   7) Run: `heroku addons:create heroku-redis:hobby-dev` which creates the redis add-on for Heroku 
   8) Deploy app by running: `git push heroku master`,  
   *or* manually in Heroku dashboard  
   *or* by pushing to your github repository, having Automatic Deploys set up    
   9) Go to `<app name>.herokuapp.com` to see the published website.  

## CI
This repository uses Github Actions to run test pipeline.  
`tests.yml` - runs backend and frontend tests separately


# To do list

### Recently done:
- [X] Browsing and adding beers to room by host (inside the room)
- [X] Desktop and mobile chat (without saving messages to db)

### In progress:
- [ ] New website design with landing page, sub pages, separate header/sidebar outside of the room - IN PROGRESS
- [ ] All rooms view - CRUD (join, create, delete) - IN PROGRESS

---
- [ ] Browsing api (beers, breweries etc.)
- [ ] User profile with list of past beer tasting sessions and statistics

- [ ] Animate route switch
- [ ] Test async db utils and consumer (+ get Github Actions postgres connection to work with async stuff)
- [ ] Enable creating multiple rooms if all rooms are in finished state (perhaps add additional room state)
- [ ] Export ratings tables to CSV (PDF kinda done)
- [ ] Additional statistics in room (e.g best/worst beer, group by votes, the longest opinion, similar ratings etc.)
- [ ] Responsiveness (right now using Mobile First Approach)
