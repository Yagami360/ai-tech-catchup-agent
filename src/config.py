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

    # プロンプト設定（レポートタイプ別のニュース件数）
    news_count: int = int(os.getenv("NEWS_COUNT", "10"))
    news_count_report: int = int(os.getenv("NEWS_COUNT_REPORT", "20"))
    news_count_weekly_report: int = int(os.getenv("NEWS_COUNT_WEEKLY_REPORT", "10"))
    news_count_monthly_report: int = int(os.getenv("NEWS_COUNT_MONTHLY_REPORT", "20"))
    news_count_test_report: int = int(os.getenv("NEWS_COUNT_TEST_REPORT", "1"))
    news_count_topic_report: int = int(os.getenv("NEWS_COUNT_TOPIC_REPORT", "10"))

    # Google ADK設定
    # Google ADKで使用するモデル（環境変数で上書き可能、デフォルトはMODEL_NAMEを使用）
    adk_model_name: str = os.getenv("ADK_MODEL_NAME", os.getenv("MODEL_NAME", "gemini-2.5-flash"))

    model_config = {"env_file": ".env", "extra": "ignore"}


# グローバル設定インスタンス
settings = Settings()
logger.debug("settings: ", settings)
