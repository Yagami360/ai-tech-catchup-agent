"""
プロンプト管理モジュール - YAMLファイルからプロンプトを読み込み・管理
"""
import yaml
import logging
from typing import Dict, Any, Optional
from pathlib import Path

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
            yaml_files = list(self.prompts_dir.glob("*.yaml")) + list(
                self.prompts_dir.glob("*.yml")
            )

            if not yaml_files:
                logger.error(f"プロンプトディレクトリにYAMLファイルが見つかりません: {self.prompts_dir}")
                return {}

            for yaml_file in yaml_files:
                try:
                    with open(yaml_file, "r", encoding="utf-8") as file:
                        file_prompts = yaml.safe_load(file)
                        if file_prompts:
                            all_prompts.update(file_prompts)
                            logger.info(
                                f"プロンプトファイルを読み込みました: {yaml_file.name} ({len(file_prompts)}個のプロンプト)"
                            )
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

    def get_prompt(self, prompt_type: str, **kwargs) -> Optional[str]:
        """指定されたタイプのプロンプトを取得"""
        if prompt_type not in self.prompts:
            logger.warning(f"プロンプトタイプが見つかりません: {prompt_type}")
            return None

        prompt_config = self.prompts[prompt_type]

        if "template" in prompt_config:
            # テンプレートプロンプト（変数置換あり）
            template = prompt_config["template"]
            try:
                return template.format(**kwargs)
            except KeyError as e:
                logger.error(f"テンプレート変数の置換エラー: {e}")
                return template
        elif "prompt" in prompt_config:
            # 固定プロンプト
            return prompt_config["prompt"]
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
        errors = []
        warnings = []

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
