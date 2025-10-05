"""
ゲームエンジンの包括的テスト
"""

import unittest
from src.game.engine import Choice, GameResult, RockPaperScissorsEngine


class TestChoice(unittest.TestCase):
    """Choiceクラスのテスト"""

    def test_choice_from_string_english(self):
        """英語入力からChoiceへの変換テスト"""
        self.assertEqual(Choice.from_string("rock"), Choice.ROCK)
        self.assertEqual(Choice.from_string("paper"), Choice.PAPER)
        self.assertEqual(Choice.from_string("scissors"), Choice.SCISSORS)

        # 大文字小文字混在のテスト
        self.assertEqual(Choice.from_string("ROCK"), Choice.ROCK)
        self.assertEqual(Choice.from_string("Rock"), Choice.ROCK)

    def test_choice_from_string_japanese(self):
        """日本語入力からChoiceへの変換テスト"""
        self.assertEqual(Choice.from_string("グー"), Choice.ROCK)
        self.assertEqual(Choice.from_string("パー"), Choice.PAPER)
        self.assertEqual(Choice.from_string("チョキ"), Choice.SCISSORS)

    def test_choice_from_string_invalid(self):
        """無効な入力のテスト"""
        self.assertIsNone(Choice.from_string("invalid"))
        self.assertIsNone(Choice.from_string(""))
        self.assertIsNone(Choice.from_string("123"))
        self.assertIsNone(Choice.from_string("ぐー"))  # ひらがな

    def test_choice_to_display_japanese(self):
        """日本語表示のテスト"""
        self.assertEqual(Choice.ROCK.to_display("ja"), "グー ✊")
        self.assertEqual(Choice.PAPER.to_display("ja"), "パー ✋")
        self.assertEqual(Choice.SCISSORS.to_display("ja"), "チョキ ✌️")

    def test_choice_to_display_english(self):
        """英語表示のテスト"""
        self.assertEqual(Choice.ROCK.to_display("en"), "Rock ✊")
        self.assertEqual(Choice.PAPER.to_display("en"), "Paper ✋")
        self.assertEqual(Choice.SCISSORS.to_display("en"), "Scissors ✌️")

    def test_choice_to_display_default(self):
        """デフォルト言語（日本語）表示のテスト"""
        self.assertEqual(Choice.ROCK.to_display(), "グー ✊")


class TestRockPaperScissorsEngine(unittest.TestCase):
    """じゃんけんエンジンのテストクラス"""

    def test_determine_winner_all_draws(self):
        """すべての引き分けパターンのテスト"""
        draws = [
            (Choice.ROCK, Choice.ROCK),
            (Choice.PAPER, Choice.PAPER),
            (Choice.SCISSORS, Choice.SCISSORS),
        ]

        for player_choice, ai_choice in draws:
            with self.subTest(player=player_choice, ai=ai_choice):
                result = RockPaperScissorsEngine.determine_winner(
                    player_choice, ai_choice
                )
                self.assertEqual(result, GameResult.DRAW)

    def test_determine_winner_all_wins(self):
        """すべてのプレイヤー勝利パターンのテスト"""
        wins = [
            (Choice.ROCK, Choice.SCISSORS),
            (Choice.PAPER, Choice.ROCK),
            (Choice.SCISSORS, Choice.PAPER),
        ]

        for player_choice, ai_choice in wins:
            with self.subTest(player=player_choice, ai=ai_choice):
                result = RockPaperScissorsEngine.determine_winner(
                    player_choice, ai_choice
                )
                self.assertEqual(result, GameResult.WIN)

    def test_determine_winner_all_losses(self):
        """すべてのプレイヤー敗北パターンのテスト"""
        losses = [
            (Choice.ROCK, Choice.PAPER),
            (Choice.PAPER, Choice.SCISSORS),
            (Choice.SCISSORS, Choice.ROCK),
        ]

        for player_choice, ai_choice in losses:
            with self.subTest(player=player_choice, ai=ai_choice):
                result = RockPaperScissorsEngine.determine_winner(
                    player_choice, ai_choice
                )
                self.assertEqual(result, GameResult.LOSE)

    def test_validate_choice_all_valid(self):
        """すべての有効な入力のテスト"""
        valid_inputs = ["rock", "paper", "scissors", "グー", "パー", "チョキ"]

        for input_str in valid_inputs:
            with self.subTest(input=input_str):
                self.assertTrue(RockPaperScissorsEngine.validate_choice(input_str))

    def test_validate_choice_all_invalid(self):
        """すべての無効な入力のテスト"""
        invalid_inputs = [
            "invalid",
            "",
            "123",
            "ぐー",
            "ぱー",
            "ちょき",
            "石",
            "紙",
            "はさみ",
        ]

        for input_str in invalid_inputs:
            with self.subTest(input=input_str):
                self.assertFalse(RockPaperScissorsEngine.validate_choice(input_str))


if __name__ == "__main__":
    unittest.main()
