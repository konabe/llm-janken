from enum import Enum
from typing import Optional


class Choice(Enum):
    """じゃんけんの手を表現する列挙型"""

    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"

    @classmethod
    def from_string(cls, choice: str) -> Optional["Choice"]:
        """文字列からChoiceを生成"""
        choice_map = {
            # 英語
            "rock": cls.ROCK,
            "paper": cls.PAPER,
            "scissors": cls.SCISSORS,
            # 日本語
            "グー": cls.ROCK,
            "パー": cls.PAPER,
            "チョキ": cls.SCISSORS,
        }
        return choice_map.get(choice.lower())

    def to_display(self, lang: str = "ja") -> str:
        """表示用文字列を生成"""
        if lang == "ja":
            display_map = {
                self.ROCK: "グー ✊",
                self.PAPER: "パー ✋",
                self.SCISSORS: "チョキ ✌️",
            }
        else:
            display_map = {
                self.ROCK: "Rock ✊",
                self.PAPER: "Paper ✋",
                self.SCISSORS: "Scissors ✌️",
            }
        return display_map[self]


class GameResult(Enum):
    """ゲーム結果を表現する列挙型"""

    WIN = "win"
    LOSE = "lose"
    DRAW = "draw"


class RockPaperScissorsEngine:
    """じゃんけんゲームエンジン"""

    @staticmethod
    def determine_winner(player_choice: Choice, ai_choice: Choice) -> GameResult:
        """勝敗を判定する"""
        if player_choice == ai_choice:
            return GameResult.DRAW

        winning_combinations = {
            (Choice.ROCK, Choice.SCISSORS),
            (Choice.PAPER, Choice.ROCK),
            (Choice.SCISSORS, Choice.PAPER),
        }

        if (player_choice, ai_choice) in winning_combinations:
            return GameResult.WIN
        else:
            return GameResult.LOSE

    @staticmethod
    def validate_choice(choice_str: str) -> bool:
        """入力された手が有効かチェック"""
        return Choice.from_string(choice_str) is not None
