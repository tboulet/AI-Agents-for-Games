# GamesAI
An implementation in python of some game agents such as AlphaBeta or MCTS, that can be applied to any n-player non deterministic game object that implements the game interface.

## Installation :
Install the package using :

    pip install git+https://github.com/tboulet/AI-Agents-for-Games
    
## Using the package :
Import games and players (agents) for performing on it.
The agents dictionnary given to a game object must be a dictionnary with the name being the names of the roles and values being either the class or a tuple class/kwargs for the agent.
```python
from GamesAI.Player import RandomPlayer, HumanPlayer, AlphaBeta
from GamesAI.games.tictactoe import TicTacToeGame

agents = {'X' : HumanPlayer,
          'O' : (MonteCarloTreeSearch, {'n_rollouts': 200}),
          }
game = TicTacToeGame(agents = agents)
game.play_game()
```

## Players/Game agents
Some AI agents that can solve games that implements the Game interface can be found in GamesAI.Player.

```python
from GamesAI.Player import RandomPlayer, HumanPlayer, Minimax, MinimaxPlus, AlphaBeta, MonteCarloTreeSearch
```

You can also create your own player classes by inheriting the Player class or NonDeterministicPlayer if your class can deal with non-deterministic games.

It should have an agent_name as static attribute and implements the method get_action(state):
```python
from GamesAI.Player import Player, NonDeterministicPlayer

class RandomPlayer(NonDeterministicPlayer):
    """A player that plays randomly."""
    agent_name = "RandomPlayer"
    
    def __init__(self, game : object, game_name: str, agent_name: str) -> None:
        super().__init__(game, game_name, agent_name)
        
    def get_action(self, state: State) -> object:
        """Return a random available action."""
        return random.choice(self.game.get_actions(state))
```
## Creating a game
For now only tic-tac-toe and a random version of it (where a box is randomly erased after each O's turn) are implemented in GamesAI.games, but you can create your own game object by inheriting the Game class.

```python
from GamesAI.Game import Game, NonDeterministicGame, State

class YourState(State):
    pass

class YourGame(Game):
    names = {"Blue", "Red", "Yellow"}
    pass
```

Your game object will use a subclass of State class that must implements the __hash__, __eq__ and __str__ methods. A state define the complete information of the game at a certain instant.

A subclass of Game should have a set of names as static attribute and implement the following methods :
    
    - get_start_state() : return the initial state of the game
    - get_player_playing(state) : return the player playing at the given state
    - get_actions(state) : return the list of actions available at the given state
    - get_result(state, action) : return the state reached by the given action in the given state
    - is_terminal_state(state) : return True if the given state is a terminal state
    - get_utilites(state) : return the utilities of the players at the given state

If you want to create a non deterministic game, where randomness is involved, you should inherit the NonDeterministicGame class and implements the get_random_action_distribution(state) method.

