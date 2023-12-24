import heapq
from itertools import count
from typeguard import typechecked
from typing import List, Optional, Tuple, Dict

from .action import Action
from .state import State


def heuristic(current_state: State, goal: State) -> float:
    """
    Heuristic function for A* algorithm.
    Currently uses the number of different values between the current state and the goal state.

    Args:
        current_state (State): Current state.
        goal (State): Target state.

    Returns:
        float: Heuristic value.
    """

    return sum(current_state[k] != v for k, v in goal.items())


@typechecked
def create_plan(goal: State, actions: List[Action], start_state: State, max_depth: int = 100) -> Tuple[Optional[List[Action]], int]:
    """
    Find a plan to achieve the goal state using A* algorithm.

    Args:
        goal (State): Target state.
        actions (List[Action]): List of actions that can be performed.
        start_state (State): Initial state.
        max_depth (int, optional): Maximum depth of the search tree. Defaults to 100.

    Returns:
        Tuple[Optional[List[Action]], int]: Tuple of the plan and the total cost of the plan.
    """

    open_set = []
    unique_counter = count()  # Unique counter for tie-breaking
    # (f-cost, unique_counter, current_state, path, g-cost)
    heapq.heappush(open_set, (0, next(unique_counter), start_state, [], 0))
    visited_states = set()
    action_map = {i: action for i, action in enumerate(
        actions)}  # Mapping action indices to actions

    while open_set:
        _, _, current_state, path, g_cost = heapq.heappop(open_set)

        if tuple(current_state.items()) in visited_states:
            continue

        visited_states.add(tuple(current_state.items()))

        if all((current_state.get(k) == v if isinstance(v, bool) else current_state.get(k, 0) >= v) for k, v in goal.items()):
            # Reconstruct path with actions
            return [action_map[action_id] for action_id in path], g_cost

        if len(path) > max_depth:
            break

        for action_id, action in action_map.items():
            if action.is_doable(current_state):
                new_state = action.apply(current_state)
                if new_state != current_state:
                    new_path = path + [action_id]
                    new_g_cost = g_cost + action.cost
                    f_cost = new_g_cost + heuristic(new_state, goal)
                    heapq.heappush(open_set, (f_cost, next(
                        unique_counter), new_state, new_path, new_g_cost))

    return None, 1000
