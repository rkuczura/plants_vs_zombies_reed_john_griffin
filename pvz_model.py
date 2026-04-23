import random
import math


#config for the game
class LawnConfig:
    def __init__(self, width: int, height: int, columns: int, rows: int, plant_radius: int):
        self.width = width
        self.height = height
        self.columns = columns
        self.rows = rows
        self.plant_radius = plant_radius

        # zombie stats
        self.zombie_speed = -2
        self.zombie_health = 15
        self.large_zombie_health = 30
        self.boss_zombie_health = 80

        # Plant Stats
        self.peashooter_health = 20
        self.wallnut_health = 35
        self.slowflower_health = 12

        self.pea_shooter_damage = 3
        self.zombie_damage = 1  # damage per bite

        self.plant_costs = {
            "peashooter": 100,
            "wallnut": 50,
            "slowflower": 75
        }

        #Level setups
        self.level_targets = {
            1: 10,   # Level 1 kill 10 zombies
            2: 20,   # Level 2 kill 20 zombies
            3: 30    # Level 3 kill 30 zombies with boss wave
        }

        self.boss_wave_threshold = 25  #boss spawns in after this many zombies are killed in level 3
        self.sun_click_radius = 40  # This is the clickradius to obtain a sun 


class LawnState:
    def __init__(self):
        # Level proression
        self.level = 1
        self.running = True
        self.game_over = False
        self.game_won = False
        self.show_level_transition = False
        self.level_transition_timer = 0

        #Zombie state
        self.zombies = []
        self.zombies_spawned = 0
        self.zombies_killed = 0
        self.boss_spawned = False

        #Plant state
        self.plants = {}  # (row, col) → {"type": str, "health": int}
        self.selected_plant = "peashooter"

        # Projectile states
        self.peas = []
        self.pea_cooldown = 0

        # Sun state
        self.suns = []
        self.sun_count = 150  # Starting suns
        self.sun_spawn_cooldown = 0
        self.sun_click_radius = 30

        # Slowflower's affected zombies
        self.slowed_zombies = {} 


#functions for plants

def place_plant(state: LawnState, row: int, col: int, plant_type: str, config: LawnConfig) -> bool:
    if plant_type not in config.plant_costs:
        return False
    if (row, col) in state.plants:
        return False
    if row < 0 or row >= config.rows or col < 0 or col >= config.columns:
        return False

    cost = config.plant_costs[plant_type]
    if state.sun_count < cost:
        return False
    state.sun_count -= cost


    health_map = {
        "peashooter": config.peashooter_health,
        "wallnut": config.wallnut_health,
        "slowflower": config.slowflower_health
    }

    state.plants[(row, col)] = {
        "type": plant_type,
        "health": health_map.get(plant_type, 30)
    }

    return True

# remove plant
def remove_plant(state: LawnState, row: int, col: int):
    state.plants.pop((row, col), None)

#check if there is a plant
def plant_in_cell(state: LawnState, row: int, col: int) -> bool:
    return (row, col) in state.plants

#check what type of plant is at a location
def get_plant_type(state: LawnState, row: int, col: int) -> str:
    plant = state.plants.get((row, col))
    return plant["type"] if plant else None


#find what cell is clicked
def get_cell_from_xy(x: int, y: int, config: LawnConfig) -> tuple[int, int]:
    """Convert pixel coordinates to grid coordinates"""
    cell_width = config.width / config.columns
    cell_height = config.height / config.rows
    col = int(x // cell_width)
    row = int(y // cell_height)
    return row, col

#find center of cell
def get_cell_center(row: int, col: int, config: LawnConfig) -> tuple[int, int]:
    """Get the center pixel coordinates of a grid cell"""
    cell_width = config.width / config.columns
    cell_height = config.height / config.rows
    center_x = int(col * cell_width + cell_width / 2)
    center_y = int(row * cell_height + cell_height / 2)
    return center_x, center_y

#find edges of a cell
def get_cell_bounds(row: int, col: int, config: LawnConfig) -> tuple[int, int, int, int]:
    cell_width = config.width / config.columns
    cell_height = config.height / config.rows
    x1 = int(col * cell_width)
    y1 = int(row * cell_height)
    x2 = int(x1 + cell_width)
    y2 = int(y1 + cell_height)
    return x1, y1, x2, y2


#Will spawn a zombie in a random row
def spawn_zombie(state: LawnState, config: LawnConfig):
    row = random.randint(0, config.rows - 1)
    start_x = config.width - 50

    # Determine zombie type based on level and number spawned
    zombie_type = "normal"
    health = config.zombie_health
    speed = -1.5

#change spawning behavior in level 2
    if state.level >= 2:
        if random.random() < 0.3:
            zombie_type = "large"
            health = config.large_zombie_health
            speed = -1.0

#change spawns in level 3
    if state.level == 3 and state.zombies_spawned >= config.boss_wave_threshold and not state.boss_spawned:
        zombie_type = "boss"
        health = config.boss_zombie_health
        speed = -0.8
        state.boss_spawned = True

#state for an individual zombie object
    zombie = {
        "row": row,
        "x": float(start_x),
        "type": zombie_type,
        "health": health,
        "speed": speed,
        "eating": False,
        "bite_cooldown": 0,
        "slow_frames": 0  
    }

    state.zombies.append(zombie)


def move_zombies(state: LawnState, config: LawnConfig):
    """Move all zombies. Eating zombies don't move."""
    for zombie in state.zombies:
        if not zombie["eating"]:
            current_speed = zombie["speed"]
            if zombie["slow_frames"] > 0:
                current_speed *= 0.5 
                zombie["slow_frames"] -= 1

            zombie["x"] += current_speed


#peashooters projectiles spawn
def spawn_peas(state: LawnState, config: LawnConfig):
    if state.pea_cooldown > 0:
        state.pea_cooldown -= 1
        return

    for (row, col), plant in state.plants.items():
        if plant["type"] == "peashooter" and plant["health"] > 0:
            px, py = get_cell_center(row, col, config)
            state.peas.append({
                "row": row,
                "x": float(px),
                "y": float(py)
            })

    state.pea_cooldown = 15  # Spawn every 15 frames

#peas will move across the screen to the right
def move_peas(state: LawnState):
    for pea in state.peas:
        pea["x"] += 10

    # Remove peas that went off screen
    state.peas = [p for p in state.peas if p["x"] < 1600]


#spawns in suns to be clicked as currency
def spawn_sun(state: LawnState, config: LawnConfig):
    if state.sun_spawn_cooldown > 0:
        state.sun_spawn_cooldown -= 1
        return

    if random.random() < 0.1:
        sun_x = random.randint(50, config.width - 50)
        state.suns.append({
            "x": float(sun_x),
            "y": 0.0,
            "collected": False
        })
        state.sun_spawn_cooldown = 60

    state.sun_spawn_cooldown = max(0, state.sun_spawn_cooldown - 1)

#suns will move down to the bottom of the screen like they are falling
def move_suns(state: LawnState, config: LawnConfig):
    """Move suns downward"""
    for sun in state.suns:
        if not sun["collected"]:
            sun["y"] += 2

    # remove suns that went off screen
    state.suns = [s for s in state.suns if s["y"] < config.height and not s["collected"]]


#collect a sun when it is clicked
def collect_sun(state: LawnState, x: int, y: int, config: LawnConfig) -> bool:
    for sun in state.suns:
        if sun["collected"]:
            continue

        distance = math.sqrt((sun["x"] - x)**2 + (sun["y"] - y)**2)
        if distance <= config.sun_click_radius:
            sun["collected"] = True
            state.sun_count += 25  # Each sun worth 25
            return True

    return False



#basic collision detection for two rectangles
def rects_overlap(a: tuple, b: tuple) -> bool:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    return not (ax2 < bx1 or ax1 > bx2 or ay2 < by1 or ay1 > by2)


def check_collisions(state: LawnState, config: LawnConfig):
    UI_HEIGHT = 80

    # Reset zombie's eating state each frame
    for zombie in state.zombies:
        zombie["eating"] = False

    # decrement bite cooldown
    for zombie in state.zombies:
        if not zombie["eating"] and zombie["bite_cooldown"] > 0:
            zombie["bite_cooldown"] -= 1

    # Check zombie plant collisions
    for zombie in state.zombies:
        row = zombie["row"]
        zx = zombie["x"]

        cell_height = config.height / config.rows
        zy = row * cell_height + cell_height / 2 + UI_HEIGHT

        # Zombie hitbox is dependent on type of zombie
        half_width = 40 if zombie["type"] == "boss" else (30 if zombie["type"] == "large" else 20)
        zombie_box = (zx - half_width, zy - 20, zx + half_width, zy + 20)

        for (prow, pcol), plant in list(state.plants.items()):
            if prow != row:
                continue

            px1, py1, px2, py2 = get_cell_bounds(prow, pcol, config)
            py1 += UI_HEIGHT
            py2 += UI_HEIGHT
            plant_box = (px1, py1, px2, py2)

            if rects_overlap(zombie_box, plant_box):
                zombie["eating"] = True

                # Bite every 12 frames
                if zombie["bite_cooldown"] <= 0:
                    plant["health"] -= config.zombie_damage
                    zombie["bite_cooldown"] = 12

                # Remove dead plants
                if plant["health"] <= 0:
                    remove_plant(state, prow, pcol)
                    zombie["eating"] = False
                    zombie["bite_cooldown"] = 0
                break

#peas will be removed as they go off screen or collide with a zombie
#zombies will be removed as they die
    peas_to_remove = []
    zombies_to_remove = []

    for pea in state.peas:
        prow = pea["row"]
        px = pea["x"]

        for zombie in state.zombies:
            if zombie["row"] != prow:
                continue

            half_width = 40 if zombie["type"] == "boss" else (30 if zombie["type"] == "large" else 20)
            zx = zombie["x"]

            if zx - half_width <= px <= zx + half_width:
                zombie["health"] -= config.pea_shooter_damage
                if pea not in peas_to_remove:
                    peas_to_remove.append(pea)

                if zombie["health"] <= 0 and zombie not in zombies_to_remove:
                    zombies_to_remove.append(zombie)
                break

    for pea in peas_to_remove:
        if pea in state.peas:
            state.peas.remove(pea)

    for zombie in zombies_to_remove:
        if zombie in state.zombies:
            state.zombies.remove(zombie)
            state.zombies_killed += 1

    # Slowdown zombies which are near enough to the slowflowers
    for (prow, pcol), plant in state.plants.items():
        if plant["type"] == "slowflower" and plant["health"] > 0:
            # find area of effect
            cell_width = config.width / config.columns
            cell_height = config.height / config.rows

            effect_radius = max(cell_width, cell_height) * 2

            px, py = get_cell_center(prow, pcol, config)
            py += UI_HEIGHT

            for zombie in state.zombies:
                zy = zombie["row"] * cell_height + cell_height / 2 + UI_HEIGHT
                distance = math.sqrt((zombie["x"] - px)**2 + (zy - py)**2)

                if distance < effect_radius:
                    zombie["slow_frames"] = 30  # Slow for 30 frames



#game state updater
def update_game_state(state: LawnState, config: LawnConfig):
    """Update overall game state after each frame"""
    # checks to see if level is beaten
    if state.zombies_killed >= config.level_targets[state.level] and not state.zombies:
        if state.level < 3:
            state.level += 1
            state.show_level_transition = True
            state.level_transition_timer = 120  # 4 seconds at 30 FPS
            state.zombies_killed = 0
            state.zombies_spawned = 0
            state.boss_spawned = False
            state.peas.clear()
            state.plants.clear()
        else:
            state.game_won = True
            state.running = False

    #timer for break inbetween levels
    if state.show_level_transition:
        state.level_transition_timer -= 1
        if state.level_transition_timer <= 0:
            state.show_level_transition = False

#check to see if a zombie made it past your plants to the left side of the screen
def check_game_over(state: LawnState):
    for zombie in state.zombies:
        if zombie["x"] < 0:
            state.game_over = True
            state.running = False
            return True
    return False


def should_spawn_zombie(state: LawnState, config: LawnConfig) -> bool:
    # Don't spawn morezombies than the level target
    if state.zombies_spawned >= config.level_targets[state.level] * 2:
        return False

   #spawn rate is dependent on level
    spawn_rates = {1: 0.01, 2: 0.018, 3: 0.025}
    return random.random() < spawn_rates.get(state.level, 0.01)

#reset level is player chooses to respawn at their last level
def reset_level(state: LawnState):
    state.zombies.clear()
    state.peas.clear()
    state.plants.clear()
    state.suns.clear()
    state.zombies_spawned = 0
    state.zombies_killed = 0
    state.boss_spawned = False
    state.sun_count = 150

#reset game if player chooses to respawn at the first level
def reset_game(state: LawnState):
    state.level = 1
    state.running = True
    state.game_over = False
    state.game_won = False
    state.zombies.clear()
    state.peas.clear()
    state.plants.clear()
    state.suns.clear()
    state.zombies_spawned = 0
    state.zombies_killed = 0
    state.boss_spawned = False
    state.sun_count = 150
    state.selected_plant = "peashooter"