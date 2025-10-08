"""
AI Tech Catchup Agent の設定ファイル
"""

import logging
import os
from typing import Optional

from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """アプリケーション設定"""

    # モデル設定
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")
    model_name: str = os.getenv("MODEL_NAME", "claude-sonnet-4-20250514")
    max_tokens: Optional[int] = int(os.getenv("MAX_TOKENS")) if os.getenv("MAX_TOKENS") else None  # type: ignore[arg-type]

    # GitHub設定
    github_token: str = os.getenv("GITHUB_TOKEN", "")
    github_repo: str = os.getenv("GITHUB_REPOSITORY", "Yagami360/ai-tech-catchup-agent")

    # MCP設定
    # カンマ区切りで有効にする MCP サーバーを指定（例: "github,slack"）
    enabled_mcp_servers: str = os.getenv("ENABLED_MCP_SERVERS", "")

    # プロンプト設定
    news_count: int = int(os.getenv("NEWS_COUNT", "20"))

    model_config = {"env_file": ".env", "extra": "ignore"}


# グローバル設定インスタンス
settings = Settings()
logger.debug("settings: ", settings)
