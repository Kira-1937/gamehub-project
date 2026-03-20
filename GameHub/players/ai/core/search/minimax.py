"""
Pure generic Minimax with alpha-beta pruning.

Knows NOTHING about any specific game.
All game knowledge is injected via callables.
"""

from __future__ import annotations
from typing import Callable, Iterable, Tuple, Optional, TypeVar

from core.types import PlayerID

StateT = TypeVar("StateT")
ActionT = TypeVar("ActionT")


# ---------------------------------------------------------------------------
# Injected behavior contracts
# ---------------------------------------------------------------------------

IsTerminalFn = Callable[[StateT], bool]
EvaluateFn = Callable[[StateT, PlayerID], float]
NextStatesFn = Callable[[StateT], Iterable[Tuple[ActionT, StateT]]]
CurrentPlayerFn = Callable[[StateT], PlayerID]


# ---------------------------------------------------------------------------
# Core minimax recursion
# ---------------------------------------------------------------------------

def minimax(
    state: StateT,
    root_player: PlayerID,
    *,
    is_terminal: IsTerminalFn,
    evaluate: EvaluateFn,
    next_states: NextStatesFn,
    current_player: CurrentPlayerFn,
    depth: Optional[int],
    alpha: float,
    beta: float,
) -> float:
    """
    Return minimax value of a state from root_player perspective.
    """

    # --- terminal or depth cutoff ---
    if is_terminal(state) or depth == 0:
        return evaluate(state, root_player)

    maximizing = current_player(state) == root_player

    # --- maximizing branch ---
    if maximizing:
        value = float("-inf")

        for _, child in next_states(state):
            value = max(
                value,
                minimax(
                    child,
                    root_player,
                    is_terminal=is_terminal,
                    evaluate=evaluate,
                    next_states=next_states,
                    current_player=current_player,
                    depth=None if depth is None else depth - 1,
                    alpha=alpha,
                    beta=beta,
                ),
            )

            alpha = max(alpha, value)
            if beta <= alpha:
                break

        return value

    # --- minimizing branch ---
    else:
        value = float("inf")

        for _, child in next_states(state):
            value = min(
                value,
                minimax(
                    child,
                    root_player,
                    is_terminal=is_terminal,
                    evaluate=evaluate,
                    next_states=next_states,
                    current_player=current_player,
                    depth=None if depth is None else depth - 1,
                    alpha=alpha,
                    beta=beta,
                ),
            )

            beta = min(beta, value)
            if beta <= alpha:
                break

        return value


# ---------------------------------------------------------------------------
# Decision helper
# ---------------------------------------------------------------------------

def minimax_decision(
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
    Return optimal action for the player to move in `state`.
    """

    root_is_maximizing = current_player(state) == root_player

    best_action: Optional[ActionT] = None
    best_value = float("-inf") if root_is_maximizing else float("inf")

    for action, child in next_states(state):
        value = minimax(
            child,
            root_player,
            is_terminal=is_terminal,
            evaluate=evaluate,
            next_states=next_states,
            current_player=current_player,
            depth=None if depth is None else depth - 1,
            alpha=float("-inf"),
            beta=float("inf"),
        )

        if root_is_maximizing:
            if best_action is None or value > best_value:
                best_value = value
                best_action = action
        else:
            if best_action is None or value < best_value:
                best_value = value
                best_action = action

    if best_action is None:
        raise ValueError("No legal actions available.")

    return best_action
