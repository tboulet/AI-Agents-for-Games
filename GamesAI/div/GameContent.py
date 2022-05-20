from abc import ABC, abstractmethod
from typing import Union

class State(ABC):
    """The class for defining a STATE of a GAME problem."""
    @abstractmethod
    def __str__(self) -> str:
        pass
    
    @abstractmethod
    def __hash__(self) -> int:
        pass
    
    @abstractmethod
    def __eq__(self, other) -> bool:
        pass

GameType = object
ActionType = object
