FROM nikolaik/python-nodejs:python3.10-nodejs16

ENV PIPENV_VENV_IN_PROJECT=1

WORKDIR /app/backend

COPY ./backend/Pipfile ./backend/Pipfile.lock /app/backend/
RUN pip install --upgrade pip && pipenv install

ENV PATH="/app/backend/.venv/bin:$PATH"

WORKDIR /app/frontend

COPY ./frontend/package.json ./frontend/yarn.lock /app/frontend/
RUN yarn install

COPY ./backend/scripts/ /app/
COPY . /app/

RUN yarn build

RUN mkdir /app/backend/staticfiles

WORKDIR /app

ENV DJANGO_SETTINGS_MODULE=core.settings.static
ENV SERVE_FRONTEND=True

RUN python3 backend/manage.py collectstatic --noinput
