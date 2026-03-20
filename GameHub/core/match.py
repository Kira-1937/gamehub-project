from __future__ import annotations
from typing import Dict, Iterable, List, Tuple

from .events import ActionTaken, EventBus, MatchEnded, TurnStarted
from .game import Game
from .player import Player
from .state import State
from .types import PlayerID, JointAction, Result

class Match:

    def __init__(self, game: Game, players: Dict[PlayerID, Player], event_bus: EventBus | None = None):
        self.game = game
        self.players = players
        self._event_bus = event_bus

    def _publish(self, event) -> None:
        if self._event_bus is not None:
            self._event_bus.publish(event)


    def run(self) -> Tuple[Result, List[State]]:
        state = self.game.initial_state()
        history: List[State] = [state]

        while not self.game.is_terminal(state):

            active = self.game.active_players(state)

            joint_action: JointAction = {}

            for pid in active:
                player = self.players[pid]

                self._publish(TurnStarted(state=state, player=pid))

                legal = self.game.legal_actions(state, pid)

                action = player.select_action(state, legal)

                self._publish(ActionTaken(state=state, player=pid, action=action))

                joint_action[pid] = action

            state = self.game.next_state(state, joint_action)
            history.append(state)
        result = self.game.result(state)
        self._publish(MatchEnded(state=state, result=result))
        return result, history
