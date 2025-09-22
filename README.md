# 🤖 AI Tech Catchup Agent

最新AI技術情報を自動収集・分析し、週次レポートをGitHub Issueで提供するAI Agentです。

## ✨ 主な機能

- **自動情報収集**: RSSフィードから最新AI技術記事を収集
- **AI分析**: Claude APIを使用した記事の分析と要約
- **週次レポート**: 毎週金曜日にGitHub Issueでレポートを自動生成
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
# キャッチアップの実行
make run

# 特定トピックの分析
make insight TOPIC="大規模言語モデル"
```

## 📋 利用可能なコマンド

| コマンド | 説明 |
|---------|------|
| `make install` | 依存関係をインストール |
| `make run` | AI Agentを実行（キャッチアップ） |
| `make insight TOPIC=<topic>` | 特定トピックの分析 |
| `make test` | テストを実行 |
| `make lint` | コードのリンティング |
| `make format` | コードのフォーマット |
| `make clean` | 環境のクリーンアップ |
| `make setup` | 開発環境のセットアップ |

## ⚙️ 設定

`config.py`で以下の設定をカスタマイズできます：

- **RSSフィード**: 収集する情報源
- **検索キーワード**: 関心のある技術分野
- **レポート頻度**: daily, weekly, monthly
- **Claudeモデル**: 使用するAIモデル

## 🔄 自動化

GitHub Actionsで毎週金曜日9:00（UTC）に自動実行されます：

```yaml
schedule:
  - cron: '0 9 * * 5'  # 毎週金曜日 9:00 (UTC)
```

## 📊 レポート例

生成されるレポートには以下が含まれます：

- 🔥 **重要ニュース**: 上位3件の重要記事
- 📈 **主要トレンド**: 技術トレンドの分析
- 🚀 **技術的ハイライト**: 新技術や手法の説明
- 💡 **開発者向けポイント**: 実践的なアドバイス
- 📚 **関連リソース**: 記事のURLと説明

## 🛠️ 技術スタック

- **Python 3.8+**: メイン言語
- **uv**: パッケージ管理
- **Anthropic Claude**: AI分析エンジン
- **GitHub Actions**: CI/CD自動化
- **RSS/Webスクレイピング**: 情報収集

## 📁 プロジェクト構造

```
ai-tech-catchup-agent/
├── src/
│   ├── __init__.py
│   ├── main.py              # メインアプリケーション
│   ├── data_collector.py    # データ収集モジュール
│   ├── ai_analyzer.py       # AI分析モジュール
│   └── github_integration.py # GitHub統合モジュール
├── .github/workflows/
│   └── claude.yml           # GitHub Actions設定
├── config.py                # 設定ファイル
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