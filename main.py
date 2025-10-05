#!/usr/bin/env python3
"""
LLM じゃんけんゲーム - メインエントリーポイント
リファクタリング後のモジュラー構成版
"""

import os
from dotenv import load_dotenv
from src.ui.cli import CLIInterface
from src.ai.player import RandomAIPlayer

def main():
    """メイン関数"""
    # 環境変数を読み込み
    load_dotenv()
    
    # API キーの確認
    openai_key = os.getenv('OPENAI_API_KEY')
    
    if not openai_key:
        print("⚠️  OpenAI API キーが設定されていません。")
        print(".env ファイルを作成し、API キーを設定してください。")
        print("例: cp .env.example .env")
        return
    
    # CLI インターフェースとAIプレイヤーを初期化
    cli = CLIInterface(language='ja')
    ai_player = RandomAIPlayer(name="ランダムAI", difficulty="easy")
    
    # 1回のゲームを実行
    cli.run_single_game(ai_player)

if __name__ == "__main__":
    main()