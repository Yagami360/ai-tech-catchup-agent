import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from claude_code_sdk import ClaudeCodeOptions, ClaudeSDKClient

from ..utils import MCPServerManager

logger = logging.getLogger(__name__)


class ClaudeCodeClient:
    """Claude Code Client クラス"""

    def __init__(
        self,
        model_name: str = "claude-sonnet-4-20250514",
        max_tokens: int | None = None,
        enabled_mcp_servers: Optional[List[str]] = None,
    ):
        """
        Claude Code Client を初期化

        Args:
            model_name: 使用するモデル名（デフォルト: claude-sonnet-4-20250514）
            max_tokens: 最大トークン数（デフォルト: None）
            enabled_mcp_servers: 有効にする MCP サーバー名のリスト（例: ["github", "filesystem"]）
        """
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.enabled_mcp_servers = enabled_mcp_servers or []
        self.mcp_manager = MCPServerManager()

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

            # 非同期関数を同期的に実行
            return asyncio.run(self._send_message_async(message, timeout))

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
            # 基本的な許可ツール
            allowed_tools = ["WebSearch", "WebFetch", "Read", "Bash"]

            # MCP サーバー設定を構築
            mcp_servers = {}
            if self.enabled_mcp_servers:
                logger.info(f"MCP サーバーを有効化: {', '.join(self.enabled_mcp_servers)}")
                mcp_servers = self.mcp_manager.build_mcp_config(self.enabled_mcp_servers)

                # 有効な MCP サーバーのツールを許可リストに追加
                mcp_tools = self.mcp_manager.get_allowed_tools(self.enabled_mcp_servers)
                allowed_tools.extend(mcp_tools)
                logger.info(f"MCP ツールを許可リストに追加: {mcp_tools}")

            # Claude Code SDKオプションを設定
            env_vars = {}
            if self.max_tokens is not None:
                env_vars["CLAUDE_CODE_MAX_OUTPUT_TOKENS"] = str(self.max_tokens)

            options = ClaudeCodeOptions(
                model=self.model_name,
                allowed_tools=allowed_tools,
                permission_mode="acceptEdits",
                mcp_servers=mcp_servers if mcp_servers else None,  # type: ignore[arg-type]
                env=env_vars if env_vars else {},
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
                    "model": self.model_name,
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
