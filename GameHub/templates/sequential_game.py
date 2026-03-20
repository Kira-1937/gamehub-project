"""Copy this file to start a new sequential game implementation."""

from __future__ import annotations

from typing import Iterable, Mapping, Any

from core.game import Game
from core.state import State
from core.types import PlayerID, Action, JointAction, Result


class SequentialTemplateState(State):
    def __init__(self, board: Mapping[str, Any]):
        self.board = dict(board)

    def active_players(self) -> Iterable[PlayerID]:
        raise NotImplementedError

    def copy(self) -> \"SequentialTemplateState\":
        return SequentialTemplateState(self.board)


class SequentialTemplateGame(Game):
    def initial_state(self) -> State:
        raise NotImplementedError

    def active_players(self, state: State) -> Iterable[PlayerID]:
        raise NotImplementedError

    def legal_actions(self, state: State, player: PlayerID) -> Iterable[Action]:
        raise NotImplementedError

    def next_state(self, state: State, joint_action: JointAction) -> State:
        raise NotImplementedError

    def is_terminal(self, state: State) -> bool:
        raise NotImplementedError

    def result(self, state: State) -> Result:
        raise NotImplementedError

    def player_ids(self) -> Iterable[PlayerID]:
        raise NotImplementedError
