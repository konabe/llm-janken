# PowerShell用 __pycache__ 無効化でPythonを実行するスクリプト

Write-Host "🚫 __pycache__ 無効化でPython実行中..." -ForegroundColor Yellow

# 環境変数を設定
$env:PYTHONDONTWRITEBYTECODE = "1"

# 引数をそのまま python に渡す
& python -B @args