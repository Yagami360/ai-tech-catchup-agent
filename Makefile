.PHONY: install run test clean lint format

# Install dependencies
install:
	uv sync

# Run AI Agent on local environment
run:
	uv run python -m src.main

run-insight:
	uv run python -m src.main insight $(TOPIC)

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
	@echo "  make install  - Install dependencies"
	@echo "  make run      - Run AI Agent (daily catchup)"
	@echo "  make insight TOPIC=<topic> - Run analysis for specific topic"
	@echo "  make test     - Run tests"
	@echo "  make lint     - Run code linting"
	@echo "  make format   - Run code formatting"
	@echo "  make clean    - Clean up environment"
	@echo "  make setup    - Setup development environment"
	@echo "  make update   - Update dependencies"
