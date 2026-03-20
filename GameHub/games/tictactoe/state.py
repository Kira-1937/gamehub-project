from __future__ import annotations
from typing import Iterable, Tuple
from core.state import State
from core.types import PlayerID

Cell = int

Board = Tuple[Tuple[Cell, ...], ...]

class TicTacToeState(State):

    def __init__(self,board:Board,current_player: PlayerID):
        self.board = board
        self.current_player = current_player

    def active_players(self) -> Iterable[PlayerID]:
        return (self.current_player,)
    
    def copy(self)->"TicTacToeState":
        return TicTacToeState(self.board,self.current_player)


    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TicTacToeState):
            return False
        return self.board == other.board and self.current_player == other.current_player

    def __hash__(self) -> int:
        return hash((self.board, self.current_player))

