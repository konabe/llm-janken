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
    
    def __init__(self, name: str, difficulty: str = "medium"):
        self.name = name
        self.difficulty = difficulty
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
    
    def __init__(self, name: str, personality: str = "balanced", difficulty: str = "medium"):
        super().__init__(name, difficulty)
        # OpenAI クライアントは遅延初期化
        self._client = None
        self.personality = personality
        self.max_history = 5  # 履歴の最大保持数
    
    def _build_prompt(self) -> str:
        """LLM用のプロンプトを構築"""
        # 性格設定
        personality_prompts = {
            "aggressive": "あなたは攻撃的で勝負強いじゃんけんプレイヤーです。相手を圧倒する戦略を好み、積極的に勝ちに行きます。",
            "defensive": "あなたは慎重で守備的なじゃんけんプレイヤーです。相手の動きを観察し、安定した戦略を取ります。",
            "random": "あなたは予測不可能で自由奔放なじゃんけんプレイヤーです。型にはまらない独創的な手を出します。",
            "balanced": "あなたはバランス感覚に優れたじゃんけんプレイヤーです。状況に応じて柔軟に戦略を変更します。",
            "analytical": "あなたは論理的で分析的なじゃんけんプレイヤーです。データとパターンを重視した戦略を立てます。"
        }
        
        base_prompt = f"""
{personality_prompts.get(self.personality, personality_prompts["balanced"])}

じゃんけんで次に出す手を決めてください。選択肢は以下の通りです：
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
                self._client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            except ImportError:
                raise ImportError("openai パッケージがインストールされていません。'pip install openai' を実行してください。")
        return self._client
    
    def make_choice(self) -> Choice:
        """OpenAI APIを使用して手を決定"""
        try:
            prompt = self._build_prompt()
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
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
                print(f"⚠️  AIの応答が無効でした: '{choice_text}'. ランダムに選択します。")
                return random.choice(list(Choice))
                
        except Exception as e:
            print(f"⚠️  OpenAI API エラー: {e}. ランダムに選択します。")
            return random.choice(list(Choice))