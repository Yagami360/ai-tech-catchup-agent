"""
Google ADK用のMCPツール統合
ADKのMcpToolsetクラスを使用してMCPサーバーと統合
参考: https://google.github.io/adk-docs/tools-custom/mcp-tools/
"""

import logging
import os
from typing import Any, Dict, List

from google.adk.tools.mcp import McpToolset, StdioConnectionParams, StdioServerParameters

from ..utils import MCPServerManager

logger = logging.getLogger(__name__)


def create_mcp_toolsets(enabled_servers: List[str]) -> List[McpToolset]:
    """
    有効化されたMCPサーバーのMcpToolsetを作成

    Args:
        enabled_servers: 有効にするMCPサーバー名のリスト

    Returns:
        McpToolsetのリスト
    """
    if not enabled_servers:
        return []

    mcp_manager = MCPServerManager()
    mcp_toolsets = []

    for server_name in enabled_servers:
        server_info = mcp_manager.get_server_info(server_name)
        if not server_info:
            logger.warning(f"MCPサーバー '{server_name}' の設定が見つかりません")
            continue

        try:
            # ADKのMcpToolsetを作成
            # 参考: https://google.github.io/adk-docs/tools-custom/mcp-tools/
            connection_params = _build_connection_params(server_name, server_info)

            # McpToolsetインスタンスを作成
            mcp_toolset = McpToolset(
                connection_params=connection_params,
            )
            mcp_toolsets.append(mcp_toolset)
            logger.info(f"MCPツールセットを追加: {server_name}")

        except Exception as e:
            logger.error(f"MCPツールセット '{server_name}' の作成に失敗: {e}")
            continue

    return mcp_toolsets


def _build_connection_params(server_name: str, server_info: Dict[str, Any]) -> StdioConnectionParams:
    """
    ADK用のMCP接続パラメータを構築

    Args:
        server_name: サーバー名
        server_info: サーバー設定情報

    Returns:
        ADK用のMCP接続パラメータ
    """
    server_type = server_info.get("type", "stdio")

    if server_type == "stdio":
        # 環境変数の展開
        env = {}
        if "env" in server_info:
            for key, value in server_info["env"].items():
                # ${VAR_NAME} 形式の環境変数を展開
                if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                    var_name = value[2:-1]
                    env_value = os.getenv(var_name, "")
                    if env_value:
                        env[key] = env_value
                else:
                    env[key] = value

        # StdioServerParametersを作成
        server_params = StdioServerParameters(
            command=server_info.get("command", "npx"),
            args=server_info.get("args", []),
            env=env if env else None,
        )

        # StdioConnectionParamsを返す
        return StdioConnectionParams(
            server_params=server_params,
        )

    else:
        # 現時点ではstdioのみサポート
        # SSE/HTTPサポートは将来的に追加可能
        logger.warning(f"MCPサーバータイプ '{server_type}' は現時点で未サポートです。stdioを使用します。")
        server_params = StdioServerParameters(
            command=server_info.get("command", "npx"),
            args=server_info.get("args", []),
        )
        return StdioConnectionParams(
            server_params=server_params,
        )
