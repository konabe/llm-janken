# コーディングルール / Coding Rules

このファイルは LLM じゃんけんプロジェクトのコーディング規約を定義します。

## 📚 基本原則 / Basic Principles

### 1. コードの可読性最優先
- **日本語コメント推奨**: 複雑なロジックは日本語でコメント
- **英語変数名必須**: 変数名・関数名・クラス名は英語
- **明確な命名規則**: 意図が伝わる名前を選択

### 2. テスト駆動開発
- **テストファースト**: 新機能はテストから作成
- **カバレッジ重視**: 新しいコードは必ずテストを含める
- **テスト構造**: `tests/` ディレクトリは `src/` の階層と一致

## 🐍 Python コーディング規約

### ファイル・モジュール構造
```python
"""
モジュールの説明（日本語OK）
AI プレイヤーの基底クラスと実装クラス
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from enum import Enum

# インポート順序：
# 1. 標準ライブラリ
# 2. サードパーティライブラリ  
# 3. ローカルモジュール（相対インポート使用）
```

### クラス定義規約
```python
class AIPlayer(ABC):
    """
    AI プレイヤーの基底抽象クラス
    
    全てのAIプレイヤー実装はこのクラスを継承する必要があります。
    """
    
    def __init__(self, name: str) -> None:
        """
        Args:
            name: プレイヤー名（日本語可）
        """
        self.name = name
        self.game_history: List[GameRecord] = []
    
    @abstractmethod
    def make_choice(self) -> Choice:
        """
        AIの選択を生成
        
        Returns:
            Choice: rock, paper, scissors のいずれか
        """
        pass
```

### 関数定義規約
```python
def determine_winner(player_choice: Choice, ai_choice: Choice) -> GameResult:
    """
    じゃんけんの勝敗を判定
    
    Args:
        player_choice: プレイヤーの選択
        ai_choice: AIの選択
        
    Returns:
        GameResult: WIN, LOSE, DRAW のいずれか
        
    Examples:
        >>> determine_winner(Choice.ROCK, Choice.SCISSORS)
        GameResult.WIN
    """
    # 実装...
```

### エラーハンドリング
```python
def validate_choice(choice_str: str) -> Choice:
    """
    ユーザー入力を Choice enum に変換
    
    Args:
        choice_str: ユーザーの入力文字列
        
    Returns:
        Choice: 有効な選択肢
        
    Raises:
        ValueError: 無効な入力の場合
    """
    try:
        return Choice.from_string(choice_str)
    except ValueError as e:
        # 具体的なエラーメッセージで再発行
        raise ValueError(f"無効な選択肢です: '{choice_str}'. 有効な選択肢: rock, paper, scissors") from e
```

## 🧪 テスト規約

### テストファイル命名
```
src/game/engine.py    → tests/game/test_engine.py
src/ai/player.py      → tests/ai/test_player.py
src/ui/cli.py         → tests/ui/test_cli.py
src/stats/tracker.py  → tests/stats/test_tracker.py
```

### テストクラス構造
```python
class TestRockPaperScissorsEngine(unittest.TestCase):
    """ゲームエンジンのテストクラス"""
    
    def setUp(self) -> None:
        """各テスト前の初期化"""
        self.engine = RockPaperScissorsEngine()
    
    def test_determine_winner_all_wins(self) -> None:
        """すべてのプレイヤー勝利パターンのテスト"""
        test_cases = [
            (Choice.ROCK, Choice.SCISSORS),
            (Choice.PAPER, Choice.ROCK),
            (Choice.SCISSORS, Choice.PAPER),
        ]
        
        for player_choice, ai_choice in test_cases:
            with self.subTest(player=player_choice, ai=ai_choice):
                result = self.engine.determine_winner(player_choice, ai_choice)
                self.assertEqual(result, GameResult.WIN)
```

### テスト命名規則
- **日本語テスト名推奨**: `test_すべてのプレイヤー勝利パターン`
- **英語も可**: `test_all_player_win_patterns`
- **テスト内容が明確**: 何をテストしているかが一目で分かる

## 🚀 Git コミット規約

### コミットメッセージ
```bash
# プレフィックス + 簡潔な説明（英語または日本語）
feat: 新しいAI戦略クラスを追加
fix: パターン学習のバグを修正
test: 統合テストを追加
docs: APIドキュメントを更新
refactor: ゲームエンジンをリファクタリング
```

### コミットプレフィックス
- `feat:` 新機能
- `fix:` バグ修正
- `test:` テスト追加・修正
- `docs:` ドキュメント
- `refactor:` リファクタリング
- `perf:` パフォーマンス改善
- `chore:` 設定・ツール・雑務
- `style:` UI・スタイル・コードフォーマット
- `build:` 依存関係・ビルドシステム
- `clean:` コードクリーンアップ

## 📦 依存関係管理

### requirements.txt
```txt
# コメント付きで整理
# AI・機械学習
openai==1.0.0

# データ処理
numpy>=1.21.0
pandas>=1.3.0

# 開発・テスト
pytest>=7.0.0
black>=22.0.0
flake8>=4.0.0
```

### 仮想環境
```bash
# 必須：プロジェクト専用の仮想環境使用
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux
```

## 🔍 コード品質

### 静的解析ツール
- **Black**: コードフォーマット自動化
- **Flake8**: コード品質チェック
- **mypy**: 型チェック（推奨）

### コード品質チェックリスト
- [ ] 型ヒントが適切に設定されている
- [ ] docstring が関数・クラスに記載されている
- [ ] テストが成功している（`python -m unittest discover tests -v`）
- [ ] Problems タブにエラー・警告がない
- [ ] 新しい依存関係は requirements.txt に追加済み

## 🤖 AI 開発特化ルール

### LLM API 使用
```python
# 環境変数による設定管理
import os
from openai import OpenAI

class LLMAIPlayer(AIPlayer):
    """LLM を使用する AI プレイヤー"""
    
    def __init__(self, name: str, personality: str = "aggressive") -> None:
        super().__init__(name)
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.personality = personality
    
    def make_choice(self) -> Choice:
        """
        LLM に基づく選択生成
        
        Returns:
            Choice: LLM が選択した手
        """
        # プロンプトエンジニアリング実装...
```

### プロンプト管理
```python
# プロンプトテンプレートの分離管理
PERSONALITY_PROMPTS = {
    "aggressive": "あなたは攻撃的なじゃんけんプレイヤーです...",
    "defensive": "あなたは守備的なじゃんけんプレイヤーです...",
    "random": "あなたはランダムなじゃんけんプレイヤーです..."
}
```

## 🌐 多言語対応

### メッセージ管理
```python
MESSAGES = {
    "ja": {
        "welcome": "じゃんけんゲームへようこそ！",
        "choose": "選択してください (rock/paper/scissors): ",
        "win": "あなたの勝ちです！"
    },
    "en": {
        "welcome": "Welcome to Rock Paper Scissors!",
        "choose": "Choose (rock/paper/scissors): ",
        "win": "You win!"
    }
}
```

---

## 📋 開発フローチェックリスト

新機能開発時は以下の順序で進めてください：

1. **🎯 要件定義**: 機能の目的と仕様を明確化
2. **🧪 テスト作成**: 期待する動作のテストを先に作成
3. **💻 実装**: テストが通るように実装
4. **🔍 品質チェック**: Problems タブの確認とテスト実行
5. **📝 ドキュメント**: 必要に応じてREADME更新
6. **🚀 コミット**: 絵文字付きのコミットメッセージでコミット
7. **🔄 プッシュ**: リモートリポジトリに反映

**全てのステップを通してから次の機能に進むことを徹底してください。**