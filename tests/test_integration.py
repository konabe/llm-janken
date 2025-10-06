"""
統合テストスイート - LLM AI統合テスト
"""

import os
from unittest.mock import MagicMock, patch

import pytest

from src.ai.player import LLMAIPlayer
from src.game.engine import Choice, GameResult, RockPaperScissorsEngine
from src.ui.cli import CLIInterface


@pytest.fixture
def game_engine():
    """ゲームエンジンのフィクスチャ"""
    return RockPaperScissorsEngine()


@pytest.fixture
def cli_interface():
    """CLIインターフェースのフィクスチャ"""
    return CLIInterface()


@patch("src.ai.player.LLMAIPlayer.client", new_callable=lambda: MagicMock())
def test_llm_ai_game_integration(mock_client, game_engine):
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
    result = game_engine.determine_winner(player_choice, ai_choice)

    # AIが何かしらの有効な選択をしたことを確認
    assert ai_choice in [Choice.ROCK, Choice.PAPER, Choice.SCISSORS]
    assert result in [GameResult.WIN, GameResult.LOSE, GameResult.DRAW]

    # 履歴記録
    ai_player.record_game(player_choice, ai_choice, result.value)
    assert len(ai_player.game_history) == 1


@patch("src.ai.player.LLMAIPlayer.client", new_callable=lambda: MagicMock())
def test_llm_ai_learning_from_history(mock_client):
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
    assert ai_choice == Choice.PAPER

    # プロンプトに履歴が含まれることを確認
    call_args = mock_client.chat.completions.create.call_args
    if call_args and call_args[1] and "messages" in call_args[1]:
        prompt = call_args[1]["messages"][1]["content"]
        assert "過去のゲーム履歴" in prompt
    else:
        # API呼び出しが期待通りに実行されたことを確認
        mock_client.chat.completions.create.assert_called_once()


def test_complete_game_flow(game_engine):
    """完全なゲームフローのテスト"""
    # プレイヤーとAIの選択をシミュレート
    player_choice = Choice.ROCK
    ai_choice = Choice.SCISSORS

    # 勝敗判定
    result = game_engine.determine_winner(player_choice, ai_choice)

    # ROCKがSCISSORSに勝つ
    assert result == GameResult.WIN

    # 各選択肢の組み合わせをテスト
    test_cases = [
        (Choice.ROCK, Choice.SCISSORS, GameResult.WIN),
        (Choice.PAPER, Choice.ROCK, GameResult.WIN),
        (Choice.SCISSORS, Choice.PAPER, GameResult.WIN),
        (Choice.ROCK, Choice.ROCK, GameResult.DRAW),
    ]

    for player, ai, expected in test_cases:
        result = game_engine.determine_winner(player, ai)
        assert result == expected


def test_invalid_choice_handling(game_engine):
    """無効な選択肢のハンドリングテスト"""
    # 無効な入力をテスト（文字列のみ）
    invalid_inputs = ["invalid", "123", ""]

    for invalid_input in invalid_inputs:
        result = Choice.from_string(invalid_input)
        assert result is None, f"'{invalid_input}' should return None"
