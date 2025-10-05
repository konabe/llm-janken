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
    
    def get_psychological_message(self) -> str:
        """心理戦メッセージを生成（サブクラスでオーバーライド可能）"""
        return "さあ、勝負だ！"
    
    def record_game(self, player_choice: Choice, ai_choice: Choice, result: str):
        """ゲーム履歴を記録"""
        self.game_history.append((player_choice, ai_choice, result))

class RandomAIPlayer(AIPlayer):
    """ランダムに手を選ぶAIプレイヤー"""
    
    def make_choice(self) -> Choice:
        """ランダムに手を選択"""
        return random.choice(list(Choice))
    
    def get_psychological_message(self) -> str:
        """心理戦メッセージをランダムに選択"""
        messages = [
            "運任せでいくぞ！",
            "予測不可能なのが私の強み！",
            "何が出るかな？お楽しみに！",
            "ランダムの力を見せてやる！",
            "読めるものなら読んでみろ！"
        ]
        return random.choice(messages)

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
    
    def get_psychological_message(self) -> str:
        """パターン分析に基づいた心理戦メッセージ"""
        if len(self.game_history) == 0:
            return "君のパターンを分析させてもらう..."
        elif len(self.game_history) < 3:
            return "データが集まってきた。面白い..."
        else:
            last_choice = self.game_history[-1][0]
            messages = {
                Choice.ROCK: "また同じ手を出すのかな？",
                Choice.PAPER: "パターンが読めてきたぞ！",
                Choice.SCISSORS: "次の手は予測済みだ！"
            }
            return messages.get(last_choice, "君の癖は見抜いた！")


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
    
    def get_psychological_message(self) -> str:
        """LLMを使って心理戦メッセージを生成"""
        try:
            # APIキーが設定されていない場合は事前チェック
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY が設定されていません。")
            
            # 心理戦メッセージ用プロンプト
            prompt = f"""
あなたは {self.name} というじゃんけんAIです。
これからじゃんけん勝負を始める前に、相手に心理的プレッシャーをかける短い一言を言ってください。

要求：
- 15文字以内の短いメッセージ
- 挑発的だが品位を保った内容
- じゃんけんに関連した内容

例：「君の手は読めているよ」「勝負の時間だ！」
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=50,
                temperature=0.8
            )
            
            message = response.choices[0].message.content.strip()
            # 不要なクォートを削除
            message = message.strip('"').strip("'")
            # メッセージが長すぎる場合は切り詰め
            if len(message) > 20:
                message = message[:17] + "..."
            return message
            
        except Exception as e:
            # APIキー未設定の場合は静かに処理、その他のエラーは表示
            if "OPENAI_API_KEY" in str(e):
                pass  # APIキー未設定は想定内なので静かに処理
            else:
                print(f"デバッグ: 心理戦メッセージ生成エラー: {e}")
            
            # フォールバックメッセージを選択
            fallback_messages = [
                "勝負だ！",
                "本気を見せる時だ", 
                "君の実力を見せてもらおう",
                "面白くなりそうだ",
                "負けないぞ！",
                "覚悟はできたか？",
                "手加減はしないぞ！"
            ]
            return random.choice(fallback_messages)