# 開発環境セットアップスクリプト（Windows PowerShell用）
# 使用方法: .\setup-dev.ps1

Write-Host "🚀 LLM じゃんけんゲーム 開発環境セットアップ" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green

# 1. 仮想環境の作成
if (-Not (Test-Path ".venv")) {
    Write-Host "📦 仮想環境を作成中..." -ForegroundColor Yellow
    python -m venv .venv
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ 仮想環境の作成完了" -ForegroundColor Green
    } else {
        Write-Host "❌ 仮想環境の作成に失敗しました" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "📦 既存の仮想環境を検出" -ForegroundColor Cyan
}

# 2. 仮想環境のアクティベート
Write-Host "🔧 仮想環境をアクティベート中..." -ForegroundColor Yellow
& ".\.venv\Scripts\Activate.ps1"

if ($env:VIRTUAL_ENV) {
    Write-Host "✅ 仮想環境がアクティベートされました: $env:VIRTUAL_ENV" -ForegroundColor Green
} else {
    Write-Host "❌ 仮想環境のアクティベートに失敗しました" -ForegroundColor Red
    Write-Host "💡 実行ポリシーの問題が考えられます。以下を実行してください:" -ForegroundColor Yellow
    Write-Host "   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Cyan
    exit 1
}

# 3. 依存関係のインストール
Write-Host "📋 依存関係をインストール中..." -ForegroundColor Yellow
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ 依存関係のインストール完了" -ForegroundColor Green
} else {
    Write-Host "❌ 依存関係のインストールに失敗しました" -ForegroundColor Red
    exit 1
}

# 4. 設定確認
Write-Host "`n🔍 設定確認" -ForegroundColor Cyan
Write-Host "   Python: " -NoNewline
python --version
Write-Host "   OpenAI: " -NoNewline
python -c "import openai; print(f'v{openai.__version__}')" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ OpenAIパッケージが見つかりません" -ForegroundColor Red
} else {
    Write-Host "✅ OpenAIパッケージが利用可能" -ForegroundColor Green
}

# 5. テスト実行
Write-Host "`n🧪 テストを実行中..." -ForegroundColor Yellow
python -m unittest discover tests -v

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n🎉 開発環境のセットアップが完了しました！" -ForegroundColor Green
    Write-Host "📝 開発開始方法:" -ForegroundColor Cyan
    Write-Host "   1. 毎回開発前に: .\.venv\Scripts\Activate.ps1" -ForegroundColor White
    Write-Host "   2. アプリ実行: python main.py" -ForegroundColor White
    Write-Host "   3. テスト実行: python -m unittest discover tests -v" -ForegroundColor White
} else {
    Write-Host "`n❌ テストに失敗しました。コードに問題がある可能性があります。" -ForegroundColor Red
    exit 1
}