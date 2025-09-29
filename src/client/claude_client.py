"""
Claude Client - Claude APIとの通信を行うクライアント
"""

import logging
from datetime import datetime
from typing import Any, Dict

import anthropic

logger = logging.getLogger(__name__)


class ClaudeClient:
    """Claude Client クラス"""

    def __init__(
        self,
        anthropic_api_key: str,
        model: str,
        max_tokens: int,
    ):
        self.anthropic_api_key = anthropic_api_key
        self.model = model
        self.max_tokens = max_tokens

    def send_message(self, message: str) -> Dict[str, Any]:
        """Claude APIにメッセージを送信"""
        try:
            client = anthropic.Anthropic(api_key=self.anthropic_api_key)

            response = client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=[{"role": "user", "content": message}],
                tools=[
                    {
                        "name": "web_search",
                        "description": "Search the web for real-time information about AI technology trends, news, and developments",
                        "input_schema": {
                            "type": "object",
                            "properties": {"query": {"type": "string", "description": "The search query to find relevant information"}},
                            "required": ["query"],
                        },
                    }
                ],
            )

            # response.content[0]はTextBlockであることを確認
            if not response.content or not hasattr(response.content[0], "text"):
                return {
                    "status": "error",
                    "message": "Invalid response format from Claude API",
                    "searched_at": datetime.now().isoformat(),
                }

            result = {
                "status": "success",
                "content": response.content[0].text,
                "searched_at": datetime.now().isoformat(),
                "model": self.model,
            }
            logger.info("Claude API呼び出しが正常に完了しました")
            return result

        except Exception as e:
            logger.error(f"Claude API呼び出しエラー: {e}")
            return {
                "status": "error",
                "message": str(e),
                "searched_at": datetime.now().isoformat(),
            }
