"""
心理戦システムのテスト
"""

import os
import unittest
from unittest.mock import MagicMock, patch

from src.ai.player import AIPlayer, LLMAIPlayer
from src.game.engine import Choice


class ConcreteAIPlayer(AIPlayer):
    """テスト用の具象AIPlayerクラス"""

    def make_choice(self) -> Choice:
        return Choice.ROCK


class TestPsychologicalMessages(unittest.TestCase):
    """心理戦メッセージのテスト"""

    @patch("openai.OpenAI")
    def test_llm_ai_psychological_message_success(self, mock_openai):
        """LLM AIの心理戦メッセージ成功テスト"""
        # OpenAI APIをモック
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "君の手は読めているよ"

        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        # 環境変数をモック
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}):
            ai_player = LLMAIPlayer("TestLLM")
            message = ai_player.get_psychological_message()

        self.assertEqual(message, "君の手は読めているよ")

    @patch("openai.OpenAI")
    def test_llm_ai_psychological_message_api_error(self, mock_openai):
        """LLM AIの心理戦メッセージAPIエラー時テスト"""
        # OpenAI APIでエラーを発生させる
        mock_openai.side_effect = Exception("API Error")

        with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}):
            ai_player = LLMAIPlayer("TestLLM")
            message = ai_player.get_psychological_message()

        # フォールバックメッセージが返されることを確認
        fallback_messages = [
            "勝負だ！",
            "本気を見せる時だ",
            "君の実力を見せてもらおう",
            "面白くなりそうだ",
            "負けないぞ！",
            "覚悟はできたか？",
            "手加減はしないぞ！",
        ]
        self.assertIn(message, fallback_messages)

    def test_base_ai_psychological_message(self):
        """基底AIクラスの心理戦メッセージテスト"""
        ai_player = ConcreteAIPlayer("TestAI")
        message = ai_player.get_psychological_message()
        self.assertEqual(message, "さあ、勝負だ！")


if __name__ == "__main__":
    unittest.main()
