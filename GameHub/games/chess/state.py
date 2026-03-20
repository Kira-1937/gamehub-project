from __future__ import annotations

from typing import Iterable

import chess

from core.state import State
from core.types import PlayerID


class ChessState(State):
    def __init__(self, fen: str):
        self.fen = fen

    @property
    def current_player(self) -> PlayerID:
        return "white" if self.board().turn == chess.WHITE else "black"

    def board(self) -> chess.Board:
        return chess.Board(self.fen)

    def active_players(self) -> Iterable[PlayerID]:
        return (self.current_player,)

    def copy(self) -> "ChessState":
        return ChessState(self.fen)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ChessState):
            return False
        return self.fen == other.fen

    def __hash__(self) -> int:
        return hash(self.fen)
