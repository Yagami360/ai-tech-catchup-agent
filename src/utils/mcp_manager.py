"""
MCP サーバー管理モジュール - MCP サーバー設定の読み込みと管理
"""

import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, cast

import yaml

logger = logging.getLogger(__name__)


class MCPServerManager:
    """MCP サーバー管理クラス"""

    def __init__(self, config_path: str = "mcp/mcp_servers.yaml"):
        self.config_path = Path(config_path)
        self.servers_config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """MCP サーバー設定ファイルを読み込み"""
        try:
            if not self.config_path.exists():
                logger.warning(f"MCP サーバー設定ファイルが見つかりません: {self.config_path}")
                return {"servers": {}}

            with open(self.config_path, "r", encoding="utf-8") as file:
                config = yaml.safe_load(file)
                if not config:
                    logger.warning("MCP サーバー設定ファイルが空です")
                    return {"servers": {}}

                logger.info(f"MCP サーバー設定を読み込みました: {self.config_path}")
                return cast(Dict[str, Any], config)

        except yaml.YAMLError as e:
            logger.error(f"MCP サーバー設定ファイルの解析エラー: {e}")
            return {"servers": {}}
        except Exception as e:
            logger.error(f"MCP サーバー設定ファイルの読み込みエラー: {e}")
            return {"servers": {}}

    def get_enabled_servers(self, enabled_list: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        有効化されている MCP サーバーの設定を取得

        Args:
            enabled_list: 有効にするサーバー名のリスト

        Returns:
            有効な MCP サーバーの設定辞書
        """
        if not enabled_list:
            return {}

        enabled_servers = {}
        all_servers = self.servers_config.get("servers", {})
        for server_name in enabled_list:
            if server_name in all_servers:
                enabled_servers[server_name] = all_servers[server_name]
            else:
                logger.warning(f"MCP サーバー '{server_name}' が設定ファイルに見つかりません")

        return enabled_servers

    def build_mcp_config(self, enabled_list: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Claude Code SDK 用の MCP サーバー設定を構築

        Args:
            enabled_list: 有効にするサーバー名のリスト

        Returns:
            Claude Code SDK 用の MCP サーバー設定
        """
        enabled_servers = self.get_enabled_servers(enabled_list)
        mcp_config = {}

        for server_name, server_config in enabled_servers.items():
            # 環境変数を展開
            env = {}
            if "env" in server_config:
                for key, value in server_config["env"].items():
                    # ${VAR_NAME} 形式の環境変数を展開
                    if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                        var_name = value[2:-1]
                        env[key] = os.getenv(var_name, "")
                    else:
                        env[key] = value

            # MCP サーバー設定を構築
            mcp_config[server_name] = {
                "type": server_config.get("type", "stdio"),
                "command": server_config.get("command"),
                "args": server_config.get("args", []),
            }

            if env:
                mcp_config[server_name]["env"] = env

        return mcp_config

    def get_allowed_tools(self, enabled_list: List[str]) -> List[str]:
        """
        有効な MCP サーバーの許可ツールリストを取得

        Args:
            enabled_list: 有効にするサーバー名のリスト

        Returns:
            許可ツールのリスト
        """
        enabled_servers = self.get_enabled_servers(enabled_list)
        allowed_tools = []

        for server_config in enabled_servers.values():
            if "allowed_tools" in server_config:
                allowed_tools.extend(server_config["allowed_tools"])

        return allowed_tools

    def list_available_servers(self) -> List[str]:
        """利用可能な MCP サーバー名のリストを取得"""
        return list(self.servers_config.get("servers", {}).keys())

    def get_server_info(self, server_name: str) -> Optional[Dict[str, Any]]:
        """指定された MCP サーバーの情報を取得"""
        result = self.servers_config.get("servers", {}).get(server_name)
        return cast(Optional[Dict[str, Any]], result)
