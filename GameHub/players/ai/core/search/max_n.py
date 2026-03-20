"""
Pure generic Max^n search.

Works for any sequential multi-player game where exactly one player moves
at each state.

All game knowledge is injected via callables.
"""

from __future__ import annotations
from typing import Callable, Iterable, Tuple, Optional, TypeVar, Sequence

from core.types import PlayerID, Result

StateT = TypeVar("StateT")
ActionT = TypeVar("ActionT")

# ---------------------------------------------------------------------------
# Injected behavior contracts
# ---------------------------------------------------------------------------

IsTerminalFn = Callable[[StateT], bool]
EvaluateFn = Callable[[StateT],Result]
NextStatesFn = Callable[[StateT], Iterable[Tuple[ActionT, StateT]]]
CurrentPlayerFn = Callable[[StateT], PlayerID]


# ---------------------------------------------------------------------------
# Max^n recursion
# ---------------------------------------------------------------------------

def max_n(
    state: StateT,
    *,
    is_terminal: IsTerminalFn,
    evaluate: EvaluateFn,
    next_states: NextStatesFn,
    current_player: CurrentPlayerFn,
    depth: Optional[int],
) -> Result:
    """
    Returns utility vector for the state.
    """

    # terminal or depth cutoff
    if is_terminal(state) or depth == 0:
        return evaluate(state)

    player = current_player(state)
    best_value: Optional[Result] = None

    for _, child in next_states(state):
        value = max_n(
            child,
            is_terminal=is_terminal,
            evaluate=evaluate,
            next_states=next_states,
            current_player=current_player,
            depth=None if depth is None else depth - 1,
        )

        if best_value is None or value[player] > best_value[player]:
            best_value = value

    if best_value is None:
        raise ValueError("No legal moves found.")

    return best_value


# ---------------------------------------------------------------------------
# Root decision
# ---------------------------------------------------------------------------

def max_n_decision(
    state: StateT,
    root_player: PlayerID,
    *,
    is_terminal: IsTerminalFn,
    evaluate: EvaluateFn,
    next_states: NextStatesFn,
    current_player: CurrentPlayerFn,
    depth: Optional[int],
) -> ActionT:
    """
    Return optimal action for root player.
    """

    best_action: Optional[ActionT] = None
    best_value: Optional[Result] = None

    for action, child in next_states(state):

        value = max_n(
            child,
            is_terminal=is_terminal,
            evaluate=evaluate,
            next_states=next_states,
            current_player=current_player,
            depth=None if depth is None else depth - 1,
        )

        if best_value is None or value[root_player] > best_value[root_player]:
            best_value = value
            best_action = action

    if best_action is None:
        raise ValueError("No legal actions available.")

    return best_action
