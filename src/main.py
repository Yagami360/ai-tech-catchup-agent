"""
AI Tech Catchup Agent メインアプリケーション
"""
import logging
import sys
from datetime import datetime
from typing import Any, Dict

from config import settings

from .ai_analyzer import AIAnalyzer
from .data_collector import DataCollector
from .github_integration import GitHubIntegration

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("ai_agent.log"), logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)


class AITechCatchupAgent:
    """AI Tech Catchup Agent メインクラス"""

    def __init__(self):
        self.data_collector = DataCollector(settings.rss_feeds)
        self.ai_analyzer = AIAnalyzer(
            api_key=settings.anthropic_api_key, model=settings.claude_model
        )
        self.github_integration = GitHubIntegration(
            token=settings.github_token, repo=settings.github_repo
        )

    def run_catchup(self) -> Dict[str, Any]:
        """キャッチアップを実行"""
        logger.info("AI技術キャッチアップを開始...")

        try:
            # 1. 記事を収集
            logger.info("最新記事を収集中...")
            articles = self.data_collector.search_articles_by_keywords(
                settings.search_keywords
            )

            if not articles:
                logger.warning("収集された記事がありません")
                return {"status": "warning", "message": "記事が見つかりませんでした"}

            logger.info(f"{len(articles)}件の記事を収集しました")

            # 2. AI分析
            logger.info("記事を分析中...")
            analysis_result = self.ai_analyzer.analyze_articles(
                articles, settings.report_language
            )

            if "error" in analysis_result:
                logger.error(f"分析エラー: {analysis_result['error']}")
                return {"status": "error", "message": analysis_result["error"]}

            # 3. GitHub Issue作成
            logger.info("GitHub Issueを作成中...")
            issue_result = self.github_integration.create_weekly_report_issue(
                analysis_result["analysis"]
            )

            if "error" in issue_result:
                logger.error(f"Issue作成エラー: {issue_result['error']}")
                return {"status": "error", "message": issue_result["error"]}

            logger.info(f"週間レポートIssueを作成しました: {issue_result.get('html_url', '')}")

            return {
                "status": "success",
                "articles_count": len(articles),
                "issue_url": issue_result.get("html_url", ""),
                "analysis": analysis_result["analysis"],
            }

        except Exception as e:
            logger.error(f"キャッチアップ実行中にエラー: {e}")
            return {"status": "error", "message": str(e)}

    def run_tech_insight_analysis(self, topic: str) -> Dict[str, Any]:
        """特定トピックの技術インサイト分析を実行"""
        logger.info(f"技術インサイト分析を開始: {topic}")

        try:
            # トピックに関連する記事を収集
            articles = self.data_collector.search_articles_by_keywords([topic])

            if not articles:
                return {"status": "warning", "message": f"'{topic}'に関する記事が見つかりませんでした"}

            # 分析実行
            analysis_result = self.ai_analyzer.analyze_articles(articles)

            if "error" in analysis_result:
                return {"status": "error", "message": analysis_result["error"]}

            # GitHub Issue作成
            issue_result = self.github_integration.create_tech_insight_issue(
                title=f"{topic}に関する最新動向",
                content=analysis_result["analysis"],
                category="Tech Insight",
            )

            return {
                "status": "success",
                "topic": topic,
                "articles_count": len(articles),
                "issue_url": issue_result.get("html_url", ""),
            }

        except Exception as e:
            logger.error(f"技術インサイト分析中にエラー: {e}")
            return {"status": "error", "message": str(e)}


def main():
    """メイン関数"""
    agent = AITechCatchupAgent()

    # コマンドライン引数で実行モードを指定
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        if mode == "insight":
            topic = sys.argv[2] if len(sys.argv) > 2 else "AI技術"
            result = agent.run_tech_insight_analysis(topic)
        else:
            print("使用法: python main.py [insight [topic]]")
            print("引数なしで実行するとキャッチアップを実行します")
            sys.exit(1)
    else:
        # デフォルトでキャッチアップを実行
        result = agent.run_catchup()

    # 結果を出力
    print(f"実行結果: {result}")

    if result["status"] == "success":
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
