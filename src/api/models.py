"""
API用データモデル - Pydanticモデルでリクエスト/レスポンスを定義
"""
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field


class ChoiceType(str, Enum):
    """選択肢の種類"""
    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"


class GameResultType(str, Enum):
    """ゲーム結果の種類"""
    WIN = "win"
    LOSE = "lose"
    DRAW = "draw"


class PlayGameRequest(BaseModel):
    """ゲーム実行リクエスト"""
    player_choice: ChoiceType = Field(..., description="プレイヤーの選択")
    ai_model: Optional[str] = Field("gpt-3.5-turbo", description="使用するAIモデル")
    language: Optional[str] = Field("ja", description="言語設定 (ja/en)")


class GameHistoryItem(BaseModel):
    """ゲーム履歴アイテム"""
    player_choice: ChoiceType
    ai_choice: ChoiceType
    result: GameResultType


class PlayGameResponse(BaseModel):
    """ゲーム実行レスポンス"""
    player_choice: ChoiceType = Field(..., description="プレイヤーの選択")
    ai_choice: ChoiceType = Field(..., description="AIの選択")
    result: GameResultType = Field(..., description="ゲーム結果")
    psychological_message: Optional[str] = Field(None, description="AIの心理戦メッセージ")
    game_id: str = Field(..., description="ゲームID")


class GameStatsResponse(BaseModel):
    """ゲーム統計レスポンス"""
    total_games: int = Field(..., description="総ゲーム数")
    wins: int = Field(..., description="プレイヤー勝利数")
    losses: int = Field(..., description="プレイヤー敗北数")
    draws: int = Field(..., description="引き分け数")
    win_rate: float = Field(..., description="勝率")


class GameHistoryResponse(BaseModel):
    """ゲーム履歴レスポンス"""
    game_id: str = Field(..., description="ゲームID")
    history: List[GameHistoryItem] = Field(..., description="ゲーム履歴")
    stats: GameStatsResponse = Field(..., description="統計情報")


class ErrorResponse(BaseModel):
    """エラーレスポンス"""
    error: str = Field(..., description="エラーメッセージ")
    detail: Optional[str] = Field(None, description="詳細情報")