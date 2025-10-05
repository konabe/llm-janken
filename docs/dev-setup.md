# 開発環境セットアップガイド

## Python仮想環境セットアップ（最重要）

### 🚨 重要: 開発前に必ず実行すること

このプロジェクトはPython仮想環境（venv）を使用します。**開発作業前に毎回以下を実行してください：**

#### Windows（コマンドプロンプト/バッチ）での仮想環境操作
```bat
REM 1. 仮想環境の作成（初回のみ）
python -m venv .venv

REM 2. 仮想環境のアクティベート（毎回必須）
.venv\Scripts\activate.bat

REM 3. 依存関係のインストール
pip install -r requirements.txt

REM 4. 仮想環境がアクティブかどうかの確認
REM プロンプトに (.venv) が表示されていればOK
```

#### 仮想環境トラブルシューティング

**問題1: openaiパッケージが見つからない**
```bat
REM 仮想環境がアクティブか確認（(.venv) がプロンプトにあるか）
REM アクティブでない場合は再アクティベート
.venv\Scripts\activate.bat
REM 依存関係を再インストール
pip install -r requirements.txt
```

**問題2: Pythonコマンドが見つからない**
```bat
REM 仮想環境内のPythonを直接指定
.venv\Scripts\python.exe main.py
```

**問題3: 自動セットアップを使いたい場合**
```bat
REM 自動セットアップスクリプトを実行
setup-dev.bat
```

#### 開発セッションの正しい手順
```bat
REM 1. プロジェクトディレクトリに移動
cd c:\Users\rtkon\workspace\llm-janken

REM 2. 仮想環境をアクティベート（必須）
.venv\Scripts\activate.bat

REM 3. プロンプトに (.venv) が表示されることを確認

REM 4. 開発作業を開始
python main.py                         REM アプリ実行
python -m unittest discover tests -v   REM テスト実行
pip install パッケージ名                REM 新しいパッケージのインストール
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