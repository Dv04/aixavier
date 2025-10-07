SHELL := /bin/bash
PYTHON := python3
VENV := .venv
ACTIVATE := source $(VENV)/bin/activate
PROFILE ?= demo
ARGS ?= --dry-run

.DEFAULT_GOAL := help

help:
	@echo "Targets:" 
	@grep -E '^[a-zA-Z_-]+:.*?#' Makefile | sed 's/:.*?#/ - /'

bootstrap: requirements.txt requirements-dev.txt
	@test -d $(VENV) || $(PYTHON) -m venv $(VENV)
	$(ACTIVATE) && pip install --upgrade pip wheel
	$(ACTIVATE) && pip install -r requirements.txt -r requirements-dev.txt
	$(ACTIVATE) && python models/bootstrap_models.py --profile=$(PROFILE)
	@echo "Bootstrap complete."

run:
	PROFILE=$(PROFILE) docker compose --profile all up --build

run-detached:
	PROFILE=$(PROFILE) docker compose --profile all up --build -d

stop:
	docker compose down

demo:
	$(PYTHON) tests/data/generate_demo.py
	CAMERA_RTSP_URL_01=demo://synthetic PROFILE=demo docker compose --profile demo up --build

perf:
	$(ACTIVATE) && $(PYTHON) tests/test_perf.py --endpoint http://localhost:9100/metrics

clean:
	docker compose down -v || true
	rm -rf $(VENV) artifacts/ logs/ cache/

lint:
	$(ACTIVATE) && ruff check src tools tests
	$(ACTIVATE) && mypy src tools

test:
	$(ACTIVATE) && pytest -q
	bash tests/test_rtsp_connect.sh

placeholders\:list:
	$(ACTIVATE) && $(PYTHON) tools/resolve_placeholders.py --list

placeholders\:resolve:
	$(ACTIVATE) && $(PYTHON) tools/resolve_placeholders.py --from $${FROM}

placeholders\:check:
	$(ACTIVATE) && $(PYTHON) tools/placeholder_lint.py

agent\:refresh:
	$(ACTIVATE) && $(PYTHON) src/agent/main.py $(ARGS)

format:
	$(ACTIVATE) && ruff check --fix src tools tests
	$(ACTIVATE) && black src tools tests

ci: lint test placeholders\:check

.PHONY: help bootstrap run run-detached stop demo perf clean lint test ci format placeholders\:list placeholders\:resolve placeholders\:check agent\:refresh
