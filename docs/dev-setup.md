# 開発環境セットアップガイド

## GitHub CLI 設定

### インストール後の初回セットアップ
```bash
# パスを通す（セッション中のみ）
export PATH="$PATH:/c/Program Files/GitHub CLI"

# GitHubにログイン
gh auth login

# 設定確認
gh config list
```

### 推奨設定
```bash
# プロンプト無効化（自動承認）
gh config set prompt disabled

# その他の便利な設定
gh config set git_protocol https
gh config set editor code  # VS Codeをエディタに設定
```

## 日常の開発フロー

```bash
# 変更をコミット
git add .
git commit -m "変更内容の説明"

# GitHubにプッシュ
git push

# ブランチ作成
git checkout -b feature/新機能

# プルリクエスト作成
gh pr create --title "タイトル" --body "説明"
```