import context
from GamesAI.Player import Player, RandomPlayer, HumanPlayer, Minimax, AlphaBeta, MinimaxPlus, MonteCarloTreeSearch
from GamesAI.games.tictactoe import TicTacToeGame, TicTacToeRandomGame

def h(state):
    return {"X" : 0, "O" : 0}

# agents = {"X" : RandomPlayer, 
#           "O" : (MinimaxPlus, {'max_depth': 6, 'heuristic': h})}
agents = {"X" : RandomPlayer, 
          "O" : (MonteCarloTreeSearch, {'n_rollouts': 100})}

ut_mean = 0
n_test = 100
for _ in range(n_test):
    #Create the game object.
    game = TicTacToeGame(agents) 

    #Play a game.
    final_state = game.play_game(verbose=0)
    ut_mean += game.get_utilities(final_state)[game.players["O"]] / n_test
print("Mean utility of player ", game.players["O"],  "against random:", ut_mean)