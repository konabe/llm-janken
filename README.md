# LLM じゃんけん

[![CI/CD Pipeline](https://github.com/konabe/llm-janken/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/konabe/llm-janken/actions/workflows/ci-cd.yml)
[![Quick Test](https://github.com/konabe/llm-janken/actions/workflows/quick-test.yml/badge.svg)](https://github.com/konabe/llm-janken/actions/workflows/quick-test.yml)
[![Python 3.9-3.12](https://img.shields.io/badge/python-3.9%20|%203.10%20|%203.11%20|%203.12-blue)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

大規模言語モデル（LLM）を活用したじゃんけんゲーム。

## 概要

このプロジェクトは、プレイヤーが LLM を搭載した AI 対戦相手と競うじゃんけんゲームを実装します。
AI は戦略的なゲームプレイを行い、解説を提供し、プレイヤーのパターンに基づいて戦略を適応させることができます。
また、AI はプレイヤーの心理をうまく利用して、じゃんけんの前にあらかじめ文章を提示することもできます。

## 機能

- **🤖 OpenAI API 統合**: GPT-3.5-turbo を使用したインテリジェントなAI対戦相手
- **🧠 多様なAI性格**: 攻撃的、守備的、分析的、バランス型など5種類の性格
- **📚 学習機能**: ゲーム履歴から相手のパターンを学習し戦略を調整
- **🌐 多言語サポート**: 英語/日本語の完全対応
- **🎯 フォールバック機能**: OpenAI APIが利用不可時はランダムAIに自動切り替え
- **📊 統計分析**: ゲーム履歴、勝率、選択パターンの詳細分析

## はじめに

### 前提条件

- Python 3.8+
- OpenAIのAPI アクセス（オプション）

### 🚨 重要: 開発環境セットアップ

このプロジェクトは**Python仮想環境（venv）を必須**で使用します。

#### クイックセットアップ
```bash
# 1. 自動セットアップスクリプトを実行（推奨）
./setup-dev.sh

# 2. 手動セットアップの場合
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

#### 開発開始前（毎回必須）
```bash
# 仮想環境をアクティベート
source .venv/Scripts/activate

# プロンプトに (.venv) が表示されることを確認
```

#### 環境チェック
```bash
# 開発環境が正しく設定されているか確認
./check-env.sh
# リポジトリをクローン
git clone https://github.com/konabe/llm-janken.git
cd llm-janken

# Python バージョンを確認・インストール（例：Python 3.11）
pyenv install 3.11.0
pyenv local 3.11.0

# 仮想環境を作成（.venv を使用）
python -m venv .venv

# 仮想環境を有効化
# Windows (Git Bash)
source .venv/Scripts/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate

# 依存関係をインストール
pip install --upgrade pip
pip install -r requirements.txt
```

### 設定

#### OpenAI API キーの設定

```bash
# 環境設定ファイルをコピー
cp .env.example .env

# .env ファイルを編集してOpenAI API キーを設定
# OPENAI_API_KEY=your_actual_api_key_here
```

**重要**: OpenAI API キーを取得するには：
1. [OpenAI Platform](https://platform.openai.com/) にアクセス
2. アカウントを作成してAPI キーを生成
3. `.env` ファイルの `OPENAI_API_KEY` に設定

**注意**: API キーが設定されていない場合、ランダムAIプレイヤーが使用されます。

### 開発環境セットアップ（GitHub CLI）

詳細な開発環境セットアップについては [`dev-setup.md`](dev-setup.md) を参照してください。

```bash
# GitHub CLIインストール（Windows）
winget install --id GitHub.cli

# パスを通す（一時的）
export PATH="$PATH:/c/Program Files/GitHub CLI"

# GitHubにログイン
gh auth login

# 推奨設定
gh config set prompt disabled  # 自動承認
```

### ゲーム実行

```bash
# 仮想環境が有効化されていることを確認
# Windows (Git Bash)
source .venv/Scripts/activate
# Windows (PowerShell)  
.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate

# ゲームを実行
python main.py

# テスト実行（__pycache__ 無効化）
# Windows PowerShell
./test-clean.bat
# Linux/Mac
./test-clean.sh

# 通常のテスト実行
python -m unittest discover tests -v

# __pycache__ を生成しないPython実行
# Windows
python-clean.bat main.py
# PowerShell
./python-clean.ps1 main.py
```

## CI/CD パイプライン

このプロジェクトでは GitHub Actions を使用して自動化された CI/CD パイプラインを実装しています。

### 🔄 ワークフロー

#### 1. **CI/CD Pipeline** (`ci-cd.yml`)
- **トリガー**: プッシュ（main/master/develop ブランチ）、プルリクエスト
- **テストマトリックス**: Python 3.9, 3.10, 3.11, 3.12
- **品質チェック**: flake8 リント、Black フォーマッタ
- **カバレッジ**: unittest + coverage レポート
- **セキュリティ**: safety、bandit によるセキュリティスキャン
- **依存関係**: 脆弱性チェック、古いパッケージ検出

#### 2. **Quick Test** (`quick-test.yml`)
- **トリガー**: プッシュ・プルリクエスト（軽量テスト）
- **実行内容**: 基本テスト、アプリケーション起動テスト

#### 3. **Environment Setup Test** (`setup-test.yml`)
- **トリガー**: 手動実行、毎週月曜日
- **実行内容**: 新規開発者向け環境セットアップテスト

### 📊 ステータスバッジ

プロジェクトの状態は以下のバッジで確認できます：
- **CI/CD Pipeline**: 全体的なテスト・品質チェックステータス
- **Quick Test**: 基本機能テストステータス  
- **Python Support**: サポートするPythonバージョン
- **Code Style**: Black フォーマッタ使用
- **License**: MIT ライセンス

### 🚀 デプロイメント

- **自動リリース**: main ブランチへのプッシュ時に自動タグ作成
- **リリースノート**: 変更内容とテスト結果を自動生成
- **バージョニング**: `v2024.01.15-abc1234` 形式（日付 + コミットハッシュ）

### 🛠️ ローカル開発での CI/CD テスト

```bash
# コード品質チェック
flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics
black --check --diff src/ tests/

# テスト実行（カバレッジ付き）
coverage run -m unittest discover tests -v
coverage report -m

# セキュリティチェック
pip install safety bandit
safety check
bandit -r src/
```

## アーキテクチャ

```
src/
├── game/           # ゲームエンジン - コアじゃんけんロジック
│   └── engine.py   # Choice enum, GameResult, 勝敗判定
├── ai/             # AIプレイヤー統合
│   └── player.py   # RandomAI, PatternAI, LLMAIPlayer (OpenAI統合)
├── ui/             # ユーザーインターフェース
│   └── cli.py      # 多言語対応コマンドラインUI
└── stats/          # 統計・分析
    └── tracker.py  # ゲーム記録、勝率計算、パターン分析
```

### AIプレイヤーの種類

| クラス | 説明 | 使用条件 |
|--------|------|----------|
| **LLMAIPlayer** | OpenAI GPT-3.5-turbo使用、5つの性格パターン | OpenAI API キー必須 |
| **PatternAIPlayer** | プレイヤーのパターンを学習する基本AI | API キー不要 |
| **RandomAIPlayer** | 完全ランダム選択のフォールバックAI | API キー不要 |

## 貢献

1. リポジトリをフォーク
2. 機能ブランチを作成（`git checkout -b feature/amazing-feature`）
3. 変更をコミット（`git commit -m 'Add some amazing feature'`）
4. ブランチにプッシュ（`git push origin feature/amazing-feature`）
5. プルリクエストを開く

## ライセンス

このプロジェクトは MIT ライセンスの下でライセンスされています - 詳細は [LICENSE](LICENSE) ファイルを参照してください。