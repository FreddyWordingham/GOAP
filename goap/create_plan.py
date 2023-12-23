from typeguard import typechecked
from typing import List, Tuple

from .action import Action
from .state import State


@typechecked
def create_plan(goal: State, actions: List[Action], state: State, depth: int = 0, max_depth: int = 100) -> Tuple[List[Action], int]:
    """Find a plan to achieve the goal state.

    Args:
        goal (State): State to achieve.
        actions (List[Action]): List of actions that can be performed.
        state (State): Current state.
        depth (int, optional): Current search depth. Defaults to 0.
        max_depth (int, optional): Maximum depth to test. Defaults to 10.

    Returns:
        Tuple[List[Action], int]: The plan of actions, and the total cost.
    """

    if depth > max_depth:
        return None, float("inf")

    if all(state.get(k, False) == v for k, v in goal.items()):
        return [], 0

    plans = []
    for action in actions:
        if action.is_doable(state):
            new_state = action.apply(state)
            # Check if state has changed, to avoid infinite recursion
            if new_state != state:
                sub_plan, sub_cost = create_plan(
                    goal, actions, new_state, depth + 1, max_depth)
                if sub_plan is not None:
                    plans.append(([action] + sub_plan, action.cost + sub_cost))

    if not plans:
        return None, float("inf")

    return min(plans, key=lambda x: x[1])
