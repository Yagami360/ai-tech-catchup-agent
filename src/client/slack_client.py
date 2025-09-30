"""
Slack Client - Slack Webhookを使用した通知機能
"""

import json
import logging
from datetime import datetime
from typing import Any, Dict, Optional

import requests

logger = logging.getLogger(__name__)


class SlackClient:
    """Slack Client クラス"""

    def __init__(self, webhook_url: str):
        """
        Slack Client を初期化

        Args:
            webhook_url: Slack Webhook URL
        """
        self.webhook_url = webhook_url

    def send_notification(
        self,
        title: str,
        content: str,
        report_type: str = "report",
        issue_url: Optional[str] = None,
        model: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Slackに通知を送信

        Args:
            title: レポートタイトル
            content: レポート内容
            report_type: レポートタイプ (report, weekly-report, monthly-report)
            issue_url: GitHub Issue URL
            model: 使用したモデル名

        Returns:
            送信結果
        """
        try:
            # レポートタイプに応じたアイコンと色を設定
            icon_emoji, color = self._get_report_style(report_type)

            # Slackメッセージのペイロードを作成
            payload: Dict[str, Any] = {
                "username": "AI Tech Catchup Agent",
                "icon_emoji": icon_emoji,
                "attachments": [
                    {
                        "color": color,
                        "title": title,
                        "title_link": issue_url,
                        "text": self._format_content(content),
                        "fields": [
                            {
                                "title": "レポートタイプ",
                                "value": self._get_report_type_display(report_type),
                                "short": True,
                            },
                            {
                                "title": "生成日時",
                                "value": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                "short": True,
                            },
                        ],
                        "footer": "AI Tech Catchup Agent",
                        "ts": int(datetime.now().timestamp()),
                    }
                ],
            }

            # モデル情報がある場合は追加
            if model:
                payload["attachments"][0]["fields"].append(
                    {
                        "title": "使用モデル",
                        "value": model,
                        "short": True,
                    }
                )

            # GitHub Issue URLがある場合は追加
            if issue_url:
                payload["attachments"][0]["fields"].append(
                    {
                        "title": "GitHub Issue",
                        "value": f"<{issue_url}|Issueを確認>",
                        "short": True,
                    }
                )

            # Slack Webhookに送信
            response = requests.post(
                self.webhook_url,
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"},
                timeout=30,
            )

            if response.status_code == 200:
                logger.info("Slack通知を送信しました")
                return {
                    "status": "success",
                    "message": "Slack通知を送信しました",
                    "sent_at": datetime.now().isoformat(),
                }
            else:
                logger.error(f"Slack通知送信エラー: {response.status_code} - {response.text}")
                return {
                    "status": "error",
                    "message": f"Slack通知送信エラー: {response.status_code}",
                    "sent_at": datetime.now().isoformat(),
                }

        except Exception as e:
            logger.error(f"Slack通知送信中にエラー: {e}")
            return {
                "status": "error",
                "message": str(e),
                "sent_at": datetime.now().isoformat(),
            }

    def _get_report_style(self, report_type: str) -> tuple[str, str]:
        """
        レポートタイプに応じたアイコンと色を取得

        Args:
            report_type: レポートタイプ

        Returns:
            (icon_emoji, color) のタプル
        """
        styles = {
            "report": (":robot_face:", "good"),  # 緑
            "weekly-report": (":chart_with_upwards_trend:", "#36a64f"),  # 緑
            "monthly-report": (":bar_chart:", "#2eb886"),  # 青緑
        }
        return styles.get(report_type, (":robot_face:", "good"))

    def _get_report_type_display(self, report_type: str) -> str:
        """
        レポートタイプの表示名を取得

        Args:
            report_type: レポートタイプ

        Returns:
            表示名
        """
        displays = {
            "report": "📰 最新レポート",
            "weekly-report": "📊 週次レポート",
            "monthly-report": "📈 月次レポート",
        }
        return displays.get(report_type, "📰 レポート")

    def _format_content(self, content: str, max_length: int = 2000) -> str:
        """
        コンテンツをSlack用にフォーマット

        Args:
            content: 元のコンテンツ
            max_length: 最大文字数

        Returns:
            フォーマットされたコンテンツ
        """
        # 文字数制限
        if len(content) > max_length:
            content = content[:max_length] + "..."

        # Markdownの一部をSlack形式に変換
        content = content.replace("**", "*")
        content = content.replace("##", "*")
        content = content.replace("###", "*")

        return content

    def test_connection(self) -> Dict[str, Any]:
        """
        Slack接続をテスト

        Returns:
            テスト結果
        """
        try:
            test_payload: Dict[str, Any] = {
                "username": "AI Tech Catchup Agent",
                "icon_emoji": ":robot_face:",
                "text": "🧪 Slack接続テスト - 正常に接続できました！",
            }

            response = requests.post(
                self.webhook_url,
                data=json.dumps(test_payload),
                headers={"Content-Type": "application/json"},
                timeout=30,
            )

            if response.status_code == 200:
                return {
                    "status": "success",
                    "message": "Slack接続テストが成功しました",
                }
            else:
                return {
                    "status": "error",
                    "message": f"Slack接続テストが失敗しました: {response.status_code}",
                }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Slack接続テスト中にエラー: {e}",
            }
