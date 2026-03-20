from __future__ import annotations

from typing import Iterable

from core.state import State
from core.types import PlayerID, Action, Result

from interaction.port import InteractionPort


class TicTacToeCLIInteraction(InteractionPort):
    def show_state(self, state: State) -> None:
        from games.tictactoe.state import TicTacToeState
        from ui.cli.tictactoe import render_board

        assert isinstance(state, TicTacToeState)
        render_board(state)

    def prompt_action(
        self, player_id: PlayerID, state: State, legal_actions: Iterable[Action]
    ) -> Action:
        from games.tictactoe.state import TicTacToeState
        from ui.cli.tictactoe import prompt_move

        assert isinstance(state, TicTacToeState)
        print(f"\nPlayer {player_id}'s turn")
        return prompt_move(legal_actions)

    def show_result(self, result: Result, final_state: State) -> None:
        from games.tictactoe.state import TicTacToeState
        from ui.cli.tictactoe import render_board

        assert isinstance(final_state, TicTacToeState)
        print("\n=== Final Board ===")
        render_board(final_state)
        print("=== Result ===")
        for pid, reward in result.items():
            print(f"Player {pid}: {reward}")


class ChessCLIInteraction(InteractionPort):
    def show_state(self, state: State) -> None:
        from games.chess.state import ChessState
        from ui.cli.chess import render_board as render_chess_board

        assert isinstance(state, ChessState)
        render_chess_board(state)

    def prompt_action(
        self, player_id: PlayerID, state: State, legal_actions: Iterable[Action]
    ) -> Action:
        from games.chess.state import ChessState
        from ui.cli.chess import prompt_move as prompt_chess_move

        assert isinstance(state, ChessState)
        print(f"\nPlayer {player_id}'s turn")
        return prompt_chess_move(legal_actions)

    def show_result(self, result: Result, final_state: State) -> None:
        from games.chess.state import ChessState
        from ui.cli.chess import render_board as render_chess_board

        assert isinstance(final_state, ChessState)
        print("\n=== Final Board ===")
        render_chess_board(final_state)
        print("=== Result ===")
        for pid, reward in result.items():
            print(f"Player {pid}: {reward}")
