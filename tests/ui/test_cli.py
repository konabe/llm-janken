"""
CLIインターフェースの包括的テスト
"""

from io import StringIO
from unittest.mock import patch

import pytest

from src.ai.player import LLMAIPlayer
from src.game.engine import Choice, GameResult
from src.ui.cli import CLIInterface


@pytest.fixture
def cli_ja():
    """日本語CLIインターフェースのフィクスチャ"""
    return CLIInterface(language="ja")


@pytest.fixture
def cli_en():
    """英語CLIインターフェースのフィクスチャ"""
    return CLIInterface(language="en")


def test_initialization_japanese(cli_ja):
    """日本語CLIの初期化テスト"""
    assert cli_ja.language == "ja"
    assert "welcome" in cli_ja.messages
    assert cli_ja.messages["welcome"] == "🎮 LLM じゃんけんゲームへようこそ！"


def test_initialization_english(cli_en):
    """英語CLIの初期化テスト"""
    assert cli_en.language == "en"
    assert "welcome" in cli_en.messages
    assert cli_en.messages["welcome"] == "🎮 Welcome to LLM Rock-Paper-Scissors!"


def test_load_messages_japanese(cli_ja):
    """日本語メッセージ読み込みテスト"""
    assert "game_end" in cli_ja.messages
    assert "invalid_input" in cli_ja.messages
    assert "win" in cli_ja.messages


def test_load_messages_english(cli_en):
    """英語メッセージ読み込みテスト"""
    assert "game_end" in cli_en.messages
    assert "invalid_input" in cli_en.messages
    assert "win" in cli_en.messages


def test_display_welcome(cli_ja):
    """ウェルカムメッセージ表示テスト"""
    with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        cli_ja.display_welcome()
        output = mock_stdout.getvalue()
        assert "🎮 LLM じゃんけんゲームへようこそ！" in output


def test_display_goodbye(cli_ja):
    """終了メッセージ表示テスト"""
    with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        cli_ja.display_goodbye()
        output = mock_stdout.getvalue()
        assert "ありがとうございました" in output


def test_display_result_win(cli_ja):
    """勝利結果表示テスト"""
    with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        cli_ja.display_result(Choice.ROCK, Choice.SCISSORS, GameResult.WIN)
        output = mock_stdout.getvalue()
        assert "あなたの勝ち" in output


def test_display_result_lose(cli_ja):
    """敗北結果表示テスト"""
    with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        cli_ja.display_result(Choice.SCISSORS, Choice.ROCK, GameResult.LOSE)
        output = mock_stdout.getvalue()
        assert "AI の勝ち" in output


def test_display_result_draw(cli_ja):
    """引き分け結果表示テスト"""
    with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        cli_ja.display_result(Choice.ROCK, Choice.ROCK, GameResult.DRAW)
        output = mock_stdout.getvalue()
        assert "引き分け" in output


def test_display_result_english(cli_en):
    """英語での結果表示テスト"""
    with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        cli_en.display_result(Choice.ROCK, Choice.SCISSORS, GameResult.WIN)
        output = mock_stdout.getvalue()
        assert "You win!" in output


def test_get_player_choice_valid_japanese(cli_ja):
    """有効な日本語入力のテスト"""
    with patch('builtins.input', return_value='グー'):
        choice = cli_ja.get_player_choice()
        assert choice == Choice.ROCK


def test_get_player_choice_valid_english(cli_ja):
    """有効な英語入力のテスト"""
    with patch('builtins.input', return_value='rock'):
        choice = cli_ja.get_player_choice()
        assert choice == Choice.ROCK


def test_get_player_choice_quit(cli_ja):
    """終了入力のテスト"""
    with patch('builtins.input', return_value='quit'):
        choice = cli_ja.get_player_choice()
        assert choice is None


def test_get_player_choice_invalid_then_valid(cli_ja):
    """無効入力後に有効入力のテスト"""
    with patch('builtins.input', side_effect=['invalid', 'rock']):
        with patch('sys.stdout', new_callable=StringIO):
            choice = cli_ja.get_player_choice()
            assert choice == Choice.ROCK


def test_run_single_game_normal(cli_ja):
    """通常ゲーム実行のテスト"""
    with patch.object(cli_ja, 'get_player_choice', return_value=Choice.ROCK):
        with patch('src.ai.player.LLMAIPlayer') as mock_player_class:
            mock_ai_player = mock_player_class.return_value
            mock_ai_player.make_choice.return_value = Choice.SCISSORS
            mock_ai_player.get_psychological_message.return_value = "テストメッセージ"

            with patch('sys.stdout', new_callable=StringIO):
                cli_ja.run_single_game(mock_ai_player)
                # 実行されることを確認
                mock_ai_player.make_choice.assert_called_once()


def test_run_single_game_quit(cli_ja):
    """終了選択時のゲーム実行テスト"""
    with patch.object(cli_ja, 'get_player_choice', return_value=None):
        with patch('src.ai.player.LLMAIPlayer') as mock_player_class:
            mock_ai_player = mock_player_class.return_value

            result = cli_ja.run_single_game(mock_ai_player)
            assert result is None
