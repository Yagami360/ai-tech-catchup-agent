"""
Google ADK版 AI Tech Catchup Agent
"""

import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

from google.adk.agents.llm_agent import Agent

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.client import GeminiClient, GitHubClient
from src.config import settings
from src.utils import PromptManager

logger = logging.getLogger(__name__)

# グローバルクライアントの初期化
# 設定から値を取得
github_client = GitHubClient(token=settings.github_token, repo=settings.github_repo)

# Google ADK用のモデル名を取得（ADK_MODEL_NAMEが優先、次にMODEL_NAME）
adk_model_name = settings.adk_model_name
if "gemini" not in adk_model_name.lower():
    logger.warning(f"Google ADKではGeminiモデルのみサポートされています。{adk_model_name} の代わりに gemini-2.5-flash を使用します。")
    adk_model_name = "gemini-2.5-flash"

gemini_client = GeminiClient(
    google_api_key=settings.google_api_key,
    model_name=adk_model_name,
    max_tokens=settings.max_tokens,
)
prompt_manager = PromptManager(prompts_dir="prompts")

logger.info(f"Google ADK クライアント初期化完了:")
logger.info(f"  - モデル: {adk_model_name}")
logger.info(f"  - 最大トークン数: {settings.max_tokens}")
logger.info(f"  - GitHubリポジトリ: {settings.github_repo}")


def run_catchup(create_issue: bool = True, news_count: Optional[int] = None, test_mode: bool = False) -> Dict[str, Any]:
    """
    最新AI技術情報をキャッチアップしてレポートを生成

    Args:
        create_issue: GitHub Issueを作成するかどうか
        news_count: 取得するニュース件数
        test_mode: テストモードで実行するかどうか

    Returns:
        実行結果の辞書
    """
    logger.info("AI技術キャッチアップを開始...")

    try:
        # プロンプトの準備
        logger.info("プロンプトを準備中...")
        prompt_type = "test_report" if test_mode else "report"
        prompt = prompt_manager.get_prompt(
            prompt_type,
            enabled_mcp_servers=[],
            news_count=str(news_count or settings.news_count),
        )
        if not prompt:
            logger.error("プロンプトを取得できませんでした")
            return {"status": "error", "message": "プロンプトの取得に失敗しました"}

        # Geminiで最新情報を検索
        logger.info("Geminiで最新情報を検索中...")
        search_result = gemini_client.send_message(prompt)

        if search_result["status"] != "success":
            logger.error(f"Gemini検索エラー: {search_result['message']}")
            return {"status": "error", "message": search_result["message"]}

        result = {
            "status": "success",
            "content": search_result["content"],
            "searched_at": search_result["searched_at"],
        }

        # GitHub Issue作成（オプション）
        if create_issue:
            logger.info("GitHub Issueを作成中...")
            issue_body = f"""# 🤖 AI Tech Catchup Report

- レポート日時: `{datetime.now().strftime("%Y-%m-%d %H:%M")}`
- 使用モデル: `{adk_model_name}`

> **💡 質疑応答について**
> このレポート内容について質問したい場合は、コメントで `@gemini-cli` とメンションすると、AI が自動的に回答します。

---

{search_result["content"]}

---

*このレポートは AI Tech Catchup Agent (Google ADK版) によって自動生成されました。*
"""
            issue_result = github_client.create_issue(
                title=f"🤖 AI Tech Catchup Report - {datetime.now().strftime('%Y-%m-%d')}",
                body=issue_body,
                labels=["report", adk_model_name, "google-adk"],
            )

            if "error" in issue_result:
                logger.error(f"Issue作成エラー: {issue_result['error']}")
                return {"status": "error", "message": issue_result["error"]}

            logger.info(f"レポートIssueを作成しました: {issue_result.get('html_url', '')}")
            result["issue_url"] = issue_result.get("html_url", "")
        else:
            logger.info("GitHub Issue作成をスキップしました")

        return result

    except Exception as e:
        logger.error(f"キャッチアップ実行中にエラー: {e}")
        return {"status": "error", "message": str(e)}


def weekly_report(create_issue: bool = True) -> Dict[str, Any]:
    """
    週次レポートを生成

    Args:
        create_issue: GitHub Issueを作成するかどうか

    Returns:
        実行結果の辞書
    """
    logger.info("週次レポート生成を開始...")

    try:
        # プロンプトの準備
        prompt = prompt_manager.get_prompt("weekly_report", enabled_mcp_servers=[])
        if not prompt:
            logger.error("週次レポートプロンプトを取得できませんでした")
            return {"status": "error", "message": "プロンプトの取得に失敗しました"}

        # Geminiでレポート生成
        logger.info(f"入力プロンプト: {prompt}")
        search_result = gemini_client.send_message(prompt)

        if search_result["status"] != "success":
            return {"status": "error", "message": search_result["message"]}

        result = {
            "status": "success",
            "content": search_result["content"],
            "searched_at": search_result["searched_at"],
        }

        # GitHub Issue作成（オプション）
        if create_issue:
            # 週次レポートの調査期間を計算（前日まで）
            today = datetime.now()
            yesterday = today - timedelta(days=1)
            week_ago = yesterday - timedelta(days=6)
            week_period = f"{week_ago.strftime('%Y-%m-%d')} ~ {yesterday.strftime('%Y-%m-%d')}"

            # 週番号を計算
            week_number = (today.day - 1) // 7 + 1
            week_title = f"{today.strftime('%Y年%m月')}第{week_number}週"
            issue_body = f"""# 📊 AI Tech Catchup Weekly Report

- レポート日時: `{datetime.now().strftime("%Y-%m-%d %H:%M")}`
- 調査期間: `{week_period}`
- 使用モデル: `{adk_model_name}`

> **💡 質疑応答について**
> このレポート内容について質問したい場合は、コメントで `@gemini-cli` とメンションすると、AI が自動的に回答します。

---

{search_result["content"]}

---

*このレポートは AI Tech Catchup Agent (Google ADK版) によって自動生成されました。*
"""
            issue_result = github_client.create_issue(
                title=f"📊 AI Tech Catchup Weekly Report - {week_title}",
                body=issue_body,
                labels=["weekly-report", adk_model_name, "google-adk"],
            )
            if issue_result.get("html_url"):
                result["issue_url"] = issue_result.get("html_url", "")
        else:
            logger.info("GitHub Issue作成をスキップしました")

        return result

    except Exception as e:
        logger.error(f"週次レポート生成中にエラー: {e}")
        return {"status": "error", "message": str(e)}


def monthly_report(create_issue: bool = True) -> Dict[str, Any]:
    """
    月次レポートを生成

    Args:
        create_issue: GitHub Issueを作成するかどうか

    Returns:
        実行結果の辞書
    """
    logger.info("月次レポート生成を開始...")

    try:
        # プロンプトの準備
        prompt = prompt_manager.get_prompt("monthly_report", enabled_mcp_servers=[])
        if not prompt:
            logger.error("月次レポートプロンプトを取得できませんでした")
            return {"status": "error", "message": "プロンプトの取得に失敗しました"}

        # Geminiでレポート生成
        logger.info(f"入力プロンプト: {prompt}")
        search_result = gemini_client.send_message(prompt)

        if search_result["status"] != "success":
            return {"status": "error", "message": search_result["message"]}

        result = {
            "status": "success",
            "content": search_result["content"],
            "searched_at": search_result["searched_at"],
        }

        # GitHub Issue作成（オプション）
        if create_issue:
            # 月次レポートの調査期間を計算（前日まで）
            today = datetime.now()
            yesterday = today - timedelta(days=1)
            month_ago = yesterday - timedelta(days=29)
            month_period = f"{month_ago.strftime('%Y-%m-%d')} ~ {yesterday.strftime('%Y-%m-%d')}"
            issue_body = f"""# 📈 AI Tech Catchup Monthly Report

- レポート日時: `{datetime.now().strftime("%Y-%m-%d %H:%M")}`
- 調査期間: `{month_period}`
- 使用モデル: `{adk_model_name}`

> **💡 質疑応答について**
> このレポート内容について質問したい場合は、コメントで `@gemini-cli` とメンションすると、AI が自動的に回答します。

---

{search_result["content"]}

---

*このレポートは AI Tech Catchup Agent (Google ADK版) によって自動生成されました。*
"""
            issue_result = github_client.create_issue(
                title=f"📈 AI Tech Catchup Monthly Report - {datetime.now().strftime('%Y年%m月')}",
                body=issue_body,
                labels=["monthly-report", adk_model_name, "google-adk"],
            )
            if issue_result.get("html_url"):
                result["issue_url"] = issue_result.get("html_url", "")
        else:
            logger.info("GitHub Issue作成をスキップしました")

        return result

    except Exception as e:
        logger.error(f"月次レポート生成中にエラー: {e}")
        return {"status": "error", "message": str(e)}


def topic_report(topic: str, create_issue: bool = True, news_count: Optional[int] = None) -> Dict[str, Any]:
    """
    特定トピックのレポートを生成

    Args:
        topic: レポート対象のトピック
        create_issue: GitHub Issueを作成するかどうか
        news_count: 取得するニュース件数

    Returns:
        実行結果の辞書
    """
    logger.info(f"トピックレポート生成を開始... トピック: {topic}")

    try:
        # プロンプトの準備
        prompt = prompt_manager.get_prompt(
            "topic_report",
            enabled_mcp_servers=[],
            topic=topic,
            news_count=str(news_count or settings.news_count),
        )
        if not prompt:
            logger.error("トピックレポートプロンプトを取得できませんでした")
            return {"status": "error", "message": "プロンプトの取得に失敗しました"}

        # Geminiでレポート生成
        logger.info(f"入力プロンプト: {prompt}")
        search_result = gemini_client.send_message(prompt)

        if search_result["status"] != "success":
            return {"status": "error", "message": search_result["message"]}

        result = {
            "status": "success",
            "content": search_result["content"],
            "searched_at": search_result["searched_at"],
        }

        # GitHub Issue作成（オプション）
        if create_issue:
            issue_body = f"""# 🎯 AI Tech Catchup Topic Report: {topic}

- レポート日時: `{datetime.now().strftime("%Y-%m-%d %H:%M")}`
- 使用モデル: `{adk_model_name}`
- トピック: `{topic}`

> **💡 質疑応答について**
> このレポート内容について質問したい場合は、コメントで `@gemini-cli` とメンションすると、AI が自動的に回答します。

---

{search_result["content"]}

---

*このレポートは AI Tech Catchup Agent (Google ADK版) によって自動生成されました。*
"""
            issue_result = github_client.create_issue(
                title=f"🎯 AI Tech Catchup Topic Report: {topic} - {datetime.now().strftime('%Y-%m-%d')}",
                body=issue_body,
                labels=["topic-report", adk_model_name, "google-adk"],
            )
            if issue_result.get("html_url"):
                result["issue_url"] = issue_result.get("html_url", "")
        else:
            logger.info("GitHub Issue作成をスキップしました")

        return result

    except Exception as e:
        logger.error(f"トピックレポート生成中にエラー: {e}")
        return {"status": "error", "message": str(e)}


# Google ADK Agent の定義
# モデル名は上記で初期化済みのadk_model_nameを使用
logger.info(f"Google ADK Agent を初期化中... モデル: {adk_model_name}")

root_agent = Agent(
    model=adk_model_name,
    name="ai_tech_catchup_agent",
    description="AI技術の最新情報をキャッチアップしてレポートを生成するエージェント",
    instruction="""あなたはAI技術の最新情報をキャッチアップし、レポートを生成する専門エージェントです。

## 利用可能な機能

### 1. 最新AI技術レポート生成 (run_catchup)
最新のAI技術動向をキャッチアップしてレポートを生成します。

**パラメータ:**
- `create_issue` (bool): GitHub Issueを作成するか (デフォルト: True)
- `news_count` (int): 取得するニュース件数 (デフォルト: 設定値)
- `test_mode` (bool): テストモードで実行するか (デフォルト: False)

**使用例:**
- "最新レポートを作成して"
- "テストモードで実行して、Issueは作成しないで"
- "ニュース5件で最新レポートを作成"

### 2. 週次レポート生成 (weekly_report)
過去1週間のAI技術動向をまとめたレポートを生成します。

**パラメータ:**
- `create_issue` (bool): GitHub Issueを作成するか (デフォルト: True)

**使用例:**
- "週次レポートを作成して"
- "先週のレポートを生成"

### 3. 月次レポート生成 (monthly_report)
過去1ヶ月のAI技術動向をまとめたレポートを生成します。

**パラメータ:**
- `create_issue` (bool): GitHub Issueを作成するか (デフォルト: True)

**使用例:**
- "月次レポートを作成して"
- "先月のレポートを生成"

### 4. 特定トピックのレポート生成 (topic_report)
指定されたトピックに関するAI技術動向をレポートします。

**パラメータ:**
- `topic` (str): レポート対象のトピック名 (必須)
- `create_issue` (bool): GitHub Issueを作成するか (デフォルト: True)
- `news_count` (int): 取得するニュース件数 (デフォルト: 設定値)

**使用例:**
- "RAGについてのレポートを作成して"
- "Vision-Language Modelsのトピックレポートを生成"
- "AI Agentについて、ニュース15件でレポート作成"

## 動作
ユーザーからの要求を理解し、適切な関数を呼び出してレポートを生成してください。
レポートは自動的にGitHub Issueとして作成され、URLが返されます。
関数実行後、結果の概要とIssue URLをユーザーに伝えてください。""",
    tools=[run_catchup, weekly_report, monthly_report, topic_report],
)
