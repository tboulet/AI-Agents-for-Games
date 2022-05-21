"""Module for defining the Game object.

Games should be define as subclasses of Game or NonDeterministicGame. They should implement abstract methods as defined in the Game abstract class.
"""

#Tool imports
from abc import ABC, abstractmethod
from time import sleep
from typing import Union
import random
#Game solving module imports
from GamesAI.div.utils import Constant
from GamesAI.div.GameContent import State, Percept, ActionType
from GamesAI.Player import Player, NonDeterministicPlayer, NonFullyObservablePlayer


class Game(ABC):
    """The class for defining a GAME problem.
    Standard games are deterministic, observable, turn-taking.
    """
    
    def __init__(self, agents : dict[str, Union[type, tuple[type, dict]]]) -> None:
        """Creation of a GAME object.
        agents is a dictionnary with game_name as keys and a class of player as values.
        If the player class initializer requires arguments, the value can instead be a tuple (PlayerClass, kwargs).
        
        A subclass of Game should implement the following methods :
        - get_start_state() : return the initial state of the game
        - get_player_playing(state) : return the player playing at the given state
        - get_actions(state) : return the list of actions available at the given state
        - get_result(state, action) : return the state reached by the given action in the given state
        - is_terminal_state(state) : return True if the given state is a terminal state
        - get_utilites(state) : return the utilities of the players at the given state
        """
        
        if not hasattr(self, 'names'): raise Exception("Game class must define class attribute .names")
        if self.names != set(agents.keys()): raise Exception("Game class names does not match agents names (agents keys)")
        
        self.players = dict()
        for game_name, PlayerClass_or_tuple in agents.items():
            if isinstance(PlayerClass_or_tuple, type):
                self.players[game_name] = PlayerClass_or_tuple(game = self, 
                                           game_name = game_name, 
                                           agent_name = PlayerClass_or_tuple.agent_name)
            elif isinstance(PlayerClass_or_tuple, tuple):
                PlayerClass, kwargs = PlayerClass_or_tuple
                self.players[game_name] = PlayerClass(game = self, 
                                           game_name = game_name, 
                                           agent_name = PlayerClass.agent_name,
                                           **kwargs)
            else:
                raise Exception("Game class must define agents as dict[str, type] or dict[str, tuple[type, dict]]")
                
    @abstractmethod
    def get_start_state(self) -> State:
        """Return the initial state of the game"""
        pass
    
    @abstractmethod
    def get_player_playing(self, state : State) -> Union[Player, None]:
        """Return the player playing in the given state. Return None if no player should play, ie if randomness plays."""
        pass
    
    @abstractmethod
    def get_actions(self, state : State) -> list[ActionType]:
        """Return the list of actions available in the given state for the player playing in the state"""
        pass
    
    @abstractmethod
    def get_result(self, state : State, action : ActionType) -> State:
        """Return the state reached by the game after having played the given action in the given state"""
        pass
    
    @abstractmethod
    def is_terminal_state(self, state : State) -> bool:
        """Return True if the given state is a terminal state, False otherwise"""
        pass
        
    @abstractmethod
    def get_utilities(self, state : State) -> dict[Player, float]:
        """Return the utilities of each player."""
        pass
    
    #Permanent methods
    def get_players(self) -> dict[str, Player]:
        """Return the players of the game with their game names as keys"""
        return self.players
    
    def get_names(self) -> set:
        """Return the set of the game names"""
        if not hasattr(self, 'names'): raise Exception("Game class must define class attribute .names")
        return self.names
    
    def play_game(self, verbose : int, wait_time : float = 0) -> State:
        """Play the game until the end, print the information, return the final state.
        verbose = 0 : no print
        verbose = 1 : print game result (utilities for each player)
        verbose = 2 : print game result and state at each step
        """
        state = self.get_start_state()
        if verbose >= 1: print("Starting game ...")
        while True:
            sleep(wait_time)
            if verbose >= 2:
                print(state)
            if self.is_terminal_state(state):
                if verbose >= 1:
                    print("\tEnd of game, utilities of players :")
                    for player in self.players.values():
                        print(player, ": ", self.get_utilities(state)[player])
                return state
            player = self.get_player_playing(state)
            if player is None:
                distribution = self.get_random_action_distribution(state)
                action = random.choices(list(distribution.keys()), weights = list(distribution.values()))[0]
                if verbose >= 2:
                    print(f"Random action : {action}")
            else:
                action = player.get_action(state)
                if verbose >= 2:
                    print(f"{player} action : {action}")
            state = self.get_result(state, action)


class NonDeterministicGame(Game):
    """Non deterministic game, where randomness happens at some node.
    
    Subclasses should implement the methods of Game as well as the get_random_action_distribution method.
    - get_random_action_distribution(state) : return the distribution of actions available at the given state for the player playing at the state.
    """
    def __init__(self, agents: dict[str, Union[type, tuple[type, dict]]]) -> None:
        for player_class in agents.values():
            if isinstance(player_class, tuple):
                player_class = player_class[0]
            if not issubclass(player_class, NonDeterministicPlayer):
                raise Exception(f"Non deterministic game must have only NonDeterministicPlayer players (player inheriting NonDeterministicPlayer class) but {player_class.agent_name} is not.")
        super().__init__(agents)
    
    @abstractmethod
    def get_random_action_distribution(self, state : State) -> dict[ActionType, float]:
        """Return the action distribution for the actions available in the given random state"""
        if self.get_player_playing is not None:
            raise Exception("The state is not a random state.")
        actions = self.get_actions(state)
        if len(actions) == 0:
            raise Exception("The state has no action available.")
        return {action : 1 / len(actions) for action in actions}
        



class NonFullyObservableGame(Game):
    """Non fully observable game are games where each agent does not have access to the complete state but rather only some information called a percept.
    
    Sub classes should implement the methods of Game as well as the get_percept method.
    - get_percept_method(state, player) : return the percept of the given state for a certain player
    """
    def __init__(self, agents: dict[str, Union[type, tuple[type, dict]]]) -> None:
        for player_class in agents.values():
            if isinstance(player_class, tuple):
                player_class = player_class[0]
            if not issubclass(player_class, NonFullyObservablePlayer):
                raise Exception(f"Non fully observable game must have only NonFullyObservablePlayer players (player inheriting NonFullyObservablePlayer class) but {player_class.agent_name} is not.")
        super().__init__(agents)
        
    @abstractmethod
    def get_percept(self, state : State, player : NonFullyObservablePlayer) -> Percept:
        """Return the percept of the given state for a certain player"""
    
    def play_game(self, verbose : int, wait_time : float = 0) -> State:
        """Play the game until the end, print the information, return the final state.
        verbose = 0 : no print
        verbose = 1 : print game result (utilities for each player)
        verbose = 2 : print game result and state at each step
        """
        state = self.get_start_state()
        if verbose >= 1: print("Starting game ...")
        while True:
            sleep(wait_time)
            player = self.get_player_playing(state)
            percept = self.get_percept(state, player)
            if verbose >= 2:
                print("State: ", state)
                print("Percept: ", percept)
            if self.is_terminal_state(state):
                if verbose >= 1:
                    print("\tEnd of game, utilities of players :")
                    for player in self.players.values():
                        print(player, ": ", self.get_utilities(state)[player])
                return state
            
            if player is None:
                distribution = self.get_random_action_distribution(state)
                action = random.choices(list(distribution.keys()), weights = list(distribution.values()))[0]
                if verbose >= 2:
                    print(f"Random action : {action}")
            else:
                distribution = player.get_action_distribution(percept)
                action = random.choices(list(distribution.keys()), weights = list(distribution.values()))[0]
                if verbose >= 2:
                    print(f"{player} action : {action}")
            state = self.get_result(state, action)