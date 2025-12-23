# 🤖 AI Tech Catchup Agent

[![CI](https://github.com/Yagami360/ai-tech-catchup-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/Yagami360/ai-tech-catchup-agent/actions/workflows/ci.yml)
[![Daily Report](https://github.com/Yagami360/ai-tech-catchup-agent/actions/workflows/daily-report.yml/badge.svg)](https://github.com/Yagami360/ai-tech-catchup-agent/actions/workflows/daily-report.yml)
[![Weekly Report](https://github.com/Yagami360/ai-tech-catchup-agent/actions/workflows/weekly-report.yml/badge.svg)](https://github.com/Yagami360/ai-tech-catchup-agent/actions/workflows/weekly-report.yml)
[![Monthly Report](https://github.com/Yagami360/ai-tech-catchup-agent/actions/workflows/monthly-report.yml/badge.svg)](https://github.com/Yagami360/ai-tech-catchup-agent/actions/workflows/monthly-report.yml)
[![Topic Report](https://github.com/Yagami360/ai-tech-catchup-agent/actions/workflows/topic-report.yml/badge.svg)](https://github.com/Yagami360/ai-tech-catchup-agent/actions/workflows/topic-report.yml)
[![Claude](https://github.com/Yagami360/ai-tech-catchup-agent/actions/workflows/claude.yml/badge.svg)](https://github.com/Yagami360/ai-tech-catchup-agent/actions/workflows/claude.yml)
[![Gemini CLI](https://github.com/Yagami360/ai-tech-catchup-agent/actions/workflows/gemini.yml/badge.svg)](https://github.com/Yagami360/ai-tech-catchup-agent/actions/workflows/gemini.yml)

最新AI技術の最新/週次/月次レポート、および特定トピックのレポートを GitHub Issue で自動作成する AI Agent です。

- [📅 最新レポート](https://github.com/Yagami360/ai-tech-catchup-agent/issues?q=is%3Aissue%20label%3Areport)
- [📊 週次レポート](https://github.com/Yagami360/ai-tech-catchup-agent/issues?q=is%3Aissue%20label%3Aweekly-report)
- [📈 月次レポート](https://github.com/Yagami360/ai-tech-catchup-agent/issues?q=is%3Aissue%20label%3Amonthly-report)
- [🎯 トピック別レポート](https://github.com/Yagami360/ai-tech-catchup-agent/issues?q=is%3Aissue%20label%3Atopic-report)


> **⚠️ 重要**: 
> - 本レポジトリは、レポート作成のための各種 APIトークンを設定していないので、レポート作成不可の状態になっています
> - 本レポジトリを自身のレポジトリに fork するか clone するなどした後に、API トークン用の各種 Secrets と Variables を自身のレポジトリに設定したうえで使用するようにしてください

## 🚀 使用方法

### 1️⃣ レポジトリを fork する

このレポジトリを自分のアカウントに fork してください。

**Fork の手順:**
1. 本ページ右上の「Fork」ボタンをクリック
2. fork 先のアカウントを選択
3. 「Create fork」をクリック

### 2️⃣ GitHub Actions で動かす場合

#### APIキーの取得

以下のサービスから必要なAPIキーを取得してください：

- **Claude を使用する場合**: [Anthropic Console](https://console.anthropic.com/) から `ANTHROPIC_API_KEY` を取得
- **Gemini を使用する場合**: [Google AI Studio](https://makersuite.google.com/app/apikey) から `GOOGLE_API_KEY` または `GEMINI_API_KEY` を取得
- **（オプション） Hugging Face MCP サーバーを使用する場合**: [Hugging Face Settings](https://huggingface.co/settings/tokens) から `HF_TOKEN` を取得

#### GitHub Secrets と Variables の設定

**fork したレポジトリ**で以下を設定してください：

1. fork したレポジトリの `Settings` → `Secrets and variables` → `Actions` に移動

2. **Secrets** タブで `New repository secret` をクリックし、以下を作成:
    - `ANTHROPIC_API_KEY`: Claude モデルを使用する場合<br>
    - `GOOGLE_API_KEY`: Gemini モデルを使用する場合<br>
    - `GEMINI_API_KEY`: Gemini CLI を使用する場合<br>
    - `HF_TOKEN`: Hugging Face MCPサーバーを使用する場合<br>

3. **Variables** タブで `New repository variable` をクリックし、以下を作成:
    - `MODEL_NAME`: 利用するモデル名<br>
        現時点では Claude モデル（`claude-sonnet-4-20250514`, `claude-opus-4-1-20250805` など）と Gemini モデル（`gemini-2.5-flash`, `gemini-2.5-pro` など）をサポートしています
    - `GEMINI_MODEL`: Gemini CLI Actions で使用する Gemini モデル名（`gemini-2.5-flash`, `gemini-2.5-pro` など）。レポート内容の質疑応答などで利用
    - `ENABLED_MCP_SERVERS`: 有効にするMCPサーバー（例: `github,huggingface`）<br>
    - `NEWS_COUNT_REPORT`: 最新レポートにおけるニュース数（例: `20`）
    - `NEWS_COUNT_WEEKLY_REPORT`: 週次レポートにおけるニュース数（例: `10`）
    - `NEWS_COUNT_MONTHLY_REPORT`: 月次レポートにおけるニュース数（例: `20`）
    - `NEWS_COUNT_TOPIC_REPORT`: トピック別レポートにおけるニュース数（例: `20`）

#### ワークフローの有効化と実行

1. fork したレポジトリの `Actions` タブに移動し、ワークフローを有効化してください

2. 一定期間間隔でワークフローが自動実行され、GitHub Issue にレポートが自動作成されます

3. （オプション）手動実行したい場合は、**fork したレポジトリ**の以下ワークフローの `Run workflow` から動かすこともできます。

    - 📅 最新レポートのワークフロー: `Actions` → `Daily Report` → `Run workflow`
    - 📊 週次レポートのワークフロー: `Actions` → `Weekly Report` → `Run workflow`
    - 📈 月次レポートのワークフロー: `Actions` → `Monthly Report` → `Run workflow`
    - 🎯 トピック別レポートのワークフロー: `Actions` → `Topic Report` → `Run workflow`
        - `Run workflow` をクリックして、調査したいトピック名を入力してください（例: `AI Agent`, `Vision-Language Models`, `PhysicalAI`）

### 3️⃣ ローカル環境で動かす場合

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

# .envファイルを編集してAPIキー等を設定
# ANTHROPIC_API_KEY=your_anthropic_api_key_here
# GOOGLE_API_KEY=your_google_api_key_here
# MODEL_NAME=gemini-2.5-flash
# GITHUB_TOKEN=your_github_token_here
# GITHUB_REPOSITORY=your_username/your_repo_name
# ENABLED_MCP_SERVERS=github,huggingface
# HF_TOKEN=your_huggingface_token_here
# MAX_TOKENS=10000
# NEWS_COUNT_REPORT=20
# NEWS_COUNT_WEEKLY_REPORT=10
# NEWS_COUNT_MONTHLY_REPORT=20
# NEWS_COUNT_TOPIC_REPORT=10
# NEWS_COUNT_TEST_REPORT=1
```

#### 3️⃣ 実行

```bash
# 📰 最新レポート作成
make run

# 📊 週次レポート作成
make run-weekly

# 📈 月次レポート作成
make run-monthly

# 🎯 トピック別レポート作成
make run-topic TOPIC="AI Agent"
```

### 🤖 レポート内容の質疑応答する

作成された Issue レポートの内容について、AI モデルと質疑応答することもできます。

#### Claude と質疑応答する

Issue レポート内のコメントで `@claude` とメンションすると、Claude が自動的に日本語で応答します。

**使用例：**
```
@claude この中で最も重要なニュースは何ですか?
@claude OpenAI の最新情報について詳しく教えてください
@claude このレポートの要点を3つにまとめてください
```

#### Gemini と質疑応答する

Issue レポート内のコメントで `@gemini-cli` とメンションすると、Gemini が自動的に日本語で応答します。

**使用例：**
```
@gemini-cli Multi-Agent System の実装例を教えてください
@gemini-cli この技術のユースケースは何ですか?
@gemini-cli 今後のトレンドについて教えてください
```

> **Note**: 
> - Claude は `@claude` メンション、Gemini は `@gemini-cli` メンションで呼び出します
> - どちらも Issue コメントおよび PR コメントで利用可能です
> - レポート Issue の内容を理解した上で回答します

## 👨‍💻 開発者向け情報

### 📋 利用可能コマンド

| コマンド | 説明 |
|---------|------|
| `make install` | 📦 依存関係をインストール |
| `make setup` | ⚙️ 開発環境のセットアップ |
| `make run` | 📰 最新レポート作成 |
| `make run-weekly` | 📊 週次レポート生成 |
| `make run-monthly` | 📈 月次レポート生成 |
| `make run-topic TOPIC="トピック名"` | 🎯 トピック別レポート生成 |
| `make test` | 🧪 テストを実行 |
| `make lint` | 🔍 コードのリンティング |
| `make format` | ✨ コードのフォーマット |

### 🔌 MCP サーバー統合

AI Tech Catchup Agent は MCP (Model Context Protocol) サーバーをサポートしており、Claude モデルを使用時に外部ツールやサービスと連携できます。

#### 利用可能な MCP サーバー

1. **GitHub MCP Server** ✅
   - GitHubリポジトリ、Issue、PRへの直接アクセス
   - GitHub Trending からトレンドプロジェクトの取得
   - Code Security アラートの確認

2. **Hugging Face MCP Server** ✅
   - 最新AIモデルの検索
   - データセット、Space、論文の検索
   - モデルの人気度・ダウンロード数の確認

#### MCPサーバーの有効化

**環境変数で設定**:
```bash
# .env ファイルに追加
ENABLED_MCP_SERVERS=github,huggingface
```

#### 事前準備

**GitHub MCP Server**:
1. GitHub CLI のインストール:
   ```bash
   # macOS
   brew install gh
   
   # Linux
   sudo apt install gh
   ```

2. 認証:
   ```bash
   gh auth login
   # または
   export GITHUB_TOKEN="your_github_token"
   ```

**Hugging Face MCP Server**:
1. Hugging Face トークンの取得:
   - [Hugging Face Settings](https://huggingface.co/settings/tokens) からアクセストークンを作成
   - トークンタイプは `read` で十分です

2. 環境変数の設定:
   ```bash
   export HF_TOKEN="your_huggingface_token"
   ```

   または `.env` ファイルに追加:
   ```
   HF_TOKEN=your_huggingface_token
   ```

> **Note**: ローカル環境では初回実行時に自動的にログインプロンプトが表示されますが、CI/CD環境では`HF_TOKEN`の設定が必須です
