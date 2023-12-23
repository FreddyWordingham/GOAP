from typeguard import typechecked
from typing import List, Tuple

from .action import Action
from .state import State


# @typechecked
# def plan(goal: State, actions: List[Action], state: State) -> List[Action]:
#     """Plan a sequence of actions that will achieve the given goal.

#     Args:
#         goal (State): The goal state.
#         actions (List[Action]): The actions that can be performed.
#         state (State): The initial state.

#     Returns:
#         Tuple[List[Action], State]: The sequence of actions that will achieve the goal and the final state.
#     """

#     if all(state.get(k, False) == v for k, v in goal.items()):
#         return []

#     applicable_actions = [a for a in actions if a.is_doable(state)]

#     if not applicable_actions:
#         return []

#     plans = []
#     for action in applicable_actions:
#         new_state = action.apply(state)
#         sub_plan = plan(goal, actions, new_state)
#         if sub_plan is not None:
#             plans.append(([action] + sub_plan, action.cost +
#                          sum(a.cost for a in sub_plan)))

#     if not plans:
#         return []

#     return min(plans, key=lambda x: x[1])


def plan(goal, actions, state, depth=0, max_depth=10):
    if depth > max_depth:
        return None, float('inf')

    if all(state.get(k, False) == v for k, v in goal.items()):
        return [], 0

    plans = []
    for action in actions:
        if action.is_doable(state):
            new_state = action.apply(state)
            # Check if state has changed, to avoid infinite recursion
            if new_state != state:
                sub_plan, sub_cost = plan(
                    goal, actions, new_state, depth + 1, max_depth)
                if sub_plan is not None:
                    plans.append(([action] + sub_plan, action.cost + sub_cost))

    if not plans:
        return None, float('inf')

    return min(plans, key=lambda x: x[1])
