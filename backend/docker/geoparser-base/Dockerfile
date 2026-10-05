FROM suurennuslasi/suurennuslasi-base:latest

WORKDIR /base

ENV HF_HOME=/opt/huggingface

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

# Download and validate the runtime model while building the image.
RUN python - <<'PY'
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer

model_name = "dguzh/geo-all-MiniLM-L6-v2"

SentenceTransformer(model_name)
AutoTokenizer.from_pretrained(model_name)
PY

RUN python -m geoparser install geonames

# Prevent unexpected runtime network access.
ENV HF_HUB_OFFLINE=1
