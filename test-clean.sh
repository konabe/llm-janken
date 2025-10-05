#!/bin/bash
# Linux/Mac用 __pycache__ 無効化テスト実行スクリプト

echo "🚫 __pycache__ 無効化でテスト実行中..."

export PYTHONDONTWRITEBYTECODE=1
python -B -m unittest discover tests -v