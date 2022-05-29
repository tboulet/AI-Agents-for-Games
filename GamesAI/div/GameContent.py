from abc import ABC, abstractmethod
from typing import Union, TypeVar

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

class Percept(ABC):
    @abstractmethod
    def __str__(self) -> str:
        pass
    
    @abstractmethod
    def __hash__(self) -> int:
        pass
    
    @abstractmethod
    def __eq__(self, other) -> bool:
        pass


class GameType: pass
class Action: pass
