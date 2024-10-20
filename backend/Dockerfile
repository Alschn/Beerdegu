ARG PYTHON_VERSION=3.12.7-alpine

# BASE-IMAGE - get base python image with poetry
FROM python:${PYTHON_VERSION} as base-image

RUN \
    apk update && \
    apk upgrade && \
    python3 -m pip install --upgrade pip && \
    pip install poetry==1.8.3

# BUILD-IMAGE - install backend dependencies, setup virtual environment
FROM base-image as build-image

ENV PYTHONUNBUFFERED=1

COPY pyproject.toml poetry.lock ./

RUN  \
    apk update && \
    apk upgrade && \
    apk add --virtual .build-deps gcc musl-dev postgresql-dev openssl-dev libffi-dev cargo && \
    mkdir .venv && \
    poetry install --verbose && \
    apk --purge del .build-deps

# RUNTIME - copy environment, install packages required at runtime
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
