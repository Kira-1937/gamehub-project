from __future__ import annotations

from config_store import DEFAULT_STORE, GameConfig
from interaction.cli import ChessCLIInteraction
from players.ai.games.chess.minimax import MinimaxChessPlayer
from players.ai.games.chess.random import RandomChessPlayer
from players.human.cli_chess import HumanCLIChessPlayer
from registry import (
    ConfigPrompt,
    register_interaction,
    register_sequential_bot,
    register_sequential_game,
)

from .game import ChessGame


def _human_factory(player_id, interaction, config):
    if interaction is None:
        raise ValueError("Human players require an interaction port.")
    return HumanCLIChessPlayer(player_id, interaction)


register_sequential_game("chess", ChessGame)
register_interaction("chess", ChessCLIInteraction)

register_sequential_bot("chess", "human", _human_factory)
register_sequential_bot(
    "chess",
    "random",
    lambda player_id, interaction, config: RandomChessPlayer(
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
    "chess",
    "minimax",
    lambda player_id, interaction, config: MinimaxChessPlayer(
        player_id, depth=config.get("depth", 2)
    ),
    config_prompts=(
        ConfigPrompt(
            key="depth",
            prompt="Enter depth limit for chess minimax",
            parser=lambda raw: int(raw.strip()),
            default="2",
        ),
    ),
)

__all__ = ["ChessGame"]


DEFAULT_STORE.register_game_config(
    GameConfig(
        name="chess",
        defaults={"starting_fen": "standard"},
        description="Standard chess with sequential turns and UCI move input.",
    )
)
