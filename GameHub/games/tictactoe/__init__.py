from __future__ import annotations

from interaction.cli import TicTacToeCLIInteraction
from players.ai.games.tictactoe.max_n import MaxnTicTacToePlayer
from players.ai.games.tictactoe.minimax import MinimaxTicTacToePlayer
from players.ai.games.tictactoe.random import RandomTicTacToePlayer
from players.human.cli_ttt import HumanCLITicTacToePlayer

from config_store import DEFAULT_STORE, GameConfig
from registry import (
    ConfigPrompt,
    register_interaction,
    register_sequential_bot,
    register_sequential_game,
)

from .game import TicTacToeGame


def _human_factory(player_id, interaction, config):
    if interaction is None:
        raise ValueError("Human players require an interaction port.")
    return HumanCLITicTacToePlayer(player_id, interaction)


register_sequential_game("tictactoe", TicTacToeGame)
register_interaction("tictactoe", TicTacToeCLIInteraction)

register_sequential_bot("tictactoe", "human", _human_factory)
register_sequential_bot(
    "tictactoe",
    "random",
    lambda player_id, interaction, config: RandomTicTacToePlayer(
        player_id, seed=config.get("seed")
    ),
    config_prompts=(
        ConfigPrompt(
            key="seed",
            prompt="Optional RNG seed for repeatable randomness (blank = random)",
            parser=lambda raw: None if raw.strip() == "" else int(raw.strip()),
            default="",
        ),
    ),
)
register_sequential_bot(
    "tictactoe",
    "minimax",
    lambda player_id, interaction, config: MinimaxTicTacToePlayer(
        player_id, depth=config.get("depth")
    ),
    config_prompts=(
        ConfigPrompt(
            key="depth",
            prompt="Enter depth limit (blank for perfect play)",
            parser=lambda raw: None if raw.strip() == "" else int(raw.strip()),
            default="",
        ),
    ),
)
register_sequential_bot(
    "tictactoe",
    "max_n",
    lambda player_id, interaction, config: MaxnTicTacToePlayer(
        player_id, depth=config.get("depth")
    ),
    config_prompts=(
        ConfigPrompt(
            key="depth",
            prompt="Enter depth limit for Max^n (blank for full search)",
            parser=lambda raw: None if raw.strip() == "" else int(raw.strip()),
            default="",
        ),
    ),
)

__all__ = [
    "TicTacToeGame",
]


DEFAULT_STORE.register_game_config(
    GameConfig(
        name="tictactoe",
        defaults={"board_size": 3},
        description="Classic 3x3 Tic-Tac-Toe with sequential turns.",
    )
)
