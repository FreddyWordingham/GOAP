from typeguard import typechecked
from typing import List, Optional, Tuple

from .action import Action
from .state import State


@typechecked
def create_plan(goal: State, actions: List[Action], state: State, visited_states: Optional[set] = None, depth: int = 0, max_depth: int = 100) -> Tuple[Optional[List[Action]], int]:
    """Find a plan to achieve the goal state."""

    if visited_states is None:
        visited_states = set()

    if depth > max_depth or tuple(state.items()) in visited_states:
        return None, 1000

    visited_states.add(tuple(state.items()))

    if all((state.get(k) == v if isinstance(v, bool) else state.get(k, 0) >= v) for k, v in goal.items()):
        return [], 0

    plans = []
    for action in actions:
        if action.is_doable(state):
            new_state = action.apply(state)
            # Check if state has changed, to avoid infinite recursion
            if new_state != state:
                sub_plan, sub_cost = create_plan(
                    goal, actions, new_state, visited_states, depth + 1, max_depth)
                if sub_plan is not None:
                    plans.append(([action] + sub_plan, action.cost + sub_cost))

    if not plans:
        return None, 1000

    return min(plans, key=lambda x: x[1])
