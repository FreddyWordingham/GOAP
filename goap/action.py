from typeguard import typechecked

from .state import State


class Action:
    """An action that can be performed by an agent."""

    @typechecked
    def __init__(self, name: str, cost: int, preconditions: State, effects: State):
        """Construct an action.

        Args:
            name (str): Name of the action.
            cost (int): Cost of the action.
            preconditions (State): What the state must be for the action to be performed.
            effects (State): Mutations to the state that occur when the action is performed.
        """

        self.name = name
        self.cost = cost
        self.preconditions = preconditions
        self.effects = effects

    @typechecked
    def is_doable(self, state: State) -> bool:
        """Check that the action can be performed in the given state.

        Args:
            state (State): The state to check.

        Returns:
            bool: True if the action can be performed in the given state.
        """

        for key, value in self.preconditions.items():
            if key in state:
                # Compare values considering type (bool or int)
                if isinstance(value, bool) and isinstance(state[key], bool):
                    if state[key] != value:
                        return False
                elif isinstance(value, int) and isinstance(state[key], int):
                    if state[key] < value:  # Assuming integer comparison is a minimum threshold
                        return False
                else:
                    # Mismatched types, precondition not met
                    return False
            else:
                # Key not in state, precondition not met
                return False
        return True

    @typechecked
    def apply(self, state: State) -> State:
        """Update the state with the effects of the action.

        Args:
            state (State): The initial state to update.

        Returns:
            Dict[str, bool | int]: The updated state.
        """

        new_state = state.copy()

        for key, value in self.effects.items():
            if isinstance(value, bool):
                new_state[key] = value
            elif isinstance(value, int):
                new_state[key] = new_state.get(key, 0) + value

        return new_state
