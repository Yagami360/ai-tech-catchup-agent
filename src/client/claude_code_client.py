"""
Claude Code Client - Claude Code Python SDKを使用するクライアント
"""

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict

from claude_code_sdk import ClaudeCodeOptions, ClaudeSDKClient

logger = logging.getLogger(__name__)


class ClaudeCodeClient:
    """Claude Code Client クラス（Python SDK使用）"""

    def __init__(self, model: str = "claude-sonnet-4-20250514", max_tokens: int = 10000):
        """
        Claude Code Client を初期化

        Args:
            model: 使用するモデル名（デフォルト: claude-sonnet-4-20250514）
            max_tokens: 最大トークン数（デフォルト: 10000）
        """
        self.model = model
        self.max_tokens = max_tokens

    def send_message(self, message: str, timeout: int = 3600) -> Dict[str, Any]:
        """
        Claude Codeにメッセージを送信してWeb Search機能を使用

        Args:
            message: 送信するメッセージ
            timeout: タイムアウト時間（秒）

        Returns:
            Claude Codeからの応答
        """
        try:
            logger.info(f"プロンプト: {message}")

            # max_tokensに基づいて文字数制限を追加
            estimated_chars = self.max_tokens * 2  # 日本語を考慮して2倍に設定
            token_instruction = f"\n\n**重要**: 回答は最大{self.max_tokens}トークン（約{estimated_chars}文字）以内で簡潔にまとめてください。"
            full_message = f"{message}{token_instruction}"

            # 非同期関数を同期的に実行
            return asyncio.run(self._send_message_async(full_message, timeout))

        except Exception as e:
            logger.error(f"Claude Code実行中にエラー: {e}")
            return {
                "status": "error",
                "message": str(e),
                "searched_at": datetime.now().isoformat(),
            }

    async def _send_message_async(self, message: str, timeout: int) -> Dict[str, Any]:
        """
        非同期でClaude Codeにメッセージを送信

        Args:
            message: 送信するメッセージ
            timeout: タイムアウト時間（秒）

        Returns:
            Claude Codeからの応答
        """
        try:
            # Claude Code SDKオプションを設定
            options = ClaudeCodeOptions(
                model=self.model,
                allowed_tools=["WebSearch", "Read", "Bash"],
                permission_mode="acceptEdits",
            )

            # Claude Code SDKクライアントを使用
            async with ClaudeSDKClient(options=options) as client:
                logger.info("Claude Code SDKで実行中...")

                # メッセージを送信
                await client.query(message)

                # レスポンスを収集
                content_parts = []
                async for msg in client.receive_response():
                    if hasattr(msg, "content"):
                        for block in msg.content:
                            if hasattr(block, "text"):
                                content_parts.append(block.text)
                    # 最終結果メッセージをチェック
                    if type(msg).__name__ == "ResultMessage":
                        break

                content = "".join(content_parts).strip()

                if not content:
                    logger.warning("Claude Codeからの応答が空です")
                    return {
                        "status": "error",
                        "message": "Claude Codeからの応答が空です",
                        "searched_at": datetime.now().isoformat(),
                    }

                logger.info("Claude Code実行が正常に完了しました")
                return {
                    "status": "success",
                    "content": content,
                    "searched_at": datetime.now().isoformat(),
                    "model": self.model,
                }

            # async with文の後に到達した場合のフォールバック
            return {
                "status": "error",
                "message": "Claude Codeからの応答を取得できませんでした",
                "searched_at": datetime.now().isoformat(),
            }

        except asyncio.TimeoutError:
            logger.error("Claude Code実行がタイムアウトしました")
            return {
                "status": "error",
                "message": "Claude Code実行がタイムアウトしました",
                "searched_at": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Claude Code SDK実行中にエラー: {e}")
            return {
                "status": "error",
                "message": str(e),
                "searched_at": datetime.now().isoformat(),
            }
