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
PIP    = ${VENV_DIR}/bin/pip3
PYTEST = ${VENV_DIR}/bin/pytest
MYPY   = ${VENV_DIR}/bin/mypy
RUFF   = ${VENV_DIR}/bin/ruff
BLACK  = ${VENV_DIR}/bin/black
ISORT  = ${VENV_DIR}/bin/isort

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
