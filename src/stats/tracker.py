"""統計情報管理モジュール"""

from typing import List, Dict, Tuple
from dataclasses import dataclass
from ..game.engine import Choice, GameResult

@dataclass
class GameRecord:
    """ゲーム記録を表現するデータクラス"""
    player_choice: Choice
    ai_choice: Choice
    result: GameResult
    timestamp: str

class GameStatistics:
    """ゲーム統計を管理するクラス"""
    
    def __init__(self):
        self.records: List[GameRecord] = []
    
    def add_game(self, record: GameRecord):
        """ゲーム記録を追加"""
        self.records.append(record)
    
    def get_win_rate(self) -> float:
        """勝率を計算"""
        if not self.records:
            return 0.0
        
        wins = sum(1 for record in self.records if record.result == GameResult.WIN)
        return wins / len(self.records) * 100
    
    def get_choice_frequency(self) -> Dict[Choice, int]:
        """プレイヤーの手の頻度を計算"""
        frequency = dict.fromkeys(Choice, 0)
        for record in self.records:
            frequency[record.player_choice] += 1
        return frequency
    
    def get_summary(self) -> Dict[str, any]:
        """統計サマリーを生成"""
        if not self.records:
            return {
                'total_games': 0,
                'wins': 0,
                'losses': 0,
                'draws': 0,
                'win_rate': 0.0
            }
        
        wins = sum(1 for record in self.records if record.result == GameResult.WIN)
        losses = sum(1 for record in self.records if record.result == GameResult.LOSE) 
        draws = sum(1 for record in self.records if record.result == GameResult.DRAW)
        
        return {
            'total_games': len(self.records),
            'wins': wins,
            'losses': losses,
            'draws': draws,
            'win_rate': self.get_win_rate()
        }