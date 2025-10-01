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
        choices=["weekly", "monthly"],
        help="レポートモード (weekly: 週次, monthly: 月次。指定なし: 最新)",
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
        "--no-issue",
        action="store_true",
        help="GitHub Issueを作成しない",
    )
    args = parser.parse_args()
    create_issue = not args.no_issue

    # Agent 実行
    agent = AITechCatchupAgent(model=args.model, max_tokens=args.max_tokens)
    if args.mode == "weekly":
        result = agent.weekly_report(create_issue=create_issue)
    elif args.mode == "monthly":
        result = agent.monthly_report(create_issue=create_issue)
    else:
        result = agent.run_catchup(create_issue=create_issue, news_count=args.news_count)

    # 結果を出力
    logger.info(f"実行結果: {result}")
    if result["status"] == "success":
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
