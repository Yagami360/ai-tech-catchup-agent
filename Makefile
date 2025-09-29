.PHONY: install update setup run run-weekly run-monthly run-topic run-custom test lint format

# Install dependencies
install:
	uv sync

# Update dependencies
update:
	uv lock --upgrade

# Setup development environment
setup: install
	if [ ! -f .env ]; then
		cp .env.example .env
		@echo "Created environment configuration file. Please edit the .env file to set the API keys."
	fi

# Run AI Agent on local environment
run:
	uv run python -m src.main

# Run AI Agent for weekly report
run-weekly:
	uv run python -m src.main weekly

# Run AI Agent for monthly report
run-monthly:
	uv run python -m src.main monthly

# Run AI Agent for specific topic
run-topic:
	uv run python -m src.main topic $(TOPIC)

# Run AI Agent with custom prompt
run-custom:
	uv run python -m src.main custom "$(PROMPT)"

# Run AI Agent with test mode
test:
	export LOG_LEVEL=DEBUG
	uv run python -m src.main --claude-model claude-3-5-haiku-20241022 --max-tokens 1000 --news-count 1 --no-issue

test-weekly:
	export LOG_LEVEL=DEBUG
	uv run python -m src.main weekly --claude-model claude-3-5-haiku-20241022 --max-tokens 1000 --news-count 1 --no-issue

test-monthly:
	export LOG_LEVEL=DEBUG
	uv run python -m src.main monthly --claude-model claude-3-5-haiku-20241022 --max-tokens 1000 --news-count 1 --no-issue

# Run code linting
lint:
	uv run flake8 . --exclude=.venv,venv,__pycache__,.git,.mypy_cache,.pytest_cache
	uv run mypy .

# Run code formatting
format:
	uv run black .
