from goap import Action, plan


actions = [
    Action("play_the_piano", 3, {}, {"music_playing": True}),
    Action("sit_by_fire", 1, {"has_fire": True}, {"is_warm": True}),
    Action("gather_wood", 2, {}, {"has_wood": True}),
    Action("build_fire", 1, {"has_wood": True}, {"has_fire": True}),
]

goal = {"is_warm": True}

initial_state = {
    "music_playing": False,
    "has_wood": False,
    "has_fire": False,
    "is_warm": False,
}

p, cost = plan(goal, actions, initial_state)
if p:
    print("Plan found:", " -> ".join(a.name for a in p), "| Total Cost:", cost)
else:
    print("No plan found")
