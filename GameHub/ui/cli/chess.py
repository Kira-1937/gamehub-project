from __future__ import annotations

from typing import Iterable

import chess


def render_board(state) -> None:
    board = state.board()
    rows = str(board).splitlines()

    print()
    for rank, row in zip(range(8, 0, -1), rows):
        print(f"{rank} {row}")
    print("  a b c d e f g h")
    print(f"Turn: {'white' if board.turn == chess.WHITE else 'black'}")

    if board.is_check():
        print("Status: check")


def prompt_move(legal_actions: Iterable[str]) -> str:
    legal = list(legal_actions)
    legal_set = set(legal)
    preview = ", ".join(legal[:20])

    while True:
        raw = input(
            "Enter a move in UCI format"
            + (f" ({preview}{' ...' if len(legal) > 20 else ''})" if legal else "")
            + ": "
        ).strip().lower()
        if raw in legal_set:
            return raw
        print("Illegal move. Example formats: e2e4, g1f3, e7e8q")
