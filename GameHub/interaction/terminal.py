from __future__ import annotations

from core.events import ActionTaken, EventHandler, MatchEvent, MatchEnded, TurnStarted


class TerminalLogger(EventHandler):
    def __init__(self, title: str | None = None) -> None:
        self.title = title or "Match"
        self._turn = 0

    def handle(self, event: MatchEvent) -> None:
        if isinstance(event, TurnStarted):
            self._turn += 1
            print(f"[{self.title}] Turn {self._turn} start – Player {event.player}")

        elif isinstance(event, ActionTaken):
            print(
                f"[{self.title}] Player {event.player} chose action: {event.action}"
            )

        elif isinstance(event, MatchEnded):
            print(f"[{self.title}] Match ended with result: {event.result}")
