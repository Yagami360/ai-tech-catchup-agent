"""
Claude Code Client - Claude Codeを直接使用するクライアント
"""

import logging
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

logger = logging.getLogger(__name__)


class ClaudeCodeClient:
    """Claude Code Client クラス"""

    def __init__(self, claude_code_path: str = "claude", model: str = "claude-sonnet-4-20250514", max_tokens: int = 10000):
        """
        Claude Code Client を初期化

        Args:
            claude_code_path: Claude Codeの実行パス（デフォルト: claude）
            model: 使用するモデル名（デフォルト: claude-sonnet-4-20250514）
            max_tokens: 最大トークン数（デフォルト: 10000）
        """
        self.claude_code_path = claude_code_path
        self.model = model
        self.max_tokens = max_tokens

    def send_message(self, message: str, timeout: int = 3600) -> Dict[str, Any]:
        """
        Claude Codeにメッセージを送信してWeb Search機能を使用

        Args:
            message: 送信するメッセージ

        Returns:
            Claude Codeからの応答
        """
        try:
            # Claude Codeを実行（--printオプションで非対話的に実行）
            cmd = [self.claude_code_path, "--print", "--model", self.model]

            logger.info(f"Claude Code実行中: {' '.join(cmd)}")

            result = subprocess.run(cmd, input=message, capture_output=True, text=True, timeout=timeout, cwd=Path.cwd())

            if result.returncode != 0:
                logger.error(f"Claude Code実行エラー (returncode: {result.returncode})")
                logger.error(f"stderr: {result.stderr}")
                logger.error(f"stdout: {result.stdout}")

                # 5時間制限に達した場合の特別な処理
                if "5-hour limit reached" in result.stdout:
                    error_message = "Claude Codeの5時間制限に達しました。"
                else:
                    error_message = f"Claude Code実行エラー (returncode: {result.returncode}): {result.stderr or result.stdout}"

                return {
                    "status": "error",
                    "message": error_message,
                    "searched_at": datetime.now().isoformat(),
                }

            # 出力から結果を抽出
            content = result.stdout.strip()

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

        except subprocess.TimeoutExpired:
            logger.error("Claude Code実行がタイムアウトしました")
            return {
                "status": "error",
                "message": "Claude Code実行がタイムアウトしました",
                "searched_at": datetime.now().isoformat(),
            }
        except FileNotFoundError:
            logger.error(f"Claude Codeが見つかりません: {self.claude_code_path}")
            return {
                "status": "error",
                "message": f"Claude Codeが見つかりません: {self.claude_code_path}",
                "searched_at": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Claude Code実行中にエラー: {e}")
            return {
                "status": "error",
                "message": str(e),
                "searched_at": datetime.now().isoformat(),
            }

    def check_availability(self) -> bool:
        """
        Claude Codeが利用可能かチェック

        Returns:
            Claude Codeが利用可能な場合True
        """
        try:
            result = subprocess.run([self.claude_code_path, "--version"], capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
