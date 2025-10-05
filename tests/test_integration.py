"""
統合テストスイート - 全モジュール連携テスト
"""

import os
import unittest
from unittest.mock import patch, MagicMock
from src.game.engine import Choice, GameResult, RockPaperScissorsEngine
from src.ai.player import RandomAIPlayer, PatternAIPlayer, LLMAIPlayer
from src.ui.cli import CLIInterface
from src.stats.tracker import GameRecord, GameStatistics


class TestGameIntegration(unittest.TestCase):
    """ゲーム全体の統合テスト"""
    
    def setUp(self):
        """テスト前の準備"""
        self.engine = RockPaperScissorsEngine()
        self.ai_player = RandomAIPlayer("TestAI")
        self.cli = CLIInterface()
        self.stats = GameStatistics()
    
    def test_complete_game_flow(self):
        """完全なゲームフローのテスト"""
        # プレイヤーの選択
        player_choice = Choice.ROCK
        
        # AIの選択（固定）
        with patch.object(self.ai_player, 'make_choice', return_value=Choice.SCISSORS):
            ai_choice = self.ai_player.make_choice()
        
        # 勝敗判定
        result = self.engine.determine_winner(player_choice, ai_choice)
        
        # AI履歴記録
        self.ai_player.record_game(player_choice, ai_choice, result.value)
        
        # 統計記録
        record = GameRecord(player_choice, ai_choice, result, "2025-10-05 10:00:00")
        self.stats.add_game(record)
        
        # 結果検証
        self.assertEqual(result, GameResult.WIN)  # ROCK vs SCISSORS
        self.assertEqual(len(self.ai_player.game_history), 1)
        self.assertEqual(len(self.stats.records), 1)
        self.assertEqual(self.stats.get_win_rate(), 100.0)
    
    def test_multiple_games_consistency(self):
        """複数ゲームでの一貫性テスト"""
        game_scenarios = [
            (Choice.ROCK, Choice.SCISSORS, GameResult.WIN),
            (Choice.PAPER, Choice.ROCK, GameResult.WIN),
            (Choice.SCISSORS, Choice.SCISSORS, GameResult.DRAW),
            (Choice.ROCK, Choice.PAPER, GameResult.LOSE)
        ]
        
        for i, (player_choice, ai_choice, expected_result) in enumerate(game_scenarios):
            with self.subTest(game=i):
                # 勝敗判定
                result = self.engine.determine_winner(player_choice, ai_choice)
                
                # 結果の一貫性確認
                self.assertEqual(result, expected_result)
                
                # AI履歴記録
                self.ai_player.record_game(player_choice, ai_choice, result.value)
                
                # 統計記録
                record = GameRecord(player_choice, ai_choice, result, f"2025-10-05 10:0{i}:00")
                self.stats.add_game(record)
        
        # 最終統計検証
        summary = self.stats.get_summary()
        self.assertEqual(summary['total_games'], 4)
        self.assertEqual(summary['wins'], 2)
        self.assertEqual(summary['losses'], 1)
        self.assertEqual(summary['draws'], 1)
        self.assertEqual(summary['win_rate'], 50.0)
        
        # AI履歴検証
        self.assertEqual(len(self.ai_player.game_history), 4)


class TestPatternLearningIntegration(unittest.TestCase):
    """パターン学習AIの統合テスト"""
    
    def setUp(self):
        """テスト前の準備"""
        self.pattern_ai = PatternAIPlayer("PatternAI")
        self.engine = RockPaperScissorsEngine()
        self.stats = GameStatistics()
    
    def test_pattern_learning_effectiveness(self):
        """パターン学習の効果性テスト"""
        # プレイヤーが常にROCKを出すパターンを学習させる
        player_pattern = Choice.ROCK
        
        # 5回同じパターンでゲーム
        for i in range(5):
            ai_choice = self.pattern_ai.make_choice()
            result = self.engine.determine_winner(player_pattern, ai_choice)
            
            # AI履歴記録
            self.pattern_ai.record_game(player_pattern, ai_choice, result.value)
            
            # 統計記録
            record = GameRecord(player_pattern, ai_choice, result, f"2025-10-05 10:0{i}:00")
            self.stats.add_game(record)
        
        # パターン学習後のテスト（確実に対策を選択するよう設定）
        with patch('random.random', return_value=0.5):  # 対策選択
            final_ai_choice = self.pattern_ai.make_choice()
        
        # ROCKに対する対策はPAPERのはず
        self.assertEqual(final_ai_choice, Choice.PAPER)
        
        # 学習効果の検証（後半のゲームで勝率向上を期待）
        summary = self.stats.get_summary()
        self.assertGreaterEqual(summary['total_games'], 5)


class TestCLIIntegration(unittest.TestCase):
    """CLI統合テスト"""
    
    def setUp(self):
        """テスト前の準備"""
        self.cli = CLIInterface()
        self.ai_player = RandomAIPlayer("TestAI")
    
    @patch('builtins.input', return_value='rock')
    @patch('sys.stdout')
    def test_cli_ai_integration(self, mock_stdout, mock_input):
        """CLI-AI統合テスト"""
        # AI選択を固定
        with patch.object(self.ai_player, 'make_choice', return_value=Choice.SCISSORS):
            # シングルゲーム実行
            self.cli.run_single_game(self.ai_player)
        
        # AI履歴が記録されることを確認
        self.assertEqual(len(self.ai_player.game_history), 1)
        
        # 正しい結果が記録されることを確認
        player_choice, ai_choice, result = self.ai_player.game_history[0]
        self.assertEqual(player_choice, Choice.ROCK)
        self.assertEqual(ai_choice, Choice.SCISSORS)
        self.assertEqual(result, 'win')


class TestErrorHandling(unittest.TestCase):
    """エラーハンドリングの統合テスト"""
    
    def test_invalid_choice_handling(self):
        """無効な選択肢のハンドリングテスト"""
        # エンジンレベルでの無効入力
        self.assertFalse(RockPaperScissorsEngine.validate_choice("invalid"))
        
        # Choiceクラスでの無効入力
        self.assertIsNone(Choice.from_string("invalid"))
    
    def test_empty_stats_handling(self):
        """空の統計データのハンドリングテスト"""
        stats = GameStatistics()
        
        # 空データでの各メソッド実行
        self.assertEqual(stats.get_win_rate(), 0.0)
        self.assertEqual(stats.get_choice_frequency(), {Choice.ROCK: 0, Choice.PAPER: 0, Choice.SCISSORS: 0})
        
        summary = stats.get_summary()
        self.assertEqual(summary['total_games'], 0)
    
    def test_ai_consistency(self):
        """AI動作の一貫性テスト"""
        ai_player = RandomAIPlayer("TestAI")
        
        # 複数回選択して全て有効な選択肢であることを確認
        for _ in range(10):
            choice = ai_player.make_choice()
            self.assertIn(choice, [Choice.ROCK, Choice.PAPER, Choice.SCISSORS])


class TestPerformance(unittest.TestCase):
    """パフォーマンステスト"""
    
    def test_large_game_simulation(self):
        """大量ゲームシミュレーションテスト"""
        stats = GameStatistics()
        ai_player = RandomAIPlayer("PerfTestAI")
        
        # 100ゲームシミュレーション
        for i in range(100):
            player_choice = Choice.ROCK  # 固定
            ai_choice = ai_player.make_choice()
            result = RockPaperScissorsEngine.determine_winner(player_choice, ai_choice)
            
            # 記録
            ai_player.record_game(player_choice, ai_choice, result.value)
            record = GameRecord(player_choice, ai_choice, result, f"2025-10-05 {i:03d}")
            stats.add_game(record)
        
        # 結果検証
        summary = stats.get_summary()
        self.assertEqual(summary['total_games'], 100)
        self.assertEqual(len(ai_player.game_history), 100)
        
        # 統計の一貫性確認
        total_results = summary['wins'] + summary['losses'] + summary['draws']
        self.assertEqual(total_results, 100)


class TestLLMIntegration(unittest.TestCase):
    """LLM AI プレイヤーの統合テスト"""
    
    def test_llm_ai_game_integration(self):
        """LLM AIプレイヤーとのゲーム統合テスト"""
        # OpenAI APIレスポンスをモック
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "rock"
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        
        # 環境変数をモック
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            # コンポーネント初期化
            engine = RockPaperScissorsEngine()
            llm_player = LLMAIPlayer(name="GPTプレイヤー", personality="analytical")
            llm_player._client = mock_client
            stats = GameStatistics()
            
            # ゲーム実行
            player_choice = Choice.SCISSORS
            ai_choice = llm_player.make_choice()
            result = engine.determine_winner(player_choice, ai_choice)
            
            # 履歴記録
            llm_player.record_game(player_choice, ai_choice, result.value)
            record = GameRecord(player_choice, ai_choice, result, "2025-10-05 12:00:00")
            stats.add_game(record)
            
            # 検証
            self.assertEqual(ai_choice, Choice.ROCK)
            self.assertEqual(result, GameResult.LOSE)  # SCISSORS vs ROCK
            self.assertEqual(len(llm_player.game_history), 1)
            self.assertEqual(stats.get_win_rate(), 0.0)
    
    def test_llm_ai_learning_from_history(self):
        """LLM AIプレイヤーの履歴学習テスト"""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "paper"
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            llm_player = LLMAIPlayer(name="学習AI", personality="analytical")
            llm_player._client = mock_client
            
            # 履歴を追加
            llm_player.record_game(Choice.ROCK, Choice.PAPER, "LOSE")
            llm_player.record_game(Choice.ROCK, Choice.SCISSORS, "WIN")
            
            # プロンプト構築確認
            prompt = llm_player._build_prompt()
            self.assertIn("過去のゲーム履歴", prompt)
            self.assertIn("rock", prompt.lower())
            
            # 選択実行
            choice = llm_player.make_choice()
            self.assertEqual(choice, Choice.PAPER)
            
            # OpenAI API が呼ばれたことを確認
            mock_client.chat.completions.create.assert_called()


if __name__ == '__main__':
    # 全テストモジュールを実行
    test_modules = [
        'test_engine',
        'test_ai_player', 
        'test_ui_cli',
        'test_stats'
    ]
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 統合テストを追加
    suite.addTest(loader.loadTestsFromTestCase(TestGameIntegration))
    suite.addTest(loader.loadTestsFromTestCase(TestPatternLearningIntegration))
    suite.addTest(loader.loadTestsFromTestCase(TestCLIIntegration))
    suite.addTest(loader.loadTestsFromTestCase(TestErrorHandling))
    suite.addTest(loader.loadTestsFromTestCase(TestPerformance))
    suite.addTest(loader.loadTestsFromTestCase(TestLLMIntegration))
    
    # 個別モジュールテストも追加
    for module in test_modules:
        try:
            tests = loader.loadTestsFromName(module)
            suite.addTest(tests)
        except ImportError as e:
            print(f"モジュール {module} をロードできませんでした: {e}")
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)