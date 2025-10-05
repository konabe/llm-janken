
from typing import Optional
from ..game.engine import Choice, GameResult, RockPaperScissorsEngine
from ..ai.player import AIPlayer, RandomAIPlayer

class CLIInterface:
    """コマンドラインインターフェース"""
    
    def __init__(self, language: str = 'ja'):
        self.language = language
        self.messages = self._load_messages()
    
    def _load_messages(self) -> dict:
        """言語別メッセージを読み込み"""
        if self.language == 'ja':
            return {
                'welcome': '🎮 LLM じゃんけんゲームへようこそ！',
                'separator': '=' * 40,
                'vs_ai': '🤖 AI 対戦相手と対戦します！',
                'choices': '選択肢: rock (グー), paper (パー), scissors (チョキ)',
                'quit_info': '終了するには \'quit\' と入力してください。',
                'game_title': '--- じゃんけん勝負！ ---',
                'input_prompt': 'あなたの手を選んでください: ',
                'invalid_input': '無効な入力です。rock, paper, scissors または グー, パー, チョキ を入力してください。',
                'you': 'あなた',
                'ai': 'AI',
                'win': '🎉 あなたの勝ち！',
                'lose': '😅 AI の勝ち！',
                'draw': '🤝 引き分け！',
                'game_end': 'ゲームを終了します。ありがとうございました！'
            }
        else:
            return {
                'welcome': '🎮 Welcome to LLM Rock-Paper-Scissors!',
                'separator': '=' * 40,
                'vs_ai': '🤖 Playing against AI opponent!',
                'choices': 'Choices: rock, paper, scissors',
                'quit_info': 'Type \'quit\' to exit.',
                'game_title': '--- Rock-Paper-Scissors Battle! ---',
                'input_prompt': 'Choose your move: ',
                'invalid_input': 'Invalid input. Please enter rock, paper, or scissors.',
                'you': 'You',
                'ai': 'AI',
                'win': '🎉 You win!',
                'lose': '😅 AI wins!',
                'draw': '🤝 It\'s a draw!',
                'game_end': 'Game ended. Thank you for playing!'
            }
    
    def display_welcome(self):
        """ウェルカムメッセージを表示"""
        print(self.messages['welcome'])
        print(self.messages['separator'])
        print(f"\n{self.messages['vs_ai']}")
        print(self.messages['choices'])
        print(self.messages['quit_info'])
    
    def get_player_choice(self) -> Optional[Choice]:
        """プレイヤーの入力を取得"""
        print(f"\n{self.messages['game_title']}")
        
        while True:
            player_input = input(self.messages['input_prompt']).strip().lower()
            
            if player_input == 'quit':
                return None
            
            choice = Choice.from_string(player_input)
            if choice:
                return choice
            
            print(self.messages['invalid_input'])
    
    def display_result(self, player_choice: Choice, ai_choice: Choice, result: GameResult):
        """ゲーム結果を表示"""
        print(f"\n{self.messages['you']}: {player_choice.to_display(self.language)}")
        print(f"{self.messages['ai']}: {ai_choice.to_display(self.language)}")
        
        if result == GameResult.WIN:
            print(self.messages['win'])
        elif result == GameResult.LOSE:
            print(self.messages['lose'])
        else:
            print(self.messages['draw'])
    
    def display_goodbye(self):
        """終了メッセージを表示"""
        print(f"\n{self.messages['game_end']}")
    
    def run_single_game(self, ai_player: AIPlayer):
        """1回のゲームを実行"""
        self.display_welcome()
        
        # 心理戦メッセージを表示
        psychological_msg = ai_player.get_psychological_message()
        print(f"🤖 {ai_player.name}: 「{psychological_msg}」")
        print()
        
        player_choice = self.get_player_choice()
        if player_choice is None:
            self.display_goodbye()
            return
        
        ai_choice = ai_player.make_choice()
        result = RockPaperScissorsEngine.determine_winner(player_choice, ai_choice)
        
        # 結果を記録
        ai_player.record_game(player_choice, ai_choice, result.value)
        
        self.display_result(player_choice, ai_choice, result)
        self.display_goodbye()