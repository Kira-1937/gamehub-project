from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict

CONFIG_ROOT = Path("configs")
CONFIG_ROOT.mkdir(exist_ok=True)


@dataclass
class GameConfig:
    name: str
    defaults: Dict[str, Any] = field(default_factory=dict)
    description: str = ""


@dataclass
class BotConfig:
    game: str
    bot: str
    values: Dict[str, Any] = field(default_factory=dict)


class ConfigStore:
    def __init__(
        self,
        game_path: Path | None = None,
        bot_path: Path | None = None,
    ) -> None:
        self.game_path = game_path or CONFIG_ROOT / "game_configs.json"
        self.bot_path = bot_path or CONFIG_ROOT / "bot_configs.json"
        self.games: Dict[str, GameConfig] = {}
        self.bots: Dict[str, Dict[str, BotConfig]] = {}
        self._load()

    def _load(self) -> None:
        if self.game_path.exists():
            data = json.loads(self.game_path.read_text())
            for name, payload in data.items():
                self.games[name.lower()] = GameConfig(
                    name=payload.get("name", name),
                    defaults=payload.get("defaults", {}),
                    description=payload.get("description", ""),
                )
        if self.bot_path.exists():
            data = json.loads(self.bot_path.read_text())
            for game_name, bot_map in data.items():
                self.bots.setdefault(game_name.lower(), {})
                for bot_name, values in bot_map.items():
                    self.bots[game_name.lower()][bot_name.lower()] = BotConfig(
                        game=game_name,
                        bot=bot_name,
                        values=values,
                    )

    def get_bot_config(self, game: str, bot: str) -> Dict[str, Any]:
        return dict(
            self.bots.get(game.lower(), {}).get(bot.lower(), BotConfig(game, bot)).values
        )

    def save_bot_config(self, game: str, bot: str, values: Dict[str, Any]) -> None:
        self.bots.setdefault(game.lower(), {})[bot.lower()] = BotConfig(
            game=game, bot=bot, values=dict(values)
        )
        self._persist(self.bot_path, self.bots)

    def register_game_config(self, config: GameConfig) -> None:
        self.games[config.name.lower()] = config
        self._persist(
            self.game_path,
            {
                name: {
                    "name": cfg.name,
                    "defaults": cfg.defaults,
                    "description": cfg.description,
                }
                for name, cfg in self.games.items()
            },
        )

    def _persist(self, path: Path, data: Dict[str, Any]) -> None:
        serialized: Dict[str, Any] = {}
        if path == self.bot_path:
            for game_name, bots in data.items():
                serialized[game_name] = {
                    bot_name: bot.values for bot_name, bot in bots.items()
                }
        else:
            serialized = data
        path.write_text(json.dumps(serialized, indent=2))


DEFAULT_STORE = ConfigStore()
