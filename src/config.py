"""
AI Tech Catchup Agent の設定ファイル
"""

import logging
import os

from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """アプリケーション設定"""

    # Anthropic Claude API
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")

    # GitHub設定
    github_token: str = os.getenv("GITHUB_TOKEN", "")
    github_repo: str = os.getenv("GITHUB_REPOSITORY", "Yagami360/ai-tech-catchup-agent")

    # Claude設定
    claude_model: str = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")
    max_tokens: int = int(os.getenv("MAX_TOKENS", "10000"))

    # プロンプト設定
    news_count: int = int(os.getenv("NEWS_COUNT", "20"))

    # Slack設定
    slack_webhook_url: str = os.getenv("SLACK_WEBHOOK_URL", "")

    model_config = {"env_file": ".env", "extra": "ignore"}


# グローバル設定インスタンス
settings = Settings()
logger.debug("settings: ", settings)
