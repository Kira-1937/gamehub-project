

from __future__ import annotations
from typing import Tuple, Iterable

from games.tictactoe.state import TicTacToeState

Move = Tuple[int, int]

RESET = "\u001b[0m"
COLORS = {
    "X": "\u001b[92m",
    "O": "\u001b[91m",
    ".": "\u001b[90m",
}


def color_token(token: str) -> str:
    return f"{COLORS.get(token,'')}{token}{RESET}"


def render_board(state: TicTacToeState) -> None:
    symbol_map = {1: "X", -1: "O", 0: "."}

    rows = []
    counts = {1: 0, -1: 0}

    for row in state.board:
        cells = []
        for cell in row:
            symbol = symbol_map[cell]
            if cell in counts:
                counts[cell] += 1
            cells.append(color_token(symbol))
        rows.append(" │ ".join(cells))

    print()
    print("   0   1   2")
    for idx, row in enumerate(rows):
        print(f"{idx}  {row}")
        if idx < len(rows) - 1:
            print("  ───┼───┼───")

    print(f"\nScore: {color_token('X')} {counts[1]}  vs  {color_token('O')} {counts[-1]}")
    print()


def prompt_move(legal_moves: Iterable[Move]) -> Move:
    """
    Ask the user for a move until a valid one is entered.
    """
    legal_moves = set(legal_moves)  # fast membership check

    while True:
        try:
            raw = input("Enter move as 'row col': ").strip()
            r_str, c_str = raw.split()

            move = (int(r_str), int(c_str))

            if move in legal_moves:
                return move

            print("Invalid move. Try again.")

        except ValueError:
            print("Invalid format. Please enter two numbers like: 1 2")
        except Exception:
            print("Unexpected error. Try again.")
