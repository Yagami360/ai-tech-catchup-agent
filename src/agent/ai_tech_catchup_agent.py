"""
AI Tech Catchup Agent メインクラス
"""

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from ..client import ClaudeCodeClient, GitHubClient, SlackClient
from ..config import settings
from ..utils import PromptManager

logger = logging.getLogger(__name__)


class AITechCatchupAgent:
    """AI Tech Catchup Agent メインクラス"""

    def __init__(
        self, claude_model: Optional[str] = None, max_tokens: Optional[int] = None, prompts_dir: str = "prompts", enable_slack: bool = False
    ):
        self.claude_model = claude_model or settings.claude_model
        self.max_tokens = max_tokens or settings.max_tokens
        self.claude_client = ClaudeCodeClient(model=self.claude_model)
        self.github_client = GitHubClient(token=settings.github_token, repo=settings.github_repo)
        self.prompt_manager = PromptManager(prompts_dir)

        # Slack通知の初期化（enable_slackがTrueでWebhook URLが設定されている場合のみ）
        self.slack_client = None
        if enable_slack and settings.slack_webhook_url:
            self.slack_client = SlackClient(webhook_url=settings.slack_webhook_url)

    def run_catchup(
        self,
        create_issue: bool = True,
        news_count: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Claude Codeで最新AI情報をキャッチアップ"""
        logger.info("Claude CodeでAI技術キャッチアップを開始...")

        try:
            # 1. プロンプトの準備
            logger.info("プロンプトを準備中...")
            prompt = self.prompt_manager.get_prompt("default_report", news_count=str(news_count or settings.news_count))
            if not prompt:
                logger.error("デフォルト検索プロンプトを取得できませんでした")
                return {"status": "error", "message": "プロンプトの取得に失敗しました"}

            # 2. Claude Codeで最新情報を検索
            logger.info("Claude Codeで最新情報を検索中...")
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
                issue_body = f"""# 🤖 AI Tech Catchup Report

- レポート日時: `{datetime.now().strftime("%Y-%m-%d %H:%M")}`
- 使用モデル: `{self.claude_model}`
---

{search_result["content"]}

---

*このレポートは AI Tech Catchup Agent によって自動生成されました。*
"""
                issue_result = self.github_client.create_issue(
                    title=f"🤖 AI Tech Catchup Report - {datetime.now().strftime('%Y-%m-%d')}",
                    body=issue_body,
                    labels=["report", self.claude_client.model],
                )

                if "error" in issue_result:
                    logger.error(f"Issue作成エラー: {issue_result['error']}")
                    return {"status": "error", "message": issue_result["error"]}

                logger.info(f"レポートIssueを作成しました: {issue_result.get('html_url', '')}")
                result["issue_url"] = issue_result.get("html_url", "")

                # Slack通知（設定されている場合）
                if self.slack_client:
                    self._send_slack_notification(
                        title=f"🤖 AI Tech Catchup Report - {datetime.now().strftime('%Y-%m-%d')}",
                        content=search_result["content"],
                        report_type="report",
                        issue_url=issue_result.get("html_url"),
                        model=self.claude_model,
                    )
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

            # Claude Codeでレポート生成
            logger.info(f"入力プロンプト: {prompt}")
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
                # 週次レポートの調査期間を計算
                today = datetime.now()
                week_ago = today - timedelta(days=7)
                week_period = f"{week_ago.strftime('%Y-%m-%d')} ~ {today.strftime('%Y-%m-%d')}"

                # 週番号を計算（月の第何週目か）
                week_number = (today.day - 1) // 7 + 1
                week_title = f"{today.strftime('%Y年%m月')}第{week_number}週"
                issue_body = f"""# AI Tech Catchup Weekly Report

- レポート日時: `{datetime.now().strftime("%Y-%m-%d %H:%M")}`
- 調査期間: `{week_period}`
- 使用モデル: `{self.claude_model}`
---

{search_result["content"]}

---

*このレポートは AI Tech Catchup Agent によって自動生成されました。*
"""
                issue_result = self.github_client.create_issue(
                    title=f"AI Tech Catchup Weekly Report - {week_title}",
                    body=issue_body,
                    labels=["weekly-report", self.claude_client.model],
                )
                if issue_result.get("html_url"):
                    result["issue_url"] = issue_result.get("html_url", "")

                    # Slack通知（設定されている場合）
                    if self.slack_client:
                        self._send_slack_notification(
                            title=f"AI Tech Catchup Weekly Report - {week_title}",
                            content=search_result["content"],
                            report_type="weekly-report",
                            issue_url=issue_result.get("html_url"),
                            model=self.claude_model,
                        )
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

            # Claude Codeでレポート生成
            logger.info(f"入力プロンプト: {prompt}")
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
                # 月次レポートの調査期間を計算
                today = datetime.now()
                month_ago = today - timedelta(days=30)
                month_period = f"{month_ago.strftime('%Y-%m-%d')} ~ {today.strftime('%Y-%m-%d')}"
                issue_body = f"""# AI Tech Catchup Monthly Report

- レポート日時: `{datetime.now().strftime("%Y-%m-%d %H:%M")}`
- 調査期間: `{month_period}`
- 使用モデル: `{self.claude_model}`
---

{search_result["content"]}

---

*このレポートは AI Tech Catchup Agent によって自動生成されました。*
"""
                issue_result = self.github_client.create_issue(
                    title=f"AI Tech Catchup Monthly Report - {datetime.now().strftime('%Y年%m月')}",
                    body=issue_body,
                    labels=["monthly-report", self.claude_client.model],
                )
                if issue_result.get("html_url"):
                    result["issue_url"] = issue_result.get("html_url", "")

                    # Slack通知（設定されている場合）
                    if self.slack_client:
                        self._send_slack_notification(
                            title=f"AI Tech Catchup Monthly Report - {datetime.now().strftime('%Y年%m月')}",
                            content=search_result["content"],
                            report_type="monthly-report",
                            issue_url=issue_result.get("html_url"),
                            model=self.claude_model,
                        )
            else:
                logger.info("GitHub Issue作成をスキップしました")

            return result

        except Exception as e:
            logger.error(f"月次レポート生成中にエラー: {e}")
            return {"status": "error", "message": str(e)}

    def _send_slack_notification(
        self,
        title: str,
        content: str,
        report_type: str,
        issue_url: Optional[str] = None,
        model: Optional[str] = None,
    ) -> None:
        """
        Slack通知を送信（ヘルパーメソッド）

        Args:
            title: レポートタイトル
            content: レポート内容
            report_type: レポートタイプ
            issue_url: GitHub Issue URL
            model: 使用したモデル名
        """
        try:
            if not self.slack_client:
                logger.warning("Slack通知が設定されていません")
                return

            slack_result = self.slack_client.send_notification(
                title=title,
                content=content,
                report_type=report_type,
                issue_url=issue_url,
                model=model,
            )

            if slack_result["status"] == "success":
                logger.info("Slack通知を送信しました")
            else:
                logger.error(f"Slack通知送信エラー: {slack_result['message']}")

        except Exception as e:
            logger.error(f"Slack通知送信中にエラー: {e}")
