from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Iterable

from .state import State
from .types import PlayerID, Action


class Player(ABC):

    def __init__(self, player_id: PlayerID):
        self.player_id = player_id

    @abstractmethod
    def select_action(self,state: State,legal_actions: Iterable[Action],) -> Action:
        raise NotImplementedError
