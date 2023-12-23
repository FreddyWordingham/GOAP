# GOAP

<p align="center">
  <img src="./resources/logo.png" alt="GOAP logo" width="200" height="200">
</p>

GOAP (Goal-Oriented Action Planning) is a form of declarative programming used in artificial intelligence systems.
It involves defining a set of actions that can be performed by an agent, each with preconditions and effects, to achieve specified goals within a dynamic environment.

## Example

Import the library:

```python
from goap import Action, plan
```

And define the current `State` of the world as:

```python
initial_state = {
    "music_playing": False,
    "has_wood": False,
    "has_fire": False,
    "is_warm": False,
}
```

And the goal we would like to achieve as:

```python
goal_state = {
    "is_warm": True,
}
```

And then we define a set of possible `Actions`:

```python
actions = [
    Action("play_the_piano", 3, {}, {"music_playing": True}),
    Action("sit_by_fire", 1, {"has_fire": True}, {"is_warm": True}),
    Action("gather_wood", 2, {}, {"has_wood": True}),
    Action("build_fire", 1, {"has_wood": True}, {"has_fire": True}),
]
```

> Note: The `Action` class takes four arguments: `name`, `cost`, `preconditions`, and `effects`.

Finally, we can `create_plan` to find the optimal plan of action to achieve the desired state:

```python
plan, cost = create_plan(goal, actions, initial_state)
```

This particular example will return the following plan:

```
Plan found: gather_wood -> build_fire -> sit_by_fire | Total Cost: 4
```

## Quickstart

Clone the repository and set the root folder as the current working directory:

```shell
git clone https://github.com/FreddyWordingham/GOAP.git goap
cd goap
```

Install the package using Poetry:

```shell
poetry env use python@3.10
poetry install
```

And then run one of the example scripts:

```shell
poetry run python scripts/run.py
```
