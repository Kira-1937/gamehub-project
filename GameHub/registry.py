from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, Optional, Sequence, TypeVar

from core.game import Game
from core.player import Player
from core.simultaneous import SimultaneousGame
from core.types import PlayerID
from interaction.port import InteractionPort, NullInteraction

SequentialGameFactory = Callable[[], Game]
SimultaneousGameFactory = Callable[[], SimultaneousGame]
SequentialBotFactory = Callable[[PlayerID, InteractionPort | None], Player]
SimultaneousBotFactory = Callable[[PlayerID], Player]
InteractionFactory = Callable[[], InteractionPort]

ConfigParser = Callable[[str], Any]

T = TypeVar("T")


@dataclass
class _Entry:
    display_name: str
    factory: T


@dataclass
class ConfigPrompt:
    key: str
    prompt: str
    parser: ConfigParser
    default: str | None = None


@dataclass
class BotEntry:
    display_name: str
    factory: T
    config_prompts: Sequence[ConfigPrompt] = ()


_sequential_games: Dict[str, _Entry[SequentialGameFactory]] = {}
_simultaneous_games: Dict[str, _Entry[SimultaneousGameFactory]] = {}
_sequential_bots: Dict[str, Dict[str, BotEntry[SequentialBotFactory]]] = defaultdict(dict)
_simultaneous_bots: Dict[str, Dict[str, BotEntry[SimultaneousBotFactory]]] = defaultdict(dict)
_interaction_factories: Dict[str, InteractionFactory] = {}


def register_sequential_game(name: str, factory: SequentialGameFactory) -> None:
    _sequential_games[name.lower()] = _Entry(display_name=name, factory=factory)


def register_simultaneous_game(name: str, factory: SimultaneousGameFactory) -> None:
    _simultaneous_games[name.lower()] = _Entry(display_name=name, factory=factory)


def register_sequential_bot(
    game_name: str,
    bot_name: str,
    factory: SequentialBotFactory,
    config_prompts: Sequence[ConfigPrompt] | None = None,
) -> None:
    _sequential_bots[game_name.lower()][bot_name.lower()] = BotEntry(
        display_name=bot_name,
        factory=factory,
        config_prompts=tuple(config_prompts or ()),
    )


def register_simultaneous_bot(
    game_name: str,
    bot_name: str,
    factory: SimultaneousBotFactory,
    config_prompts: Sequence[ConfigPrompt] | None = None,
) -> None:
    _simultaneous_bots[game_name.lower()][bot_name.lower()] = BotEntry(
        display_name=bot_name,
        factory=factory,
        config_prompts=tuple(config_prompts or ()),
    )


def register_interaction(game_name: str, factory: InteractionFactory) -> None:
    _interaction_factories[game_name.lower()] = factory


def list_sequential_games() -> Iterable[str]:
    return tuple(entry.display_name for entry in _sequential_games.values())


def list_simultaneous_games() -> Iterable[str]:
    return tuple(entry.display_name for entry in _simultaneous_games.values())


def list_sequential_bots(game_name: str) -> Iterable[str]:
    return tuple(
        entry.display_name for entry in _sequential_bots.get(game_name.lower(), {}).values()
    )


def list_simultaneous_bots(game_name: str) -> Iterable[str]:
    return tuple(
        entry.display_name
        for entry in _simultaneous_bots.get(game_name.lower(), {}).values()
    )


def sequential_game_entries() -> Iterable[tuple[str, str]]:
    return tuple((key, entry.display_name) for key, entry in _sequential_games.items())


def simultaneous_game_entries() -> Iterable[tuple[str, str]]:
    return tuple((key, entry.display_name) for key, entry in _simultaneous_games.items())


def sequential_bot_entries(game_name: str) -> Iterable[tuple[str, str]]:
    return tuple(
        (key, entry.display_name)
        for key, entry in _sequential_bots.get(game_name.lower(), {}).items()
    )


def simultaneous_bot_entries(game_name: str) -> Iterable[tuple[str, str]]:
    return tuple(
        (key, entry.display_name)
        for key, entry in _simultaneous_bots.get(game_name.lower(), {}).items()
    )


def get_sequential_game_factory(name: str) -> Optional[SequentialGameFactory]:
    entry = _sequential_games.get(name.lower())
    return entry.factory if entry is not None else None


def get_simultaneous_game_factory(name: str) -> Optional[SimultaneousGameFactory]:
    entry = _simultaneous_games.get(name.lower())
    return entry.factory if entry is not None else None


def make_sequential_bot(
    game_name: str,
    bot_name: str,
    player_id: PlayerID,
    interaction: InteractionPort | None,
    config: dict[str, Any],
) -> Player:
    entry = _sequential_bots[game_name.lower()][bot_name.lower()]
    return entry.factory(player_id, interaction, config)


def make_simultaneous_bot(
    game_name: str, bot_name: str, player_id: PlayerID, config: dict[str, Any]
) -> Player:
    entry = _simultaneous_bots[game_name.lower()][bot_name.lower()]
    return entry.factory(player_id, config)


def get_sequential_bot_entry(
    game_name: str, bot_key: str
) -> BotEntry[SequentialBotFactory]:
    return _sequential_bots[game_name.lower()][bot_key.lower()]


def get_simultaneous_bot_entry(
    game_name: str, bot_key: str
) -> BotEntry[SimultaneousBotFactory]:
    return _simultaneous_bots[game_name.lower()][bot_key.lower()]


def get_interaction(game_name: str) -> InteractionPort:
    factory = _interaction_factories.get(game_name.lower())
    return factory() if factory is not None else NullInteraction()
