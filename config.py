"""
AI Tech Catchup Agent の設定ファイル
"""
import os
from typing import Any, Dict, List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """アプリケーション設定"""

    # Anthropic Claude API
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")

    # GitHub設定
    github_token: str = os.getenv("GITHUB_TOKEN", "")
    github_repo: str = os.getenv("GITHUB_REPOSITORY", "Yagami360/ai-tech-catchup-agent")

    # レポート設定
    report_frequency: str = "weekly"  # daily, weekly, monthly
    report_language: str = "ja"  # ja, en

    # Claude設定
    claude_model: str = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")
    max_tokens: int = os.getenv("MAX_TOKENS", 100000)

    # レポート詳細設定
    news_count: int = os.getenv("NEWS_COUNT", 10)

    model_config = {"env_file": ".env", "extra": "ignore"}


# グローバル設定インスタンス
settings = Settings()
print("settings: ", settings)
