PYTHON = uv run python3 -m
MAP ?= maps/easy_linear.txt

.PHONY: install run debug clean lint lint-strict

all: run

install:
	pip install -r requirements.txt

run:
	@$(PYTHON) main

debug:
	@$(PYTHON) -m pdb main.py $(MAP)

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true

lint:
	flake8 . --max-line-length=100 --exclude=.git,__pycache__,.mypy_cache
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports \
	       --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 . --max-line-length=100 --exclude=.git,__pycache__,.mypy_cache
	mypy . --strict
