# MCP (Model Context Protocol) 設定ガイド

## MCP とは？
Model Context Protocol（MCP）は、AI アシスタント（GitHub Copilot など）がツールやリソースにアクセスするための標準プロトコルです。

## VS Code での MCP 設定

### 1. ワークスペース設定
`.vscode/settings.json` でプロジェクト固有の設定を行います：

```json
{
  "github.copilot.enable": {
    "*": true,
    "yaml": true,
    "plaintext": true,
    "markdown": true
  },
  "github.copilot.editor.enableAutoCompletions": true,
  "python.defaultInterpreterPath": "./.venv/Scripts/python.exe",
  "python.terminal.activateEnvironment": true
}
```

### 2. グローバル設定
ユーザー設定でシステム全体の MCP 設定を行います：

1. `Ctrl+Shift+P` でコマンドパレットを開く
2. `Preferences: Open User Settings (JSON)` を選択
3. 設定を追加

### 3. MCP サーバー設定
カスタム MCP サーバーを使用する場合：

```json
{
  "mcp.servers": {
    "custom-server": {
      "command": "python",
      "args": ["path/to/mcp-server.py"],
      "env": {
        "API_KEY": "${env:API_KEY}"
      }
    }
  }
}
```

## 利用可能な MCP ツール

### ブラウザ関連
- `open_simple_browser`: VS Code 内でブラウザを開く
- ローカル開発サーバーのプレビューに最適

### ファイル操作
- `create_file`: 新しいファイルの作成
- `read_file`: ファイル内容の読み込み
- `replace_string_in_file`: ファイル内容の編集

### ターミナル操作
- `run_in_terminal`: コマンド実行
- `get_terminal_output`: 出力の取得

### Git 操作
- `get_changed_files`: 変更ファイルの確認
- リポジトリ状態の管理

### 検索機能
- `semantic_search`: セマンティック検索
- `grep_search`: テキスト検索
- `file_search`: ファイル名検索

## トラブルシューティング

### MCP が動作しない場合
1. VS Code を再起動
2. 拡張機能の確認（GitHub Copilot が有効か）
3. 設定ファイルの JSON 構文エラーをチェック

### パフォーマンス最適化
```json
{
  "github.copilot.advanced": {
    "length": 500,
    "temperature": 0.1
  }
}
```

## 環境変数設定
`.env` ファイルで MCP に関連する設定：

```bash
# MCP 関連設定
MCP_DEBUG=true
MCP_LOG_LEVEL=info
```