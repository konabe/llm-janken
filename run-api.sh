#!/bin/bash

# Web API サーバー起動スクリプト

echo "🚀 LLM じゃんけん API サーバーを起動します..."

# 仮想環境の確認
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  仮想環境がアクティベートされていません"
    echo "以下のコマンドを実行してください："
    echo "source .venv/Scripts/activate"
    exit 1
fi

# 環境変数の確認
if [ ! -f ".env" ]; then
    echo "⚠️  .envファイルが見つかりません"
    echo "OpenAI APIキーを設定してください"
    exit 1
fi

# FastAPIサーバー起動
echo "📡 APIサーバーを起動中..."
echo "🌐 URL: http://localhost:8000"
echo "📖 API文書: http://localhost:8000/docs"
echo "📚 ReDoc: http://localhost:8000/redoc"
echo ""
echo "🛑 停止するにはCtrl+Cを押してください"

uvicorn src.api.app:app --host 0.0.0.0 --port 8000 --reload