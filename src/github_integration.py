"""
GitHub統合モジュール - Issue/PRの自動作成と管理
"""
import json
import logging
from datetime import datetime
from typing import Any, Dict, Optional

import requests

logger = logging.getLogger(__name__)


class GitHubIntegration:
    """GitHub統合クラス"""

    def __init__(self, token: str, repo: str):
        self.token = token
        self.repo = repo
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json",
        }
        self.base_url = f"https://api.github.com/repos/{repo}"

    def _format_model_label(self, model_name: str) -> str:
        """モデル名をラベル用にフォーマット"""
        # モデル名を短縮形に変換
        model_mapping = {
            "claude-3-5-sonnet-20241022": "claude-3.5-sonnet",
            "claude-3-5-haiku-20241022": "claude-3.5-haiku",
            "claude-3-opus-20240229": "claude-3-opus",
            "gpt-4": "gpt-4",
            "gpt-4-turbo": "gpt-4-turbo",
            "gpt-3.5-turbo": "gpt-3.5-turbo",
        }

        # マッピングにない場合は汎用的な形式で作成
        if model_name in model_mapping:
            return f"model:{model_mapping[model_name]}"
        else:
            # モデル名から主要部分を抽出
            if "claude" in model_name.lower():
                return "model:claude"
            elif "gpt" in model_name.lower():
                return "model:gpt"
            else:
                return f"model:{model_name.split('-')[0]}"

    def create_issue(
        self,
        title: str,
        body: str,
        labels: Optional[list] = None,
        model_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """GitHub Issueを作成"""
        try:
            # モデル名がある場合は本文に追加
            if model_name:
                body = f"""**使用モデル**: `{model_name}`

---

{body}"""

            # ラベルにモデル名を追加
            issue_labels = labels or []
            if model_name:
                # モデル名からラベル用の短縮形を作成
                model_label = self._format_model_label(model_name)
                issue_labels.append(model_label)

            data = {
                "title": title,
                "body": body,
                "labels": issue_labels,
            }

            response = requests.post(
                f"{self.base_url}/issues", headers=self.headers, data=json.dumps(data)
            )

            if response.status_code != 201:
                error_detail = response.text
                logger.error(f"Issue作成に失敗: {response.status_code} - {error_detail}")
                logger.error(f"リクエストデータ: {json.dumps(data, ensure_ascii=False)}")

                # 422エラーの場合、ラベルなしで再試行
                if response.status_code == 422 and issue_labels:
                    logger.info("ラベルなしでIssue作成を再試行します...")
                    data_without_labels = {"title": title, "body": body}
                    retry_response = requests.post(
                        f"{self.base_url}/issues",
                        headers=self.headers,
                        data=json.dumps(data_without_labels),
                    )
                    if retry_response.status_code == 201:
                        retry_data = retry_response.json()
                        logger.info(f"ラベルなしでIssue作成成功: {retry_data['html_url']}")
                        return retry_data

                return {"error": f"{response.status_code}: {error_detail}"}

            response.raise_for_status()
            issue_data = response.json()
            logger.info(f"Issue created: {issue_data['html_url']}")
            return issue_data

        except Exception as e:
            logger.error(f"Issue作成に失敗: {e}")
            return {"error": str(e)}

    def create_pr(
        self, title: str, body: str, head: str, base: str = "main"
    ) -> Dict[str, Any]:
        """Pull Requestを作成"""
        try:
            data = {"title": title, "body": body, "head": head, "base": base}

            response = requests.post(
                f"{self.base_url}/pulls", headers=self.headers, data=json.dumps(data)
            )
            response.raise_for_status()

            pr_data = response.json()
            logger.info(f"PR created: {pr_data['html_url']}")
            return pr_data

        except Exception as e:
            logger.error(f"PR作成に失敗: {e}")
            return {"error": str(e)}

    def create_weekly_report_issue(
        self, report_content: str, model_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """週間レポートのIssueを作成"""
        today = datetime.now().strftime("%Y-%m-%d")
        title = f"🤖 AI Tech Catchup Weekly Report - {today}"

        # Issue本文をフォーマット
        body = f"""# 🤖 AI Tech Catchup Weekly Report

**レポート日時**: {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

{report_content}

---

*このレポートは AI Tech Catchup Agent によって自動生成されました。*
"""

        # ラベルにモデル名を追加
        labels = ["weekly-report"]
        if model_name:
            model_label = self._format_model_label(model_name)
            labels.append(model_label)

        return self.create_issue(
            title=title,
            body=body,
            labels=labels,
            model_name=model_name,
        )

    def create_tech_insight_issue(
        self, title: str, content: str, category: str, model_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """技術インサイトのIssueを作成"""
        issue_title = f"🔍 {category}: {title}"

        body = f"""# {category}: {title}

**作成日時**: {datetime.now().strftime("%Y年%m月%d日 %H:%M")}

---

{content}

---

*このインサイトは AI Tech Catchup Agent によって自動生成されました。*
"""

        # ラベルにモデル名を追加
        labels = ["tech-insight", category.lower()]
        if model_name:
            model_label = self._format_model_label(model_name)
            labels.append(model_label)

        return self.create_issue(
            title=issue_title,
            body=body,
            labels=labels,
            model_name=model_name,
        )

    def update_issue(self, issue_number: int, body: str) -> Dict[str, Any]:
        """Issueを更新"""
        try:
            data = {"body": body}

            response = requests.patch(
                f"{self.base_url}/issues/{issue_number}",
                headers=self.headers,
                data=json.dumps(data),
            )
            response.raise_for_status()

            return response.json()

        except Exception as e:
            logger.error(f"Issue更新に失敗: {e}")
            return {"error": str(e)}
