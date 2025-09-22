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

    def create_issue(
        self, title: str, body: str, labels: Optional[list] = None
    ) -> Dict[str, Any]:
        """GitHub Issueを作成"""
        try:
            data = {
                "title": title,
                "body": body,
                "labels": labels or ["ai-tech-catchup", "automated"],
            }

            response = requests.post(
                f"{self.base_url}/issues", headers=self.headers, data=json.dumps(data)
            )
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

    def create_weekly_report_issue(self, report_content: str) -> Dict[str, Any]:
        """週間レポートのIssueを作成"""
        today = datetime.now().strftime("%Y年%m月%d日")
        title = f"🤖 AI Tech Catchup Weekly Report - {today}"

        # Issue本文をフォーマット
        body = f"""# 🤖 AI Tech Catchup Weekly Report

**レポート日時**: {datetime.now().strftime("%Y年%m月%d日 %H:%M")}

---

{report_content}

---

*このレポートは AI Tech Catchup Agent によって自動生成されました。*
"""

        return self.create_issue(
            title=title,
            body=body,
            labels=["ai-tech-catchup", "weekly-report", "automated"],
        )

    def create_tech_insight_issue(
        self, title: str, content: str, category: str
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

        return self.create_issue(
            title=issue_title,
            body=body,
            labels=["ai-tech-catchup", "tech-insight", category.lower(), "automated"],
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
