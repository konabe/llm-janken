"""
統合テストスイート - LLM AI統合テスト
"""

import os
import unittest
from unittest.mock import MagicMock, patch

from src.ai.player import LLMAIPlayer
from src.game.engine import Choice, GameResult, RockPaperScissorsEngine
from src.ui.cli import CLIInterface


class TestLLMIntegration(unittest.TestCase):
    """LLM AI統合テスト"""

    def setUp(self):
        """テスト前の準備"""
        self.engine = RockPaperScissorsEngine()
        self.cli = CLIInterface()

    @patch("src.ai.player.LLMAIPlayer.client", new_callable=lambda: MagicMock())
    def test_llm_ai_game_integration(self, mock_client):
        """LLM AIプレイヤーとのゲーム統合テスト"""
        # OpenAI APIをモック
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "rock"

        mock_client.chat.completions.create.return_value = mock_response

        # LLMAIPlayerでテスト
        ai_player = LLMAIPlayer("TestLLM")

        # プレイヤーの選択
        player_choice = Choice.SCISSORS

        # AIの選択
        ai_choice = ai_player.make_choice()

        # 勝敗判定
        result = self.engine.determine_winner(player_choice, ai_choice)

        # AIが何かしらの有効な選択をしたことを確認
        self.assertIn(ai_choice, [Choice.ROCK, Choice.PAPER, Choice.SCISSORS])
        self.assertIn(result, [GameResult.WIN, GameResult.LOSE, GameResult.DRAW])

        # 履歴記録
        ai_player.record_game(player_choice, ai_choice, result.value)
        self.assertEqual(len(ai_player.game_history), 1)

    @patch("src.ai.player.LLMAIPlayer.client", new_callable=lambda: MagicMock())
    def test_llm_ai_learning_from_history(self, mock_client):
        """LLM AIプレイヤーの履歴学習テスト"""
        # OpenAI APIをモック
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "paper"

        mock_client.chat.completions.create.return_value = mock_response

        ai_player = LLMAIPlayer("LearningAI")

        # 履歴を追加
        ai_player.record_game(Choice.ROCK, Choice.SCISSORS, "win")
        ai_player.record_game(Choice.PAPER, Choice.ROCK, "win")

        # 履歴を考慮した選択
        ai_choice = ai_player.make_choice()

        # APIが呼び出され、PAPERが選択される
        self.assertEqual(ai_choice, Choice.PAPER)

        # プロンプトに履歴が含まれることを確認
        call_args = mock_client.chat.completions.create.call_args
        if call_args and call_args[1] and "messages" in call_args[1]:
            prompt = call_args[1]["messages"][1]["content"]
            self.assertIn("過去のゲーム履歴", prompt)
        else:
            # API呼び出しが期待通りに実行されたことを確認
            mock_client.chat.completions.create.assert_called_once()


class TestGameBasics(unittest.TestCase):
    """基本的なゲーム機能の統合テスト"""

    def setUp(self):
        """テスト前の準備"""
        self.engine = RockPaperScissorsEngine()

    def test_complete_game_flow(self):
        """完全なゲームフローのテスト"""
        # 基本的な勝敗判定のテスト
        test_cases = [
            (Choice.ROCK, Choice.SCISSORS, GameResult.WIN),
            (Choice.PAPER, Choice.ROCK, GameResult.WIN),
            (Choice.SCISSORS, Choice.SCISSORS, GameResult.DRAW),
            (Choice.ROCK, Choice.PAPER, GameResult.LOSE),
        ]

        for player_choice, ai_choice, expected_result in test_cases:
            with self.subTest(
                player=player_choice, ai=ai_choice, expected=expected_result
            ):
                result = self.engine.determine_winner(player_choice, ai_choice)
                self.assertEqual(result, expected_result)


class TestErrorHandling(unittest.TestCase):
    """エラーハンドリングテスト"""

    def test_invalid_choice_handling(self):
        """無効な選択肢のハンドリングテスト"""
        # 無効な文字列のテスト
        invalid_inputs = ["invalid", "", "123", "グーパー"]

        for invalid_input in invalid_inputs:
            with self.subTest(input=invalid_input):
                result = Choice.from_string(invalid_input)
                self.assertIsNone(result, f"'{invalid_input}' should return None")


if __name__ == "__main__":
    unittest.main()
