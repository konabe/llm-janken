"""
LLMAIPlayer のテスト
"""

import os
from unittest.mock import MagicMock, patch

import pytest

from src.ai.player import LLMAIPlayer
from src.game.engine import Choice


@pytest.fixture
def llm_player():
    """LLMAIPlayerのフィクスチャ"""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        return LLMAIPlayer(name="テストAI")


def test_initialization(llm_player):
    """初期化のテスト"""
    assert llm_player.name == "テストAI"
    assert llm_player.max_history == 5
    assert len(llm_player.game_history) == 0
    # デフォルトモデルがgpt-4o-miniであることを確認
    assert llm_player.model == "gpt-4o-mini"


def test_custom_model():
    """カスタムモデル設定のテスト"""
    with patch.dict(
        os.environ, {"OPENAI_API_KEY": "test-key", "OPENAI_MODEL": "gpt-3.5-turbo"}
    ):
        custom_player = LLMAIPlayer(name="カスタムAI")
        assert custom_player.model == "gpt-3.5-turbo"


def test_build_prompt_no_history(llm_player):
    """履歴なしでのプロンプト構築テスト"""
    prompt = llm_player._build_prompt()
    assert "じゃんけんプレイヤー" in prompt
    assert "rock" in prompt
    assert "paper" in prompt
    assert "scissors" in prompt
    assert "過去のゲーム履歴" not in prompt


def test_build_prompt_with_history(llm_player):
    """履歴ありでのプロンプト構築テスト"""
    # テスト履歴を追加
    llm_player.record_game(Choice.ROCK, Choice.PAPER, "WIN")
    llm_player.record_game(Choice.SCISSORS, Choice.ROCK, "LOSE")

    prompt = llm_player._build_prompt()
    assert "過去のゲーム履歴" in prompt
    assert "rock" in prompt.lower()
    assert "paper" in prompt.lower()
    assert "scissors" in prompt.lower()


def test_make_choice_rock_response():
    """OpenAI APIがrockを返す場合のテスト"""
    # モックレスポンスを設定
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "rock"
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response

    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        player = LLMAIPlayer(name="テスト")
        player._client = mock_client
        choice = player.make_choice()
        assert choice == Choice.ROCK


def test_make_choice_paper_response():
    """OpenAI APIがpaperを返す場合のテスト"""
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "paper"
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response

    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        player = LLMAIPlayer(name="テスト")
        player._client = mock_client
        choice = player.make_choice()
        assert choice == Choice.PAPER


def test_make_choice_scissors_response():
    """OpenAI APIがscissorsを返す場合のテスト"""
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "scissors"
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response

    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        player = LLMAIPlayer(name="テスト")
        player._client = mock_client
        choice = player.make_choice()
        assert choice == Choice.SCISSORS


def test_make_choice_japanese_response():
    """OpenAI APIが日本語で返す場合のテスト"""
    test_cases = [
        ("グー", Choice.ROCK),
        ("パー", Choice.PAPER),
        ("チョキ", Choice.SCISSORS),
    ]

    for japanese_response, expected_choice in test_cases:
        mock_response = MagicMock()
        mock_response.choices[0].message.content = japanese_response
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response

        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            player = LLMAIPlayer(name="テスト")
            player._client = mock_client
            choice = player.make_choice()
            assert choice == expected_choice


def test_make_choice_invalid_response():
    """OpenAI APIが無効な応答を返す場合のテスト"""
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "invalid_choice"
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response

    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        player = LLMAIPlayer(name="テスト")
        player._client = mock_client
        choice = player.make_choice()
        # 無効な応答の場合、ランダムにフォールバック
        assert choice in [Choice.ROCK, Choice.PAPER, Choice.SCISSORS]


def test_make_choice_api_error():
    """OpenAI APIエラー時のテスト"""
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = Exception("API Error")

    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        player = LLMAIPlayer(name="テスト")
        player._client = mock_client
        choice = player.make_choice()
        # APIエラーの場合、ランダムにフォールバック
        assert choice in [Choice.ROCK, Choice.PAPER, Choice.SCISSORS]


def test_history_limit(llm_player):
    """履歴制限のテスト"""
    # 制限を超える履歴を追加
    for i in range(10):
        llm_player.record_game(Choice.ROCK, Choice.PAPER, f"game_{i}")

    # 最大履歴数を超えないことを確認
    prompt = llm_player._build_prompt()
    # 最新の5件のみ含まれることを確認
    assert llm_player.max_history == 5
    # プロンプト内で game_5以降の履歴が含まれることを確認
    assert "game_5" in prompt
    assert "game_0" not in prompt
