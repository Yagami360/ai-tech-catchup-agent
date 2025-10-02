# 🤖 AI Tech Catchup Agent

[![CI](https://github.com/Yagami360/ai-tech-catchup-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/Yagami360/ai-tech-catchup-agent/actions/workflows/ci.yml)
[![Daily Report](https://github.com/Yagami360/ai-tech-catchup-agent/actions/workflows/daily-report.yml/badge.svg)](https://github.com/Yagami360/ai-tech-catchup-agent/actions/workflows/daily-report.yml)
[![Weekly Report](https://github.com/Yagami360/ai-tech-catchup-agent/actions/workflows/weekly-report.yml/badge.svg)](https://github.com/Yagami360/ai-tech-catchup-agent/actions/workflows/weekly-report.yml)
[![Monthly Report](https://github.com/Yagami360/ai-tech-catchup-agent/actions/workflows/monthly-report.yml/badge.svg)](https://github.com/Yagami360/ai-tech-catchup-agent/actions/workflows/monthly-report.yml)
[![Claude](https://github.com/Yagami360/ai-tech-catchup-agent/actions/workflows/claude.yml/badge.svg)](https://github.com/Yagami360/ai-tech-catchup-agent/actions/workflows/claude.yml)

最新AI技術の最新/週次/月次レポートを GitHub Issue で自動作成する AI Agent です。

- [📅 最新レポート](https://github.com/Yagami360/ai-tech-catchup-agent/issues?q=is%3Aissue%20state%3Aopen%20label%3Areport)
- [📊 週次レポート](https://github.com/Yagami360/ai-tech-catchup-agent/issues?q=is%3Aissue%20state%3Aopen%20label%3Aweekly-report)
- [📈 月次レポート](https://github.com/Yagami360/ai-tech-catchup-agent/issues?q=is%3Aissue%20state%3Aopen%20label%3Amonthly-report)


## 🚀 使用方法

### ☁️ GitHub Actions で動かす場合

1. GitHub secrets and variables を設定する

    - Variables<br>
        - `MODEL_NAME`: 利用するモデル名<br>
            現時点では Claude モデル（`claude-sonnet-4-20250514`, `claude-opus-4-1-20250805` など）と Gemini モデル（`gemini-2.5-flash`, `gemini-2.5-pro` など）をサポートしています

    - Secrets<br>
        - `ANTHROPIC_API_KEY`: Claude モデルを使用する場合<br>
        - `GOOGLE_API_KEY`: Gemini モデルを使用する場合<br>

1. 一定期間間隔でワークフローが自動実行され、GitHub Issue にレポートが自動作成されます

1. （オプション）手動実行したい場合は、以下ワークフローの `Run workflow` から動かすこともできます。

    - [📅 最新レポートのワークフロー](https://github.com/Yagami360/ai-tech-catchup-agent/actions/workflows/daily-report.yml)
    - [📊 週次レポートのワークフロー](https://github.com/Yagami360/ai-tech-catchup-agent/actions/workflows/weekly-report.yml)
    - [📈 月次レポートのワークフロー](https://github.com/Yagami360/ai-tech-catchup-agent/actions/workflows/monthly-report.yml)

### 💻 ローカル環境で動かす場合

#### 1️⃣ 依存関係のインストール

```bash
# uvのインストール（まだの場合）
curl -LsSf https://astral.sh/uv/install.sh | sh

# PATHの設定
source $HOME/.local/bin/env

# 依存関係のインストール
make install
```

#### 2️⃣ 環境設定

```bash
# 環境設定ファイルの作成
make setup

# .envファイルを編集してAPIキーを設定
# ANTHROPIC_API_KEY=your_anthropic_api_key_here
# GOOGLE_API_KEY=your_google_api_key_here
# MODEL_NAME=claude-sonnet-4-20250514
# GITHUB_TOKEN=your_github_token_here
# GITHUB_REPOSITORY=your_username/your_repo
# MAX_TOKENS=10000
# NEWS_COUNT=20
```

#### 3️⃣ 実行

```bash
# 📰 最新レポート作成
make run

# 📊 週次レポート作成
make run-weekly

# 📈 月次レポート作成
make run-monthly
```

## 👨‍💻 開発者向け情報

### 📋 利用可能コマンド

| コマンド | 説明 |
|---------|------|
| `make install` | 📦 依存関係をインストール |
| `make setup` | ⚙️ 開発環境のセットアップ |
| `make run` | 📰 最新レポート作成 |
| `make run-weekly` | 📊 週次レポート生成 |
| `make run-monthly` | 📈 月次レポート生成 |
| `make test` | 🧪 テストを実行 |
| `make lint` | 🔍 コードのリンティング |
| `make format` | ✨ コードのフォーマット |
