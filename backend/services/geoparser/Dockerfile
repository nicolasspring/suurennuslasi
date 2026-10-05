FROM suurennuslasi/geoparser-base:latest

WORKDIR /app

COPY services/geoparser/pyproject.toml services/geoparser/poetry.lock ./services/geoparser/

COPY packages/db ./packages/db
COPY packages/domain ./packages/domain
COPY packages/events ./packages/events
COPY packages/messaging ./packages/messaging

WORKDIR /app/services/geoparser
RUN poetry install --no-root

COPY services/geoparser/suurennuslasi_geoparser ./services/geoparser/suurennuslasi_geoparser
