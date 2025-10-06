"""
心理戦システムのテスト
"""

import os
from unittest.mock import MagicMock, patch

import pytest

from src.ai.player import AIPlayer, LLMAIPlayer
from src.game.engine import Choice


class ConcreteAIPlayer(AIPlayer):
    """テスト用の具象AIPlayerクラス"""

    def make_choice(self) -> Choice:
        return Choice.ROCK


@pytest.fixture
def concrete_ai_player():
    """ConcreteAIPlayerのフィクスチャ"""
    return ConcreteAIPlayer("TestAI")


def test_base_ai_psychological_message(concrete_ai_player):
    """基底AIクラスの心理戦メッセージテスト"""
    message = concrete_ai_player.get_psychological_message()
    assert message == "さあ、勝負だ！"


def test_llm_ai_psychological_message_success():
    """LLM AIの心理戦メッセージ成功テスト"""
    # OpenAI APIをモック
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "君の手は読めているよ"

    with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}):
        with patch("openai.OpenAI") as mock_openai:
            mock_client = MagicMock()
            mock_client.chat.completions.create.return_value = mock_response
            mock_openai.return_value = mock_client

            ai_player = LLMAIPlayer("TestLLM")
            message = ai_player.get_psychological_message()

        assert message == "君の手は読めているよ"


@patch("openai.OpenAI")
def test_llm_ai_psychological_message_api_error(mock_openai):
    """LLM AIの心理戦メッセージAPIエラー時テスト"""
    # OpenAI APIでエラーを発生させる
    mock_openai.side_effect = Exception("API Error")

    with patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"}):
        ai_player = LLMAIPlayer("TestLLM")

        # エラー時にはデフォルトメッセージが返される
        with patch("builtins.print"):  # デバッグメッセージをキャプチャ
            message = ai_player.get_psychological_message()
        # フォールバックメッセージのリストから一つが返される
        fallback_messages = [
            "勝負だ！",
            "本気を見せる時だ",
            "君の実力を見せてもらおう",
            "面白くなりそうだ",
            "負けないぞ！",
            "覚悟はできたか？",
            "手加減はしないぞ！",
        ]
        assert message in fallback_messages
