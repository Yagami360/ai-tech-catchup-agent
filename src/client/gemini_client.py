"""
Gemini Client - Google Generative AI API を使用するクライアント
"""

import logging
from datetime import datetime
from typing import Any, Dict

import google.generativeai as genai

logger = logging.getLogger(__name__)


class GeminiClient:
    """Gemini Client クラス"""

    def __init__(self, google_api_key: str, model_name: str = "gemini-2.0-flash-exp", max_tokens: int = 10000):
        """
        Gemini Client を初期化

        Args:
            google_api_key: Google API Key
            model_name: 使用するモデル名（デフォルト: gemini-2.0-flash-exp）
            max_tokens: 最大トークン数（デフォルト: 10000）
        """
        self.google_api_key = google_api_key
        self.model_name = model_name
        self.max_tokens = max_tokens

        # Google AI APIの設定
        genai.configure(api_key=self.google_api_key)

    def send_message(self, message: str) -> Dict[str, Any]:
        """Gemini APIにメッセージを送信"""
        try:
            # Geminiモデルの初期化
            model = genai.GenerativeModel(
                self.model_name,
                # tools=["google_search_retrieval"],
            )

            # メッセージを送信
            response = model.generate_content(
                message,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=self.max_tokens,
                ),
            )

            # レスポンスの確認
            if not response.text:
                return {
                    "status": "error",
                    "message": "Geminiからの応答が空です",
                    "searched_at": datetime.now().isoformat(),
                }

            return {
                "status": "success",
                "content": response.text,
                "searched_at": datetime.now().isoformat(),
                "model": self.model_name,
            }

        except Exception as e:
            logger.error(f"Gemini API実行中にエラー: {e}")
            return {
                "status": "error",
                "message": str(e),
                "searched_at": datetime.now().isoformat(),
            }
