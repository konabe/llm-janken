# プロジェクト構造

```
llm-janken/
├── src/                    # ソースコード
│   ├── game/              # ゲームエンジン
│   │   ├── __init__.py
│   │   └── engine.py      # コアじゃんけんロジック
│   ├── ai/                # AI プレイヤー
│   │   ├── __init__.py
│   │   └── player.py      # AI戦略とプレイヤー実装
│   ├── ui/                # ユーザーインターフェース
│   │   ├── __init__.py
│   │   └── cli.py         # コマンドラインインターフェース
│   ├── stats/             # 統計・分析
│   │   ├── __init__.py
│   │   └── tracker.py     # ゲーム統計とパターン分析
│   └── __init__.py
├── tests/                 # テストコード
│   ├── __init__.py
│   └── test_engine.py     # ユニットテスト
├── docs/                  # ドキュメント
│   ├── dev-setup.md       # 開発環境セットアップ
│   └── mcp-setup.md       # MCP設定ガイド
├── .vscode/               # VS Code設定
│   └── settings.json      # プロジェクト設定
├── .github/               # GitHub設定
│   └── copilot-instructions.md
├── main.py                # 旧メインファイル（レガシー）
├── main_new.py           # 新メインファイル（モジュラー版）
├── requirements.txt       # Python依存関係
├── .env.example          # 環境変数テンプレート
├── .gitignore            # Git除外設定
├── LICENSE               # ライセンス
└── README.md             # プロジェクト説明
```

## アーキテクチャ

### ゲームエンジン (`src/game/`)
- **責任**: コアじゃんけんロジック、ルール、ゲーム状態管理
- **主要クラス**: 
  - `Choice`: じゃんけんの手の列挙型
  - `GameResult`: ゲーム結果の列挙型
  - `RockPaperScissorsEngine`: ゲームロジックエンジン

### AI統合 (`src/ai/`)
- **責任**: AI プレイヤー戦略、プロンプトエンジニアリング、LLM API連携
- **主要クラス**:
  - `AIPlayer`: AIプレイヤーの基底クラス
  - `RandomAIPlayer`: ランダム戦略AI
  - `PatternAIPlayer`: パターン学習AI（将来実装）

### UIレイヤー (`src/ui/`)
- **責任**: ユーザーインターフェース（CLI ファースト、Web 拡張可能）
- **主要クラス**:
  - `CLIInterface`: コマンドライン用インターフェース
  - 多言語サポート（日本語/英語）

### 統計 (`src/stats/`)
- **責任**: ゲーム履歴、パターン分析、プレイヤープロファイリング
- **主要クラス**:
  - `GameRecord`: ゲーム記録データ
  - `GameStatistics`: 統計分析機能

## 設計パターン

### AI戦略システム
- 各AI対戦相手は共通インターフェース`AIPlayer`を実装
- 簡単に新しいAIパーソナリティを追加可能
- 手の生成と学習のための統一API

### ゲーム状態管理
- 不変ゲーム履歴を維持（パターン分析とリプレイ機能）
- 決定論的ゲームロジック（AI意思決定から分離）

### 多言語サポート
- 英語/日本語の用語管理
- 拡張可能な言語システム

## 今後の拡張予定

1. **LLM統合**: OpenAI/Anthropic APIを使った賢いAI
2. **Web UI**: Flask/FastAPIを使ったWebインターフェース
3. **高度な統計**: プレイヤーパターンの機械学習分析
4. **マルチプレイヤー**: 複数人対戦機能
5. **AIパーソナリティ**: キャラクター性を持つAI対戦相手