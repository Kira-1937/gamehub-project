from __future__ import annotations

import json
from pathlib import Path

from core.events import ActionTaken, EventHandler, MatchEvent, MatchEnded, TurnStarted


class SimpleWebBridge(EventHandler):
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or Path("tmp/web_view.json")
        self.path.parent.mkdir(exist_ok=True, parents=True)

    def handle(self, event: MatchEvent) -> None:
        payload = {"type": event.__class__.__name__}

        if isinstance(event, TurnStarted):
            payload["player"] = event.player
        elif isinstance(event, ActionTaken):
            payload["player"] = event.player
            payload["action"] = event.action
        elif isinstance(event, MatchEnded):
            payload["result"] = event.result

        payload["state"] = repr(event.state)

        self.path.write_text(json.dumps(payload, indent=2))
