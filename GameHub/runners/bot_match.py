
"""
Automated bot-vs-bot match runner for Tic-Tac-Toe.

Runs multiple games and prints win/draw statistics.
"""

from __future__ import annotations

from collections import Counter

from core.match import Match

from games.tictactoe.game import TicTacToeGame

from players.ai.games.tictactoe.random import RandomTicTacToePlayer
from players.ai.games.tictactoe.minimax import MinimaxTicTacToePlayer
from players.ai.games.tictactoe.max_n import MaxnTicTacToePlayer
from core.types import PlayerID
from core.player import Player
from typing import Dict
# ---------------------------------------------------------------------------
# Configure matchup here
# ---------------------------------------------------------------------------

NUM_GAMES = 50

PLAYER_X_FACTORY = lambda: MinimaxTicTacToePlayer("X", depth=None)
PLAYER_O_FACTORY = lambda: MaxnTicTacToePlayer("O", depth=None)


# ---------------------------------------------------------------------------
# Run matches
# ---------------------------------------------------------------------------

def run_series(num_games: int) -> None:
    game = TicTacToeGame()

    results = Counter()

    for _ in range(num_games):
        players:Dict[PlayerID, Player] = {
            game.PLAYER_X: PLAYER_X_FACTORY(),
            game.PLAYER_O: PLAYER_O_FACTORY(),
        }

        match = Match(game=game, players=players)
        final_result, _ = match.run()

        # Determine winner label
        if final_result[game.PLAYER_X] > final_result[game.PLAYER_O]:
            results["X_win"] += 1
        elif final_result[game.PLAYER_O] > final_result[game.PLAYER_X]:
            results["O_win"] += 1
        else:
            results["draw"] += 1

    # -----------------------------------------------------------------------
    # Print summary
    # -----------------------------------------------------------------------

    print("\n=== Bot Match Results ===")
    print(f"Total games: {num_games}")
    print(f"X wins: {results['X_win']}")
    print(f"O wins: {results['O_win']}")
    print(f"Draws : {results['draw']}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run_series(NUM_GAMES)
