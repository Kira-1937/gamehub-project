from __future__ import annotations

import random
from typing import Iterable

from core.player import Player
from core.state import State
from core.types import Action, PlayerID


class RandomRockPaperScissorsPlayer(Player):
    def __init__(self, player_id: PlayerID, seed: int | None = None):
        super().__init__(player_id)
        self._rng = random.Random(seed)

    def select_action(
        self,
        state: State,
        legal_actions: Iterable[Action],
    ) -> Action:
        choices = list(legal_actions)
        if not choices:
            raise ValueError("No legal actions available for the rock-paper-scissors player.")
        return self._rng.choice(choices)
