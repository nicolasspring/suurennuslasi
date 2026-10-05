REGISTRY := suurennuslasi
BACKEND  := backend

.PHONY: base stack all

base:
	docker build -t $(REGISTRY)/suurennuslasi-base:latest $(BACKEND)/docker/suurennuslasi-base/
	docker build -t $(REGISTRY)/geoparser-base:latest $(BACKEND)/docker/geoparser-base/

stack:
	docker build -t $(REGISTRY)/api:latest -f $(BACKEND)/services/api/Dockerfile $(BACKEND)
	docker build -t $(REGISTRY)/importer:latest -f $(BACKEND)/services/importer/Dockerfile $(BACKEND)
	docker build -t $(REGISTRY)/geoparser:latest -f $(BACKEND)/services/geoparser/Dockerfile $(BACKEND)
	docker build -t $(REGISTRY)/frontend:latest -f frontend/Dockerfile frontend

all: base stack
