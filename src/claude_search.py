"""
Claude Code統合モジュール - ClaudeのWeb検索機能を活用した最新情報取得
"""
import logging
from typing import Dict, Any
from datetime import datetime
import anthropic

from .prompt_manager import PromptManager


logger = logging.getLogger(__name__)


class ClaudeSearch:
    """Claude Code統合クラス"""

    def __init__(
        self,
        anthropic_api_key: str,
        model: str,
        max_tokens: int,
        prompts_dir: str = "prompts",
    ):
        self.anthropic_api_key = anthropic_api_key
        self.model = model
        self.max_tokens = max_tokens
        self.prompt_manager = PromptManager(prompts_dir)

    def search_latest_ai_news(
        self, custom_prompt: str = None, news_count: int = None
    ) -> Dict[str, Any]:
        """最新AI情報をClaude Codeで検索"""
        try:
            client = anthropic.Anthropic(api_key=self.anthropic_api_key)

            # プロンプトの取得
            if not custom_prompt:
                prompt = self.prompt_manager.get_prompt(
                    "default_search", news_count=str(news_count) if news_count else None
                )
                if not prompt:
                    logger.error("デフォルト検索プロンプトを取得できませんでした")
                    return {"status": "error", "message": "プロンプトの取得に失敗しました"}
            else:
                prompt = self.prompt_manager.get_prompt(
                    "custom_search",
                    custom_prompt=custom_prompt,
                    news_count=str(news_count) if news_count else None,
                )
                if not prompt:
                    # フォールバック: カスタムプロンプトをそのまま使用
                    prompt = custom_prompt

            # Claude APIにリクエスト
            response = client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=[{"role": "user", "content": prompt}],
            )
            result = {
                "status": "success",
                "content": response.content[0].text,
                "searched_at": datetime.now().isoformat(),
                "model": self.model,
            }
            logger.info("Claude Code検索が正常に完了しました")
            return result

        except Exception as e:
            logger.error(f"Claude Code検索エラー: {e}")
            return {
                "status": "error",
                "message": str(e),
                "searched_at": datetime.now().isoformat(),
            }

    def search_specific_topic(self, topic: str) -> Dict[str, Any]:
        """特定トピックについてClaude Codeで検索"""
        prompt = self.prompt_manager.get_prompt("topic_search", topic=topic)
        if not prompt:
            logger.error("トピック検索プロンプトを取得できませんでした")
            return {"status": "error", "message": "プロンプトの取得に失敗しました"}

        return self.search_latest_ai_news(prompt)

    def search_weekly_report(self) -> Dict[str, Any]:
        """週次レポートを生成"""
        prompt = self.prompt_manager.get_prompt("weekly_report")
        if not prompt:
            logger.error("週次レポートプロンプトを取得できませんでした")
            return {"status": "error", "message": "プロンプトの取得に失敗しました"}

        return self.search_latest_ai_news(prompt)

    def search_monthly_summary(self) -> Dict[str, Any]:
        """月次サマリーを生成"""
        prompt = self.prompt_manager.get_prompt("monthly_summary")
        if not prompt:
            logger.error("月次サマリープロンプトを取得できませんでした")
            return {"status": "error", "message": "プロンプトの取得に失敗しました"}

        return self.search_latest_ai_news(prompt)
