PYTHON = uv run python3 -m

.PHONY: install run debug clean lint lint-strict

all: run

install:
	uv sync

run:
	@$(PYTHON) main

debug:
	@$(PYTHON) pdb main.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true

lint:
	flake8 . --max-line-length=79 --exclude=.git,__pycache__,.mypy_cache,.venv
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports \
	       --disallow-untyped-defs --check-untyped-defs
