# syntax=docker/dockerfile:1

FROM python:3.9.9-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY Pipfile Pipfile.lock /code/

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir pipenv \
    && pipenv install --system --clear

COPY . /code/