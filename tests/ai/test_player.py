"""
AIプレイヤーの基底クラステスト（LLMAIPlayerのテストは別ファイル）
"""

import unittest
from unittest.mock import MagicMock

from src.ai.player import AIPlayer
from src.game.engine import Choice


class ConcreteAIPlayer(AIPlayer):
    """テスト用の具象AIPlayerクラス"""

    def make_choice(self) -> Choice:
        return Choice.ROCK


class TestAIPlayer(unittest.TestCase):
    """AIPlayer基底クラスのテスト"""

    def setUp(self):
        """テスト前の準備"""
        self.ai_player = ConcreteAIPlayer("TestAI")

    def test_initialization(self):
        """初期化のテスト"""
        self.assertEqual(self.ai_player.name, "TestAI")
        self.assertEqual(len(self.ai_player.game_history), 0)

    def test_record_game(self):
        """ゲーム履歴記録のテスト"""
        self.ai_player.record_game(Choice.ROCK, Choice.SCISSORS, "win")

        self.assertEqual(len(self.ai_player.game_history), 1)
        self.assertEqual(
            self.ai_player.game_history[0], (Choice.ROCK, Choice.SCISSORS, "win")
        )

    def test_record_multiple_games(self):
        """複数ゲーム履歴記録のテスト"""
        games = [
            (Choice.ROCK, Choice.SCISSORS, "win"),
            (Choice.PAPER, Choice.ROCK, "win"),
            (Choice.SCISSORS, Choice.SCISSORS, "draw"),
        ]

        for player_choice, ai_choice, result in games:
            self.ai_player.record_game(player_choice, ai_choice, result)

        self.assertEqual(len(self.ai_player.game_history), 3)
        for i, expected in enumerate(games):
            self.assertEqual(self.ai_player.game_history[i], expected)

    def test_make_choice_abstract(self):
        """make_choiceメソッドの実装テスト"""
        choice = self.ai_player.make_choice()
        self.assertIsInstance(choice, Choice)

    def test_default_psychological_message(self):
        """デフォルト心理戦メッセージのテスト"""
        message = self.ai_player.get_psychological_message()
        self.assertEqual(message, "さあ、勝負だ！")


if __name__ == "__main__":
    unittest.main()
