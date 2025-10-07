"""
APIサービス層 - ゲームロジックとAPIレスポンスを橋渡し
"""
import uuid
from typing import Dict, List, Optional
from datetime import datetime

from ..game.engine import Choice, GameResult, RockPaperScissorsEngine
from ..ai.player import LLMAIPlayer
from .models import (
    ChoiceType, GameResultType, PlayGameRequest, PlayGameResponse,
    GameStatsResponse, GameHistoryResponse, GameHistoryItem
)


class GameSession:
    """ゲームセッション管理"""
    
    def __init__(self, game_id: str):
        self.game_id = game_id
        self.history: List[GameHistoryItem] = []
        self.created_at = datetime.now()
    
    def add_game(self, player_choice: Choice, ai_choice: Choice, result: GameResult):
        """ゲーム結果を履歴に追加"""
        # Choice -> ChoiceType 変換
        choice_mapping = {
            Choice.ROCK: ChoiceType.ROCK,
            Choice.PAPER: ChoiceType.PAPER,
            Choice.SCISSORS: ChoiceType.SCISSORS
        }
        
        # GameResult -> GameResultType 変換
        result_mapping = {
            GameResult.WIN: GameResultType.WIN,
            GameResult.LOSE: GameResultType.LOSE,
            GameResult.DRAW: GameResultType.DRAW
        }
        
        game_item = GameHistoryItem(
            player_choice=choice_mapping[player_choice],
            ai_choice=choice_mapping[ai_choice],
            result=result_mapping[result]
        )
        
        self.history.append(game_item)
    
    def get_stats(self) -> GameStatsResponse:
        """統計情報を取得"""
        total_games = len(self.history)
        if total_games == 0:
            return GameStatsResponse(
                total_games=0, wins=0, losses=0, draws=0, win_rate=0.0
            )
        
        wins = sum(1 for item in self.history if item.result == GameResultType.WIN)
        losses = sum(1 for item in self.history if item.result == GameResultType.LOSE)
        draws = sum(1 for item in self.history if item.result == GameResultType.DRAW)
        win_rate = wins / total_games if total_games > 0 else 0.0
        
        return GameStatsResponse(
            total_games=total_games,
            wins=wins,
            losses=losses,
            draws=draws,
            win_rate=round(win_rate, 3)
        )


class GameService:
    """ゲームサービス - APIのビジネスロジック"""
    
    def __init__(self):
        self.sessions: Dict[str, GameSession] = {}
        self.engine = RockPaperScissorsEngine()
    
    def create_session(self) -> str:
        """新しいゲームセッションを作成"""
        game_id = str(uuid.uuid4())
        self.sessions[game_id] = GameSession(game_id)
        return game_id
    
    def get_session(self, game_id: str) -> Optional[GameSession]:
        """ゲームセッションを取得"""
        return self.sessions.get(game_id)
    
    def play_game(self, request: PlayGameRequest, game_id: str) -> PlayGameResponse:
        """ゲームを実行"""
        # セッション取得
        session = self.get_session(game_id)
        if not session:
            raise ValueError(f"ゲームセッション '{game_id}' が見つかりません")
        
        # プレイヤーの選択を変換
        choice_mapping = {
            ChoiceType.ROCK: Choice.ROCK,
            ChoiceType.PAPER: Choice.PAPER,
            ChoiceType.SCISSORS: Choice.SCISSORS
        }
        player_choice = choice_mapping[request.player_choice]
        
        # AI プレイヤーを作成
        ai_player = LLMAIPlayer(request.ai_model or "gpt-3.5-turbo")
        
        # 履歴をAIプレイヤーに設定
        for game_item in session.history:
            # GameResultTypeを文字列に変換
            result_str = game_item.result.value  # "win", "lose", "draw"
            ai_player.record_game(
                choice_mapping[game_item.player_choice],
                choice_mapping[game_item.ai_choice],
                result_str
            )
        
        # AI の選択と心理戦メッセージを取得
        ai_choice = ai_player.make_choice()
        psychological_message = ai_player.get_psychological_message()
        
        # 勝敗判定
        result = self.engine.determine_winner(player_choice, ai_choice)
        
        # セッションに記録
        session.add_game(player_choice, ai_choice, result)
        
        # Choice -> ChoiceType の逆変換マッピング
        reverse_choice_mapping = {
            Choice.ROCK: ChoiceType.ROCK,
            Choice.PAPER: ChoiceType.PAPER,
            Choice.SCISSORS: ChoiceType.SCISSORS
        }
        
        # GameResult -> GameResultType 変換
        if result == GameResult.WIN:
            result_type = GameResultType.WIN
        elif result == GameResult.LOSE:
            result_type = GameResultType.LOSE
        else:
            result_type = GameResultType.DRAW
        
        # レスポンス作成
        return PlayGameResponse(
            player_choice=request.player_choice,
            ai_choice=reverse_choice_mapping[ai_choice],
            result=result_type,
            psychological_message=psychological_message,
            game_id=game_id
        )
    
    def get_game_history(self, game_id: str) -> GameHistoryResponse:
        """ゲーム履歴を取得"""
        session = self.get_session(game_id)
        if not session:
            raise ValueError(f"ゲームセッション '{game_id}' が見つかりません")
        
        return GameHistoryResponse(
            game_id=game_id,
            history=session.history,
            stats=session.get_stats()
        )