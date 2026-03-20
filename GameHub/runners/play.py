from __future__ import annotations

from core.events import EventBus, EventHandler
from core.match import Match
from core.player import Player
from core.simultaneous import SimultaneousMatch
from core.types import PlayerID
from typing import Any, Iterable, Sequence

from config_store import DEFAULT_STORE
from interaction.port import InteractionPort
from interaction.terminal import TerminalLogger
from interaction.web import SimpleWebBridge

import games  # ensure game modules register themselves

from registry import (
    ConfigPrompt,
    get_interaction,
    get_sequential_bot_entry,
    get_sequential_game_factory,
    get_simultaneous_bot_entry,
    get_simultaneous_game_factory,
    make_sequential_bot,
    make_simultaneous_bot,
    sequential_bot_entries,
    sequential_game_entries,
    simultaneous_bot_entries,
    simultaneous_game_entries,
)


def choose_index(label: str, options: list[str]) -> int | None:
    print(f"\n{label}")
    for idx, option in enumerate(options, start=1):
        print(f"  {idx}. {option}")
    choice = input("Choose a number (or press Enter to go back): ").strip()
    if choice == "":
        return None
    try:
        index = int(choice)
    except ValueError:
        print("Invalid choice.")
        return -1

    if 1 <= index <= len(options):
        return index - 1

    print("Choice out of range.")
    return -1


def choose_entry(label: str, entries: list[tuple[str, str]]) -> str | None:
    while True:
        index = choose_index(label, [entry[1] for entry in entries])
        if index is None:
            return None
        if index >= 0:
            return entries[index][0]


def choose_game_type() -> str | None:
    options = ["Sequential games", "Simultaneous games", "Quit"]
    while True:
        index = choose_index("Select the game type you want to play:", options)
        if index is None or index == 2:
            return None
        if index >= 0:
            return "sequential" if index == 0 else "simultaneous"


CONFIG_STORE = DEFAULT_STORE


def gather_bot_config(
    prompts: Sequence[ConfigPrompt], stored: dict[str, Any]
) -> dict[str, Any]:
    config = dict(stored)

    if not prompts:
        return config

    if stored:
        print("Loaded saved configuration — press Enter to reuse values or override.")

    for prompt in prompts:
        default = config.get(prompt.key, prompt.default)
        label = prompt.prompt
        if default is not None:
            label += f" [{default}]"

        while True:
            raw = input(f"{label}: ").strip()
            if raw == "" and default is not None:
                raw = str(default)

            try:
                value = prompt.parser(raw)
                config[prompt.key] = value
                break
            except Exception as exc:
                print(f"Invalid value: {exc}")

    return config


def make_event_bus(interaction: InteractionPort | None) -> EventBus:
    event_bus = EventBus()
    if isinstance(interaction, EventHandler):
        event_bus.subscribe(interaction)

    event_bus.subscribe(TerminalLogger())
    event_bus.subscribe(SimpleWebBridge())
    return event_bus


def pick_sequential_bots(
    game_name: str, player_ids: list[PlayerID], interaction: InteractionPort
) -> dict[PlayerID, Player]:
    players: dict[PlayerID, Player] = {}
    entries = list(sequential_bot_entries(game_name))
    if not entries:
        raise RuntimeError(f"No bots registered for {game_name}")

    for pid in player_ids:
        bot_key = choose_entry(f"Choose a bot for {pid}:", entries)
        if bot_key is None:
            raise KeyboardInterrupt

        entry = get_sequential_bot_entry(game_name, bot_key)
        stored = CONFIG_STORE.get_bot_config(game_name, bot_key)
        config = gather_bot_config(entry.config_prompts, stored)
        CONFIG_STORE.save_bot_config(game_name, bot_key, config)
        players[pid] = make_sequential_bot(
            game_name, bot_key, pid, interaction, config
        )

    return players


def pick_simultaneous_bots(
    game_name: str, player_ids: list[PlayerID]
) -> dict[PlayerID, Player]:
    players: dict[PlayerID, Player] = {}
    entries = list(simultaneous_bot_entries(game_name))
    if not entries:
        raise RuntimeError(f"No bots registered for {game_name}")

    for pid in player_ids:
        bot_key = choose_entry(f"Choose a bot for {pid}:", entries)
        if bot_key is None:
            raise KeyboardInterrupt

        entry = get_simultaneous_bot_entry(game_name, bot_key)
        stored = CONFIG_STORE.get_bot_config(game_name, bot_key)
        config = gather_bot_config(entry.config_prompts, stored)
        CONFIG_STORE.save_bot_config(game_name, bot_key, config)
        players[pid] = make_simultaneous_bot(game_name, bot_key, pid, config)

    return players


def run_sequential() -> None:
    entries = list(sequential_game_entries())
    if not entries:
        print("No sequential games registered.")
        return

    game_key = choose_entry("Pick a sequential game:", entries)
    if not game_key:
        return

    factory = get_sequential_game_factory(game_key)
    if factory is None:
        print("Game not registered.")
        return

    game = factory()
    interaction = get_interaction(game_key)
    player_ids = list(game.player_ids())

    try:
        players = pick_sequential_bots(game_key, player_ids, interaction)
    except KeyboardInterrupt:
        print("Bot selection cancelled.")
        return

    event_bus = make_event_bus(interaction)
    match = Match(game=game, players=players, event_bus=event_bus)
    result, history = match.run()
    interaction.show_result(result, history[-1])


def run_simultaneous() -> None:
    entries = list(simultaneous_game_entries())
    if not entries:
        print("No simultaneous games registered.")
        return

    game_key = choose_entry("Pick a simultaneous game:", entries)
    if not game_key:
        return

    factory = get_simultaneous_game_factory(game_key)
    if factory is None:
        print("Game not registered.")
        return

    game = factory()
    player_ids = list(game.player_ids())

    try:
        players = pick_simultaneous_bots(game_key, player_ids)
    except KeyboardInterrupt:
        print("Bot selection cancelled.")
        return

    event_bus = make_event_bus(None)
    match = SimultaneousMatch(game=game, players=players, event_bus=event_bus)
    result, history = match.run()
    print("\nMatch complete. Results:")
    for pid, reward in result.items():
        print(f"  {pid}: {reward}")


def main() -> None:
    while True:
        choice = choose_game_type()
        if choice is None:
            print("Goodbye.")
            return

        if choice == "sequential":
            run_sequential()
        else:
            run_simultaneous()


if __name__ == "__main__":
    main()
