"""
AI Tech Catchup Agent メインクラス
"""

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union

from ..client import ClaudeCodeClient, GeminiClient, GitHubClient
from ..config import settings
from ..utils import PromptManager

logger = logging.getLogger(__name__)


class AITechCatchupAgent:
    """AI Tech Catchup Agent メインクラス"""

    def __init__(self, model: Optional[str] = None, max_tokens: Optional[int] = None, prompts_dir: str = "prompts"):
        self.model_name = model or settings.model_name
        self.max_tokens = max_tokens or settings.max_tokens

        # モデル名に基づいてクライアントを選択
        self.ai_client: Union[ClaudeCodeClient, GeminiClient]
        if "claude" in self.model_name.lower():
            self.ai_client = ClaudeCodeClient(model_name=self.model_name, max_tokens=self.max_tokens)
        elif "gemini" in self.model_name.lower():
            self.ai_client = GeminiClient(google_api_key=settings.google_api_key, model_name=self.model_name, max_tokens=self.max_tokens)
        else:
            logger.error(f"未対応のモデルです: {self.model_name}")
            raise ValueError(f"未対応のモデルです: {self.model_name}")

        self.github_client = GitHubClient(token=settings.github_token, repo=settings.github_repo)
        self.prompt_manager = PromptManager(prompts_dir)

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

            # 2. LLM で最新情報を検索
            logger.info("LLM モデル名で最新情報を検索中...")
            search_result = self.ai_client.send_message(prompt)

            if search_result["status"] != "success":
                logger.error(f"LLM 検索エラー: {search_result['message']}")
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
- 使用モデル: `{self.model_name}`
---

{search_result["content"]}

---

*このレポートは AI Tech Catchup Agent によって自動生成されました。*
"""
                issue_result = self.github_client.create_issue(
                    title=f"🤖 AI Tech Catchup Report - {datetime.now().strftime('%Y-%m-%d')}",
                    body=issue_body,
                    labels=["report", self.model_name],
                )

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

            # LLM モデル名でレポート生成
            logger.info(f"入力プロンプト: {prompt}")
            search_result = self.ai_client.send_message(prompt)

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
                issue_body = f"""# 📊 AI Tech Catchup Weekly Report

- レポート日時: `{datetime.now().strftime("%Y-%m-%d %H:%M")}`
- 調査期間: `{week_period}`
- 使用モデル: `{self.model_name}`
---

{search_result["content"]}

---

*このレポートは AI Tech Catchup Agent によって自動生成されました。*
"""
                issue_result = self.github_client.create_issue(
                    title=f"📊 AI Tech Catchup Weekly Report - {week_title}",
                    body=issue_body,
                    labels=["weekly-report", self.model_name],
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

            # LLM モデル名でレポート生成
            logger.info(f"入力プロンプト: {prompt}")
            search_result = self.ai_client.send_message(prompt)

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
                issue_body = f"""# 📈 AI Tech Catchup Monthly Report

- レポート日時: `{datetime.now().strftime("%Y-%m-%d %H:%M")}`
- 調査期間: `{month_period}`
- 使用モデル: `{self.model_name}`
---

{search_result["content"]}

---

*このレポートは AI Tech Catchup Agent によって自動生成されました。*
"""
                issue_result = self.github_client.create_issue(
                    title=f"📈 AI Tech Catchup Monthly Report - {datetime.now().strftime('%Y年%m月')}",
                    body=issue_body,
                    labels=["monthly-report", self.model_name],
                )
                if issue_result.get("html_url"):
                    result["issue_url"] = issue_result.get("html_url", "")
            else:
                logger.info("GitHub Issue作成をスキップしました")

            return result

        except Exception as e:
            logger.error(f"月次レポート生成中にエラー: {e}")
            return {"status": "error", "message": str(e)}
