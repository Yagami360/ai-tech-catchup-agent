.PHONY: install update setup run run-news run-no-issue run-weekly run-monthly run-topic run-custom lint format

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

# Run AI Agent with custom news count
run-news:
	uv run python -m src.main --news-count $(NEWS_COUNT)

# Run AI Agent without creating GitHub Issues
run-no-issue:
	uv run python -m src.main --no-issue

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

# Run code linting
lint:
	uv run flake8 .
	uv run mypy .

# Run code formatting
format:
	uv run black .

# Claude Code Actions workflow commands
# workflow-dispatch:
# 	gh workflow run claude-code-actions.yml

# workflow-status:
# 	gh run list --workflow=claude-code-actions.yml --limit=5
