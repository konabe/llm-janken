@echo off
REM Windows用 __pycache__ 無効化でPythonを実行するバッチファイル

echo 🚫 __pycache__ 無効化でPython実行中...
set PYTHONDONTWRITEBYTECODE=1
python -B %*