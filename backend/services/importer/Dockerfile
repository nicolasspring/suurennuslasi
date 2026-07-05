FROM python:3.12-slim

ENV POETRY_VERSION=2.1.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY services/importer/pyproject.toml services/importer/poetry.lock ./services/importer/

COPY packages/db ./packages/db
COPY packages/domain ./packages/domain
COPY packages/storage ./packages/storage
COPY packages/events ./packages/events
COPY packages/messaging ./packages/messaging

WORKDIR /app/services/importer
RUN poetry install --no-root

COPY services/importer/suurennuslasi_importer ./services/importer/suurennuslasi_importer
