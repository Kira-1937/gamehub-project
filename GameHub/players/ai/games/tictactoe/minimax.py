"""
Tic-Tac-Toe Minimax player using generic minimax engine.
"""

from __future__ import annotations
from typing import Iterable, Tuple, Optional

from core.player import Player
from core.types import Action, PlayerID

from games.tictactoe.game import TicTacToeGame
from games.tictactoe.state import TicTacToeState


from players.ai.core.search.minimax import minimax_decision


_game = TicTacToeGame()


# ---------------------------------------------------------------------------
# Bitboard-based terminal + evaluation
# ---------------------------------------------------------------------------


def is_terminal(state: TicTacToeState) -> bool:
    return _game.is_terminal(state)


def evaluate(state: TicTacToeState, root_player: PlayerID) -> float:
    return _game.result(state).get(root_player, 0.0)


def next_states(state: TicTacToeState) -> Iterable[Tuple[Action, TicTacToeState]]:
    player = state.current_player

    results: list[Tuple[Action, TicTacToeState]] = []

    for action in _game.legal_actions(state, player):
        joint = {player: action}
        results.append((action, _game.next_state(state, joint)))

    return results


def current_player(state: TicTacToeState) -> PlayerID:
    return state.current_player


# ---------------------------------------------------------------------------
# Player implementation
# ---------------------------------------------------------------------------


class MinimaxTicTacToePlayer(Player):
    """
    Perfect or depth-limited Tic-Tac-Toe AI.
    """

    def __init__(self, player_id: PlayerID, depth: Optional[int] = None):
        super().__init__(player_id)
        self.depth = depth

    def select_action(self, state, legal_actions) -> Action:
        assert isinstance(state, TicTacToeState)

        return minimax_decision(
            state,
            self.player_id,
            is_terminal=is_terminal,
            evaluate=evaluate,
            next_states=next_states,
            current_player=current_player,
            depth=self.depth,
        )
