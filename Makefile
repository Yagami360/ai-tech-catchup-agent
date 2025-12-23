.PHONY: install setup run run-weekly run-monthly run-topic test lint format format-check

# Install dependencies
install:
	uv lock --upgrade
	uv sync --extra dev

# Setup development environment
setup: install
	if [ ! -f .env ]; then
		cp .env.example .env
		@echo "Created environment configuration file. Please edit the .env file to set the API keys."
	fi

# Run AI Agent for latest report
run: install
	uv run python -m src.main

# Run AI Agent for weekly report
run-weekly: install
	uv run python -m src.main weekly

# Run AI Agent for monthly report
run-monthly: install
	uv run python -m src.main monthly

# Run AI Agent for topic report
# Usage: make run-topic TOPIC="RAG"
TOPIC ?= ""
run-topic: install
	@if [ -z "$(TOPIC)" ]; then \
		echo "Error: Please specify TOPIC. Usage: make run-topic TOPIC=\"your topic\""; \
		exit 1; \
	fi
	@echo "Running topic report for: $(TOPIC)"
	uv run python -m src.main topic --topic "$(TOPIC)"

# Run AI Agent with test mode
# TEST_MODEL ?= claude-3-5-haiku-20241022
TEST_MODEL ?= gemini-2.0-flash-lite
# TEST_MODEL ?= gemini-2.5-flash
test: install
	@echo "Running test report..."
	uv run python -m src.main test --model $(TEST_MODEL) --max-tokens 100 --news-count 1 --no-issue --mcp-servers github,huggingface

# Run code linting
lint: install
	uv run flake8 .
	uv run mypy .

# Run code formatting
format: install
	uv run black .
	uv run isort .

# Run code formatting check
format-check: install
	uv run black --check .
	uv run isort --check-only .
