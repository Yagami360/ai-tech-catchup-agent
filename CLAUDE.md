# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an AI Tech Catchup Agent that generates automated AI technology reports by leveraging LLM web search capabilities (Claude Code SDK and Gemini API). The agent runs on GitHub Actions and publishes daily/weekly/monthly/topic-specific reports as GitHub Issues.

**Key Features**:
- Supports both Claude models (via Claude Code SDK) and Gemini models (via Gemini API) with automatic client selection based on model name
- Four report types: Latest (daily), Weekly, Monthly, and Topic-specific reports

## Development Commands

### Environment Setup
```bash
# Install dependencies
make install

# Setup development environment (creates .env from .env.example)
make setup
```

### Running Reports
```bash
# Daily/latest report
make run

# Weekly report
make run-weekly

# Monthly report
make run-monthly

# Topic-specific report
make run-topic TOPIC="AI Agent"

# Test mode (uses test_report prompt, no GitHub issue)
make test
```

### Code Quality
```bash
# Lint (flake8 + mypy)
make lint

# Format (black + isort)
make format

# Format check only
make format-check
```

### Direct Execution with Custom Options
```bash
# Custom model and token limits
uv run python -m src.main --model gemini-2.5-flash --max-tokens 5000

# Specific news count
uv run python -m src.main --news-count 10

# Skip GitHub issue creation
uv run python -m src.main --no-issue

# Enable MCP servers (Claude models only)
uv run python -m src.main --mcp-servers github

# Enable multiple MCP servers
uv run python -m src.main --mcp-servers github,filesystem

# Weekly report with custom model
uv run python -m src.main weekly --model claude-sonnet-4-20250514

# Topic-specific report
uv run python -m src.main topic --topic "RAG" --model claude-sonnet-4-20250514

# Test report (uses test_report prompt)
uv run python -m src.main test --model claude-3-5-haiku-20241022
```

## Architecture

### Core Flow
1. **Main Entry** (`src/main.py`): CLI argument parsing and execution orchestration
2. **Agent** (`src/agent/ai_tech_catchup_agent.py`): Core report generation logic with client selection
3. **Clients** (`src/client/`): LLM and GitHub API integrations
4. **Prompt Management** (`src/utils/prompt_manager.py`): YAML-based prompt loading with dynamic variable substitution
5. **Configuration** (`src/config.py`): Pydantic-based settings from environment variables

### Multi-Model Support Architecture

The agent automatically selects the appropriate AI client based on the model name:

- **Claude Models**: Uses `ClaudeCodeClient` with Claude Code SDK
  - Supports web search via `WebSearch` and `WebFetch` tools
  - Async execution with `claude-code-sdk` package
  - **MCP Server support**: Extensible integration for external tools (GitHub, filesystem, database, etc.)
  - Model examples: `claude-sonnet-4-20250514`, `claude-3-5-haiku-20241022`

- **Gemini Models**: Uses `GeminiClient` with Google Generative AI SDK
  - Supports web search via Google Search grounding
  - Synchronous API calls with `google-genai` package
  - **MCP Server support**: Not supported
  - Model examples: `gemini-2.5-flash`, `gemini-2.0-flash-exp`, `gemini-1.5-pro`

**Client Selection Logic** (`src/agent/ai_tech_catchup_agent.py:23-31`):
```python
if "claude" in self.model_name.lower():
    self.ai_client = ClaudeCodeClient(...)
elif "gemini" in self.model_name.lower():
    self.ai_client = GeminiClient(...)
```

### Prompt System Design

All prompts are centralized in `prompts/default.yaml` with:

- **Keyword Sets**: `key_words` - AI technology keywords for consistent search targeting
- **URL Sources**: `key_urls` - Priority information sources (company blogs, tech news, academic sites)
- **Report Templates**: `report`, `weekly_report`, `monthly_report`, `topic_report` with dynamic variable substitution

**Dynamic Variables** automatically injected by `PromptManager`:
- `{key_words}`: AI technology keywords from YAML
- `{key_urls}`: Priority source URLs from YAML
- `{news_count}`: Number of news items (from env or CLI)
- `{topic}`: Topic name for topic reports
- `{current_year}`: Current year
- `{week_period}`: Last 7 days period (ending yesterday)
- `{month_period}`: Last 30 days period (ending yesterday)

### GitHub Actions Integration

Four workflows in `.github/workflows/`:
- `daily-report.yml`: Daily execution (currently manual trigger only)
- `weekly-report.yml`: Weekly execution
- `monthly-report.yml`: Monthly execution
- `topic-report.yml`: On-demand topic-specific reports (manual trigger with topic input)

**Required Secrets**:
- `ANTHROPIC_API_KEY`: For Claude models
- `GOOGLE_API_KEY`: For Gemini models
- `GITHUB_TOKEN`: Auto-provided for issue creation
- `HF_TOKEN`: For Hugging Face MCP server (optional)

**Required Variables**:
- `MODEL_NAME`: AI model to use (e.g., `claude-sonnet-4-20250514` or `gemini-2.5-flash`)
- `ENABLED_MCP_SERVERS`: MCP servers to enable (e.g., `github,huggingface`)

## Configuration Management

### Environment Variables (.env)

```bash
# AI Model Configuration
ANTHROPIC_API_KEY=sk-...           # Required for Claude models
GOOGLE_API_KEY=...                 # Required for Gemini models
MODEL_NAME=claude-sonnet-4-20250514  # or gemini-2.5-flash

# Output Configuration
MAX_TOKENS=10000                   # Optional: response length limit
NEWS_COUNT=20                      # Number of important news items

# GitHub Integration
GITHUB_TOKEN=ghp_...               # For issue creation and MCP server
GITHUB_REPOSITORY=owner/repo       # Target repository

# MCP Configuration (Claude models only)
ENABLED_MCP_SERVERS=github,huggingface  # Comma-separated list
HF_TOKEN=hf_...                    # For Hugging Face MCP server
```

**Model Selection**: Set `MODEL_NAME` to any supported model:
- Claude: `claude-sonnet-4-20250514`, `claude-opus-4-1-20250805`, `claude-3-5-haiku-20241022`
- Gemini: `gemini-2.5-flash`, `gemini-2.5-pro`, `gemini-2.0-flash-exp`, `gemini-1.5-pro`

### Prompt Configuration (prompts/default.yaml)

To modify search behavior or report structure:
1. Edit `key_words.keywords` to adjust AI technology focus areas
2. Edit `key_urls.sources` to change priority information sources
3. Edit report templates (`report.prompt`, `weekly_report.prompt`, etc.) to change output format

**Important**: Use `{key_words}`, `{key_urls}`, and other placeholders in templates - they're auto-populated by `PromptManager`.

## Package Management

- **Tool**: `uv` for fast Python dependency management
- **Dependencies**: Defined in `pyproject.toml`
- **Dev Dependencies**: Include `pytest`, `black`, `isort`, `flake8`, `mypy`
- **Lock File**: `uv.lock` (committed to repository)

## MCP Server Integration

The agent supports extensible MCP (Model Context Protocol) Server integration for Claude models, enabling integration with various external tools and services.

### MCP Server Architecture

**Configuration Files**:
- `mcp/mcp_servers.yaml`: MCP server definitions (command, args, environment variables)
- `prompts/default.yaml`: MCP-specific prompt instructions under `mcp_tools`
- `src/utils/mcp_manager.py`: MCP server configuration management

### Enabling MCP Servers

**Via Environment Variable**:
```bash
ENABLED_MCP_SERVERS=github,filesystem
```

**Via CLI**:
```bash
uv run python -m src.main --mcp-servers github
uv run python -m src.main --mcp-servers github,filesystem,database
```

**Note on Gemini Support**:
- **Claude models**: Full MCP server integration via Claude Code SDK
- **Gemini models**: MCP servers not supported
  - If `--mcp-servers` is specified with Gemini models, it will be ignored with a warning

### Available MCP Servers

#### GitHub MCP Server
- **Configuration**: `mcp/mcp_servers.yaml` (github section)
- **Requirements**: Node.js/npm, GITHUB_TOKEN
- **Tools**: Repository ops, issues, PRs, code security, Actions, GitHub Trending
- **Prompt Instructions**: `prompts/default.yaml` (github_mcp)

#### Hugging Face MCP Server
- **Configuration**: `mcp/mcp_servers.yaml` (huggingface section)
- **Requirements**: Python/uvx, HF_TOKEN (optional for local, required for CI/CD)
- **Tools**: Model search, dataset search, Space search, paper search, popularity metrics
- **Prompt Instructions**: `prompts/default.yaml` (huggingface_mcp)
- **Note**: Auto-login on first run in local environments; HF_TOKEN required in CI/CD

#### Adding New MCP Servers

1. **Define server in `mcp/mcp_servers.yaml`**:
```yaml
servers:
  your_server:
    name: "Your MCP Server"
    type: "stdio"
    command: "npx"
    args: ["-y", "@your/mcp-server"]
    env:
      API_KEY: "${YOUR_API_KEY}"
    allowed_tools:
      - "mcp__your_server__*"
    description: "Server description"
```

2. **Add prompt instructions in `prompts/default.yaml`**:
```yaml
mcp_tools:
  your_server_mcp: |
    **Your Server MCP ツールが利用可能な場合**:
    - Tool usage instructions
    - Best practices
```

3. **Enable the server**:
```bash
uv run python -m src.main --mcp-servers your_server
```

### How It Works

1. **MCPServerManager** (`src/utils/mcp_manager.py`) loads `mcp/mcp_servers.yaml`
2. Builds MCP configuration for enabled servers with environment variable expansion
3. **ClaudeCodeClient** receives MCP config and allowed tools list
4. **PromptManager** injects server-specific instructions into prompts
5. Claude can use MCP tools during execution

### Supported MCP Servers

- **GitHub** (Active): Repository and issue management, GitHub Trending
- **Hugging Face** (Active): AI model, dataset, space, and paper search
- **Slack** (Available): Message operations (commented out in config)

## Important Implementation Notes

1. **Japanese Primary**: Reports are generated in Japanese; prompts are in Japanese
2. **Web Search Required**: Both clients rely on web search capabilities for real-time information
3. **Async vs Sync**: Claude Code SDK uses async/await; Gemini API is synchronous
4. **Token Limits**: `max_tokens` parameter passed to both clients but handled differently (Claude: prompt instruction, Gemini: API config)
5. **Date Calculations**: Weekly/monthly reports use "yesterday" as end date to avoid incomplete current-day data (`src/agent/ai_tech_catchup_agent.py:148-151, 212-215`)
6. **Error Handling**: GitHub client retries issue creation without labels if 422 error occurs (`src/client/github_client.py`)
7. **Report Types** (`src/main.py:32-36`):
   - Default (no mode): Latest daily report
   - `weekly`: Last 7 days ending yesterday
   - `monthly`: Last 30 days ending yesterday
   - `topic`: Topic-specific research with `--topic` parameter required
   - `test`: Test mode with test_report prompt
8. **MCP Server Support**:
   - Claude: Native MCP integration via Claude Code SDK
   - Gemini: Not supported (MCP options ignored with warning)
9. **MCP Extensibility**: New MCP servers can be added via `mcp/mcp_servers.yaml` without code changes

## Testing Strategy

Use `make test` which runs a test report with:
- Minimal tokens (`--max-tokens 100`)
- Single news item (`--news-count 1`)
- No GitHub issue creation (`--no-issue`)
- Fast model (`gemini-2.0-flash-lite` by default)
- MCP servers enabled for testing (`--mcp-servers github,huggingface`)

Override test model via: `make test TEST_MODEL=claude-3-5-haiku-20241022`
