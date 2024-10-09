SHELL := bash
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

# ------------------------------------------------------------------------------
BOOTSTRAP_PY = python3

VENV_DIR := .venv
TEST_DIR := tests
DIST_DIR := dist
DOCS_DIR := docs

UV     := uv
PYTHON := ${VENV_DIR}/bin/python3
PIP    := ${UV} pip
PYTEST := ${UV} run pytest
MYPY   := ${UV} run mypy
RUFF   := ${UV} run ruff
BLACK  := ${UV} run black
ISORT  := ${UV} run isort

# -----------------------------------------------------------------------------
.PHONY: bootstrap-venv bootstrap-dev bootstrap

bootstrap-venv:
	@echo "Bootstraping python virtual environment"
	$(BOOTSTRAP_PY) -m venv ${VENV_DIR}

bootstrap-dev:
	@echo "Installing development dependencies"
	$(PIP) install -e '.[dev]'

bootstrap: bootstrap-venv bootstrap-dev

sync:
	$(UV) sync

sync-dev:
	$(UV) sync --extra dev

sync-all:
	$(UV) sync --all-extras

# -----------------------------------------------------------------------------
.PHONY: build

build:
	@echo "Building package"
	$(UV) build

.PHONY: test
test:
	@echo "Running tests"
	$(PYTEST) ${TEST_DIR}

.PHONY: lint
lint:
	@echo "Running linters"
	$(ISORT) .
	$(BLACK) .
	$(RUFF) . --ignore "F401,F811"
	$(MYPY) .

# -----------------------------------------------------------------------------
.PHONY: docs live-docs

docs:
	@echo "Building docs"
	$(MAKE) -C ./docs html

live-docs:
	@echo "Start a server for docs live preview ..."
	$(MAKE) -C ./docs live-html
