"""Copy this file to start a new simultaneous game implementation."""

from __future__ import annotations

from typing import Iterable, Mapping, Any

from core.simultaneous import SimultaneousGame
from core.state import State
from core.types import PlayerID, Action, JointAction, Result


class SimultaneousTemplateState(State):
    def __init__(self, data: Mapping[str, Any]):
        self.data = dict(data)

    def active_players(self) -> Iterable[PlayerID]:
        raise NotImplementedError

    def copy(self) -> \"SimultaneousTemplateState\":
        return SimultaneousTemplateState(self.data)


class SimultaneousTemplateGame(SimultaneousGame):
    def initial_state(self) -> State:
        raise NotImplementedError

    def player_ids(self) -> Iterable[PlayerID]:
        raise NotImplementedError

    def legal_actions(self, state: State, player: PlayerID) -> Iterable[Action]:
        raise NotImplementedError

    def next_state(self, state: State, joint_action: JointAction) -> State:
        raise NotImplementedError

    def is_terminal(self, state: State) -> bool:
        raise NotImplementedError

    def result(self, state: State) -> Result:
        raise NotImplementedError
