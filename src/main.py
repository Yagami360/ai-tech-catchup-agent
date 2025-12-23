"""
AI Tech Catchup Agent メインアプリケーション
"""

import argparse
import logging
import sys

from .agent import AITechCatchupAgent
from .config import settings

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("ai_agent.log"), logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)


def main() -> None:
    """メイン関数"""
    logger.info("Started AI Tech Catchup Agent")
    logger.debug(f"settings: {settings}")

    parser = argparse.ArgumentParser(
        description="AI Tech Catchup Agent - 最新AI技術動向レポート生成ツール",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "mode",
        nargs="?",
        choices=["weekly", "monthly", "topic", "test"],
        help="レポートモード (weekly: 週次, monthly: 月次, topic: トピック別, test: テスト。指定なし: 最新)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help=f"AIモデル名 (デフォルト: {settings.model_name})\n"
        "  Claude: claude-sonnet-4-20250514, claude-3-5-haiku-20241022, etc.\n"
        "  Gemini: gemini-2.0-flash-exp, gemini-1.5-pro, etc.",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=None,
        help=f"最大トークン数 (デフォルト: {settings.max_tokens})",
    )
    parser.add_argument(
        "--news-count",
        type=int,
        default=None,
        help=f"重要ニュースの件数 (デフォルト: {settings.news_count})",
    )
    parser.add_argument(
        "--topic",
        type=str,
        default=None,
        help="トピック別レポートのトピック名（例: RAG, Claude Code, Vision-Language Models）",
    )
    parser.add_argument(
        "--no-issue",
        action="store_true",
        help="GitHub Issueを作成しない",
    )
    parser.add_argument(
        "--mcp-servers",
        type=str,
        default=None,
        help="有効にする MCP サーバー（カンマ区切り、例: github,slack",
    )
    args = parser.parse_args()
    create_issue = not args.no_issue

    # MCP サーバーの有効化（CLI引数または環境変数）
    enabled_mcp_servers = []
    if args.mcp_servers:
        enabled_mcp_servers = [s.strip() for s in args.mcp_servers.split(",")]
    elif settings.enabled_mcp_servers:
        enabled_mcp_servers = [s.strip() for s in settings.enabled_mcp_servers.split(",")]

    # Agent 実行
    agent = AITechCatchupAgent(
        model=args.model,
        max_tokens=args.max_tokens,
        enabled_mcp_servers=enabled_mcp_servers,
    )
    if args.mode == "weekly":
        result = agent.weekly_report(create_issue=create_issue)
    elif args.mode == "monthly":
        result = agent.monthly_report(create_issue=create_issue)
    elif args.mode == "topic":
        if not args.topic:
            logger.error("トピックモードを使用する場合は --topic オプションでトピック名を指定してください")
            sys.exit(1)
        result = agent.topic_report(topic=args.topic, create_issue=create_issue, news_count=args.news_count)
    elif args.mode == "test":
        result = agent.run_catchup(create_issue=create_issue, news_count=args.news_count, test_mode=True)
    else:
        result = agent.run_catchup(create_issue=create_issue, news_count=args.news_count, test_mode=False)

    # 結果を出力
    logger.info(f"実行結果: {result}")
    if result["status"] == "success":
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
