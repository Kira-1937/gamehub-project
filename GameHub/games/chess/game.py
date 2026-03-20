from __future__ import annotations

from typing import Iterable

import chess

from core.game import Game
from core.state import State
from core.types import Action, JointAction, PlayerID, Result

from .state import ChessState


class ChessGame(Game):
    PLAYER_WHITE: PlayerID = "white"
    PLAYER_BLACK: PlayerID = "black"
    PLAYERS = (PLAYER_WHITE, PLAYER_BLACK)

    def initial_state(self) -> State:
        return ChessState(chess.Board().fen())

    def active_players(self, state: State) -> Iterable[PlayerID]:
        assert isinstance(state, ChessState)
        return state.active_players()

    def legal_actions(self, state: State, player: PlayerID) -> Iterable[Action]:
        assert isinstance(state, ChessState)
        if player != state.current_player:
            return ()

        board = state.board()
        return [move.uci() for move in board.legal_moves]

    def next_state(self, state: State, joint_action: JointAction) -> State:
        assert isinstance(state, ChessState)

        (player, action), = joint_action.items()
        if player != state.current_player:
            raise ValueError(f"It is not {player}'s turn.")

        board = state.board()
        move = chess.Move.from_uci(str(action))
        if move not in board.legal_moves:
            raise ValueError(f"Illegal chess move: {action}")

        board.push(move)
        return ChessState(board.fen())

    def is_terminal(self, state: State) -> bool:
        assert isinstance(state, ChessState)
        return state.board().is_game_over()

    def result(self, state: State) -> Result:
        assert isinstance(state, ChessState)

        outcome = state.board().outcome()
        if outcome is None or outcome.winner is None:
            return {
                self.PLAYER_WHITE: 0.0,
                self.PLAYER_BLACK: 0.0,
            }

        winner = self.PLAYER_WHITE if outcome.winner == chess.WHITE else self.PLAYER_BLACK
        loser = self.PLAYER_BLACK if winner == self.PLAYER_WHITE else self.PLAYER_WHITE
        return {
            winner: 1.0,
            loser: -1.0,
        }

    def player_ids(self) -> Iterable[PlayerID]:
        return self.PLAYERS
