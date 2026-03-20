from __future__ import annotations

from config_store import DEFAULT_STORE, GameConfig
from registry import ConfigPrompt, register_simultaneous_bot, register_simultaneous_game

from .game import RockPaperScissorsGame
from players.ai.games.rps.random import RandomRockPaperScissorsPlayer


register_simultaneous_game("rock-paper-scissors", RockPaperScissorsGame)
register_simultaneous_bot(
    "rock-paper-scissors",
    "random",
    lambda player_id, config: RandomRockPaperScissorsPlayer(
        player_id, seed=config.get("seed")
    ),
    config_prompts=(
        ConfigPrompt(
            key="seed",
            prompt="Optional RNG seed for RPS bots (blank = random)",
            parser=lambda raw: None if raw.strip() == "" else int(raw.strip()),
            default="",
        ),
    ),
)

__all__ = ["RockPaperScissorsGame"]


DEFAULT_STORE.register_game_config(
    GameConfig(
        name="rock-paper-scissors",
        defaults={"rounds": 5},
        description="Simultaneous rock-paper-scissors best-of series.",
    )
)
