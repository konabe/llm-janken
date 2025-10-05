"""
LLMAIPlayer のテスト
"""

import unittest
from unittest.mock import patch, MagicMock
import os
from src.ai.player import LLMAIPlayer
from src.game.engine import Choice


class TestLLMAIPlayer(unittest.TestCase):
    """LLMAIPlayerのテストクラス"""
    
    def setUp(self) -> None:
        """各テスト前の初期化"""
        # 環境変数をモック
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            self.player = LLMAIPlayer(name="テストAI", personality="balanced")
    
    def test_initialization(self) -> None:
        """初期化のテスト"""
        self.assertEqual(self.player.name, "テストAI")
        self.assertEqual(self.player.personality, "balanced")
        self.assertEqual(self.player.max_history, 5)
        self.assertEqual(len(self.player.game_history), 0)
        # デフォルトモデルがgpt-4o-miniであることを確認
        self.assertEqual(self.player.model, "gpt-4o-mini")
    
    def test_custom_model(self) -> None:
        """カスタムモデル設定のテスト"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key', 'OPENAI_MODEL': 'gpt-3.5-turbo'}):
            custom_player = LLMAIPlayer(name="カスタムAI")
            self.assertEqual(custom_player.model, "gpt-3.5-turbo")
    
    def test_build_prompt_no_history(self) -> None:
        """履歴なしでのプロンプト構築テスト"""
        prompt = self.player._build_prompt()
        self.assertIn("バランス感覚に優れた", prompt)
        self.assertIn("rock", prompt)
        self.assertIn("paper", prompt)
        self.assertIn("scissors", prompt)
        self.assertNotIn("過去のゲーム履歴", prompt)
    
    def test_build_prompt_with_history(self) -> None:
        """履歴ありでのプロンプト構築テスト"""
        # テスト履歴を追加
        self.player.record_game(Choice.ROCK, Choice.PAPER, "WIN")
        self.player.record_game(Choice.SCISSORS, Choice.ROCK, "LOSE")
        
        prompt = self.player._build_prompt()
        self.assertIn("過去のゲーム履歴", prompt)
        self.assertIn("rock", prompt.lower())
        self.assertIn("paper", prompt.lower())
        self.assertIn("scissors", prompt.lower())
    
    def test_personality_prompts(self) -> None:
        """各性格でのプロンプト生成テスト"""
        personalities = ["aggressive", "defensive", "random", "balanced", "analytical"]
        
        for personality in personalities:
            with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
                player = LLMAIPlayer(name="テスト", personality=personality)
                prompt = player._build_prompt()
                self.assertIsInstance(prompt, str)
                self.assertGreater(len(prompt), 0)
    
    def test_make_choice_rock_response(self) -> None:
        """OpenAI APIがrockを返す場合のテスト"""
        # モックレスポンスを設定
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "rock"
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            player = LLMAIPlayer(name="テスト")
            player._client = mock_client
            choice = player.make_choice()
            self.assertEqual(choice, Choice.ROCK)
    
    def test_make_choice_paper_response(self) -> None:
        """OpenAI APIがpaperを返す場合のテスト"""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "paper"
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            player = LLMAIPlayer(name="テスト")
            player._client = mock_client
            choice = player.make_choice()
            self.assertEqual(choice, Choice.PAPER)
    
    def test_make_choice_scissors_response(self) -> None:
        """OpenAI APIがscissorsを返す場合のテスト"""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "scissors"
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            player = LLMAIPlayer(name="テスト")
            player._client = mock_client
            choice = player.make_choice()
            self.assertEqual(choice, Choice.SCISSORS)
    
    def test_make_choice_japanese_response(self) -> None:
        """OpenAI APIが日本語で返す場合のテスト"""
        test_cases = [
            ("グー", Choice.ROCK),
            ("パー", Choice.PAPER),
            ("チョキ", Choice.SCISSORS)
        ]
        
        for japanese_response, expected_choice in test_cases:
            with self.subTest(response=japanese_response):
                mock_response = MagicMock()
                mock_response.choices[0].message.content = japanese_response
                mock_client = MagicMock()
                mock_client.chat.completions.create.return_value = mock_response
                
                with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
                    player = LLMAIPlayer(name="テスト")
                    player._client = mock_client
                    choice = player.make_choice()
                    self.assertEqual(choice, expected_choice)
    
    @patch('random.choice')
    def test_make_choice_invalid_response(self, mock_random_choice) -> None:
        """OpenAI APIが無効な応答を返す場合のテスト"""
        # 無効な応答を設定
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "invalid_choice"
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        
        # ランダム選択の結果を設定
        mock_random_choice.return_value = Choice.ROCK
        
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            player = LLMAIPlayer(name="テスト")
            player._client = mock_client
            choice = player.make_choice()
            self.assertEqual(choice, Choice.ROCK)
            mock_random_choice.assert_called_once()
    
    @patch('random.choice')
    def test_make_choice_api_error(self, mock_random_choice) -> None:
        """OpenAI APIエラー時のテスト"""
        # API エラーを発生させる
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        
        # ランダム選択の結果を設定
        mock_random_choice.return_value = Choice.SCISSORS
        
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            player = LLMAIPlayer(name="テスト")
            player._client = mock_client
            choice = player.make_choice()
            self.assertEqual(choice, Choice.SCISSORS)
            mock_random_choice.assert_called_once()
    
    def test_history_limit(self) -> None:
        """履歴制限のテスト"""
        # max_history を超える履歴を追加
        for _ in range(10):
            self.player.record_game(Choice.ROCK, Choice.PAPER, "WIN")
        
        prompt = self.player._build_prompt()
        
        # プロンプトに含まれる履歴の数を確認
        history_lines = [line for line in prompt.split('\n') if '.' in line and 'プレイヤー:' in line]
        self.assertLessEqual(len(history_lines), self.player.max_history)


if __name__ == '__main__':
    unittest.main()