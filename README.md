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

## ✨ 主な機能

- **自動レポート生成**: 毎週や毎月などの一定期間間隔で GitHub Issue でのレポートを自動生成
- **Claude Code統合**: Claude code の Web 検索機能を活用した最新情報取得
- **カスタム調査**: Issue 内での `@claude` メンションで任意プロンプトで特定トピックを調査

## 🚀 使用方法

### ☁️ GitHub Actions で動かす場合

自動実行されるので特別な操作は不要です。

手動実行したい場合は、以下ワークフローの `Run workflow` から動かすこともできます。

- [📅 最新レポートのワークフロー](https://github.com/Yagami360/ai-tech-catchup-agent/actions/workflows/daily-report.yml)
- [📊 週次レポートのワークフロー](https://github.com/Yagami360/ai-tech-catchup-agent/actions/workflows/weekly-report.yml)
- [📈 月次レポートのワークフロー](https://github.com/Yagami360/ai-tech-catchup-agent/actions/workflows/monthly-report.yml)

⚠️ 注意点: claude API 利用のクレジットが尽きた場合は、GitHub シークレットの claude の API キー（`ANTHROPIC_API_KEY`）の値を利用可能な API キーにする必要があります

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
# ANTHROPIC_API_KEY=your_api_key_here
# GITHUB_TOKEN=your_github_token_here
# GITHUB_REPOSITORY=your_username/your_repo
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
