"""
プロンプト管理モジュール - YAMLファイルからプロンプトを読み込み・管理
"""

import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

from ..config import settings

logger = logging.getLogger(__name__)


class PromptManager:
    """プロンプト管理クラス"""

    def __init__(self, prompts_dir: str = "prompts"):
        self.prompts_dir = Path(prompts_dir)
        self.prompts = self._load_prompts()

    def _load_prompts(self) -> Dict[str, Any]:
        """promptsディレクトリからYAMLファイルを読み込み"""
        try:
            if not self.prompts_dir.exists():
                logger.error(f"プロンプトディレクトリが見つかりません: {self.prompts_dir}")
                return {}

            all_prompts = {}
            yaml_files = list(self.prompts_dir.glob("*.yaml")) + list(self.prompts_dir.glob("*.yml"))

            if not yaml_files:
                logger.error(f"プロンプトディレクトリにYAMLファイルが見つかりません: {self.prompts_dir}")
                return {}

            for yaml_file in yaml_files:
                try:
                    with open(yaml_file, "r", encoding="utf-8") as file:
                        file_prompts = yaml.safe_load(file)
                        if file_prompts:
                            all_prompts.update(file_prompts)
                            logger.info(f"プロンプトファイルを読み込みました: {yaml_file.name} ({len(file_prompts)}個のプロンプト)")
                except yaml.YAMLError as e:
                    logger.error(f"YAMLファイルの解析エラー ({yaml_file.name}): {e}")
                    continue
                except Exception as e:
                    logger.error(f"プロンプトファイルの読み込みエラー ({yaml_file.name}): {e}")
                    continue

            logger.info(f"合計{len(all_prompts)}個のプロンプトを読み込みました")
            return all_prompts

        except Exception as e:
            logger.error(f"プロンプトディレクトリの読み込みエラー: {e}")
            return {}

    def get_prompt(self, prompt_type: str, enabled_mcp_servers: Optional[list] = None, **kwargs: Any) -> Optional[str]:
        """指定されたタイプのプロンプトを取得"""
        if prompt_type not in self.prompts:
            logger.warning(f"プロンプトタイプが見つかりません: {prompt_type}")
            return None

        prompt_config = self.prompts[prompt_type]

        # キーワードを動的に統合
        if "key_words" in self.prompts:
            # 自動的にkey_wordsを統合
            key_words_config = self.prompts["key_words"]
            if "keywords" in key_words_config:
                kwargs["key_words"] = key_words_config["keywords"]

        # key_urlsを動的に統合
        if "key_urls" in self.prompts:
            # 自動的にkey_urlsを統合
            key_urls_config = self.prompts["key_urls"]
            if "sources" in key_urls_config:
                kwargs["key_urls"] = key_urls_config["sources"]

        # MCP ツール指示を動的に統合（有効なサーバーがある場合のみ）
        mcp_tools_parts = []
        if enabled_mcp_servers and "mcp_tools" in self.prompts:
            mcp_config = self.prompts["mcp_tools"]
            for server_name in enabled_mcp_servers:
                # サーバー名に対応する指示を取得（例: "github_mcp", "filesystem_mcp"）
                tool_key = f"{server_name}_mcp"
                if tool_key in mcp_config:
                    mcp_tools_parts.append(mcp_config[tool_key])
                    logger.info(f"MCP ツール指示を追加: {server_name}")

        # 統合された MCP ツール指示を設定
        kwargs["mcp_tools"] = "\n\n".join(mcp_tools_parts) if mcp_tools_parts else ""

        # ニュース件数を動的に設定
        if "news_count" not in kwargs:
            kwargs["news_count"] = str(settings.news_count)

        # 現在の年号を動的に設定
        if "current_year" not in kwargs:
            kwargs["current_year"] = str(datetime.now().year)

        # 期間を動的に設定（前日まで）
        if "week_period" not in kwargs:
            today = datetime.now()
            yesterday = today - timedelta(days=1)
            week_ago = yesterday - timedelta(days=6)  # 前日から7日間
            kwargs["week_period"] = f"{week_ago.strftime('%Y年%m月%d日')}から{yesterday.strftime('%Y年%m月%d日')}までの過去1週間"

        if "month_period" not in kwargs:
            today = datetime.now()
            yesterday = today - timedelta(days=1)
            month_ago = yesterday - timedelta(days=29)  # 前日から30日間
            kwargs["month_period"] = f"{month_ago.strftime('%Y年%m月%d日')}から{yesterday.strftime('%Y年%m月%d日')}までの過去1ヶ月"

        if "template" in prompt_config:
            # テンプレートプロンプト（変数置換あり）
            template = prompt_config["template"]
            try:
                formatted: str = template.format(**kwargs)
                return formatted
            except KeyError as e:
                logger.error(f"テンプレート変数の置換エラー: {e}")
                return str(template)
        elif "prompt" in prompt_config:
            # 固定プロンプト
            prompt_text = prompt_config["prompt"]
            # キーワードが含まれている場合は置換
            if "{key_words}" in prompt_text and "key_words" in kwargs:
                prompt_text = prompt_text.replace("{key_words}", kwargs["key_words"])
            # key_urlsが含まれている場合は置換
            if "{key_urls}" in prompt_text and "key_urls" in kwargs:
                prompt_text = prompt_text.replace("{key_urls}", kwargs["key_urls"])
            # ニュース件数が含まれている場合は置換
            if "{news_count}" in prompt_text and "news_count" in kwargs:
                prompt_text = prompt_text.replace("{news_count}", kwargs["news_count"])
            # 現在の年号が含まれている場合は置換
            if "{current_year}" in prompt_text and "current_year" in kwargs:
                prompt_text = prompt_text.replace("{current_year}", kwargs["current_year"])
            # 週間期間が含まれている場合は置換
            if "{week_period}" in prompt_text and "week_period" in kwargs:
                prompt_text = prompt_text.replace("{week_period}", kwargs["week_period"])
            # 月間期間が含まれている場合は置換
            if "{month_period}" in prompt_text and "month_period" in kwargs:
                prompt_text = prompt_text.replace("{month_period}", kwargs["month_period"])
            # MCP指示が含まれている場合は置換
            if "{mcp_tools}" in prompt_text and "mcp_tools" in kwargs:
                prompt_text = prompt_text.replace("{mcp_tools}", kwargs["mcp_tools"])
            # トピックが含まれている場合は置換
            if "{topic}" in prompt_text and "topic" in kwargs:
                prompt_text = prompt_text.replace("{topic}", kwargs["topic"])
            return str(prompt_text)
        else:
            logger.error(f"プロンプト設定が無効です: {prompt_type}")
            return None

    def get_prompt_info(self, prompt_type: str) -> Dict[str, Any]:
        """プロンプトの情報を取得"""
        if prompt_type not in self.prompts:
            return {}

        prompt_config = self.prompts[prompt_type]
        return {
            "title": prompt_config.get("title", ""),
            "has_template": "template" in prompt_config,
            "has_prompt": "prompt" in prompt_config,
        }

    def list_prompt_types(self) -> list:
        """利用可能なプロンプトタイプのリストを取得"""
        return list(self.prompts.keys())

    def reload_prompts(self) -> bool:
        """プロンプトファイルを再読み込み"""
        try:
            self.prompts = self._load_prompts()
            logger.info("プロンプトファイルを再読み込みしました")
            return True
        except Exception as e:
            logger.error(f"プロンプトファイルの再読み込みエラー: {e}")
            return False

    def validate_prompts(self) -> Dict[str, list]:
        """プロンプトファイルの妥当性を検証"""
        errors: list[str] = []
        warnings: list[str] = []

        if not self.prompts:
            errors.append("プロンプトが読み込まれていません")
            return {"errors": errors, "warnings": warnings}

        for prompt_type, config in self.prompts.items():
            # 必須フィールドのチェック
            if "title" not in config:
                warnings.append(f"{prompt_type}: titleが設定されていません")

            if "prompt" not in config and "template" not in config:
                errors.append(f"{prompt_type}: promptまたはtemplateが設定されていません")

            # テンプレートの変数チェック
            if "template" in config:
                template = config["template"]
                import re

                variables = re.findall(r"\{(\w+)\}", template)
                if variables:
                    logger.info(f"{prompt_type}: テンプレート変数 {variables}")

        return {"errors": errors, "warnings": warnings}

    def get_key_words(self) -> Optional[str]:
        """キーワードを取得"""
        if "key_words" not in self.prompts:
            logger.warning("key_wordsが見つかりません")
            return None

        key_words_config = self.prompts["key_words"]
        if "keywords" in key_words_config:
            keywords = key_words_config["keywords"]
            return str(keywords) if isinstance(keywords, str) else keywords

        logger.warning("key_wordsのkeywordsが見つかりません")
        return None
