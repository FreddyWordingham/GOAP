from goap import Action, create_plan


# Initial state
initial_state = {
    "music_playing": False,
    "has_wood": False,
    "has_fire": False,
    "is_warm": False,
}

# Desired state
goal_state = {"is_warm": True}


# Possible actions
actions = [
    Action("play_the_piano", 3, {}, {"music_playing": True}),
    Action("sit_by_fire", 1, {"has_fire": True}, {"is_warm": True}),
    Action("gather_wood", 2, {}, {"has_wood": True}),
    Action("build_fire", 1, {"has_wood": True}, {"has_fire": True}),
]


# Formulate and print plan
plan, cost = create_plan(goal_state, actions, initial_state)
if plan:
    print("Plan found:", " -> ".join(a.name for a in plan), "| Total Cost:", cost)
else:
    print("No plan found")
