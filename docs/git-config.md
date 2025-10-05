# Git 設定メモ

## UTF-8 エンコーディング設定

```bash
git config --global core.quotepath false
git config --global i18n.commitencoding utf-8  
git config --global i18n.logoutputencoding utf-8
```

これで絵文字を含むコミットメッセージがGitHubで正しく表示されるはず。