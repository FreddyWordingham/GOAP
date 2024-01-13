use std::cmp::Ordering;

#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
struct Vec2 {
    x: i32,
    y: i32,
}

impl Vec2 {
    fn new(x: i32, y: i32) -> Self {
        Self { x, y }
    }
}

fn main() {
    let world_state = WorldState {
        player_position: Vec2::new(0, 0),
        has_weapon: false,
        enemy_alive: true,
        num_wood: 0,
        has_bonfire: false,
    };
    println!("INIT: {:?}", world_state);

    let goal_state = WorldState {
        player_position: Vec2::new(14, 7),
        has_weapon: true,
        enemy_alive: false,
        num_wood: 0,
        has_bonfire: true,
    };
    println!("GOAL: {:?}", goal_state);

    println!("PLAN:");
    let plan = plan_actions(&world_state, &goal_state);
    for (n, action) in plan.iter().enumerate() {
        println!("{} > {}", n, action.as_str());
    }
}

// == STATE ==

const NUM_WOOD_NEEDED_FOR_BONFIRE: u32 = 10;

#[derive(Clone, Debug, PartialEq, Eq, Hash)]
struct WorldState {
    player_position: Vec2,
    has_weapon: bool,
    enemy_alive: bool,
    num_wood: u32,
    has_bonfire: bool,
}

impl WorldState {
    /// Generate and return all possible actions for the given state
    fn get_possible_actions(state: &WorldState) -> Vec<BasicAction> {
        let mut actions = Vec::new();

        if !state.has_weapon {
            actions.push(BasicAction::PickUpWeapon);
        }

        if state.has_weapon && state.enemy_alive {
            actions.push(BasicAction::AttackEnemy);
        }

        actions.push(BasicAction::PickUpWood);

        if state.num_wood >= NUM_WOOD_NEEDED_FOR_BONFIRE {
            actions.push(BasicAction::LightBonfire);
        }

        // Add all possible walk actions
        for x in -1..=1 {
            for y in -1..=1 {
                if x == 0 && y == 0 {
                    continue;
                }
                actions.push(BasicAction::Walk(Vec2::new(x, y)));
            }
        }

        actions
    }

    // Adjust this method based on your new goal condition for wood
    fn matches_goal(&self, goal_state: &WorldState) -> bool {
        self.player_position == goal_state.player_position
            && self.has_weapon == goal_state.has_weapon
            && self.enemy_alive == goal_state.enemy_alive
            && self.has_bonfire == goal_state.has_bonfire
        // Ignore num_wood or handle it differently
    }
}

// == ACTION ==

trait Action {
    fn as_str(&self) -> String;
    fn execute(&self, world_state: &mut WorldState);
    fn can_execute(&self, world_state: &WorldState) -> bool;
}

// == BASIC ACTIONS ==

#[derive(Clone, Debug)]
enum BasicAction {
    Walk(Vec2),
    PickUpWeapon,
    AttackEnemy,
    PickUpWood,
    LightBonfire,
}

impl Action for BasicAction {
    fn as_str(&self) -> String {
        match self {
            BasicAction::Walk(delta) => format!("Walk {},{}", delta.x, delta.y).to_owned(),
            BasicAction::PickUpWeapon => "PickUpWeapon".to_owned(),
            BasicAction::AttackEnemy => "AttackEnemy".to_owned(),
            BasicAction::PickUpWood => "PickUpWood".to_owned(),
            BasicAction::LightBonfire => "LightBonfire".to_owned(),
        }
    }

    fn execute(&self, world_state: &mut WorldState) {
        match self {
            BasicAction::Walk(delta) => {
                world_state.player_position.x += delta.x;
                world_state.player_position.y += delta.y;
            }
            BasicAction::PickUpWeapon => world_state.has_weapon = true,
            BasicAction::AttackEnemy => {
                if world_state.has_weapon {
                    world_state.enemy_alive = false;
                }
            }
            BasicAction::PickUpWood => world_state.num_wood += 1,
            BasicAction::LightBonfire => {
                world_state.has_bonfire = true;
                world_state.num_wood = 0;
            }
        }
    }

    fn can_execute(&self, world_state: &WorldState) -> bool {
        match self {
            BasicAction::Walk(_) => true,
            BasicAction::PickUpWeapon => !world_state.has_weapon,
            BasicAction::AttackEnemy => world_state.has_weapon && world_state.enemy_alive,
            BasicAction::PickUpWood => true,
            BasicAction::LightBonfire => world_state.num_wood >= NUM_WOOD_NEEDED_FOR_BONFIRE,
        }
    }
}

// Define the struct for storing states along with their costs
struct StateWithCost {
    cost: i32,
    state: WorldState,
}

impl PartialEq for StateWithCost {
    fn eq(&self, other: &Self) -> bool {
        self.cost == other.cost
    }
}

impl Eq for StateWithCost {}

impl PartialOrd for StateWithCost {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        other.cost.partial_cmp(&self.cost) // Min-heap
    }
}

impl Ord for StateWithCost {
    fn cmp(&self, other: &Self) -> Ordering {
        other.cost.cmp(&self.cost) // Min-heap
    }
}

// == PLANNER ==

use std::collections::{BinaryHeap, HashMap};

fn plan_actions(initial_state: &WorldState, goal_state: &WorldState) -> Vec<BasicAction> {
    // Heuristic function (can be improved based on game logic)
    let heuristic = |state: &WorldState| -> i32 {
        let mut cost = 0;
        if state.player_position.x != goal_state.player_position.x {
            cost += (state.player_position.x - goal_state.player_position.x).abs();
        }
        if state.player_position.y != goal_state.player_position.y {
            cost += (state.player_position.y - goal_state.player_position.y).abs();
        }
        if state.has_weapon != goal_state.has_weapon {
            cost += 1;
        }
        if state.enemy_alive != goal_state.enemy_alive {
            cost += 1;
        }
        if state.has_bonfire != goal_state.has_bonfire {
            cost += 1;
        }
        // cost += (goal_state.num_wood as i32 - state.num_wood as i32).abs();
        cost
    };

    // A* search
    let mut heap = BinaryHeap::new();
    let mut came_from: HashMap<WorldState, (WorldState, BasicAction)> = HashMap::new();
    let mut cost_so_far: HashMap<WorldState, i32> = HashMap::new();

    heap.push(StateWithCost {
        cost: 0,
        state: initial_state.clone(),
    });
    cost_so_far.insert(initial_state.clone(), 0);

    while let Some(StateWithCost { cost, state }) = heap.pop() {
        if state.matches_goal(goal_state) {
            // Reconstruct path
            let mut current = state;
            let mut plan = Vec::new();
            while let Some((prev_state, action)) = came_from.get(&current) {
                plan.push(action.clone());
                current = prev_state.clone();
            }
            plan.reverse();
            return plan;
        }

        for action in WorldState::get_possible_actions(&state) {
            if !action.can_execute(&state) {
                continue;
            }
            let mut new_state = state.clone();
            action.execute(&mut new_state);
            let new_cost = cost_so_far[&state] + 1; // Assuming uniform cost for simplicity

            if new_cost < *cost_so_far.get(&new_state).unwrap_or(&i32::MAX) {
                cost_so_far.insert(new_state.clone(), new_cost);
                let priority = new_cost + heuristic(&new_state);
                heap.push(StateWithCost {
                    cost: priority,
                    state: new_state.clone(),
                });
                came_from.insert(new_state, (state.clone(), action));
            }
        }
    }

    Vec::new() // Return empty plan if no path is found
}
