"""
AI Tech Catchup Agent メインアプリケーション
"""
import logging
import sys
from datetime import datetime
from typing import Any, Dict

from config import settings
from .claude_search import ClaudeSearch
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
        self.claude_search = ClaudeSearch(
            anthropic_api_key=settings.anthropic_api_key, model=settings.claude_model
        )
        self.github_integration = GitHubIntegration(
            token=settings.github_token, repo=settings.github_repo
        )

    def run_catchup(
        self,
        custom_prompt: str = None,
        create_issue: bool = True,
        news_count: int = None,
    ) -> Dict[str, Any]:
        """Claude Codeで最新AI情報をキャッチアップ"""
        logger.info("Claude CodeでAI技術キャッチアップを開始...")

        try:
            # 1. Claude Codeで最新情報を検索
            logger.info("Claude Codeで最新情報を検索中...")
            logger.debug(f"カスタムプロンプト: {custom_prompt}")
            search_result = self.claude_search.search_latest_ai_news(
                custom_prompt, news_count=news_count or settings.news_count
            )

            if search_result["status"] != "success":
                logger.error(f"Claude Code検索エラー: {search_result['message']}")
                return {"status": "error", "message": search_result["message"]}

            result = {
                "status": "success",
                "content": search_result["content"],
                "searched_at": search_result["searched_at"],
            }

            # 2. GitHub Issue作成（オプション）
            if create_issue:
                logger.info("GitHub Issueを作成中...")
                issue_result = self.github_integration.create_weekly_report_issue(
                    search_result["content"], model_name=self.claude_search.model
                )

                if "error" in issue_result:
                    logger.error(f"Issue作成エラー: {issue_result['error']}")
                    return {"status": "error", "message": issue_result["error"]}

                logger.info(f"週間レポートIssueを作成しました: {issue_result.get('html_url', '')}")
                result["issue_url"] = issue_result.get("html_url", "")
            else:
                logger.info("GitHub Issue作成をスキップしました")

            return result

        except Exception as e:
            logger.error(f"キャッチアップ実行中にエラー: {e}")
            return {"status": "error", "message": str(e)}

    def search_topic(self, topic: str, create_issue: bool = True) -> Dict[str, Any]:
        """特定トピックについてClaude Codeで検索"""
        logger.info(f"特定トピック検索を開始: {topic}")

        try:
            search_result = self.claude_search.search_specific_topic(topic)

            if search_result["status"] != "success":
                return {"status": "error", "message": search_result["message"]}

            result = {
                "status": "success",
                "topic": topic,
                "content": search_result["content"],
            }

            # GitHub Issue作成（オプション）
            if create_issue:
                issue_result = self.github_integration.create_tech_insight_issue(
                    title=f"{topic}に関する最新動向",
                    content=search_result["content"],
                    category="Tech Insight",
                    model_name=self.claude_search.model,
                )
                result["issue_url"] = issue_result.get("html_url", "")
            else:
                logger.info("GitHub Issue作成をスキップしました")

            return result

        except Exception as e:
            logger.error(f"トピック検索中にエラー: {e}")
            return {"status": "error", "message": str(e)}


def main():
    """メイン関数"""
    agent = AITechCatchupAgent()

    # --no-issueフラグをチェック
    no_issue = "--no-issue" in sys.argv
    if no_issue:
        sys.argv.remove("--no-issue")  # フラグを削除して通常の引数処理に影響しないようにする

    # --news-countオプションをチェック
    news_count = None
    if "--news-count" in sys.argv:
        try:
            index = sys.argv.index("--news-count")
            if index + 1 < len(sys.argv):
                news_count = int(sys.argv[index + 1])
                # オプションと値を削除
                sys.argv.pop(index)
                sys.argv.pop(index)
        except (ValueError, IndexError):
            logger.error("--news-countには有効な数値を指定してください")
            sys.exit(1)

    # コマンドライン引数で実行モードを指定
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        if mode == "topic":
            topic = sys.argv[2] if len(sys.argv) > 2 else "大規模言語モデル"
            result = agent.search_topic(topic, create_issue=not no_issue)
        elif mode == "weekly":
            result = agent.claude_search.search_weekly_report()
            if result["status"] == "success" and not no_issue:
                # GitHub Issue作成
                issue_result = agent.github_integration.create_issue(
                    title=f"週次AI技術レポート - {datetime.now().strftime('%Y年%m月%d日')}",
                    body=result["content"],
                    model_name=agent.claude_search.model,
                )
                if issue_result.get("html_url"):
                    result["issue_url"] = issue_result.get("html_url", "")
        elif mode == "monthly":
            result = agent.claude_search.search_monthly_summary()
            if result["status"] == "success" and not no_issue:
                # GitHub Issue作成
                issue_result = agent.github_integration.create_issue(
                    title=f"月次AI技術サマリー - {datetime.now().strftime('%Y年%m月')}",
                    body=result["content"],
                    model_name=agent.claude_search.model,
                )
                if issue_result.get("html_url"):
                    result["issue_url"] = issue_result.get("html_url", "")
        elif mode == "custom":
            prompt = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else None
            result = agent.run_catchup(
                prompt, create_issue=not no_issue, news_count=news_count
            )
        else:
            print(
                "使用法: python main.py [topic <topic>|weekly|monthly|custom <prompt>] [--no-issue] [--news-count N]"
            )
            print("引数なしで実行するとデフォルトのキャッチアップを実行します")
            print("--no-issueフラグを指定するとGitHub Issueを作成しません")
            print("--news-count N で重要ニュースの件数を指定できます（デフォルト: 10）")
            sys.exit(1)
    else:
        # デフォルトでキャッチアップを実行
        result = agent.run_catchup(create_issue=not no_issue, news_count=news_count)

    # 結果を出力
    print(f"実行結果: {result}")

    if result["status"] == "success":
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
