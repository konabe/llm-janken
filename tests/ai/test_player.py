"""
AIプレイヤーの基底クラステスト（LLMAIPlayerのテストは別ファイル）
"""

from unittest.mock import MagicMock

import pytest

from src.ai.player import AIPlayer
from src.game.engine import Choice


class ConcreteAIPlayer(AIPlayer):
    """テスト用の具象AIPlayerクラス"""

    def make_choice(self) -> Choice:
        return Choice.ROCK


@pytest.fixture
def ai_player():
    """AIプレイヤーのフィクスチャ"""
    return ConcreteAIPlayer("TestAI")


def test_initialization(ai_player):
    """初期化のテスト"""
    assert ai_player.name == "TestAI"
    assert len(ai_player.game_history) == 0

def test_record_game(ai_player):
    """ゲーム履歴記録のテスト"""
    ai_player.record_game(Choice.ROCK, Choice.SCISSORS, "win")

    assert len(ai_player.game_history) == 1
    assert ai_player.game_history[0] == (Choice.ROCK, Choice.SCISSORS, "win")


def test_record_multiple_games(ai_player):
    """複数ゲーム履歴記録のテスト"""
    games = [
        (Choice.ROCK, Choice.SCISSORS, "win"),
        (Choice.PAPER, Choice.ROCK, "win"),
        (Choice.SCISSORS, Choice.SCISSORS, "draw"),
    ]

    for player_choice, ai_choice, result in games:
        ai_player.record_game(player_choice, ai_choice, result)

    assert len(ai_player.game_history) == 3
    for i, expected in enumerate(games):
        assert ai_player.game_history[i] == expected


def test_make_choice_abstract(ai_player):
    """make_choiceメソッドの実装テスト"""
    choice = ai_player.make_choice()
    assert isinstance(choice, Choice)


def test_default_psychological_message(ai_player):
    """デフォルト心理戦メッセージのテスト"""
    message = ai_player.get_psychological_message()
    assert message == "さあ、勝負だ！"
