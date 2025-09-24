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
# デフォルトキャッチアップの実行
make run

# 特定トピックの検索
make run-topic TOPIC="大規模言語モデル"

# 週次レポート
make run-weekly

# 月次サマリー
make run-monthly

# カスタムプロンプトで検索
make run-custom PROMPT="GPT-5の最新情報について調べて"
```

## 📋 利用可能なコマンド

| コマンド | 説明 |
|---------|------|
| `make install` | 依存関係をインストール |
| `make run` | AI Agentを実行（デフォルトキャッチアップ） |
| `make run-news NEWS_COUNT=N` | 重要ニュース件数を指定してキャッチアップを実行 |
| `make run-no-issue` | Issue作成なしでキャッチアップを実行 |
| `make run-topic TOPIC=<topic>` | 特定トピックの検索 |
| `make run-weekly` | 週次レポート生成 |
| `make run-monthly` | 月次サマリー生成 |
| `make run-custom PROMPT="<prompt>"` | カスタムプロンプトで検索 |
| `make test` | テストを実行 |
| `make lint` | コードのリンティング |
| `make format` | コードのフォーマット |
| `make clean` | 環境のクリーンアップ |
| `make setup` | 開発環境のセットアップ |

## ⚙️ 設定

### 基本設定 (`config.py`)
- **レポート頻度**: daily, weekly, monthly
- **レポート言語**: ja (日本語), en (英語)
- **Claudeモデル**: 使用するAIモデル
- **ニュース件数**: 重要ニュースの表示件数（デフォルト: 10）

### プロンプト設定 (`prompts/`ディレクトリ)
プロンプトを外部YAMLファイルで管理できます：

#### `prompts/default.yaml`（統合プロンプトファイル）
- **key_words**: AI技術キーワードリスト（全プロンプトで共有）
- **default_search**: デフォルト検索プロンプト（キーワード自動統合）
- **topic_search**: 特定トピック検索プロンプト
- **custom_search**: カスタム検索プロンプト
- **weekly_report**: 週次レポートプロンプト（キーワード自動統合）
- **monthly_summary**: 月次サマリープロンプト（キーワード自動統合）

#### 🤖 AI技術キーワード（単一管理）
`key_words`キーで一元管理され、すべてのプロンプトで自動的に統合されます：
- **AGI技術**: GPT-5, Claude Sonnet 4, Gemini Ultra
- **AI技術**: RAG, Vector Database, AI Agent, Multimodal AI
- **AI応用**: Healthcare AI, Finance AI, Education AI, Climate AI
- **AI基盤**: AI Safety, Edge AI, AI Hardware, Quantum AI
- **AI開発**: AI Code Generation, Developer Tools, AI-assisted Programming

**メリット**: 
- キーワードの更新時は`default.yaml`の`key_words`のみを修正すれば、すべてのプロンプトに自動反映されます
- 全プロンプトが1つのファイルで管理され、保守性が向上します

## 🔄 自動化

GitHub Actionsで毎週金曜日9:00（UTC）に自動実行されます：

```yaml
schedule:
  - cron: '0 9 * * 5'  # 毎週金曜日 9:00 (UTC)
```

## 📊 レポート例

生成されるレポートには以下が含まれます：

- 🤖 **使用モデル**: 使用されたAIモデル名（本文とラベルに表示）
- 🏷️ **自動ラベル**: `weekly-report`, `tech-insight`, `model:claude-3.5-sonnet` など
- 🎯 **トレンドワード優先**: 最新AI技術トレンドワードを重視した調査
- 🔥 **重要ニュース**: 上位10件の重要記事（トレンドワード関連を優先）
- 📈 **主要トレンド**: 技術トレンドの分析
- 🚀 **技術的ハイライト**: 新技術や手法の説明
- 💡 **開発者向けポイント**: 実践的なアドバイス
- 📚 **関連リソース**: 記事のURLと説明

## 🛠️ 技術スタック

- **Python 3.8+**: メイン言語
- **uv**: パッケージ管理
- **Anthropic Claude**: AI分析エンジン（Web検索機能付き）
- **GitHub Actions**: CI/CD自動化
- **GitHub API**: Issue作成・管理

## 📁 プロジェクト構造

```
ai-tech-catchup-agent/
├── src/
│   ├── __init__.py
│   ├── main.py              # メインアプリケーション
│   ├── claude_search.py     # Claude Code検索機能
│   ├── prompt_manager.py    # プロンプト管理機能
│   └── github_integration.py # GitHub統合モジュール
├── .github/workflows/
│   └── claude.yml           # GitHub Actions設定
├── config.py                # 基本設定ファイル
├── prompts/                 # プロンプト設定ディレクトリ
│   └── default.yaml        # 統合プロンプトファイル（全プロンプト含む）
├── pyproject.toml          # プロジェクト設定
├── Makefile                # 開発用コマンド
└── README.md               # このファイル
```

## 🤝 貢献

1. このリポジトリをフォーク
2. フィーチャーブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 🆘 サポート

問題が発生した場合は、GitHubのIssuesで報告してください。

---

*このプロジェクトは Claude Code と GitHub Actions を使用して開発されました。*