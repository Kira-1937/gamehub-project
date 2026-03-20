from __future__ import annotations
from typing import Iterable, Tuple, Dict

from core.game import Game
from core.state import State
from core.types import PlayerID, Action, JointAction, Result

from .state import TicTacToeState, Board


Move = Tuple[int, int]  # (row, col)


class TicTacToeGame(Game):
    PLAYER_X: PlayerID = "X"
    PLAYER_O: PlayerID = "O"
    PLAYERS = (PLAYER_X, PLAYER_O)
    def initial_state(self) -> State:
        empty_row = (0, 0, 0)
        board: Board = (empty_row, empty_row, empty_row)

        return TicTacToeState(board=board, current_player=self.PLAYER_X)

    def active_players(self, state: State) -> Iterable[PlayerID]:
        assert isinstance(state, TicTacToeState)
        return state.active_players()


    def legal_actions(self, state: State, player: PlayerID) -> Iterable[Action]:
        assert isinstance(state, TicTacToeState)

        moves: list[Move] = []

        for r in range(3):
            for c in range(3):
                if state.board[r][c] == 0:
                    moves.append((r, c))

        return moves

    def next_state(self, state: State, joint_action: JointAction) -> State:
        assert isinstance(state, TicTacToeState)

        (player, move), = joint_action.items()
        r, c = move

        board_list = [list(row) for row in state.board]
        board_list[r][c] = 1 if player == self.PLAYER_X else -1
        new_board: Board = tuple(tuple(row) for row in board_list)

        next_player = (
            self.PLAYER_O if player == self.PLAYER_X else self.PLAYER_X
        )

        return TicTacToeState(new_board, next_player)


    def is_terminal(self, state: State) -> bool:
        assert isinstance(state, TicTacToeState)

        return self._winner(state) is not None or self._is_draw(state)


    def result(self, state: State) -> Result:
        assert isinstance(state, TicTacToeState)

        winner = self._winner(state)

        if winner is None:
            # draw
            return {
                self.PLAYER_X: 0.0,
                self.PLAYER_O: 0.0,
            }

        loser = self.PLAYER_O if winner == self.PLAYER_X else self.PLAYER_X

        return {
            winner: 1.0,
            loser: -1.0,
        }


    def _winner(self, state: TicTacToeState) -> PlayerID | None:
        b = state.board

        lines = []

        for i in range(3):
            lines.append(b[i])
            lines.append((b[0][i], b[1][i], b[2][i]))

        lines.append((b[0][0], b[1][1], b[2][2]))
        lines.append((b[0][2], b[1][1], b[2][0]))

        for line in lines:
            s = sum(line)
            if s == 3:
                return self.PLAYER_X
            if s == -3:
                return self.PLAYER_O

        return None

    def _is_draw(self, state: TicTacToeState) -> bool:
        return (
            all(cell != 0 for row in state.board for cell in row)
            and self._winner(state) is None
        )

    def player_ids(self) -> Iterable[PlayerID]:
        return self.PLAYERS
