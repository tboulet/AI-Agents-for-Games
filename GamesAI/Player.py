from abc import ABC, abstractmethod
import random
from time import time
from typing import Callable, Union

from GamesAI.GameContent import State, GameType, ActionType
from GamesAI.utils import argmin, argmax

class Player(ABC):
    """The class for defining a PLAYER in a GAME. A player has a game_name inside the game and an agent_name that explains its strategy.
    It is defined by its get_action method.
    Two players are considered equal (inside a game) if their game name is equal."""
    agent_name = "BasicPlayer"
    
    def __init__(self, game : GameType, game_name : str, agent_name : str) -> None:
        """A player instance.

        Args:
            game (GameType): the Game object in which the player will play
            game_name (str): the name of the player in the game eg "X", "Red", "Player1" etc
            agent_name (str): the name of the agent (AI) that is used eg Minimax, AlphaBeta etc
        """
        self.game = game
        self.agent_name = agent_name
        self.game_name = game_name
    
    def __repr__(self) -> str:
        return f"[Player '{self.game_name}' ({self.agent_name})]"

    def __hash__(self) -> int:
        return hash(self.game_name)
    
    def __eq__(self, other) -> bool:
        if other is None: 
            return False
        return self.game_name == other.game_name
    
    @abstractmethod
    def get_action(self, state: State) -> ActionType:
        """Return the action to be played in the given state"""
        pass


class RandomPlayer(Player):
    """A player that plays randomly."""
    agent_name = "RandomPlayer"
    
    def __init__(self, game : GameType, game_name: str, agent_name: str) -> None:
        super().__init__(game, game_name, agent_name)
        
    def get_action(self, state: State) -> object:
        """Return a random available action."""
        return random.choice(self.game.get_actions(state))
    
    
class HumanPlayer(Player):
    """A player asking for input for actions to take. Adapted to int and str actions."""
    agent_name = "Human"
    
    def __init__(self, game: GameType, game_name: str, agent_name: str) -> None:
        super().__init__(game, game_name, agent_name)
        
    def get_action(self, state: State) -> object:
        while True:
            actions = self.game.get_actions(state)
            print(f"\t{self.game_name}'s actions : {actions}")
            action = input("Enter action: ")
            if action in actions:
                return action
            elif action == '':
                continue
            elif int(action) in actions:
                return int(action)
            else:
                print("Invalid action")
            

class Minimax(Player):
    """A player that uses the minimax algorithm to choose its actions. Only works for 2 player, zero sum games.
    For big state tree, the algorithm can't explore all tree and need to have a max_depth and a heuristic associated."""
    agent_name = "Minimax"
    
    def __init__(self, game: GameType, game_name: str, agent_name: str, max_depth: int = float("inf"), heuristic : Callable[[State], dict[str, float]] = None) -> None:
        super().__init__(game, game_name, agent_name)
        if (max_depth == float("inf")) != (heuristic is None): 
            raise ValueError("Heuristic and max_depth are either inf/None (default) or non_inf/non_None")
        if len(game.names) != 2:
            raise ValueError("Minimax can only be used for 2 player games")
        self.max_depth = max_depth
        self.heuristic = heuristic
        
    def get_action(self, state: State) -> object:
        """Return the action that maximize Max (the player) utility."""
        return argmax(indexes = self.game.get_actions(state), func = lambda action: self.min_value(self.game.get_result(state, action), depth = 1))
        
        
    def min_value(self, state : State, depth : int) -> float:
        """Return the minimum utility of the next states of the given state after the given action."""
        if self.game.is_terminal_state(state):
            return self.game.get_utilities(state)[self]
        elif depth >= self.max_depth:
            return self.heuristic(state)[self.game_name]
        else:
            return min([self.max_value(self.game.get_result(state, action), depth = depth + 1) for action in self.game.get_actions(state)])
        
    def max_value(self, state : State, depth : int) -> float:
        """Return the maximum utility of the next states of the given state after the given action."""
        if self.game.is_terminal_state(state):
            return self.game.get_utilities(state)[self]
        elif depth >= self.max_depth:
            return self.heuristic(state)[self.game_name]
        else:
            return max([self.min_value(self.game.get_result(state, action), depth = depth + 1) for action in self.game.get_actions(state)])

        

class AlphaBeta(Player):
    """AlphaBeta provide the same solution as Minimax but compute faster by pruning branches that are useless to explore (according to the heuristic)"""
    agent_name = "AlphaBeta"
    
    def __init__(self, game: GameType, game_name: str, agent_name: str, max_depth: int = float("inf"), heuristic : Callable[[State], dict[str, float]] = None) -> None:
        super().__init__(game, game_name, agent_name)
        if (max_depth == float("inf")) != (heuristic is None): 
            raise ValueError("Heuristic and max_depth are either inf/None or non_inf/non_None")
        if len(game.names) != 2:
            raise ValueError("AlphaBeta can only be used for 2 player games")
        self.max_depth = max_depth
        self.heuristic = heuristic
    
    def get_action(self, state: State) -> object:
        """Return the action that maximize Max (the player) utility."""
        return argmax(indexes = self.game.get_actions(state), func = lambda action: self.min_value(self.game.get_result(state, action), depth = 1, alpha = float("-inf"), beta = float("inf")))
        
    def min_value(self, state : State, depth : int, alpha : float, beta : float) -> float:
        """Return the minimum utility of the next states of the given state after the given action."""
        if self.game.is_terminal_state(state):
            return self.game.get_utilities(state)[self]
        elif depth >= self.max_depth:
            return self.heuristic(state)
        else:
            value = float('inf')
            for action in self.game.get_actions(state):
                successor_state = self.game.get_result(state, action)
                value = min(value, self.max_value(successor_state, depth = depth + 1, alpha = alpha, beta = beta))
                if value <= alpha:
                    return value
                beta = min(beta, value)
            return value
        
    def max_value(self, state : State, depth : int, alpha : float, beta : float) -> float:
        """Return the maximum utility of the next states of the given state after the given action."""
        if self.game.is_terminal_state(state):
            return self.game.get_utilities(state)[self]
        elif depth >= self.max_depth:
            return self.heuristic(state)
        else:
            value = float('-inf')
            for action in self.game.get_actions(state):
                successor_state = self.game.get_result(state, action)
                value = max(value, self.min_value(successor_state, depth = depth + 1, alpha = alpha, beta = beta))
                if value >= beta:
                    return value
                alpha = max(alpha, value)
            return value

    
    
class MinimaxPlus(Player):
    """A generalization of Minimax to games wtih any number of players and with randomness."""
    agent_name = "MinimaxPlus"
    
    def __init__(self, game: GameType, game_name: str, agent_name: str, max_depth: int = float("inf"), heuristic: Callable[[State], dict[str, float]] = None) -> None:
        if (max_depth == float("inf")) != (heuristic is None): 
            raise ValueError("Heuristic and max_depth are either inf/None or non_inf/non_None")
        super().__init__(game, game_name, agent_name)
        self.max_depth = max_depth
        self.heuristic = heuristic
        
    def get_action(self, state: State) -> object:
        """Return action that maximizes the expected utility."""
        def func_to_optimize(action):
            next_state = self.game.get_result(state, action)
            return self.best_utilities_for_player(next_state, depth = 1)[self]
        return argmax(indexes = self.game.get_actions(state), 
                      func = func_to_optimize)
    
    def best_utilities_for_player(self, state : State, depth : int) -> dict[Player, float]:
        """Return the best predicted final utilities of a state according to a given player playing as Expectiminimax and assuming each other player plays as Expectiminimax."""
        if self.game.is_terminal_state(state):
            return self.game.get_utilities(state)
        elif depth >= self.max_depth:
            return {self.game.get_players()[game_name] : utility for game_name, utility in self.heuristic(state).items()}
        player_playing = self.game.get_player_playing(state)
        
        if player_playing is None:
            # The state is a random state
            utilities = {player : 0 for player in self.game.get_players().values()}
            for action, prob in self.game.get_random_action_distribution(state).items():
                next_state = self.game.get_result(state, action)
                next_utilities = self.best_utilities_for_player(next_state, depth = depth + 1)
                for player in utilities:
                    utilities[player] += prob * next_utilities[player]
            return utilities

        else:
            #The state is a deterministic state, a Player has to play
            best_value = float("-inf")
            for action in self.game.get_actions(state):
                next_state = self.game.get_result(state, action)
                next_utilities = self.best_utilities_for_player(next_state, depth = depth + 1)
                value = next_utilities[player_playing]
                if value > best_value:
                    best_value = value
                    best_utilities = next_utilities
            return best_utilities
        


from algorithms.MCTS import MonteCarloTreeSearch