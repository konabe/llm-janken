# ユニットテスト設定

## テストスイート概要

このプロジェクトは包括的なユニットテストスイートを備えています。

### テストカバレッジ

#### 1. ゲームエンジンテスト (`test_engine.py`)
- **TestChoice**: 選択肢の変換と表示機能
  - 英語/日本語入力の変換
  - 無効入力のハンドリング
  - 多言語表示機能
- **TestRockPaperScissorsEngine**: ゲームロジック
  - 全ての勝敗パターン（勝利/敗北/引き分け）
  - 入力バリデーション

#### 2. AIプレイヤーテスト (`test_ai_player.py`)
- **TestAIPlayer**: 基底クラス機能
  - 初期化とゲーム履歴管理
- **TestRandomAIPlayer**: ランダムAI
  - 選択のランダム性と有効性
- **TestPatternAIPlayer**: パターン学習AI  
  - 学習アルゴリズムと対策選択

#### 3. UIインターフェーステスト (`test_ui_cli.py`)
- **TestCLIInterface**: CLI機能
  - 多言語メッセージシステム
  - ユーザー入力処理
  - 結果表示とゲームフロー
- **TestCLIInterfaceEnglish**: 英語UI

#### 4. 統計モジュールテスト (`test_stats.py`)
- **TestGameRecord**: ゲーム記録
- **TestGameStatistics**: 統計計算
  - 勝率計算
  - 選択頻度分析
  - 大量データ処理

#### 5. 統合テスト (`test_integration.py`)
- **TestGameIntegration**: 全モジュール連携
- **TestPatternLearningIntegration**: AI学習効果
- **TestCLIIntegration**: UI-AI統合
- **TestErrorHandling**: エラー処理
- **TestPerformance**: パフォーマンス

### テスト実行

#### 全テスト実行
```bash
python run_tests.py
```

#### 特定モジュールのテスト
```bash
python run_tests.py test_engine
python run_tests.py test_ai_player
python run_tests.py test_ui_cli
python run_tests.py test_stats
python run_tests.py test_integration
```

#### VS Code内でのテスト実行
1. VS Codeのテストエクスプローラーを使用
2. 個別テストの実行とデバッグ
3. カバレッジレポートの生成

### テスト統計

- **総テスト数**: 63
- **成功率**: 100%
- **カバレッジ**: 全主要機能
- **実行時間**: < 0.1秒

### テスト品質

#### 使用技術
- `unittest`: Python標準テストフレームワーク
- `unittest.mock`: モックとパッチ機能
- `subTest`: パラメータ化テスト
- 統合テストによるモジュール間連携確認

#### テスト設計原則
- **単体テスト**: 各クラス・メソッドの独立テスト
- **統合テスト**: モジュール間連携の確認
- **エッジケーステスト**: 境界値と異常系
- **パフォーマンステスト**: 大量データ処理
- **モックテスト**: 外部依存の分離

### 継続的インテグレーション

今後の拡張：
- GitHub Actionsでの自動テスト実行
- カバレッジレポート生成
- テスト結果バッジの追加
- テスト失敗時の自動通知