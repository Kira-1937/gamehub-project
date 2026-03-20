from __future__ import annotations

from typing import Iterable, Mapping

from core.state import State
from core.types import PlayerID


class RockPaperScissorsState(State):
    def __init__(self, round_number: int, max_rounds: int, scores: Mapping[PlayerID, int]):
        self.round_number = round_number
        self.max_rounds = max_rounds
        self.scores = dict(scores)

    def active_players(self) -> Iterable[PlayerID]:
        return tuple(self.scores.keys())

    def copy(self) -> "RockPaperScissorsState":
        return RockPaperScissorsState(self.round_number, self.max_rounds, self.scores)

    def __repr__(self) -> str:
        return (
            f"RockPaperScissorsState(round={self.round_number}, "
            f"scores={self.scores})"
        )
