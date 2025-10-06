"""
ゲームエンジンの包括的テスト
"""

import pytest

from src.game.engine import Choice, GameResult, RockPaperScissorsEngine


@pytest.fixture
def game_engine():
    """ゲームエンジンのフィクスチャ"""
    return RockPaperScissorsEngine()


# Choice クラスのテスト
def test_choice_from_string_english():
    """英語入力からChoiceへの変換テスト"""
    assert Choice.from_string("rock") == Choice.ROCK
    assert Choice.from_string("paper") == Choice.PAPER
    assert Choice.from_string("scissors") == Choice.SCISSORS

    # 大文字小文字混在のテスト
    assert Choice.from_string("ROCK") == Choice.ROCK
    assert Choice.from_string("Rock") == Choice.ROCK


def test_choice_from_string_japanese():
    """日本語入力からChoiceへの変換テスト"""
    assert Choice.from_string("グー") == Choice.ROCK
    assert Choice.from_string("パー") == Choice.PAPER
    assert Choice.from_string("チョキ") == Choice.SCISSORS


def test_choice_from_string_invalid():
    """無効な入力のテスト"""
    assert Choice.from_string("invalid") is None
    assert Choice.from_string("") is None


def test_choice_to_display_japanese():
    """日本語表示のテスト"""
    assert Choice.ROCK.to_display("ja") == "グー ✊"
    assert Choice.PAPER.to_display("ja") == "パー ✋"
    assert Choice.SCISSORS.to_display("ja") == "チョキ ✌️"


def test_choice_to_display_english():
    """英語表示のテスト"""
    assert Choice.ROCK.to_display("en") == "Rock ✊"
    assert Choice.PAPER.to_display("en") == "Paper ✋"
    assert Choice.SCISSORS.to_display("en") == "Scissors ✌️"


def test_choice_to_display_default():
    """デフォルト言語（日本語）表示のテスト"""
    assert Choice.ROCK.to_display() == "グー ✊"
    assert Choice.PAPER.to_display() == "パー ✋"
    assert Choice.SCISSORS.to_display() == "チョキ ✌️"


# RockPaperScissorsEngine クラスのテスト
def test_validate_choice_all_valid(game_engine):
    """すべての有効な入力のテスト"""
    valid_choices = ["rock", "paper", "scissors", "グー", "パー", "チョキ"]
    for choice in valid_choices:
        assert game_engine.validate_choice(choice) is True


def test_validate_choice_all_invalid(game_engine):
    """すべての無効な入力のテスト"""
    invalid_inputs = ["invalid", "123", ""]
    for invalid in invalid_inputs:
        assert game_engine.validate_choice(invalid) is False


def test_determine_winner_all_wins(game_engine):
    """すべてのプレイヤー勝利パターンのテスト"""
    win_combinations = [
        (Choice.ROCK, Choice.SCISSORS),
        (Choice.PAPER, Choice.ROCK),
        (Choice.SCISSORS, Choice.PAPER),
    ]

    for player_choice, ai_choice in win_combinations:
        result = game_engine.determine_winner(player_choice, ai_choice)
        assert result == GameResult.WIN


def test_determine_winner_all_losses(game_engine):
    """すべてのプレイヤー敗北パターンのテスト"""
    loss_combinations = [
        (Choice.SCISSORS, Choice.ROCK),
        (Choice.ROCK, Choice.PAPER),
        (Choice.PAPER, Choice.SCISSORS),
    ]

    for player_choice, ai_choice in loss_combinations:
        result = game_engine.determine_winner(player_choice, ai_choice)
        assert result == GameResult.LOSE


def test_determine_winner_all_draws(game_engine):
    """すべての引き分けパターンのテスト"""
    draw_combinations = [
        (Choice.ROCK, Choice.ROCK),
        (Choice.PAPER, Choice.PAPER),
        (Choice.SCISSORS, Choice.SCISSORS),
    ]

    for player_choice, ai_choice in draw_combinations:
        result = game_engine.determine_winner(player_choice, ai_choice)
        assert result == GameResult.DRAW
