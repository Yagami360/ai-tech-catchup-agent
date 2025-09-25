# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an AI Tech Catchup Agent that leverages Claude Code's web search functionality to gather and analyze the latest AI technology information, generating weekly reports through GitHub Issues. The agent is built in Python and automatically runs on Fridays via GitHub Actions.

## Development Commands

### Environment Setup
```bash
# Install dependencies
make install

# Setup development environment (creates .env from .env.example)
make setup
```

### Running the Application
```bash
# Default AI tech catchup
make run

# Weekly report
make run-weekly

# Monthly report
make run-monthly

# Specific topic search
make run-topic TOPIC="大規模言語モデル"

# Custom prompt search
make run-custom PROMPT="GPT-5の最新情報について調べて"

# Run with custom news count
make run-news NEWS_COUNT=15

# Run without creating GitHub Issues
make run-no-issue
```

### Development Tools
```bash
# Code linting
make lint          # Runs flake8 and mypy

# Code formatting
make format        # Runs black formatter

# Testing (if tests exist)
uv run pytest     # Standard pytest command
```

## Architecture

### Core Components

- **`src/main.py`**: Main application entry point containing `AITechCatchupAgent` class
- **`src/claude_search.py`**: Claude Code search functionality integration
- **`src/github_integration.py`**: GitHub API integration for creating Issues
- **`src/prompt_manager.py`**: Centralized prompt management system
- **`config.py`**: Application configuration using Pydantic settings

### Key Design Patterns

1. **Centralized Configuration**: Uses `config.py` with Pydantic settings for environment variable management
2. **Modular Search System**: Separates Claude search logic from main application logic
3. **Prompt Template System**: All prompts are managed in `prompts/default.yaml` with keyword interpolation
4. **GitHub Integration**: Automated issue creation with labels and structured content

### Configuration Management

- **Environment Variables**: Defined in `.env` file (copy from `.env.example`)
  - `ANTHROPIC_API_KEY`: Claude API key
  - `GITHUB_TOKEN`: GitHub token for issue creation
  - `GITHUB_REPOSITORY`: Target repository for issues
  - `CLAUDE_MODEL`: Claude model to use (default: claude-sonnet-4-20250514)
  - `NEWS_COUNT`: Number of important news items to include

- **Prompt Configuration**: `prompts/default.yaml` contains:
  - `key_words`: Central AI technology keywords used across all prompts
  - `default_search`: Default tech catchup prompt
  - `topic_search`: Specific topic search template
  - `custom_search`: Custom prompt template
  - `weekly_report`: Weekly report generation
  - `monthly_summary`: Monthly summary generation

### Package Management

- **Tool**: Uses `uv` for fast Python package management
- **Dependencies**: Defined in `pyproject.toml`
- **Development Dependencies**: Include pytest, black, flake8, mypy

### Automation

- **GitHub Actions**: `.github/workflows/ai-tech-catchup.yml`
  - Runs every Friday at 9:00 UTC (`0 9 * * 5`)
  - Uses `make run` command
  - Requires `ANTHROPIC_API_KEY` and `GITHUB_TOKEN` secrets

## Important Implementation Notes

1. **Japanese Language Support**: The application primarily generates reports in Japanese but supports English through configuration
2. **Web Search Integration**: Leverages Claude Code's web search capabilities for real-time information gathering
3. **Keyword-Driven Search**: Uses centralized AI technology keywords from `prompts/default.yaml` for consistent search targeting
4. **Structured Output**: Generates well-formatted reports with specific sections (news, trends, technical highlights, etc.)
5. **GitHub Integration**: Creates issues with appropriate labels (`weekly-report`, `tech-insight`, model-specific tags)

## Development Workflow

1. **Local Development**: Use `make run-no-issue` to test without creating GitHub issues
2. **Testing Prompts**: Use `make run-custom PROMPT="test prompt"` for quick prompt testing
3. **Configuration Changes**: Modify `config.py` for application settings or `prompts/default.yaml` for prompt templates
4. **Code Quality**: Run `make lint` before committing changes