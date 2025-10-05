# 開発環境セットアップガイド

## Python仮想環境セットアップ（最重要）

### 🚨 重要: 開発前に必ず実行すること

このプロジェクトはPython仮想環境（venv）を使用します。**開発作業前に毎回以下を実行してください：**

#### Windows（PowerShell）での仮想環境操作
```powershell
# 1. 仮想環境の作成（初回のみ）
python -m venv .venv

# 2. 仮想環境のアクティベート（毎回必須）
.venv\Scripts\Activate.ps1

# 3. 依存関係のインストール
pip install -r requirements.txt

# 4. 仮想環境がアクティブかどうかの確認
# プロンプトに (.venv) が表示されていればOK
```

#### 仮想環境トラブルシューティング

**問題1: "実行ポリシー" エラーが出る場合**
```powershell
# 一時的に実行ポリシーを変更
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# その後、再度アクティベートを実行
.venv\Scripts\Activate.ps1
```

**問題2: openaiパッケージが見つからない**
```powershell
# 仮想環境がアクティブか確認（(.venv) がプロンプトにあるか）
# アクティブでない場合は再アクティベート
.venv\Scripts\Activate.ps1
# 依存関係を再インストール
pip install -r requirements.txt
```

**問題3: Pythonコマンドが見つからない**
```powershell
# 仮想環境内のPythonを直接指定
.venv\Scripts\python.exe main.py
```

#### 開発セッションの正しい手順
```powershell
# 1. プロジェクトディレクトリに移動
cd c:\Users\rtkon\workspace\llm-janken

# 2. 仮想環境をアクティベート（必須）
.venv\Scripts\Activate.ps1

# 3. プロンプトに (.venv) が表示されることを確認

# 4. 開発作業を開始
python main.py                    # アプリ実行
python -m unittest discover tests -v  # テスト実行
pip install パッケージ名           # 新しいパッケージのインストール
```

#### VSCode統合設定
VSCodeで開発する場合、以下を確認：
1. Python拡張機能がインストールされている
2. コマンドパレット（Ctrl+Shift+P）で "Python: Select Interpreter" を実行
3. `.venv\Scripts\python.exe` を選択

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