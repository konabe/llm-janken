"""
心理戦システムのテスト
"""

import unittest
from unittest.mock import patch, MagicMock
import os
from src.ai.player import RandomAIPlayer, PatternAIPlayer, LLMAIPlayer
from src.game.engine import Choice


class TestPsychologicalMessages(unittest.TestCase):
    """心理戦メッセージのテスト"""
    
    def test_random_ai_psychological_message(self):
        """ランダムAIの心理戦メッセージテスト"""
        ai_player = RandomAIPlayer("TestRandomAI")
        message = ai_player.get_psychological_message()
        
        # メッセージが文字列であることを確認
        self.assertIsInstance(message, str)
        # メッセージが空でないことを確認
        self.assertGreater(len(message), 0)
        
        # 複数回呼び出してバリエーションがあることを確認
        messages = [ai_player.get_psychological_message() for _ in range(10)]
        # 少なくとも2種類のメッセージがあることを期待
        unique_messages = set(messages)
        self.assertGreaterEqual(len(unique_messages), 2)
    
    def test_pattern_ai_psychological_message_no_history(self):
        """パターンAIの履歴なし時の心理戦メッセージテスト"""
        ai_player = PatternAIPlayer("TestPatternAI")
        message = ai_player.get_psychological_message()
        
        self.assertIsInstance(message, str)
        self.assertIn("分析", message)
    
    def test_pattern_ai_psychological_message_with_history(self):
        """パターンAIの履歴あり時の心理戦メッセージテスト"""
        ai_player = PatternAIPlayer("TestPatternAI")
        
        # 履歴を追加
        ai_player.record_game(Choice.ROCK, Choice.PAPER, "LOSE")
        ai_player.record_game(Choice.ROCK, Choice.PAPER, "LOSE")
        ai_player.record_game(Choice.ROCK, Choice.PAPER, "LOSE")
        
        message = ai_player.get_psychological_message()
        self.assertIsInstance(message, str)
        self.assertGreater(len(message), 0)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_llm_ai_psychological_message_success(self):
        """LLM AIの心理戦メッセージ成功テスト"""
        # OpenAI APIレスポンスをモック
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "勝負の時だ！"
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        
        ai_player = LLMAIPlayer("TestLLMAI")
        ai_player._client = mock_client
        
        message = ai_player.get_psychological_message()
        
        self.assertEqual(message, "勝負の時だ！")
        # OpenAI APIが適切なパラメータで呼ばれたことを確認
        mock_client.chat.completions.create.assert_called_once()
        call_args = mock_client.chat.completions.create.call_args
        self.assertIn("心理的プレッシャー", call_args[1]['messages'][0]['content'])
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_llm_ai_psychological_message_api_error(self):
        """LLM AIの心理戦メッセージAPIエラー時テスト"""
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        
        ai_player = LLMAIPlayer("TestLLMAI")
        ai_player._client = mock_client
        
        message = ai_player.get_psychological_message()
        
        # フォールバックメッセージが返されることを確認
        self.assertIsInstance(message, str)
        self.assertGreater(len(message), 0)
        # デフォルトメッセージのいずれかであることを確認
        fallback_messages = [
            "勝負だ！",
            "本気を見せる時だ",
            "君の実力を見せてもらおう",
            "面白くなりそうだ",
            "負けないぞ！"
        ]
        self.assertIn(message, fallback_messages)
    
    def test_base_ai_psychological_message(self):
        """基底AIクラスの心理戦メッセージテスト"""
        # RandomAIPlayerを使用して基底クラスのメソッドをテスト
        ai_player = RandomAIPlayer("TestAI")
        

        message = ai_player.get_psychological_message()
        self.assertNotEqual(message, "さあ、勝負だ！")


if __name__ == '__main__':
    unittest.main()