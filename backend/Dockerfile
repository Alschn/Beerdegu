ARG PYTHON_VERSION=3.10.5-alpine

# BASE-IMAGE - get base python image with pipenv
FROM python:${PYTHON_VERSION} as base-image

RUN \
    apk update && \
    apk upgrade && \
    pip install --upgrade pip && \
    pip install pipenv

# BUILD-IMAGE - install backend dependencies, setup virtual environment
FROM base-image as build-image

ENV PYTHONUNBUFFERED=1
ENV PIPENV_VENV_IN_PROJECT=1

COPY Pipfile ./

RUN  \
    apk update && \
    apk upgrade && \
    apk add --virtual .build-deps gcc musl-dev postgresql-libs postgresql-dev libressl-dev libffi-dev cargo && \
    pipenv install --dev --python 3.10 --skip-lock && \
    apk --purge del .build-deps

# RUNTIME - copy environment, collect staticfiles, install packages required at runtime
FROM base-image as runtime

ENV PYTHONUNBUFFERED=1

COPY --from=build-image /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

RUN  \
    apk update && \
    apk upgrade && \
    apk add bash postgresql-libs gettext && \
    rm -rf /var/cache/apk/*

COPY . /app/backend
COPY ./scripts/ /app/

ENV PORT 8000
EXPOSE 8000

WORKDIR /app/backend

RUN ["chmod", "+x", "/app/entrypoint-dev.sh"]
ENTRYPOINT [ "/app/entrypoint-dev.sh" ]
