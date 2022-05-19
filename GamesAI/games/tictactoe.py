from typing import Union
from GamesAI.Game import Game, Player, State, RandomGame

class TicTacToeState(State):
    
    def __init__(self, player_playing : Player, board : list[str]) -> None:
        super().__init__()
        self.board = board
        self.player_playing = player_playing

    def __str__(self) -> str:
        res = ""
        for i in range(3):
            for j in range(3):
                elem = self.board[3*i + j]
                if elem == 0:
                    res += '.'
                else:
                    res += elem
            res += '\n'
        return res
    
    def __eq__(self, other) -> bool:
        return self.board == other.board
        
    def __hash__(self) -> int:
        return hash(tuple(self.board))


class TicTacToeGame(Game):
    
    def __init__(self, agents : dict[str, type]) -> None:
        self.names = {"X", "O"}
        super().__init__(agents)
        board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.initial_state = TicTacToeState(self.players["X"], board)
        
    def get_start_state(self) -> TicTacToeState:
        return self.initial_state
    
    def get_player_playing(self, state: TicTacToeState) -> Player:
        return state.player_playing
    
    def get_actions(self, state: TicTacToeState) -> list[object]:
        actions = []
        for i in range(9):
            if state.board[i] == 0:
                actions.append(i)
        return actions
    
    def get_result(self, state: TicTacToeState, action: object) -> TicTacToeState:
        board = state.board.copy()
        board[action] = state.player_playing.game_name
        next_name = "X" if state.player_playing.game_name == "O" else "O"
        next_player = self.players[next_name]
        return TicTacToeState(next_player, board)
    
    def is_terminal_state(self, state: State) -> bool:
        return (self.get_actions(state) == []) or (self.get_winner(state) is not None)
    
    def get_utilities(self, state: dict[Player, float]) -> float:
        winner = self.get_winner(state)
        if winner is None: 
            return {player : 0 for player in self.get_players().values()}
        return {player : 1 if player == winner else -1 for player in self.get_players().values()}
    
    
    # specific methods to TicTacToe
    def get_winner_string(self, state: TicTacToeState) -> Union[str, None]:
        """Returns the winner of the board, or None if no winner"""
        board = state.board
        # Check rows
        for i in range(3):
            if board[3*i] == board[3*i+1] == board[3*i+2] != 0:
                return board[3*i]
        # Check columns
        for i in range(3):
            if board[i] == board[i+3] == board[i+6] != 0:
                return board[i]
        # Check diagonals
        if board[0] == board[4] == board[8] != 0:
            return board[0]
        if board[2] == board[4] == board[6] != 0:
            return board[2]
        return None
    
    def get_winner(self, state: TicTacToeState) -> Union[Player, None]:
        winner_str = self.get_winner_string(state)
        if winner_str is None: return None
        return self.players[winner_str]
    


class TicTacToeRandomGame(TicTacToeGame, RandomGame):
    """TicTacToe game where a random agent randomly reset one of the box."""
    
    def __init__(self, agents: dict[str, type]) -> None:
        TicTacToeGame.__init__(self, agents)
        
    def get_actions(self, state: TicTacToeState) -> list[object]:
        if state.player_playing is not None:
            return TicTacToeGame.get_actions(self, state)
        else:
            return [k for k in range(9)]
    
    def get_result(self, state: TicTacToeState, action: object) -> TicTacToeState:
        player_playing = state.player_playing
        if player_playing is None:
            board = state.board.copy()
            board[action] = 0
            next_player = self.players['X']
            return TicTacToeState(next_player, board)
        
        else:
            board = state.board.copy()
            board[action] = state.player_playing.game_name
            if player_playing.game_name == "X":
                next_player = self.players['O']
            elif player_playing.game_name == "O":
                next_player = None
            else:
                raise Exception("Invalid player")
            return TicTacToeState(next_player, board)
    
    def get_random_action_distribution(self, state: TicTacToeState) -> dict[object, float]:
        if state.player_playing is None:
            return {action: 1/9 for action in [k for k in range(9)]}
        else:
            raise Exception("The state is not a random state.")