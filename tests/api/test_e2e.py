"""
API E2E（End-to-End）統合テスト
実際のAPIサーバーを起動してHTTPリクエストをテスト
"""
import pytest
import httpx
import asyncio
import uvicorn
import threading
import time
import os
from typing import AsyncGenerator


class APITestServer:
    """テスト用APIサーバー管理"""
    
    def __init__(self, host="127.0.0.1", port=8001):
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"
        self.server = None
        self.server_thread = None
    
    def start(self):
        """APIサーバーを起動"""
        def run_server():
            # テスト用の設定でサーバーを起動
            config = uvicorn.Config(
                "src.api.app:app",
                host=self.host,
                port=self.port,
                log_level="error"  # ログレベルを下げてノイズを削減
            )
            self.server = uvicorn.Server(config)
            asyncio.run(self.server.serve())
        
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
        
        # サーバー起動を待機
        for _ in range(50):  # 最大5秒待機
            try:
                response = httpx.get(f"{self.base_url}/health", timeout=1.0)
                if response.status_code == 200:
                    break
            except Exception:
                pass
            time.sleep(0.1)
        else:
            raise RuntimeError("テストサーバーの起動に失敗しました")
    
    def stop(self):
        """APIサーバーを停止"""
        if self.server:
            self.server.should_exit = True


@pytest.fixture(scope="session")
def test_server():
    """テストサーバーのセッションスコープフィクスチャ"""
    server = APITestServer()
    server.start()
    yield server
    server.stop()


@pytest.fixture
def api_client(test_server: APITestServer):
    """HTTPクライアントのフィクスチャ"""
    return httpx.Client(base_url=test_server.base_url, timeout=10.0)


def test_api_health_check(api_client: httpx.Client):
    """ヘルスチェックE2Eテスト"""
    response = api_client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "正常に動作" in data["message"]


def test_api_root_endpoint(api_client: httpx.Client):
    """ルートエンドポイントE2Eテスト"""
    response = api_client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert "じゃんけん API" in data["message"]
    assert data["docs"] == "/docs"
    assert data["redoc"] == "/redoc"


def test_complete_game_flow_e2e(api_client: httpx.Client):
    """完全なゲームフローE2Eテスト"""
    
    # 1. ゲームセッション開始
    start_response = api_client.post("/game/start")
    assert start_response.status_code == 200
    start_data = start_response.json()
    assert "game_id" in start_data
    game_id = start_data["game_id"]
    
    # 2. 複数回のゲーム実行
    game_results = []
    for player_choice in ["rock", "paper", "scissors"]:
        play_data = {
            "player_choice": player_choice,
            "ai_model": "gpt-4o-mini",
            "language": "ja"
        }
        
        play_response = api_client.post(f"/game/{game_id}/play", json=play_data)
        assert play_response.status_code == 200
        
        result_data = play_response.json()
        assert result_data["game_id"] == game_id
        assert result_data["player_choice"] == player_choice
        assert result_data["ai_choice"] in ["rock", "paper", "scissors"]
        assert result_data["result"] in ["win", "lose", "draw"]
        assert "psychological_message" in result_data
        
        game_results.append(result_data)
    
    # 3. ゲーム履歴取得
    history_response = api_client.get(f"/game/{game_id}/history")
    assert history_response.status_code == 200
    
    history_data = history_response.json()
    assert history_data["game_id"] == game_id
    assert len(history_data["history"]) == 3
    
    # 統計の検証
    stats = history_data["stats"]
    assert stats["total_games"] == 3
    assert stats["wins"] + stats["losses"] + stats["draws"] == 3
    assert 0.0 <= stats["win_rate"] <= 1.0


def test_multiple_sessions_e2e(api_client: httpx.Client):
    """複数セッション管理E2Eテスト"""
    
    # 複数のゲームセッションを作成
    sessions = []
    for i in range(2):  # 簡略化のため2つに削減
        response = api_client.post("/game/start")
        assert response.status_code == 200
        game_id = response.json()["game_id"]
        sessions.append(game_id)
    
    # 各セッションで異なるゲームを実行
    for i, game_id in enumerate(sessions):
        choices = ["rock", "paper"]
        play_data = {
            "player_choice": choices[i],
            "ai_model": "gpt-4o-mini",
            "language": "ja"
        }
        
        response = api_client.post(f"/game/{game_id}/play", json=play_data)
        assert response.status_code == 200
        
        result = response.json()
        assert result["game_id"] == game_id
        assert result["player_choice"] == choices[i]
    
    # 各セッションの履歴を確認
    for game_id in sessions:
        response = api_client.get(f"/game/{game_id}/history")
        assert response.status_code == 200
        
        data = response.json()
        assert data["game_id"] == game_id
        assert len(data["history"]) == 1


def test_invalid_requests_e2e(api_client: httpx.Client):
    """無効なリクエストのエラーハンドリングE2Eテスト"""
    
    # 存在しないセッションでゲーム実行
    invalid_play_data = {
        "player_choice": "rock",
        "ai_model": "gpt-4o-mini",
        "language": "ja"
    }
    
    response = api_client.post("/game/invalid-id/play", json=invalid_play_data)
    assert response.status_code == 404
    
    # 存在しないセッションで履歴取得
    response = api_client.get("/game/invalid-id/history")
    assert response.status_code == 404
    
    # 無効な選択肢バリデーション: セッション作成
    start_response = api_client.post("/game/start")
    game_id = start_response.json()["game_id"]
    
    invalid_choice_data = {
        "player_choice": "invalid_choice",
        "ai_model": "gpt-4o-mini",
        "language": "ja"
    }
    
    response = api_client.post(f"/game/{game_id}/play", json=invalid_choice_data)
    assert response.status_code == 422  # バリデーションエラー


def test_language_and_model_variations_e2e(api_client: httpx.Client):
    """多言語・モデルバリエーションE2Eテスト"""
    
    # ゲームセッション開始
    response = api_client.post("/game/start")
    game_id = response.json()["game_id"]
    
    # 日本語でゲーム実行
    ja_data = {
        "player_choice": "rock",
        "ai_model": "gpt-4o-mini",
        "language": "ja"
    }
    
    response = api_client.post(f"/game/{game_id}/play", json=ja_data)
    assert response.status_code == 200
    
    # 英語でゲーム実行
    en_data = {
        "player_choice": "paper",
        "ai_model": "gpt-3.5-turbo",
        "language": "en"
    }
    
    response = api_client.post(f"/game/{game_id}/play", json=en_data)
    assert response.status_code == 200
    
    # 履歴確認
    response = api_client.get(f"/game/{game_id}/history")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data["history"]) == 2
    assert data["stats"]["total_games"] == 2