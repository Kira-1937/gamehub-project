from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Iterable
from .types import PlayerID

class State(ABC):

    @abstractmethod
    def active_players(self)-> Iterable[PlayerID]:
        raise NotImplementedError

    @abstractmethod
    def copy(self)->"State":
        raise NotImplementedError


