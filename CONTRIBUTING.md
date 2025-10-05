# 🤝 コントリビューションガイド

**LLM じゃんけん**プロジェクトへのコントリビューションをありがとうございます！このガイドでは、効果的に貢献するための方法を説明します。

## 📋 目次

- [🚀 はじめに](#-はじめに)
- [🔧 開発環境の構築](#-開発環境の構築)
- [💻 開発ワークフロー](#-開発ワークフロー)
- [📝 コーディング規約](#-コーディング規約)
- [🧪 テスト](#-テスト)
- [📋 Issue と Pull Request](#-issue-と-pull-request)

## 🚀 はじめに

### 🎯 プロジェクトの目的

このプロジェクトは、LLM（大規模言語モデル）を活用した戦略的じゃんけんゲームです。AI対戦相手との心理戦を楽しめるPythonアプリケーションを目指しています。

### 🤝 コントリビューションの種類

以下のような貢献を歓迎します：

- 🐛 **バグ修正**: 既存の問題の解決
- ✨ **新機能**: AI戦略の改善、UI/UX向上、新しいゲームモード
- 📚 **ドキュメント**: README、コメント、ガイドの改善
- 🧪 **テスト**: テストケースの追加・改善
- 🔧 **リファクタリング**: コード品質の向上

## 🔧 開発環境の構築

### 📋 前提条件

- **Python 3.9以上** （推奨: 3.12）
- **Git**
- **VS Code** （推奨）

### ⚡ クイックセットアップ

```bash
# 1. リポジトリのフォーク・クローン
git clone https://github.com/YOUR_USERNAME/llm-janken.git
cd llm-janken

# 2. 仮想環境の作成・アクティベート
python -m venv .venv
source .venv/Scripts/activate  # Windows
# source .venv/bin/activate    # macOS/Linux

# 3. 依存関係のインストール
pip install -r requirements.txt

# 4. OpenAI API キーの設定
echo "OPENAI_API_KEY=your_api_key_here" > .env

# 5. テスト実行で動作確認
python -m unittest discover tests -v
```

### 🎮 アプリケーション実行

```bash
python main.py
```

## 💻 開発ワークフロー

### 🌿 ブランチ戦略

1. **Fork** このリポジトリをフォーク
2. **Clone** フォークしたリポジトリをローカルにクローン
3. **Branch** 機能別にブランチを作成
   ```bash
   git checkout -b feature/新機能名
   git checkout -b fix/バグ修正名
   ```
4. **Develop** 開発作業を実施
5. **Test** テストを実行して品質を確認
6. **Commit** コミットメッセージ規約に従ってコミット
7. **Push** フォークしたリポジトリにプッシュ
8. **Pull Request** 本家リポジトリにプルリクエストを作成

### 📝 コミットメッセージ規約

```bash
# 形式: <タイプ>: <概要>
feat: 新しいAI戦略を追加
fix: パターン学習のバグを修正
docs: READMEのインストール手順を更新
test: 統合テストを追加
refactor: ゲームエンジンをリファクタリング
```

**タイプ一覧:**
- `feat:` 新機能
- `fix:` バグ修正  
- `docs:` ドキュメント
- `test:` テスト
- `refactor:` リファクタリング
- `perf:` パフォーマンス改善
- `chore:` 雑務・設定

## 📝 コーディング規約

### 🐍 Python スタイル

- **PEP 8** 準拠
- **Black** フォーマッター使用（自動適用）
- **Flake8** リンター使用
- **型ヒント** 必須

```python
def calculate_score(wins: int, losses: int, draws: int) -> float:
    """
    勝率を計算する
    
    Args:
        wins: 勝利数
        losses: 敗北数
        draws: 引き分け数
        
    Returns:
        勝率（0.0-1.0）
    """
    total_games = wins + losses + draws
    return wins / total_games if total_games > 0 else 0.0
```

### 📖 ドキュメント

- **docstring** は日本語OK
- **変数名・関数名** は英語
- **複雑なロジック** は日本語コメント

### 📁 ディレクトリ構造

```
src/
├── game/           # ゲームエンジン
├── ai/            # AIプレイヤー
├── ui/            # ユーザーインターフェース
└── stats/         # 統計・分析

tests/
├── game/          # ゲームテスト
├── ai/            # AIテスト  
├── ui/            # UIテスト
└── test_*.py      # 統合テスト
```

## 🧪 テスト

### 🎯 テスト実行

```bash
# 全テスト実行
python -m unittest discover tests -v

# カバレッジ付き実行
coverage run -m unittest discover tests -v
coverage report -m
```

### ✅ テスト要件

- **新機能**: 対応するテストケース必須
- **バグ修正**: 再現テストケース追加
- **カバレッジ**: 既存レベルを維持
- **テスト品質**: 64個のテスト全て成功必須

### 🧪 テスト例

```python
def test_ai_choice_validity(self):
    """AI選択の妥当性テスト"""
    ai_player = RandomAIPlayer("TestAI")
    
    for _ in range(10):
        choice = ai_player.make_choice()
        self.assertIn(choice, [Choice.ROCK, Choice.PAPER, Choice.SCISSORS])
```

## 📋 Issue と Pull Request

### 🐛 Issue作成

1. **検索**: 既存Issueを確認
2. **テンプレート**: 適切なテンプレートを使用
3. **詳細**: 再現手順・環境情報を明記
4. **ラベル**: 適切なラベルを付与

### 🔄 Pull Request

1. **Issue参照**: 関連Issueを明記
2. **テンプレート**: PRテンプレートに従って記述
3. **CI/CD**: 全てのチェックが成功していることを確認
4. **レビュー**: フィードバックに建設的に対応

### 🏷️ ラベルガイド

- `bug`: バグ報告
- `enhancement`: 新機能・改善
- `documentation`: ドキュメント関連
- `good first issue`: 初心者向け
- `help wanted`: ヘルプ求む
- `needs-review`: レビュー待ち

## 🎉 コントリビューター認定

貢献していただいた方は以下の方法で認定されます：

- 📝 **CONTRIBUTORS.md** への追加
- 🌟 **README** の Contributors セクションへの記載
- 🏆 **リリースノート** での言及

## 📞 質問・サポート

困ったときは遠慮なくお尋ねください：

- 💬 **Discussions**: 一般的な質問・議論
- 🐛 **Issues**: バグ報告・機能要求
- 📧 **直接連絡**: セキュリティ関連

---

**あなたの貢献を心よりお待ちしています！** 🚀