# Makefile for tot
# Usage examples:
#   make venv
#   make lint
#   make fmt
#   make test
#   make run CMD="run -f demo.nds --debug"
#   make clean

SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c

# ---- config ---------------------------------------------------------------

PYTHON_BIN ?= python3.11
VENV_DIR   ?= venv
PYTHON     := $(VENV_DIR)/bin/python
PIP        := $(VENV_DIR)/bin/pip

PKG_NAME   := tot

# ---- helpers --------------------------------------------------------------

$(VENV_DIR)/bin/python:  ## internal: create venv if missing
	@$(PYTHON_BIN) -m venv "$(VENV_DIR)"
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements.txt  # Use variable for the requirements file

venv: $(VENV_DIR)/bin/python  ## Create virtualenv (.venv) and upgrade pip
	@echo "✅ venv ready at $(VENV_DIR)"

$(VENV_DIR)/bin/tot: $(VENV_DIR)/bin/python  ## Installs package into the venv
	@$(PIP) install -e .

install: $(VENV_DIR)/bin/tot  ## Installs package into the venv
	@$(PIP) install -e .

# ---- install / setup ------------------------------------------------------

precommit:  ## Install pre-commit hooks
	@$(VENV_DIR)/bin/pre-commit install
	@echo "✅ pre-commit hooks installed"

# ---- quality --------------------------------------------------------------

lint:  ## Run static checks (ruff + mypy)
	@$(VENV_DIR)/bin/ruff check .
	@$(VENV_DIR)/bin/mypy src

fmt:  ## Auto-format (black + ruff --fix)
	@$(VENV_DIR)/bin/black src tests
	@$(VENV_DIR)/bin/ruff check --fix .

test:  ## Run tests
	@$(VENV_DIR)/bin/pytest -q

# ---- run ------------------------------------------------------------------

# Pass arguments to the CLI via CMD, e.g.:
#   make run CMD="run -f demo.nds --debug"
CMD ?= --help
run: $(VENV_DIR)/bin/tot  ## Run the tot CLI (python -m tot)
	@$(PYTHON) -m $(PKG_NAME) $(CMD)

# ---- maintenance ----------------------------------------------------------

clean:  ## Remove build/test artifacts
	@rm -rf .pytest_cache .mypy_cache .ruff_cache dist build *.egg-info "$(VENV_DIR)"

# ---- meta -----------------------------------------------------------------

.PHONY: venv precommit lint fmt test run clean help

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .+$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'
