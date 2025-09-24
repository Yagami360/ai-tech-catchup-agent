.PHONY: install run test clean lint format

# Install dependencies
install:
	uv sync

# Run AI Agent on local environment
run:
	uv run python -m src.main

# Run AI Agent without creating GitHub Issues
run-no-issue:
	uv run python -m src.main --no-issue

# 特定トピックの検索
run-topic:
	uv run python -m src.main topic $(TOPIC)

# 週次レポート
run-weekly:
	uv run python -m src.main weekly

# 月次サマリー
run-monthly:
	uv run python -m src.main monthly

# カスタムプロンプトで検索
run-custom:
	uv run python -m src.main custom "$(PROMPT)"

# Run tests
test:
	uv run pytest

# Run code linting
lint:
	uv run flake8 .
	uv run mypy .

# Run code formatting
format:
	uv run black .

# Clean up environment
clean:
	rm -rf __pycache__/
	rm -rf src/__pycache__/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete

# Setup development environment
setup: install
	cp env.example .env
	@echo "Created environment configuration file. Please edit the .env file to set the API keys."

# Update dependencies
update:
	uv lock --upgrade

# Display help
help:
	@echo "Available commands:"
	@echo "  make install        - Install dependencies"
	@echo "  make run            - Run AI Agent (daily catchup)"
	@echo "  make run-no-issue   - Run AI Agent without creating GitHub Issues"
	@echo "  make run-topic TOPIC=   - Run analysis for specific topic"
	@echo "  make run-weekly     - Generate weekly report"
	@echo "  make run-monthly    - Generate monthly summary"
	@echo "  make run-custom PROMPT= - Run custom prompt search"
	@echo "  make test           - Run tests"
	@echo "  make lint           - Run code linting"
	@echo "  make format         - Run code formatting"
	@echo "  make clean          - Clean up environment"
	@echo "  make setup          - Setup development environment"
	@echo "  make update         - Update dependencies"
