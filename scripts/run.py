from goap import Action, create_plan


# Initial state
initial_state = {
    "music_playing": False,
    "wood_count": 0,
    "has_fire": False,
    "is_warm": False,
}

# Desired state
goal_state = {"is_warm": True}


# Possible actions
actions = [
    Action("play_the_piano", 3, {}, {"music_playing": True}),
    Action("gather_wood", 2, {}, {"wood_count": 1}),
    Action("build_fire", 1, {"wood_count": 3}, {"has_fire": True}),
    Action("sit_by_fire", 1, {"has_fire": True}, {"is_warm": True}),
]


# Formulate and print plan
plan, cost = create_plan(goal_state, actions, initial_state)
if plan:
    print("Plan found:", " -> ".join(a.name for a in plan), "| Total Cost:", cost)
else:
    print("No plan found")
