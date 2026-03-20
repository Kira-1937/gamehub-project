from __future__ import annotations

from collections import Counter

from core.simultaneous import SimultaneousMatch
from core.types import PlayerID

from games.rps.game import RockPaperScissorsGame
from players.ai.games.rps.random import RandomRockPaperScissorsPlayer

NUM_GAMES = 20

def run_series(num_games: int) -> None:
    game = RockPaperScissorsGame(max_rounds=5)
    results = Counter()

    for _ in range(num_games):
        players: dict[PlayerID, RandomRockPaperScissorsPlayer] = {
            player: RandomRockPaperScissorsPlayer(player, seed=None)
            for player in game.PLAYERS
        }

        match = SimultaneousMatch(game=game, players=players)
        final_result, _ = match.run()

        if final_result[game.PLAYER_A] > final_result[game.PLAYER_B]:
            results["A_win"] += 1
        elif final_result[game.PLAYER_B] > final_result[game.PLAYER_A]:
            results["B_win"] += 1
        else:
            results["draw"] += 1

    print("\n=== Rock-Paper-Scissors Series ===")
    print(f"Total games: {num_games}")
    print(f"A wins: {results['A_win']}")
    print(f"B wins: {results['B_win']}")
    print(f"Draws: {results['draw']}")


if __name__ == "__main__":
    run_series(NUM_GAMES)
