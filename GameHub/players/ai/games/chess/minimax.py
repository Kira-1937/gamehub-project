from __future__ import annotations

from typing import Iterable, Optional, Tuple

import chess

from core.player import Player
from core.types import Action, PlayerID
from games.chess.game import ChessGame
from games.chess.state import ChessState
from players.ai.core.search.minimax import minimax_decision


_game = ChessGame()
_PIECE_VALUES = {
    chess.PAWN: 1.0,
    chess.KNIGHT: 3.2,
    chess.BISHOP: 3.3,
    chess.ROOK: 5.0,
    chess.QUEEN: 9.0,
    chess.KING: 0.0,
}


def is_terminal(state: ChessState) -> bool:
    return _game.is_terminal(state)


def evaluate(state: ChessState, root_player: PlayerID) -> float:
    board = state.board()
    outcome = board.outcome()
    if outcome is not None:
        if outcome.winner is None:
            return 0.0
        winner = ChessGame.PLAYER_WHITE if outcome.winner == chess.WHITE else ChessGame.PLAYER_BLACK
        return 10_000.0 if winner == root_player else -10_000.0

    score = 0.0
    for piece_type, value in _PIECE_VALUES.items():
        score += len(board.pieces(piece_type, chess.WHITE)) * value
        score -= len(board.pieces(piece_type, chess.BLACK)) * value

    if board.is_check():
        score += -0.25 if board.turn == chess.WHITE else 0.25

    return score if root_player == ChessGame.PLAYER_WHITE else -score


def next_states(state: ChessState) -> Iterable[Tuple[Action, ChessState]]:
    player = state.current_player
    results: list[Tuple[Action, ChessState]] = []

    for action in _game.legal_actions(state, player):
        joint = {player: action}
        results.append((action, _game.next_state(state, joint)))

    return results


def current_player(state: ChessState) -> PlayerID:
    return state.current_player


class MinimaxChessPlayer(Player):
    def __init__(self, player_id: PlayerID, depth: Optional[int] = 2):
        super().__init__(player_id)
        self.depth = depth

    def select_action(self, state, legal_actions) -> Action:
        assert isinstance(state, ChessState)
        available = list(legal_actions)
        if not available:
            raise ValueError("No legal actions available for MinimaxChessPlayer.")

        return minimax_decision(
            state,
            self.player_id,
            is_terminal=is_terminal,
            evaluate=evaluate,
            next_states=next_states,
            current_player=current_player,
            depth=self.depth,
        )
