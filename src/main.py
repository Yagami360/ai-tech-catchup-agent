"""
AI Tech Catchup Agent メインアプリケーション
"""
import logging
import sys
from typing import Any, Dict

from .config import settings
from .agent import AITechCatchupAgent

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("ai_agent.log"), logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)


def main():
    """メイン関数"""
    logger.info("Started AI Tech Catchup Agent")
    logger.debug(f"settings: {settings}")

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

    # --claude-modelオプションをチェック
    claude_model = None
    if "--claude-model" in sys.argv:
        try:
            index = sys.argv.index("--claude-model")
            if index + 1 < len(sys.argv):
                claude_model = sys.argv[index + 1]
                # オプションと値を削除
                sys.argv.pop(index)
                sys.argv.pop(index)
        except IndexError:
            logger.error("--claude-modelには有効なモデル名を指定してください")
            sys.exit(1)

    # --max-tokensオプションをチェック
    max_tokens = None
    if "--max-tokens" in sys.argv:
        try:
            index = sys.argv.index("--max-tokens")
            if index + 1 < len(sys.argv):
                max_tokens = int(sys.argv[index + 1])
                # オプションと値を削除
                sys.argv.pop(index)
                sys.argv.pop(index)
        except (ValueError, IndexError):
            logger.error("--max-tokensには有効な数値を指定してください")
            sys.exit(1)

    agent = AITechCatchupAgent(claude_model=claude_model, max_tokens=max_tokens)

    # コマンドライン引数で実行モードを指定
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        if mode == "topic":
            topic = sys.argv[2] if len(sys.argv) > 2 else "大規模言語モデル"
            result = agent.search_topic(topic, create_issue=not no_issue)
        elif mode == "weekly":
            result = agent.weekly_report(create_issue=not no_issue)
        elif mode == "monthly":
            result = agent.monthly_report(create_issue=not no_issue)
        elif mode == "custom":
            prompt = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else None
            result = agent.run_catchup(prompt, create_issue=not no_issue, news_count=news_count)
        else:
            print(
                "使用法: python main.py [topic <topic>|weekly|monthly|custom <prompt>] [--no-issue] [--news-count N] [--claude-model MODEL] [--max-tokens N]"
            )
            print("引数なしで実行するとデフォルトのキャッチアップを実行します")
            print("--no-issueフラグを指定するとGitHub Issueを作成しません")
            print("--news-count N で重要ニュースの件数を指定できます（デフォルト: 20）")
            print("--claude-model MODEL でClaudeモデルを指定できます（デフォルト: claude-sonnet-4-20250514）")
            print("--max-tokens N で最大トークン数を指定できます（デフォルト: 10000）")
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
