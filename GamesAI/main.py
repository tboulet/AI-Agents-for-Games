from GamesAI.Player import Player, RandomPlayer, HumanPlayer, Minimax, AlphaBeta, MinimaxPlus, MonteCarloTreeSearch
from games.tictactoe import TicTacToeGame, TicTacToeRandomGame

#Define agents ie dictionnary with key being game name and value being either agent class or tuple of agent class and kwargs for initializing the class
def h(state):
    return {"X" : 0, "O" : 0}
agents = {"X" : HumanPlayer, "O" : (MinimaxPlus, {'max_depth': 4, 'heuristic': h})}
# agents = {"O" : RandomPlayer, "X" : (MonteCarloTreeSearch, {'n_rollouts': 300})}

#Create the game object.
game = TicTacToeRandomGame(agents) 

#Play a game.
game.play_game(verbose=2)