#!/usr/bin/env python3
"""
LLM じゃんけんゲーム
メインエントリーポイント
"""

import os
from dotenv import load_dotenv

def main():
    """メイン関数"""
    # 環境変数を読み込み
    load_dotenv()
    
    print("🎮 LLM じゃんけんゲームへようこそ！")
    print("=" * 40)
    
    # API キーの確認
    openai_key = os.getenv('OPENAI_API_KEY')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')
    
    if not openai_key and not anthropic_key:
        print("⚠️  LLM API キーが設定されていません。")
        print(".env ファイルを作成し、API キーを設定してください。")
        print("例: cp .env.example .env")
        return
    
    # 簡単なじゃんけんゲームのプロトタイプ
    print("\n🤖 AI 対戦相手と対戦します！")
    print("選択肢: rock (グー), paper (パー), scissors (チョキ)")
    print("終了するには 'quit' と入力してください。")
    
    print("\n--- じゃんけん勝負！ ---")
    
    # プレイヤーの入力
    while True:
        player_choice = input("あなたの手を選んでください: ").strip().lower()
        
        if player_choice not in ['rock', 'paper', 'scissors', 'グー', 'パー', 'チョキ']:
            print("無効な入力です。rock, paper, scissors または グー, パー, チョキ を入力してください。")
            continue
        break
    
    # 入力の正規化
    choice_map = {
        'グー': 'rock',
        'パー': 'paper', 
        'チョキ': 'scissors'
    }
    player_choice = choice_map.get(player_choice, player_choice)
    
    # 現在は単純なランダム AI（後で LLM に置き換え予定）
    import random
    ai_choices = ['rock', 'paper', 'scissors']
    ai_choice = random.choice(ai_choices)
    
    # 結果判定
    result = determine_winner(player_choice, ai_choice)
    
    # 日本語での表示
    choice_display = {
        'rock': 'グー ✊',
        'paper': 'パー ✋', 
        'scissors': 'チョキ ✌️'
    }
    
    print(f"\nあなた: {choice_display[player_choice]}")
    print(f"AI: {choice_display[ai_choice]}")
    
    if result == 'win':
        print("🎉 あなたの勝ち！")
    elif result == 'lose':
        print("😅 AI の勝ち！")
    else:
        print("🤝 引き分け！")
    
    print("\nゲームを終了します。ありがとうございました！")

def determine_winner(player, ai):
    """勝敗を判定する関数"""
    if player == ai:
        return 'draw'
    elif (player == 'rock' and ai == 'scissors') or \
         (player == 'paper' and ai == 'rock') or \
         (player == 'scissors' and ai == 'paper'):
        return 'win'
    else:
        return 'lose'

if __name__ == "__main__":
    main()