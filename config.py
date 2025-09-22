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
    github_repo: str = os.getenv("GITHUB_REPOSITORY", "")

    # 情報ソース設定
    rss_feeds: List[str] = [
        "https://feeds.feedburner.com/oreilly/radar",
        "https://openai.com/blog/rss.xml",
        "https://blog.google/technology/ai/feed/",
        "https://ai.googleblog.com/feeds/posts/default",
        "https://www.anthropic.com/news/rss.xml",
        "https://huggingface.co/blog/rss.xml",
        "https://blog.ml.cmu.edu/feed/",
        "https://distill.pub/rss.xml",
    ]

    # 検索キーワード
    search_keywords: List[str] = [
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "LLM",
        "Local LLM",
        "GPT",
        "ChatGPT",
        "Claude",
        "Gemini",
        "AI Agent",
        "RAG",
        "MCP server",
        "computer vision",
        "reinforcement learning",
        "robotics",
        "Robotics AI",
        "Pyshical AI",
        "VLMs",
        "VLA",
    ]

    # レポート設定
    report_frequency: str = "weekly"  # daily, weekly, monthly
    max_articles_per_report: int = 10
    report_language: str = "ja"  # ja, en

    # Claude設定
    claude_model: str = "claude-3-5-sonnet-20241022"
    max_tokens: int = 4000

    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }


# グローバル設定インスタンス
settings = Settings()
