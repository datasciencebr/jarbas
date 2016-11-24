FROM python:3.5

MAINTAINER Pedro Maia <pedro@pedromm.com>

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY requirements-dev.txt ./

RUN pip install -r requirements.txt

COPY . .
