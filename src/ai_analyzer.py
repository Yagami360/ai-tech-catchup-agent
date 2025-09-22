"""
AI分析モジュール - Claude APIを使用した記事の分析と要約
"""
import json
import logging
from datetime import datetime
from typing import Any, Dict, List

import anthropic

from .data_collector import Article

logger = logging.getLogger(__name__)


class AIAnalyzer:
    """AI分析クラス"""

    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022"):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def analyze_articles(
        self, articles: List[Article], language: str = "ja"
    ) -> Dict[str, Any]:
        """記事リストを分析してレポートを生成"""
        if not articles:
            return {"error": "分析する記事がありません"}

        # 記事をまとめてプロンプトを作成
        articles_text = self._format_articles_for_analysis(articles)

        # システムプロンプトを設定
        system_prompt = self._get_system_prompt(language)

        # Claude APIにリクエスト
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": f"以下の最新AI技術に関する記事を分析してください：\n\n{articles_text}",
                    }
                ],
            )

            analysis_result = response.content[0].text

            # 結果をパースして構造化
            structured_result = self._parse_analysis_result(analysis_result, articles)

            return structured_result

        except Exception as e:
            logger.error(f"記事分析に失敗: {e}")
            return {"error": f"分析中にエラーが発生しました: {e}"}

    def _format_articles_for_analysis(self, articles: List[Article]) -> str:
        """記事を分析用にフォーマット"""
        formatted_text = ""

        for i, article in enumerate(articles[:10], 1):  # 最大10記事
            formatted_text += f"【記事{i}】\n"
            formatted_text += f"タイトル: {article.title}\n"
            formatted_text += f"URL: {article.url}\n"
            formatted_text += f"ソース: {article.source}\n"
            formatted_text += f"公開日: {article.published_date.strftime('%Y-%m-%d')}\n"
            formatted_text += f"内容: {article.content[:1000]}...\n\n"

        return formatted_text

    def _get_system_prompt(self, language: str) -> str:
        """システムプロンプトを取得"""
        if language == "ja":
            return """あなたは最新のAI技術動向を分析する専門家です。以下の記事を分析して、以下の形式でレポートを作成してください：

## 📊 今週のAI技術動向サマリー

### 🔥 重要ニュース（上位3件）
1. **[記事タイトル]** - 簡潔な説明
2. **[記事タイトル]** - 簡潔な説明  
3. **[記事タイトル]** - 簡潔な説明

### 📈 主要トレンド
- トレンド1: 詳細説明
- トレンド2: 詳細説明
- トレンド3: 詳細説明

### 🚀 技術的ハイライト
- 新技術や手法の説明
- 実装例や応用例

### 💡 開発者向けポイント
- 実践的なアドバイス
- 学習リソースの提案

### 📚 関連リソース
- 各記事のURLと簡単な説明

分析は客観的で実用的な観点から行い、技術者にとって価値のある情報を提供してください。"""
        else:
            return """You are an expert in analyzing the latest AI technology trends. Analyze the following articles and create a report in the following format:

## 📊 This Week's AI Technology Trends Summary

### 🔥 Top News (Top 3)
1. **[Article Title]** - Brief description
2. **[Article Title]** - Brief description  
3. **[Article Title]** - Brief description

### 📈 Major Trends
- Trend 1: Detailed explanation
- Trend 2: Detailed explanation
- Trend 3: Detailed explanation

### 🚀 Technical Highlights
- New technologies and methodologies
- Implementation examples and applications

### 💡 Developer Insights
- Practical advice
- Learning resource suggestions

### 📚 Related Resources
- URLs and brief descriptions of each article

Provide objective and practical analysis that offers valuable information for developers."""

    def _parse_analysis_result(
        self, analysis_text: str, articles: List[Article]
    ) -> Dict[str, Any]:
        """分析結果をパースして構造化"""
        return {
            "analysis": analysis_text,
            "article_count": len(articles),
            "analyzed_at": datetime.now().isoformat(),
            "articles": [article.to_dict() for article in articles],
        }

    def generate_weekly_summary(self, articles: List[Article]) -> str:
        """週間サマリーを生成"""
        analysis = self.analyze_articles(articles, "ja")

        if "error" in analysis:
            return f"エラー: {analysis['error']}"

        return analysis["analysis"]
