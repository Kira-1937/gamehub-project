from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Iterable
from .state import State
from .types import PlayerID, Action, JointAction, Result

class Game(ABC):

    @abstractmethod
    def initial_state(self)->State:
        raise NotImplementedError

    @abstractmethod
    def active_players(self,state: State)->Iterable[PlayerID]:
        raise NotImplementedError


    @abstractmethod
    def legal_actions(self,state:State,player:PlayerID)-> Iterable[Action]:
        raise NotImplementedError

    @abstractmethod
    def next_state(self,state:State,joint_action:JointAction)->State:
        raise NotImplementedError

    @abstractmethod
    def is_terminal(self,state:State)->bool:
        raise NotImplementedError

    @abstractmethod
    def result(self,state:State)->Result:
        raise NotImplementedError

    @abstractmethod
    def player_ids(self) -> Iterable[PlayerID]:
        raise NotImplementedError
