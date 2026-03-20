"""
Tic-Tac-Toe Max^n player using generic engine.
"""

from __future__ import annotations
from typing import Iterable, Tuple, Optional, Sequence

from core.player import Player
from core.types import Action, PlayerID,Result

from games.tictactoe.game import TicTacToeGame
from games.tictactoe.state import TicTacToeState

from players.ai.core.search.max_n import max_n_decision


_game = TicTacToeGame()


# ---------------------------------------------------------------------------
# Terminal + evaluation
# ---------------------------------------------------------------------------

def is_terminal(state: TicTacToeState) -> bool:
    return _game.is_terminal(state)


def evaluate(state: TicTacToeState) -> Result:
    """
    Return utility vector for all players.
    """
    result = _game.result(state)
    return result



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

class MaxnTicTacToePlayer(Player):
    """
    Perfect or depth-limited Tic-Tac-Toe AI using Max^n.
    """

    def __init__(self, player_id: PlayerID, depth: Optional[int] = None):
        super().__init__(player_id)
        self.depth = depth

    def select_action(self, state, legal_actions) -> Action:
        assert isinstance(state, TicTacToeState)

        return max_n_decision(
            state,
            self.player_id,
            is_terminal=is_terminal,
            evaluate=evaluate,
            next_states=next_states,
            current_player=current_player,
            depth=self.depth,
        )
