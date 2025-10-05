# Git 設定メモ

## UTF-8 エンコーディング設定

### コマンドライン設定
```bash
git config --global core.quotepath false
git config --global i18n.commitencoding utf-8  
git config --global i18n.logoutputencoding utf-8
```

### VS Code での管理

#### 1. プロジェクト設定 (`.vscode/settings.json`)
```json
{
  "files.encoding": "utf8",
  "git.inputValidation": true,
  "terminal.integrated.env.windows": {
    "LC_ALL": "C.UTF-8",
    "LANG": "C.UTF-8"
  }
}
```

#### 2. タスクランナー (`Ctrl+Shift+P` → `Tasks: Run Task`)
- "Git UTF-8 設定": Git設定を自動実行
- "Git エンコーディング設定": エンコーディング設定
- "Git 設定確認": 現在の設定を確認

これで絵文字を含むコミットメッセージがGitHubで正しく表示される。