"""
API サービス層のテスト
"""
import pytest
from unittest.mock import Mock, patch

from src.api.service import GameService, GameSession
from src.api.models import PlayGameRequest, ChoiceType, GameResultType
from src.game.engine import Choice, GameResult


@pytest.fixture
def game_service():
    """ゲームサービスのフィクスチャ"""
    return GameService()


@pytest.fixture
def game_session():
    """ゲームセッションのフィクスチャ"""
    return GameSession("test-game-id")


def test_create_session(game_service):
    """ゲームセッション作成テスト"""
    game_id = game_service.create_session()
    
    # ゲームIDが生成されること
    assert isinstance(game_id, str)
    assert len(game_id) > 0
    
    # セッションが保存されること
    session = game_service.get_session(game_id)
    assert session is not None
    assert session.game_id == game_id


def test_get_session_not_found(game_service):
    """存在しないセッション取得テスト"""
    session = game_service.get_session("non-existent-id")
    assert session is None


def test_game_session_add_game(game_session):
    """ゲームセッションに履歴追加テスト"""
    # ゲーム結果を追加
    game_session.add_game(Choice.ROCK, Choice.SCISSORS, GameResult.WIN)
    
    # 履歴が追加されること
    assert len(game_session.history) == 1
    history_item = game_session.history[0]
    assert history_item.player_choice == ChoiceType.ROCK
    assert history_item.ai_choice == ChoiceType.SCISSORS
    assert history_item.result == GameResultType.WIN


def test_game_session_stats_empty(game_session):
    """空のゲームセッション統計テスト"""
    stats = game_session.get_stats()
    
    assert stats.total_games == 0
    assert stats.wins == 0
    assert stats.losses == 0
    assert stats.draws == 0
    assert abs(stats.win_rate - 0.0) < 0.001


def test_game_session_stats_with_games(game_session):
    """ゲーム履歴ありセッション統計テスト"""
    # 複数のゲーム結果を追加
    game_session.add_game(Choice.ROCK, Choice.SCISSORS, GameResult.WIN)    # 勝ち
    game_session.add_game(Choice.PAPER, Choice.ROCK, GameResult.WIN)        # 勝ち
    game_session.add_game(Choice.SCISSORS, Choice.PAPER, GameResult.WIN)    # 勝ち
    game_session.add_game(Choice.ROCK, Choice.PAPER, GameResult.LOSE)       # 負け
    game_session.add_game(Choice.ROCK, Choice.ROCK, GameResult.DRAW)        # 引き分け
    
    stats = game_session.get_stats()
    
    assert stats.total_games == 5
    assert stats.wins == 3
    assert stats.losses == 1
    assert stats.draws == 1
    assert abs(stats.win_rate - 0.6) < 0.001


@patch('src.api.service.LLMAIPlayer')
def test_play_game_success(mock_llm_player, game_service):
    """ゲーム実行成功テスト"""
    # ゲームセッション作成
    game_id = game_service.create_session()
    
    # LLMAIPlayerのモック設定
    mock_ai_instance = Mock()
    mock_ai_instance.make_choice.return_value = Choice.ROCK
    mock_ai_instance.get_psychological_message.return_value = "勝負だ！"
    mock_llm_player.return_value = mock_ai_instance
    
    # ゲーム実行リクエスト作成
    request = PlayGameRequest(
        player_choice=ChoiceType.PAPER,
        ai_model="gpt-4o-mini",
        language="ja"
    )
    
    # ゲーム実行
    response = game_service.play_game(request, game_id)
    
    # レスポンスの検証
    assert response.game_id == game_id
    assert response.player_choice == ChoiceType.PAPER
    assert response.ai_choice == ChoiceType.ROCK
    assert response.result == GameResultType.WIN  # Paper beats Rock
    assert response.psychological_message == "勝負だ！"
    
    # セッション履歴の検証
    session = game_service.get_session(game_id)
    assert len(session.history) == 1


def test_play_game_invalid_session(game_service):
    """無効なセッションでのゲーム実行テスト"""
    request = PlayGameRequest(
        player_choice=ChoiceType.ROCK,
        ai_model="gpt-4o-mini",
        language="ja"
    )
    
    with pytest.raises(ValueError, match="ゲームセッション.*が見つかりません"):
        game_service.play_game(request, "invalid-game-id")


def test_get_game_history_success(game_service):
    """ゲーム履歴取得成功テスト"""
    # ゲームセッション作成と履歴追加
    game_id = game_service.create_session()
    session = game_service.get_session(game_id)
    session.add_game(Choice.ROCK, Choice.SCISSORS, GameResult.WIN)
    
    # 履歴取得
    history_response = game_service.get_game_history(game_id)
    
    # レスポンスの検証
    assert history_response.game_id == game_id
    assert len(history_response.history) == 1
    assert history_response.stats.total_games == 1
    assert history_response.stats.wins == 1


def test_get_game_history_invalid_session(game_service):
    """無効なセッションでの履歴取得テスト"""
    with pytest.raises(ValueError, match="ゲームセッション.*が見つかりません"):
        game_service.get_game_history("invalid-game-id")