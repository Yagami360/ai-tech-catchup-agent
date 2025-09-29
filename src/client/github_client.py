"""
GitHub Client - Issue/PRの自動作成と管理
"""

import json
import logging
from typing import Any, Dict, Optional

import requests

logger = logging.getLogger(__name__)


class GitHubClient:
    """GitHubクライアントクラス"""

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
        self,
        title: str,
        body: str,
        labels: Optional[list] = None,
    ) -> Dict[str, Any]:
        """GitHub Issueを作成"""
        try:
            data = {
                "title": title,
                "body": body,
                "labels": labels or [],
            }

            response = requests.post(f"{self.base_url}/issues", headers=self.headers, data=json.dumps(data))

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
                        retry_data: Dict[str, Any] = retry_response.json()
                        logger.info(f"ラベルなしでIssue作成成功: {retry_data['html_url']}")
                        return retry_data

                return {"error": f"{response.status_code}: {error_detail}"}

            response.raise_for_status()
            issue_data: Dict[str, Any] = response.json()
            logger.info(f"Issue created: {issue_data['html_url']}")
            return issue_data

        except Exception as e:
            logger.error(f"Issue作成に失敗: {e}")
            return {"error": str(e)}

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

            result: Dict[str, Any] = response.json()
            return result

        except Exception as e:
            logger.error(f"Issue更新に失敗: {e}")
            return {"error": str(e)}
