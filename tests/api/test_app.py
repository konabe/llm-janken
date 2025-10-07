"""
FastAPI アプリケーションのテスト
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock

from src.api.app import app


@pytest.fixture
def client():
    """テストクライアントのフィクスチャ"""
    return TestClient(app)


def test_root_endpoint(client):
    """ルートエンドポイントテスト"""
    response = client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "じゃんけん API" in data["message"]


def test_health_check(client):
    """ヘルスチェックエンドポイントテスト"""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_start_game(client):
    """ゲーム開始エンドポイントテスト"""
    response = client.post("/game/start")
    
    assert response.status_code == 200
    data = response.json()
    assert "game_id" in data
    assert "message" in data
    assert len(data["game_id"]) > 0


@patch('src.api.app.game_service')
def test_play_game_success(mock_service, client):
    """ゲーム実行エンドポイント成功テスト"""
    # モックレスポンス設定
    from src.api.models import PlayGameResponse, ChoiceType, GameResultType
    
    mock_response = PlayGameResponse(
        player_choice=ChoiceType.ROCK,
        ai_choice=ChoiceType.SCISSORS,
        result=GameResultType.WIN,
        psychological_message="勝負だ！",
        game_id="test-game-id"
    )
    mock_service.play_game.return_value = mock_response
    
    # リクエスト実行
    request_data = {
        "player_choice": "rock",
        "ai_model": "gpt-4o-mini",
        "language": "ja"
    }
    
    response = client.post("/game/test-game-id/play", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["player_choice"] == "rock"
    assert data["ai_choice"] == "scissors"
    assert data["result"] == "win"
    assert data["game_id"] == "test-game-id"


def test_play_game_invalid_session(client):
    """無効なセッションでのゲーム実行テスト"""
    request_data = {
        "player_choice": "rock",
        "ai_model": "gpt-4o-mini",
        "language": "ja"
    }
    
    response = client.post("/game/invalid-id/play", json=request_data)
    
    assert response.status_code == 404


@patch('src.api.app.game_service')
def test_get_game_history_success(mock_service, client):
    """ゲーム履歴エンドポイント成功テスト"""
    # モックレスポンス設定
    from src.api.models import GameHistoryResponse, GameStatsResponse
    
    mock_stats = GameStatsResponse(
        total_games=1,
        wins=1,
        losses=0,
        draws=0,
        win_rate=1.0
    )
    
    mock_response = GameHistoryResponse(
        game_id="test-game-id",
        history=[],
        stats=mock_stats
    )
    mock_service.get_game_history.return_value = mock_response
    
    # リクエスト実行
    response = client.get("/game/test-game-id/history")
    
    assert response.status_code == 200
    data = response.json()
    assert data["game_id"] == "test-game-id"
    assert "stats" in data


def test_get_game_history_invalid_session(client):
    """無効なセッションでの履歴取得テスト"""
    response = client.get("/game/invalid-id/history")
    
    assert response.status_code == 404


def test_invalid_choice_validation(client):
    """無効な選択肢のバリデーションテスト"""
    request_data = {
        "player_choice": "invalid_choice",
        "ai_model": "gpt-4o-mini",
        "language": "ja"
    }
    
    response = client.post("/game/test-id/play", json=request_data)
    
    assert response.status_code == 422  # バリデーションエラー