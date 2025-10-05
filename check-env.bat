@echo off
echo 🔍 開発環境チェック
echo ====================

echo 📦 仮想環境確認...
if defined VIRTUAL_ENV (
    echo ✅ 仮想環境: アクティブ
) else (
    echo ❌ 仮想環境: 非アクティブ
    echo 💡 実行してください: .venv\Scripts\activate.bat
    pause
    exit /b 1
)

echo 🐍 Python確認...
python --version
if errorlevel 1 (
    echo ❌ Python が見つかりません
    pause
    exit /b 1
)

echo 📋 OpenAI確認...
python -c "import openai; print('✅ OpenAI: 利用可能')" 2>nul
if errorlevel 1 (
    echo ❌ OpenAI: パッケージが見つかりません
    echo 💡 実行してください: pip install -r requirements.txt
) else (
    echo ✅ OpenAI: パッケージが利用可能
)

echo 📁 重要ファイル確認...
if exist "src\ai\player.py" (echo ✅ src\ai\player.py) else (echo ❌ src\ai\player.py)
if exist "main.py" (echo ✅ main.py) else (echo ❌ main.py) 
if exist "requirements.txt" (echo ✅ requirements.txt) else (echo ❌ requirements.txt)

echo.
echo 🎉 環境チェック完了
pause