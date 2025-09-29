"""
AI Tech Catchup Agent メインクラス
"""

import logging
from typing import Any, Dict, Optional

from ..client import ClaudeClient, GitHubClient
from ..config import settings
from ..utils import PromptManager

logger = logging.getLogger(__name__)


class AITechCatchupAgent:
    """AI Tech Catchup Agent メインクラス"""

    def __init__(self, claude_model: Optional[str] = None, max_tokens: Optional[int] = None, prompts_dir: str = "prompts"):
        model = claude_model or settings.claude_model
        tokens = max_tokens or settings.max_tokens
        self.claude_client = ClaudeClient(
            anthropic_api_key=settings.anthropic_api_key,
            model=model,
            max_tokens=tokens,
        )
        self.github_client = GitHubClient(token=settings.github_token, repo=settings.github_repo)
        self.prompt_manager = PromptManager(prompts_dir)

    def run_catchup(
        self,
        custom_prompt: Optional[str] = None,
        create_issue: bool = True,
        news_count: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Claude Codeで最新AI情報をキャッチアップ"""
        logger.info("Claude CodeでAI技術キャッチアップを開始...")

        try:
            # 1. プロンプトの準備
            logger.info("プロンプトを準備中...")
            logger.debug(f"カスタムプロンプト: {custom_prompt}")

            if not custom_prompt:
                prompt = self.prompt_manager.get_prompt("default_report", news_count=str(news_count or settings.news_count))
                if not prompt:
                    logger.error("デフォルト検索プロンプトを取得できませんでした")
                    return {"status": "error", "message": "プロンプトの取得に失敗しました"}
            else:
                prompt = self.prompt_manager.get_prompt(
                    "custom_search",
                    custom_prompt=custom_prompt,
                    news_count=str(news_count or settings.news_count),
                )
                if not prompt:
                    # フォールバック: カスタムプロンプトをそのまま使用
                    prompt = custom_prompt

            # 2. Claude APIで最新情報を検索
            logger.info("Claude APIで最新情報を検索中...")
            search_result = self.claude_client.send_message(prompt)

            if search_result["status"] != "success":
                logger.error(f"Claude Code検索エラー: {search_result['message']}")
                return {"status": "error", "message": search_result["message"]}

            result = {
                "status": "success",
                "content": search_result["content"],
                "searched_at": search_result["searched_at"],
            }

            # 2. GitHub Issue作成（オプション）
            if create_issue:
                logger.info("GitHub Issueを作成中...")
                issue_result = self.github_client.create_report_issue(search_result["content"], model_name=self.claude_client.model)

                if "error" in issue_result:
                    logger.error(f"Issue作成エラー: {issue_result['error']}")
                    return {"status": "error", "message": issue_result["error"]}

                logger.info(f"レポートIssueを作成しました: {issue_result.get('html_url', '')}")
                result["issue_url"] = issue_result.get("html_url", "")
            else:
                logger.info("GitHub Issue作成をスキップしました")

            return result

        except Exception as e:
            logger.error(f"キャッチアップ実行中にエラー: {e}")
            return {"status": "error", "message": str(e)}

    def weekly_report(self, create_issue: bool = True) -> Dict[str, Any]:
        """週次レポートを生成"""
        logger.info("週次レポート生成を開始...")

        try:
            # プロンプトの準備
            prompt = self.prompt_manager.get_prompt("weekly_report")
            if not prompt:
                logger.error("週次レポートプロンプトを取得できませんでした")
                return {"status": "error", "message": "プロンプトの取得に失敗しました"}

            # Claude APIでレポート生成
            search_result = self.claude_client.send_message(prompt)

            if search_result["status"] != "success":
                return {"status": "error", "message": search_result["message"]}

            result = {
                "status": "success",
                "content": search_result["content"],
                "searched_at": search_result["searched_at"],
            }

            # GitHub Issue作成（オプション）
            if create_issue:
                from datetime import datetime

                issue_result = self.github_client.create_issue(
                    title=f"AI Tech Catchup Weekly Report - {datetime.now().strftime('%Y-%m-%d')}",
                    body=search_result["content"],
                    model_name=self.claude_client.model,
                )
                if issue_result.get("html_url"):
                    result["issue_url"] = issue_result.get("html_url", "")
            else:
                logger.info("GitHub Issue作成をスキップしました")

            return result

        except Exception as e:
            logger.error(f"週次レポート生成中にエラー: {e}")
            return {"status": "error", "message": str(e)}

    def monthly_report(self, create_issue: bool = True) -> Dict[str, Any]:
        """月次レポートを生成"""
        logger.info("月次レポート生成を開始...")

        try:
            # プロンプトの準備
            prompt = self.prompt_manager.get_prompt("monthly_report")
            if not prompt:
                logger.error("月次レポートプロンプトを取得できませんでした")
                return {"status": "error", "message": "プロンプトの取得に失敗しました"}

            # Claude APIでレポート生成
            search_result = self.claude_client.send_message(prompt)

            if search_result["status"] != "success":
                return {"status": "error", "message": search_result["message"]}

            result = {
                "status": "success",
                "content": search_result["content"],
                "searched_at": search_result["searched_at"],
            }

            # GitHub Issue作成（オプション）
            if create_issue:
                from datetime import datetime

                issue_result = self.github_client.create_issue(
                    title=f"AI Tech Catchup Monthly Report - {datetime.now().strftime('%Y-%m')}",
                    body=search_result["content"],
                    model_name=self.claude_client.model,
                )
                if issue_result.get("html_url"):
                    result["issue_url"] = issue_result.get("html_url", "")
            else:
                logger.info("GitHub Issue作成をスキップしました")

            return result

        except Exception as e:
            logger.error(f"月次レポート生成中にエラー: {e}")
            return {"status": "error", "message": str(e)}
