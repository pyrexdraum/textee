# syntax=docker/dockerfile:1

FROM python:3.9.9-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY Pipfile* ./

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir pipenv \
    && pipenv install --system --clear

COPY ./entrypoint.sh ./src ./