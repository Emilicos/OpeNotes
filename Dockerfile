# Base Image  
FROM python:3.7.4-alpine3.10

# Set an environment variable to indicate the working directory
ENV PYTHONUNBUFFERED 1

# Make a directory in your Docker image, which you can use to store your source code
RUN mkdir /app

# Set the /app as the working directory
WORKDIR /app

# Copy project to our home directory (/app). 
COPY . /app/  

RUN set -ex \
    && apk add --no-cache --virtual .build-deps postgresql-dev build-base \
    && python -m venv /env \
    && /env/bin/pip install --upgrade pip \
    && /env/bin/pip install --no-cache-dir -r /app/requirements.txt \
    && runDeps="$(scanelf --needed --nobanner --recursive /env \
        | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
        | sort -u \
        | xargs -r apk info --installed \
        | sort -u)" \
    && apk add --virtual rundeps $runDeps \
    && apk del .build-deps

RUN apk add --no-cache bash

ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

EXPOSE 8000