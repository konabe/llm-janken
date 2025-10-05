"""
AIプレイヤーの基底クラスと基本実装
"""

import random
from abc import ABC, abstractmethod
from typing import List, Optional
from ..game.engine import Choice

class AIPlayer(ABC):
    """AIプレイヤーの基底クラス"""
    
    def __init__(self, name: str, difficulty: str = "medium"):
        self.name = name
        self.difficulty = difficulty
        self.game_history: List[tuple] = []
    
    @abstractmethod
    def make_choice(self) -> Choice:
        """AIの手を決定する（サブクラスで実装）"""
        pass
    
    def record_game(self, player_choice: Choice, ai_choice: Choice, result: str):
        """ゲーム履歴を記録"""
        self.game_history.append((player_choice, ai_choice, result))

class RandomAIPlayer(AIPlayer):
    """ランダムに手を選ぶAIプレイヤー"""
    
    def make_choice(self) -> Choice:
        """ランダムに手を選択"""
        return random.choice(list(Choice))

class PatternAIPlayer(AIPlayer):
    """プレイヤーのパターンを学習するAIプレイヤー（将来実装）"""
    
    def make_choice(self) -> Choice:
        """現在は基本的なパターン分析（プレースホルダー）"""
        if len(self.game_history) < 3:
            return random.choice(list(Choice))
        
        # 簡単なパターン分析: 最後の手の対策を出す
        last_player_choice = self.game_history[-1][0]
        counter_choices = {
            Choice.ROCK: Choice.PAPER,
            Choice.PAPER: Choice.SCISSORS, 
            Choice.SCISSORS: Choice.ROCK
        }
        
        # 70%の確率で対策、30%でランダム
        if random.random() < 0.7:
            return counter_choices[last_player_choice]
        else:
            return random.choice(list(Choice))