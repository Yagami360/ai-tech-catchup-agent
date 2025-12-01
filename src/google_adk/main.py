"""
Google ADK版 AI Tech Catchup Agent CLI
非対話的に実行するためのコマンドラインインターフェース
"""

import argparse
import logging
import sys

# エージェントモジュールをインポート（これによりグローバル初期化が実行される）
from . import agent

logger = logging.getLogger(__name__)

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("ai_agent.log"), logging.StreamHandler(sys.stdout)],
)


def main() -> None:
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description="Google ADK版 AI Tech Catchup Agent - 最新AI技術動向レポート生成ツール",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "mode",
        nargs="?",
        choices=["weekly", "monthly", "topic", "test"],
        help="レポートモード (weekly: 週次, monthly: 月次, topic: トピック別, test: テスト。指定なし: 最新)",
    )
    parser.add_argument(
        "--topic",
        type=str,
        default=None,
        help="トピック別レポートのトピック名（例: RAG, Claude Code, Vision-Language Models）",
    )
    parser.add_argument(
        "--news-count",
        type=int,
        default=None,
        help="重要ニュースの件数",
    )
    parser.add_argument(
        "--no-issue",
        action="store_true",
        help="GitHub Issueを作成しない",
    )
    args = parser.parse_args()
    create_issue = not args.no_issue

    # レポート実行
    try:
        if args.mode == "weekly":
            logger.info("週次レポートを生成中...")
            result = agent.weekly_report(create_issue=create_issue)
        elif args.mode == "monthly":
            logger.info("月次レポートを生成中...")
            result = agent.monthly_report(create_issue=create_issue)
        elif args.mode == "topic":
            if not args.topic:
                logger.error("トピックモードを使用する場合は --topic オプションでトピック名を指定してください")
                sys.exit(1)
            logger.info(f"トピックレポートを生成中: {args.topic}")
            result = agent.topic_report(topic=args.topic, create_issue=create_issue, news_count=args.news_count)
        elif args.mode == "test":
            logger.info("テストモードで最新レポートを生成中...")
            result = agent.run_catchup(create_issue=create_issue, news_count=args.news_count, test_mode=True)
        else:
            logger.info("最新レポートを生成中...")
            result = agent.run_catchup(create_issue=create_issue, news_count=args.news_count, test_mode=False)

        # 結果を出力
        logger.info(f"実行結果: {result}")
        if result["status"] == "success":
            if "issue_url" in result:
                print(f"\n✅ レポートを作成しました: {result['issue_url']}")
            else:
                print("\n✅ レポートを生成しました（Issue作成はスキップ）")
            sys.exit(0)
        else:
            print(f"\n❌ エラーが発生しました: {result.get('message', '不明なエラー')}")
            sys.exit(1)

    except Exception as e:
        logger.error(f"実行中にエラーが発生しました: {e}")
        print(f"\n❌ エラーが発生しました: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
