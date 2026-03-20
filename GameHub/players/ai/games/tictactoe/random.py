
from __future__ import annotations
import random
from typing import Iterable

from core.player import Player
from core.state import State
from core.types import Action, PlayerID


class RandomTicTacToePlayer(Player):
    def __init__(self, player_id: PlayerID, seed: int | None = None):
        super().__init__(player_id)
        self._rng = random.Random(seed)  # local RNG for reproducibility
    def select_action(
        self,
        state: State,
        legal_actions: Iterable[Action],
    ) -> Action:
        legal_list = list(legal_actions)

        if not legal_list:
            raise ValueError("No legal actions available for RandomTicTacToePlayer.")

        return self._rng.choice(legal_list)
