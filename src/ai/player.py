"""
AIプレイヤーの基底クラスと基本実装
"""

import os
import random
from abc import ABC, abstractmethod
from typing import List, Optional
from ..game.engine import Choice

class AIPlayer(ABC):
    """AIプレイヤーの基底クラス"""
    
    def __init__(self, name: str):
        self.name = name
        self.game_history: List[tuple] = []
    
    @abstractmethod
    def make_choice(self) -> Choice:
        """AIの手を決定する（サブクラスで実装）"""
        pass
    
    def record_game(self, player_choice: Choice, ai_choice: Choice, result: str):
        """ゲーム履歴を記録"""
        self.game_history.append((player_choice, ai_choice, result))

class RandomAIPlayer(AIPlayer):
    """ランダムに手を選ぶAIプレイヤー"""
    
    def make_choice(self) -> Choice:
        """ランダムに手を選択"""
        return random.choice(list(Choice))

class PatternAIPlayer(AIPlayer):
    """プレイヤーのパターンを学習するAIプレイヤー（将来実装）"""
    
    def make_choice(self) -> Choice:
        """現在は基本的なパターン分析（プレースホルダー）"""
        if len(self.game_history) < 3:
            return random.choice(list(Choice))
        
        # 簡単なパターン分析: 最後の手の対策を出す
        last_player_choice = self.game_history[-1][0]
        counter_choices = {
            Choice.ROCK: Choice.PAPER,
            Choice.PAPER: Choice.SCISSORS, 
            Choice.SCISSORS: Choice.ROCK
        }
        
        # 70%の確率で対策、30%でランダム
        if random.random() < 0.7:
            return counter_choices[last_player_choice]
        else:
            return random.choice(list(Choice))


class LLMAIPlayer(AIPlayer):
    """OpenAI APIを使用してじゃんけんの手を決定するAIプレイヤー"""
    
    def __init__(self, name: str):
        super().__init__(name)
        # OpenAI クライアントは遅延初期化
        self._client = None
        self.max_history = 5  # 履歴の最大保持数
        # 環境変数からモデル名を取得（デフォルトは安価なgpt-4o-mini）
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    def _build_prompt(self) -> str:
        """LLM用のプロンプトを構築"""
        base_prompt = """
あなたはじゃんけんプレイヤーです。次に出す手を決めてください。

選択肢は以下の通りです：
- rock (グー)
- paper (パー) 
- scissors (チョキ)

"""
        
        # ゲーム履歴がある場合は追加
        if self.game_history:
            history_text = "\n過去のゲーム履歴:\n"
            # 最新の履歴のみを使用
            recent_history = self.game_history[-self.max_history:]
            for i, (player_choice, ai_choice, result) in enumerate(recent_history, 1):
                history_text += f"{i}. プレイヤー: {player_choice.name.lower()}, あなた: {ai_choice.name.lower()}, 結果: {result}\n"
            base_prompt += history_text + "\n"
        
        base_prompt += """
この情報を踏まえて、次に出すべき手を「rock」「paper」「scissors」のいずれかで回答してください。
他の文字や説明は不要で、単語のみを回答してください。
"""
        
        return base_prompt
    
    @property
    def client(self):
        """OpenAI クライアントを遅延初期化"""
        if self._client is None:
            try:
                from openai import OpenAI
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    raise ValueError("OPENAI_API_KEY が設定されていません。")
                self._client = OpenAI(api_key=api_key)
            except ImportError:
                raise ImportError("openai パッケージがインストールされていません。'pip install openai' を実行してください。")
        return self._client
    
    def make_choice(self) -> Choice:
        """OpenAI APIを使用して手を決定"""
        try:
            prompt = self._build_prompt()
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "あなたはじゃんけんの専門家です。与えられた指示に従って、適切な手を選択してください。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=10,
                temperature=0.7
            )
            
            # レスポンスから選択肢を抽出
            choice_text = response.choices[0].message.content.strip().lower()
            
            # 文字列からChoiceに変換
            if "rock" in choice_text or "グー" in choice_text:
                return Choice.ROCK
            elif "paper" in choice_text or "パー" in choice_text:
                return Choice.PAPER
            elif "scissors" in choice_text or "チョキ" in choice_text:
                return Choice.SCISSORS
            else:
                # 無効なレスポンスの場合はランダムにフォールバック
                print(f"警告: AIの応答が無効でした: '{choice_text}'. ランダムに選択します。")
                return random.choice(list(Choice))
                
        except Exception as e:
            print(f"警告: OpenAI API エラー: {e}. ランダムに選択します。")
            return random.choice(list(Choice))