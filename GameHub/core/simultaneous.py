from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, Mapping

from .events import ActionTaken, EventBus, MatchEnded, TurnStarted
from .player import Player
from .state import State
from .types import PlayerID, Action, JointAction, Result


class SimultaneousGame(ABC):

    @abstractmethod
    def initial_state(self) -> State:
        raise NotImplementedError

    @abstractmethod
    def player_ids(self) -> Iterable[PlayerID]:
        raise NotImplementedError

    @abstractmethod
    def legal_actions(self, state: State, player: PlayerID) -> Iterable[Action]:
        raise NotImplementedError

    @abstractmethod
    def next_state(self, state: State, joint_action: JointAction) -> State:
        raise NotImplementedError

    @abstractmethod
    def is_terminal(self, state: State) -> bool:
        raise NotImplementedError

    @abstractmethod
    def result(self, state: State) -> Result:
        raise NotImplementedError


class SimultaneousMatch:

    def __init__(self, game: SimultaneousGame, players: Mapping[PlayerID, Player], event_bus: EventBus | None = None):
        self.game = game
        self.players = players
        self._event_bus = event_bus

    def _publish(self, event) -> None:
        if self._event_bus is not None:
            self._event_bus.publish(event)

    def run(self) -> tuple[Result, list[State]]:
        state = self.game.initial_state()
        history: list[State] = [state]

        while not self.game.is_terminal(state):
            joint_action: dict[PlayerID, Action] = {}

            for pid in self.game.player_ids():
                player = self.players[pid]
                legal = self.game.legal_actions(state, pid)
                self._publish(TurnStarted(state=state, player=pid))
                action = player.select_action(state, legal)
                joint_action[pid] = action
                self._publish(ActionTaken(state=state, player=pid, action=action))

            state = self.game.next_state(state, joint_action)
            history.append(state)

        result = self.game.result(state)
        self._publish(MatchEnded(state=state, result=result))
        return result, history
