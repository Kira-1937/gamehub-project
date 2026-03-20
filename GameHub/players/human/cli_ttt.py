
from __future__ import annotations
from typing import Iterable

from core.player import Player
from core.state import State
from core.types import Action, PlayerID

from games.tictactoe.state import TicTacToeState
from interaction.port import InteractionPort


class HumanCLITicTacToePlayer(Player):
    def __init__(self, player_id: PlayerID, interaction: InteractionPort):
        super().__init__(player_id)
        self._interaction = interaction

    def select_action(
        self,
        state: State,
        legal_actions: Iterable[Action],
    ) -> Action:
        assert isinstance(state, TicTacToeState)
        self._interaction.show_state(state)
        return self._interaction.prompt_action(self.player_id, state, legal_actions)
