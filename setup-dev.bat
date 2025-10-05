@echo off
echo ========================================
echo   LLM じゃんけんゲーム 開発環境セットアップ
echo ========================================
echo.

echo [1/4] 仮想環境確認中...
if not exist ".venv" (
    echo 仮想環境が見つかりません。作成します...
    python -m venv .venv
    if errorlevel 1 (
        echo エラー: 仮想環境の作成に失敗しました
        pause
        exit /b 1
    )
    echo ✅ 仮想環境を作成しました
) else (
    echo ✅ 既存の仮想環境を発見
)

echo.
echo [2/4] 仮想環境をアクティベート中...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo エラー: 仮想環境のアクティベートに失敗しました
    pause
    exit /b 1
)
echo ✅ 仮想環境がアクティベートされました

echo.
echo [3/4] 依存関係をインストール中...
pip install -r requirements.txt
if errorlevel 1 (
    echo エラー: 依存関係のインストールに失敗しました
    pause
    exit /b 1
)
echo ✅ 依存関係のインストール完了

echo.
echo [4/4] テスト実行中...
python -m unittest discover tests -v
if errorlevel 1 (
    echo 警告: テストに失敗しました
) else (
    echo ✅ 全テストが成功しました
)

echo.
echo ========================================
echo   セットアップ完了！
echo ========================================
echo.
echo 開発開始方法:
echo   1. .venv\Scripts\activate.bat
echo   2. python main.py
echo.
pause