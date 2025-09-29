# 🤖 AI Tech Catchup Agent

Claude CodeのWeb検索機能を活用して、最新AI技術情報を取得・分析し、週次レポートをGitHub Issueで提供するAI Agentです。

## ✨ 主な機能

- **Claude Code統合**: ClaudeのWeb検索機能を活用した最新情報取得
- **自動レポート生成**: 毎週金曜日にGitHub Issueでレポートを自動生成
- **カスタム検索**: 任意のプロンプトで特定トピックを検索
- **技術インサイト**: 特定トピックの深掘り分析
- **日本語対応**: 日本語でのレポート生成

## 🚀 クイックスタート

### 1. 依存関係のインストール

```bash
# uvのインストール（まだの場合）
curl -LsSf https://astral.sh/uv/install.sh | sh

# PATHの設定
source $HOME/.local/bin/env

# 依存関係のインストール
make install
```

### 2. 環境設定

```bash
# 環境設定ファイルの作成
make setup

# .envファイルを編集してAPIキーを設定
# ANTHROPIC_API_KEY=your_api_key_here
# GITHUB_TOKEN=your_github_token_here
# GITHUB_REPOSITORY=your_username/your_repo
```

### 3. 実行

```bash
# 最新レポート作成
make run

# 週次レポート作成
make run-weekly

# 月次レポート作成
make run-monthly
```

## 📋 利用可能なコマンド

| コマンド | 説明 |
|---------|------|
| `make install` | 依存関係をインストール |
| `make setup` | 開発環境のセットアップ |
| `make run` | 最新レポート作成 |
| `make run-weekly` | 週次レポート生成 |
| `make run-monthly` | 月次レポート生成 |
| `make test` | テストを実行 |
| `make lint` | コードのリンティング |
| `make format` | コードのフォーマット |

## 🔄 自動化

GitHub Actionsで毎週金曜日9:00（UTC）に自動実行されます：

```yaml
schedule:
  - cron: '0 9 * * 5'  # 毎週金曜日 9:00 (UTC)
```

## 📊 レポート例

生成されるレポートには以下が含まれます：

- 🤖 **使用モデル**: 使用されたAIモデル名（本文とラベルに表示）
- 🏷️ **自動ラベル**: `weekly-report`, `claude-3.5-sonnet` など
- 🎯 **トレンドワード優先**: 最新AI技術トレンドワードを重視した調査
- 🔥 **重要ニュース**: 上位10件の重要記事（トレンドワード関連を優先）
- 📈 **主要トレンド**: 技術トレンドの分析
- 🚀 **技術的ハイライト**: 新技術や手法の説明
- 💡 **開発者向けポイント**: 実践的なアドバイス
- 📚 **関連リソース**: 記事のURLと説明
