from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable

from core.state import State
from core.types import PlayerID, Action, Result


class InteractionPort(ABC):
    def show_state(self, state: State) -> None:
        """
        Render the current state for a human player.
        """
        return None

    @abstractmethod
    def prompt_action(
        self, player_id: PlayerID, state: State, legal_actions: Iterable[Action]
    ) -> Action:
        raise NotImplementedError

    def show_result(self, result: Result, final_state: State) -> None:
        """
        Display the final result of a match.
        """
        return None


class NullInteraction(InteractionPort):
    """
    No-op port for bot-only contexts.
    """

    def prompt_action(
        self, player_id: PlayerID, state: State, legal_actions: Iterable[Action]
    ) -> Action:
        raise NotImplementedError("NullInteraction should not prompt actions.")
