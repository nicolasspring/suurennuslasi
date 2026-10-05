FROM suurennuslasi/suurennuslasi-base:latest

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
