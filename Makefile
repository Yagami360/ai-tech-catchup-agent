.PHONY: install setup run run-weekly run-monthly test lint format format-check

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

# Run AI Agent with test mode
test: install
	@echo "Running report test..."
	uv run python -m src.main --claude-model claude-3-5-haiku-20241022 --max-tokens 50 --news-count 1 --no-issue
	@echo "Running weekly report test..."
	uv run python -m src.main weekly --claude-model claude-3-5-haiku-20241022 --max-tokens 50 --news-count 1 --no-issue
	@echo "Running monthly report test..."
	uv run python -m src.main monthly --claude-model claude-3-5-haiku-20241022 --max-tokens 50 --news-count 1 --no-issue

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
