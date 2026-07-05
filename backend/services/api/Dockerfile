FROM python:3.12-slim

ENV POETRY_VERSION=2.1.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY services/api/pyproject.toml services/api/poetry.lock ./services/api/

COPY packages/db ./packages/db
COPY packages/domain ./packages/domain
COPY packages/storage ./packages/storage
COPY packages/messaging ./packages/messaging

WORKDIR /app/services/api
RUN poetry install --no-root

COPY services/api/suurennuslasi_api ./services/api/suurennuslasi_api

EXPOSE 8000
