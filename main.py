#!/usr/bin/env python3
"""
LLM じゃんけんゲーム - メインエントリーポイント
リファクタリング後のモジュラー構成版
"""

import os
from dotenv import load_dotenv
from src.ui.cli import CLIInterface
from src.ai.player import RandomAIPlayer, LLMAIPlayer

def main():
    """メイン関数"""
    # 環境変数を読み込み
    load_dotenv()
    
    # API キーの確認
    openai_key = os.getenv('OPENAI_API_KEY')
    
    # CLI インターフェースを初期化
    cli = CLIInterface(language='ja')
    
    # AIプレイヤーを初期化（OpenAI APIキーがあればLLM、なければランダム）
    if openai_key:
        print("🤖 OpenAI APIを使用したAIプレイヤーを使用します")
        ai_player = LLMAIPlayer(
            name="GPT じゃんけんマスター", 
            personality="analytical",  # 分析的な性格
            difficulty="hard"
        )
    else:
        print("⚠️  OpenAI API キーが設定されていません。ランダムAIを使用します。")
        print("📝 .env ファイルを作成してAPI キーを設定すると、より高度なAIと対戦できます。")
        print("例: cp .env.example .env")
        ai_player = RandomAIPlayer(name="ランダムAI", difficulty="easy")
    
    # 1回のゲームを実行
    cli.run_single_game(ai_player)

if __name__ == "__main__":
    main()