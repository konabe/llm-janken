"""
統計モジュールの包括的テスト
"""

import unittest
from datetime import datetime
from src.stats.tracker import GameRecord, GameStatistics
from src.game.engine import Choice, GameResult


class TestGameRecord(unittest.TestCase):
    """GameRecordクラスのテスト"""
    
    def test_game_record_creation(self):
        """GameRecord作成のテスト"""
        timestamp = "2025-10-05 10:30:00"
        record = GameRecord(
            player_choice=Choice.ROCK,
            ai_choice=Choice.SCISSORS,
            result=GameResult.WIN,
            timestamp=timestamp
        )
        
        self.assertEqual(record.player_choice, Choice.ROCK)
        self.assertEqual(record.ai_choice, Choice.SCISSORS)
        self.assertEqual(record.result, GameResult.WIN)
        self.assertEqual(record.timestamp, timestamp)
    
    def test_game_record_equality(self):
        """GameRecordの等価性テスト"""
        timestamp = "2025-10-05 10:30:00"
        record1 = GameRecord(Choice.ROCK, Choice.SCISSORS, GameResult.WIN, timestamp)
        record2 = GameRecord(Choice.ROCK, Choice.SCISSORS, GameResult.WIN, timestamp)
        record3 = GameRecord(Choice.PAPER, Choice.SCISSORS, GameResult.WIN, timestamp)
        
        self.assertEqual(record1, record2)
        self.assertNotEqual(record1, record3)


class TestGameStatistics(unittest.TestCase):
    """GameStatisticsクラスのテスト"""
    
    def setUp(self):
        """テスト前の準備"""
        self.stats = GameStatistics()
        
        # テスト用のサンプルデータ
        self.sample_records = [
            GameRecord(Choice.ROCK, Choice.SCISSORS, GameResult.WIN, "2025-10-05 10:00:00"),
            GameRecord(Choice.PAPER, Choice.ROCK, GameResult.WIN, "2025-10-05 10:01:00"),
            GameRecord(Choice.SCISSORS, Choice.SCISSORS, GameResult.DRAW, "2025-10-05 10:02:00"),
            GameRecord(Choice.ROCK, Choice.PAPER, GameResult.LOSE, "2025-10-05 10:03:00"),
            GameRecord(Choice.PAPER, Choice.SCISSORS, GameResult.LOSE, "2025-10-05 10:04:00")
        ]
    
    def test_initialization(self):
        """初期化のテスト"""
        self.assertEqual(len(self.stats.records), 0)
        self.assertIsInstance(self.stats.records, list)
    
    def test_add_single_game(self):
        """単一ゲーム記録追加のテスト"""
        record = self.sample_records[0]
        self.stats.add_game(record)
        
        self.assertEqual(len(self.stats.records), 1)
        self.assertEqual(self.stats.records[0], record)
    
    def test_add_multiple_games(self):
        """複数ゲーム記録追加のテスト"""
        for record in self.sample_records:
            self.stats.add_game(record)
        
        self.assertEqual(len(self.stats.records), 5)
        
        for i, expected in enumerate(self.sample_records):
            self.assertEqual(self.stats.records[i], expected)
    
    def test_get_win_rate_empty(self):
        """空の統計での勝率計算テスト"""
        win_rate = self.stats.get_win_rate()
        self.assertEqual(win_rate, 0.0)
    
    def test_get_win_rate_with_data(self):
        """データありでの勝率計算テスト"""
        # 2勝、1引分、2敗 = 勝率40%
        for record in self.sample_records:
            self.stats.add_game(record)
        
        win_rate = self.stats.get_win_rate()
        self.assertEqual(win_rate, 40.0)  # 2/5 * 100 = 40%
    
    def test_get_win_rate_all_wins(self):
        """全勝時の勝率計算テスト"""
        win_records = [
            GameRecord(Choice.ROCK, Choice.SCISSORS, GameResult.WIN, "2025-10-05 10:00:00"),
            GameRecord(Choice.PAPER, Choice.ROCK, GameResult.WIN, "2025-10-05 10:01:00"),
            GameRecord(Choice.SCISSORS, Choice.PAPER, GameResult.WIN, "2025-10-05 10:02:00")
        ]
        
        for record in win_records:
            self.stats.add_game(record)
        
        win_rate = self.stats.get_win_rate()
        self.assertEqual(win_rate, 100.0)
    
    def test_get_win_rate_all_losses(self):
        """全敗時の勝率計算テスト"""
        lose_records = [
            GameRecord(Choice.ROCK, Choice.PAPER, GameResult.LOSE, "2025-10-05 10:00:00"),
            GameRecord(Choice.PAPER, Choice.SCISSORS, GameResult.LOSE, "2025-10-05 10:01:00"),
            GameRecord(Choice.SCISSORS, Choice.ROCK, GameResult.LOSE, "2025-10-05 10:02:00")
        ]
        
        for record in lose_records:
            self.stats.add_game(record)
        
        win_rate = self.stats.get_win_rate()
        self.assertEqual(win_rate, 0.0)
    
    def test_get_choice_frequency_empty(self):
        """空の統計での選択頻度計算テスト"""
        frequency = self.stats.get_choice_frequency()
        
        expected = {Choice.ROCK: 0, Choice.PAPER: 0, Choice.SCISSORS: 0}
        self.assertEqual(frequency, expected)
    
    def test_get_choice_frequency_with_data(self):
        """データありでの選択頻度計算テスト"""
        for record in self.sample_records:
            self.stats.add_game(record)
        
        frequency = self.stats.get_choice_frequency()
        
        # ROCK: 2回, PAPER: 2回, SCISSORS: 1回
        expected = {Choice.ROCK: 2, Choice.PAPER: 2, Choice.SCISSORS: 1}
        self.assertEqual(frequency, expected)
    
    def test_get_choice_frequency_single_choice(self):
        """単一選択での頻度計算テスト"""
        rock_records = [
            GameRecord(Choice.ROCK, Choice.SCISSORS, GameResult.WIN, "2025-10-05 10:00:00"),
            GameRecord(Choice.ROCK, Choice.PAPER, GameResult.LOSE, "2025-10-05 10:01:00"),
            GameRecord(Choice.ROCK, Choice.ROCK, GameResult.DRAW, "2025-10-05 10:02:00")
        ]
        
        for record in rock_records:
            self.stats.add_game(record)
        
        frequency = self.stats.get_choice_frequency()
        
        expected = {Choice.ROCK: 3, Choice.PAPER: 0, Choice.SCISSORS: 0}
        self.assertEqual(frequency, expected)
    
    def test_get_summary_empty(self):
        """空の統計でのサマリー生成テスト"""
        summary = self.stats.get_summary()
        
        expected = {
            'total_games': 0,
            'wins': 0,
            'losses': 0,
            'draws': 0,
            'win_rate': 0.0
        }
        
        self.assertEqual(summary, expected)
    
    def test_get_summary_with_data(self):
        """データありでのサマリー生成テスト"""
        for record in self.sample_records:
            self.stats.add_game(record)
        
        summary = self.stats.get_summary()
        
        expected = {
            'total_games': 5,
            'wins': 2,
            'losses': 2,
            'draws': 1,
            'win_rate': 40.0
        }
        
        self.assertEqual(summary, expected)
    
    def test_get_summary_consistency(self):
        """サマリーの一貫性テスト（合計が総ゲーム数と一致）"""
        for record in self.sample_records:
            self.stats.add_game(record)
        
        summary = self.stats.get_summary()
        
        total_results = summary['wins'] + summary['losses'] + summary['draws']
        self.assertEqual(total_results, summary['total_games'])
    
    def test_get_summary_win_rate_calculation(self):
        """サマリー内勝率計算の正確性テスト"""
        for record in self.sample_records:
            self.stats.add_game(record)
        
        summary = self.stats.get_summary()
        
        # 手動計算での勝率と比較
        expected_win_rate = (summary['wins'] / summary['total_games']) * 100
        self.assertEqual(summary['win_rate'], expected_win_rate)
    
    def test_large_dataset_performance(self):
        """大量データでのパフォーマンステスト"""
        # 1000ゲームのデータを生成
        large_records = []
        choices = [Choice.ROCK, Choice.PAPER, Choice.SCISSORS]
        results = [GameResult.WIN, GameResult.LOSE, GameResult.DRAW]
        
        for i in range(1000):
            record = GameRecord(
                choices[i % 3],
                choices[(i + 1) % 3],
                results[i % 3],
                f"2025-10-05 {i:02d}:00:00"
            )
            large_records.append(record)
        
        # データ追加
        for record in large_records:
            self.stats.add_game(record)
        
        # 統計計算（パフォーマンステスト）
        summary = self.stats.get_summary()
        frequency = self.stats.get_choice_frequency()
        
        # 基本的な正確性チェック
        self.assertEqual(summary['total_games'], 1000)
        self.assertEqual(len(self.stats.records), 1000)
        
        # 頻度の合計がゲーム数と一致することを確認
        total_choices = sum(frequency.values())
        self.assertEqual(total_choices, 1000)


if __name__ == '__main__':
    unittest.main()