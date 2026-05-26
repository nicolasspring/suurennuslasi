FROM python:3.12-slim

ENV POETRY_VERSION=2.1.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY services/api/pyproject.toml services/api/poetry.lock ./services/api/
COPY packages/db/pyproject.toml packages/db/poetry.lock ./packages/db/

COPY services/api ./services/api
COPY packages/db ./packages/db

WORKDIR /app/services/api

RUN poetry install --no-root

EXPOSE 8000
