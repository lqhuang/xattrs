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

PYTHON = ${VENV_DIR}/bin/python3
PIP = ${VENV_DIR}/bin/pip3
PYTEST = ${VENV_DIR}/bin/pytest


# -----------------------------------------------------------------------------
.PHONY: bootstrap-venv bootstrap-dev bootstrap

bootstrap-venv:
	@echo "Bootstraping python virtual environment"
	$(BOOTSTRAP_PY) -m venv ${VENV_DIR}

bootstrap-dev:
	@echo "Installing development dependencies"
	$(PIP) install -e .[dev]

bootstrap: bootstrap-venv bootstrap-dev

# -----------------------------------------------------------------------------
.PHONY: build

build:
	@echo "Building package"
	$(PYTHON) -m build --sdist --wheel --outdir ${DIST_DIR}

# -----------------------------------------------------------------------------
.PHONY: docs live-docs

docs:
	@echo "Building docs"
	$(MAKE) -C ./docs html

live-docs:
	@echo "Start a server for docs live preview ..."
	$(MAKE) -C ./docs live-html
