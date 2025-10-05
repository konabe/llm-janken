"""
AIプレイヤーの包括的テスト
"""

import unittest
from unittest.mock import patch
from src.ai.player import AIPlayer, RandomAIPlayer, PatternAIPlayer
from src.game.engine import Choice, GameResult


class TestAIPlayer(unittest.TestCase):
    """AIPlayer基底クラスのテスト"""

    def setUp(self):
        """テスト前の準備"""
        # AIPlayerは抽象クラスなので、RandomAIPlayerを使用してテスト
        self.ai_player = RandomAIPlayer("TestAI")

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


class TestRandomAIPlayer(unittest.TestCase):
    """RandomAIPlayerのテスト"""

    def setUp(self):
        """テスト前の準備"""
        self.ai_player = RandomAIPlayer("RandomAI")

    def test_make_choice_returns_valid_choice(self):
        """make_choiceが有効な選択肢を返すかテスト"""
        choice = self.ai_player.make_choice()
        self.assertIn(choice, [Choice.ROCK, Choice.PAPER, Choice.SCISSORS])

    def test_make_choice_randomness(self):
        """複数回の選択でランダム性があるかテスト"""
        choices = [self.ai_player.make_choice() for _ in range(100)]

        # すべての選択肢が出現することを確認
        unique_choices = set(choices)
        self.assertGreater(len(unique_choices), 1, "選択肢に多様性がありません")

    @patch("random.choice")
    def test_make_choice_uses_random(self, mock_random_choice):
        """randomライブラリを使用しているかテスト"""
        mock_random_choice.return_value = Choice.ROCK

        choice = self.ai_player.make_choice()

        mock_random_choice.assert_called_once()
        self.assertEqual(choice, Choice.ROCK)


class TestPatternAIPlayer(unittest.TestCase):
    """PatternAIPlayerのテスト"""

    def setUp(self):
        """テスト前の準備"""
        self.ai_player = PatternAIPlayer("PatternAI")

    def test_make_choice_with_no_history(self):
        """履歴なしでの選択テスト"""
        choice = self.ai_player.make_choice()
        self.assertIn(choice, [Choice.ROCK, Choice.PAPER, Choice.SCISSORS])

    def test_make_choice_with_insufficient_history(self):
        """履歴不足時の選択テスト"""
        # 2回の履歴を追加（3回未満なのでランダム選択）
        self.ai_player.record_game(Choice.ROCK, Choice.PAPER, "lose")
        self.ai_player.record_game(Choice.SCISSORS, Choice.ROCK, "lose")

        choice = self.ai_player.make_choice()
        self.assertIn(choice, [Choice.ROCK, Choice.PAPER, Choice.SCISSORS])

    @patch("random.random")
    @patch("random.choice")
    def test_make_choice_pattern_learning_counter(
        self, mock_random_choice, mock_random
    ):
        """パターン学習での対策選択テスト"""
        # 70%の確率で対策を選択するよう設定
        mock_random.return_value = 0.5  # 0.7未満なので対策選択

        # 3回の履歴を追加
        for _ in range(3):
            self.ai_player.record_game(Choice.ROCK, Choice.PAPER, "lose")

        choice = self.ai_player.make_choice()

        # 最後のプレイヤー選択（ROCK）に対する対策はPAPER
        self.assertEqual(choice, Choice.PAPER)

    @patch("random.random")
    @patch("random.choice")
    def test_make_choice_pattern_learning_random(self, mock_random_choice, mock_random):
        """パターン学習でのランダム選択テスト"""
        # 30%の確率でランダム選択するよう設定
        mock_random.return_value = 0.8  # 0.7以上なのでランダム選択
        mock_random_choice.return_value = Choice.SCISSORS

        # 3回の履歴を追加
        for _ in range(3):
            self.ai_player.record_game(Choice.ROCK, Choice.PAPER, "lose")

        choice = self.ai_player.make_choice()

        mock_random_choice.assert_called_once()
        self.assertEqual(choice, Choice.SCISSORS)

    def test_counter_choice_mapping(self):
        """対策選択のマッピングテスト"""
        test_cases = [
            (Choice.ROCK, Choice.PAPER),  # ROCKに対してPAPER
            (Choice.PAPER, Choice.SCISSORS),  # PAPERに対してSCISSORS
            (Choice.SCISSORS, Choice.ROCK),  # SCISSORSに対してROCK
        ]

        for player_choice, expected_counter in test_cases:
            with self.subTest(player_choice=player_choice):
                # 履歴をリセット
                self.ai_player.game_history = []

                # 3回同じ選択の履歴を追加
                for _ in range(3):
                    self.ai_player.record_game(player_choice, Choice.ROCK, "win")

                # パターン学習をテスト（確実に対策選択になるよう設定）
                with patch("random.random", return_value=0.5):
                    choice = self.ai_player.make_choice()
                    self.assertEqual(choice, expected_counter)


if __name__ == "__main__":
    unittest.main()
