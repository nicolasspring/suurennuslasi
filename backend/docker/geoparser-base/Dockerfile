FROM python:3.12-slim

ENV POETRY_VERSION=2.1.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /base

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

RUN python -m geoparser install geonames
