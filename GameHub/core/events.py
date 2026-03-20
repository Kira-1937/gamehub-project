from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Protocol, runtime_checkable

from .state import State
from .types import PlayerID, Action, Result


@dataclass
class MatchEvent:
    state: State


@dataclass
class TurnStarted(MatchEvent):
    player: PlayerID


@dataclass
class ActionTaken(MatchEvent):
    player: PlayerID
    action: Action


@dataclass
class MatchEnded(MatchEvent):
    result: Result


@runtime_checkable
class EventHandler(Protocol):
    def handle(self, event: MatchEvent) -> None:
        ...


class EventBus:
    def __init__(self) -> None:
        self._subscribers: list[EventHandler] = []

    def subscribe(self, handler: EventHandler) -> None:
        self._subscribers.append(handler)

    def publish(self, event: MatchEvent) -> None:
        for handler in self._subscribers:
            handler.handle(event)
