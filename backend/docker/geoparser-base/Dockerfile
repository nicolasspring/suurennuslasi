FROM suurennuslasi/suurennuslasi-base:latest

WORKDIR /base

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

RUN python -m geoparser install geonames
