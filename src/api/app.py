"""
FastAPI アプリケーション - じゃんけんゲームのWeb API
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from .models import (
    PlayGameRequest, PlayGameResponse, GameHistoryResponse, ErrorResponse
)
from .service import GameService


# FastAPI アプリケーションの作成
app = FastAPI(
    title="LLM じゃんけん API",
    description="AI対戦相手と競う戦略的じゃんけんゲームのWeb API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切に設定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ゲームサービスのシングルトンインスタンス
game_service = GameService()


def get_game_service() -> GameService:
    """ゲームサービス依存性注入"""
    return game_service


@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {
        "message": "🚀 LLM じゃんけん API へようこそ！",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.post("/game/start", response_model=dict)
async def start_game(service: GameService = Depends(get_game_service)):
    """
    新しいゲームセッションを開始
    
    Returns:
        dict: ゲームIDを含むレスポンス
    """
    try:
        game_id = service.create_session()
        return {
            "game_id": game_id,
            "message": "🎮 新しいゲームセッションを開始しました！"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ゲーム開始エラー: {str(e)}")


@app.post("/game/{game_id}/play", response_model=PlayGameResponse)
async def play_game(
    game_id: str,
    request: PlayGameRequest,
    service: GameService = Depends(get_game_service)
):
    """
    じゃんけんゲームを実行
    
    Args:
        game_id: ゲームセッションID
        request: ゲーム実行リクエスト
        
    Returns:
        PlayGameResponse: ゲーム結果
    """
    try:
        result = service.play_game(request, game_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ゲーム実行エラー: {str(e)}")


@app.get("/game/{game_id}/history", response_model=GameHistoryResponse)
async def get_game_history(
    game_id: str,
    service: GameService = Depends(get_game_service)
):
    """
    ゲーム履歴と統計を取得
    
    Args:
        game_id: ゲームセッションID
        
    Returns:
        GameHistoryResponse: ゲーム履歴と統計
    """
    try:
        history = service.get_game_history(game_id)
        return history
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"履歴取得エラー: {str(e)}")


@app.get("/health")
async def health_check():
    """ヘルスチェックエンドポイント"""
    return {"status": "healthy", "message": "🟢 API は正常に動作しています"}


# エラーハンドラー
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """グローバル例外ハンドラー"""
    return ErrorResponse(
        error="内部サーバーエラー",
        detail=str(exc)
    )