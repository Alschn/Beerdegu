ARG PYTHON_VERSION=3.12.7-alpine
ARG NODE_VERSION=16.16.0-alpine

# BASE-IMAGE - get base python image with poetry
FROM python:${PYTHON_VERSION} as base-image

RUN \
    apk update && \
    apk upgrade && \
    python3 -m pip install --upgrade pip && \
    pip install poetry

# COMPILE-IMAGE - install backend dependencies, setup virtual environment
FROM base-image as compile-image

ENV PYTHONUNBUFFERED 1

WORKDIR /app/backend

COPY backend/pyproject.toml backend/poetry.lock /app/backend/

RUN \
    apk update && \
    apk upgrade && \
    apk add --virtual .build-deps gcc musl-dev postgresql-dev && \
    mkdir .venv && \
    poetry install --verbose && \
    apk --purge del .build-deps

# NODE-IMAGE - install frontend dependencies, build frontend files
FROM node:${NODE_VERSION} as node-image

ARG VITE_BACKEND_URL
ARG VITE_WEBSOCKET_URL

ENV VITE_BACKEND_URL=$VITE_BACKEND_URL
ENV VITE_WEBSOCKET_URL=$VITE_WEBSOCKET_URL

WORKDIR /app/frontend

COPY frontend /app/frontend/

RUN \
    apk update && \
    apk upgrade && \
    yarn install && \
    yarn build && \
    rm -rf /var/cache/apk/*

# RUNTIME - copy environment, collect staticfiles, install packages required at runtime
FROM base-image as runtime

ARG SERVE_FRONTEND=True

ENV PATH="/app/backend/.venv/bin:$PATH"

COPY --from=compile-image /app/backend/.venv /app/backend/.venv
COPY --from=node-image /app/frontend/build /app/frontend/build
COPY backend /app/backend/

RUN \
    apk add bash postgresql-libs && \
    rm -rf /var/cache/apk/*

WORKDIR /app

ENV SERVE_FRONTEND=$SERVE_FRONTEND
ENV DJANGO_SETTINGS_MODULE core.settings.static

RUN mkdir -p /app/staticfiles && python backend/manage.py collectstatic --noinput

WORKDIR /app/backend
