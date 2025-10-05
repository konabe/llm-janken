"""
ゲームエンジンのテスト
"""

import unittest
from src.game.engine import Choice, GameResult, RockPaperScissorsEngine

class TestRockPaperScissorsEngine(unittest.TestCase):
    """じゃんけんエンジンのテストクラス"""
    
    def test_choice_from_string(self):
        """文字列からChoiceへの変換テスト"""
        self.assertEqual(Choice.from_string("rock"), Choice.ROCK)
        self.assertEqual(Choice.from_string("グー"), Choice.ROCK)
        self.assertIsNone(Choice.from_string("invalid"))
    
    def test_determine_winner(self):
        """勝敗判定テスト"""
        # 引き分け
        self.assertEqual(
            RockPaperScissorsEngine.determine_winner(Choice.ROCK, Choice.ROCK),
            GameResult.DRAW
        )
        
        # プレイヤー勝利
        self.assertEqual(
            RockPaperScissorsEngine.determine_winner(Choice.ROCK, Choice.SCISSORS),
            GameResult.WIN
        )
        
        # AI勝利
        self.assertEqual(
            RockPaperScissorsEngine.determine_winner(Choice.ROCK, Choice.PAPER),
            GameResult.LOSE
        )
    
    def test_validate_choice(self):
        """入力バリデーションテスト"""
        self.assertTrue(RockPaperScissorsEngine.validate_choice("rock"))
        self.assertTrue(RockPaperScissorsEngine.validate_choice("グー"))
        self.assertFalse(RockPaperScissorsEngine.validate_choice("invalid"))

if __name__ == '__main__':
    unittest.main()