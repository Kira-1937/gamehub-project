from __future__ import annotations

from typing import Iterable, Mapping, Literal

from core.simultaneous import SimultaneousGame
from core.types import PlayerID, Result

from .state import RockPaperScissorsState

Action = Literal["rock", "paper", "scissors"]


class RockPaperScissorsGame(SimultaneousGame):
    PLAYER_A: PlayerID = "A"
    PLAYER_B: PlayerID = "B"
    PLAYERS = (PLAYER_A, PLAYER_B)
    ACTIONS: tuple[Action, ...] = ("rock", "paper", "scissors")

    def __init__(self, max_rounds: int = 3):
        self.max_rounds = max_rounds

    def initial_state(self) -> RockPaperScissorsState:
        return RockPaperScissorsState(
            round_number=0,
            max_rounds=self.max_rounds,
            scores={self.PLAYER_A: 0, self.PLAYER_B: 0},
        )

    def player_ids(self) -> Iterable[PlayerID]:
        return self.PLAYERS

    def legal_actions(self, state: RockPaperScissorsState, player: PlayerID) -> Iterable[Action]:
        assert player in self.PLAYERS
        return self.ACTIONS

    def next_state(self, state: RockPaperScissorsState, joint_action: Mapping[PlayerID, Action]) -> RockPaperScissorsState:
        winner = self._round_winner(joint_action)
        scores = dict(state.scores)

        if winner is not None:
            scores[winner] += 1

        return RockPaperScissorsState(
            round_number=state.round_number + 1,
            max_rounds=self.max_rounds,
            scores=scores,
        )

    def is_terminal(self, state: RockPaperScissorsState) -> bool:
        return state.round_number >= state.max_rounds

    def result(self, state: RockPaperScissorsState) -> Result:
        score_a = state.scores[self.PLAYER_A]
        score_b = state.scores[self.PLAYER_B]

        if score_a == score_b:
            return {self.PLAYER_A: 0.0, self.PLAYER_B: 0.0}

        winner = self.PLAYER_A if score_a > score_b else self.PLAYER_B
        loser = self.PLAYER_B if winner == self.PLAYER_A else self.PLAYER_A

        return {winner: 1.0, loser: -1.0}

    def _round_winner(self, joint_action: Mapping[PlayerID, Action]) -> PlayerID | None:
        moves = tuple(joint_action[player] for player in self.PLAYERS)

        if moves[0] == moves[1]:
            return None

        wins = {
            ("rock", "scissors"): self.PLAYER_A,
            ("scissors", "paper"): self.PLAYER_A,
            ("paper", "rock"): self.PLAYER_A,
        }

        return wins.get(moves, self.PLAYER_B)
