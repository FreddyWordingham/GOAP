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

        return all(state.get(k, False) == v for k, v in self.preconditions.items())

    @typechecked
    def apply(self, state: State) -> State:
        """Update the state with the effects of the action.

        Args:
            state (State): The initial state to update.

        Returns:
            Dict[str, bool | int]: The updated state.
        """

        new_state = state.copy()
        new_state.update(self.effects)
        return new_state
