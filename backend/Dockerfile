# Use an official Python runtime as a parent image
FROM python:3.9.6-alpine as build-image

# Setup venv in build image
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app/backend

# Install dependencies and packages only needed in build stage
COPY requirements.txt .

RUN  \
    apk update && \
    apk upgrade && \
    apk add --virtual .deps gcc musl-dev postgresql-libs postgresql-dev libressl-dev musl-dev libffi-dev cargo && \
    pip3 install --upgrade pip -r requirements.txt && \
    apk --purge del .deps

# Use an official Python runtime as a parent image - Run stage
FROM python:3.9.6-alpine as runtime

ENV PYTHONUNBUFFERED=1

# Copy venv from build stage
COPY --from=build-image /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install packages that are only needed runtime
RUN  \
    apk update && \
    apk upgrade && \
    apk add bash postgresql-libs && \
    rm -rf /var/cache/apk/*

# Add the rest of the code
COPY . /app/backend
COPY ./scripts/ /app/

# Make port 8000 available for the app
ENV PORT=8000
EXPOSE 8000

WORKDIR /app/backend

# Be sure to use 0.0.0.0 for the host within the Docker container,
# otherwise the browser won't be able to find it
RUN ["chmod", "+x", "/app/entrypoint-dev.sh"]
ENTRYPOINT [ "/app/entrypoint-dev.sh" ]
