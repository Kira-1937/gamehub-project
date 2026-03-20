"""Copy this file when wiring a new bot into the registry."""

from __future__ import annotations

from typing import Iterable

from core.player import Player
from core.state import State
from core.types import PlayerID, Action

from interaction.port import InteractionPort

from registry import register_sequential_bot, register_simultaneous_bot


class TemplateBot(Player):
    def __init__(self, player_id: PlayerID):
        super().__init__(player_id)

    def select_action(
        self, state: State, legal_actions: Iterable[Action]
    ) -> Action:
        raise NotImplementedError


def register():
    register_sequential_bot(
        \"your-game\",
        \"template-bot\",
        lambda pid, interaction: TemplateBot(pid),
    )

    register_simultaneous_bot(
        \"your-simultaneous-game\",
        \"template-bot\",
        lambda pid: TemplateBot(pid),
    )
