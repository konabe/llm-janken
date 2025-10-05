"""
CLIインターフェースの包括的テスト
"""

import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
from src.ui.cli import CLIInterface
from src.ai.player import RandomAIPlayer
from src.game.engine import Choice, GameResult


class TestCLIInterface(unittest.TestCase):
    """CLIInterfaceのテスト"""
    
    def setUp(self):
        """テスト前の準備"""
        self.cli_ja = CLIInterface(language='ja')
        self.cli_en = CLIInterface(language='en')
    
    def test_initialization_japanese(self):
        """日本語CLIの初期化テスト"""
        self.assertEqual(self.cli_ja.language, 'ja')
        self.assertIn('welcome', self.cli_ja.messages)
        self.assertEqual(self.cli_ja.messages['welcome'], '🎮 LLM じゃんけんゲームへようこそ！')
    
    def test_initialization_english(self):
        """英語CLIの初期化テスト"""
        self.assertEqual(self.cli_en.language, 'en')
        self.assertIn('welcome', self.cli_en.messages)
        self.assertEqual(self.cli_en.messages['welcome'], '🎮 Welcome to LLM Rock-Paper-Scissors!')
    
    def test_load_messages_japanese(self):
        """日本語メッセージ読み込みテスト"""
        messages = self.cli_ja.messages
        
        required_keys = [
            'welcome', 'separator', 'vs_ai', 'choices', 'quit_info',
            'game_title', 'input_prompt', 'invalid_input', 'you', 'ai',
            'win', 'lose', 'draw', 'game_end'
        ]
        
        for key in required_keys:
            with self.subTest(key=key):
                self.assertIn(key, messages)
                self.assertIsInstance(messages[key], str)
                self.assertGreater(len(messages[key]), 0)
    
    def test_load_messages_english(self):
        """英語メッセージ読み込みテスト"""
        messages = self.cli_en.messages
        
        required_keys = [
            'welcome', 'separator', 'vs_ai', 'choices', 'quit_info',
            'game_title', 'input_prompt', 'invalid_input', 'you', 'ai',
            'win', 'lose', 'draw', 'game_end'
        ]
        
        for key in required_keys:
            with self.subTest(key=key):
                self.assertIn(key, messages)
                self.assertIsInstance(messages[key], str)
                self.assertGreater(len(messages[key]), 0)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_display_welcome(self, mock_stdout):
        """ウェルカムメッセージ表示テスト"""
        self.cli_ja.display_welcome()
        output = mock_stdout.getvalue()
        
        self.assertIn('🎮 LLM じゃんけんゲームへようこそ！', output)
        self.assertIn('🤖 AI 対戦相手と対戦します！', output)
        self.assertIn('選択肢: rock (グー), paper (パー), scissors (チョキ)', output)
    
    @patch('builtins.input', return_value='rock')
    @patch('sys.stdout', new_callable=StringIO)
    def test_get_player_choice_valid_english(self, mock_stdout, mock_input):
        """有効な英語入力のテスト"""
        choice = self.cli_ja.get_player_choice()
        self.assertEqual(choice, Choice.ROCK)
    
    @patch('builtins.input', return_value='グー')
    @patch('sys.stdout', new_callable=StringIO)
    def test_get_player_choice_valid_japanese(self, mock_stdout, mock_input):
        """有効な日本語入力のテスト"""
        choice = self.cli_ja.get_player_choice()
        self.assertEqual(choice, Choice.ROCK)
    
    @patch('builtins.input', return_value='quit')
    @patch('sys.stdout', new_callable=StringIO)
    def test_get_player_choice_quit(self, mock_stdout, mock_input):
        """終了入力のテスト"""
        choice = self.cli_ja.get_player_choice()
        self.assertIsNone(choice)
    
    @patch('builtins.input', side_effect=['invalid', 'rock'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_get_player_choice_invalid_then_valid(self, mock_stdout, mock_input):
        """無効入力後に有効入力のテスト"""
        choice = self.cli_ja.get_player_choice()
        output = mock_stdout.getvalue()
        
        self.assertEqual(choice, Choice.ROCK)
        self.assertIn('無効な入力です', output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_display_result_win(self, mock_stdout):
        """勝利結果表示テスト"""
        self.cli_ja.display_result(Choice.ROCK, Choice.SCISSORS, GameResult.WIN)
        output = mock_stdout.getvalue()
        
        self.assertIn('あなた: グー ✊', output)
        self.assertIn('AI: チョキ ✌️', output)
        self.assertIn('🎉 あなたの勝ち！', output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_display_result_lose(self, mock_stdout):
        """敗北結果表示テスト"""
        self.cli_ja.display_result(Choice.ROCK, Choice.PAPER, GameResult.LOSE)
        output = mock_stdout.getvalue()
        
        self.assertIn('あなた: グー ✊', output)
        self.assertIn('AI: パー ✋', output)
        self.assertIn('😅 AI の勝ち！', output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_display_result_draw(self, mock_stdout):
        """引き分け結果表示テスト"""
        self.cli_ja.display_result(Choice.ROCK, Choice.ROCK, GameResult.DRAW)
        output = mock_stdout.getvalue()
        
        self.assertIn('あなた: グー ✊', output)
        self.assertIn('AI: グー ✊', output)
        self.assertIn('🤝 引き分け！', output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_display_goodbye(self, mock_stdout):
        """終了メッセージ表示テスト"""
        self.cli_ja.display_goodbye()
        output = mock_stdout.getvalue()
        
        self.assertIn('ゲームを終了します。ありがとうございました！', output)
    
    @patch('builtins.input', return_value='rock')
    @patch('sys.stdout', new_callable=StringIO)
    def test_run_single_game_normal(self, mock_stdout, mock_input):
        """通常ゲーム実行のテスト"""
        ai_player = RandomAIPlayer("TestAI")
        
        # AI選択を固定
        with patch.object(ai_player, 'make_choice', return_value=Choice.SCISSORS):
            self.cli_ja.run_single_game(ai_player)
        
        output = mock_stdout.getvalue()
        
        # ウェルカムメッセージ
        self.assertIn('🎮 LLM じゃんけんゲームへようこそ！', output)
        
        # ゲーム結果（ROCK vs SCISSORS = WIN）
        self.assertIn('あなた: グー ✊', output)
        self.assertIn('AI: チョキ ✌️', output)
        self.assertIn('🎉 あなたの勝ち！', output)
        
        # 終了メッセージ
        self.assertIn('ゲームを終了します。ありがとうございました！', output)
        
        # AI履歴記録の確認
        self.assertEqual(len(ai_player.game_history), 1)
        self.assertEqual(ai_player.game_history[0], (Choice.ROCK, Choice.SCISSORS, 'win'))
    
    @patch('builtins.input', return_value='quit')
    @patch('sys.stdout', new_callable=StringIO)
    def test_run_single_game_quit(self, mock_stdout, mock_input):
        """終了選択時のゲーム実行テスト"""
        ai_player = RandomAIPlayer("TestAI")
        
        self.cli_ja.run_single_game(ai_player)
        
        output = mock_stdout.getvalue()
        
        # ウェルカムメッセージ
        self.assertIn('🎮 LLM じゃんけんゲームへようこそ！', output)
        
        # 終了メッセージ
        self.assertIn('ゲームを終了します。ありがとうございました！', output)
        
        # ゲーム履歴は記録されない
        self.assertEqual(len(ai_player.game_history), 0)


class TestCLIInterfaceEnglish(unittest.TestCase):
    """英語CLIインターフェースのテスト"""
    
    def setUp(self):
        """テスト前の準備"""
        self.cli = CLIInterface(language='en')
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_display_result_english(self, mock_stdout):
        """英語での結果表示テスト"""
        self.cli.display_result(Choice.ROCK, Choice.SCISSORS, GameResult.WIN)
        output = mock_stdout.getvalue()
        
        self.assertIn('You: Rock ✊', output)
        self.assertIn('AI: Scissors ✌️', output)
        self.assertIn('🎉 You win!', output)


if __name__ == '__main__':
    unittest.main()