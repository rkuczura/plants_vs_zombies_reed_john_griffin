import random

class LawnConfig:
    def __init__(self, width: int, height: int, columns: int, rows: int, plant_radius: int):
        self.width = width
        self.height = height
        self.columns = columns
        self.rows = rows
        self.plant_radius = plant_radius

        # Zombie stats
        self.zombie_speed = -2
        self.zombie_health = 10
        self.larger_zombie_health = 16

        # Plant stats
        self.pea_shooter_health = 20
        self.wallnut_health = 10      # 10 bites × 0.4s = ~4 seconds
        self.pea_shooter_damage = 2
        self.zombie_damage = 1        # damage per bite


class LawnState:
    def __init__(self):
        self.round_num = 1
        self.zombies_present = 0
        self.running = True

        # (row, col) → {"type": str, "health": int}
        self.plants: dict[tuple[int, int], dict] = {}

        # List of zombie dictionaries
        self.zombies = []

        # Peas fired by peashooters
        self.peas = []

        # cooldown so peas don't fire every frame
        self.pea_cooldown = 0
        
        #level data
        self.level = 1
        self.zombies_spawned = 0
        self.zombies_killed = 0
        self.level_target = {1: 10, 2: 18}
        self.victory = False
        self.game_over = False
        self.level_2_shown = False

        self.selected_plant = "peashooter"


# Plant placement
def place_plant(state: LawnState, row: int, col: int, plant_type: str):
    if plant_type == "peashooter":
        health = 20
    else:
        health = 10  # wallnut lasts ~4 seconds

    state.plants[(row, col)] = {"type": plant_type, "health": health}

# Removes plant
def remove_plant(state: LawnState, row: int, col: int):
    state.plants.pop((row, col), None)

# Determines whether their is a plant in a cell
def plant_in_cell(state: LawnState, row: int, col: int) -> bool:
    return (row, col) in state.plants

# Determines what type of plant it is
def get_plant_type(state: LawnState, row: int, col: int):
    plant = state.plants.get((row, col))
    return plant["type"] if plant else None


# -----------------------------
# Grid helpers
# -----------------------------

def get_cell_from_xy(x: int, y: int, config: LawnConfig) -> tuple[int, int]:
    cell_width = config.width / config.columns
    cell_height = config.height / config.rows
    col = int(x // cell_width)
    row = int(y // cell_height)
    return row, col

# Determines center of a cell for plant placement
def get_cell_center(row: int, col: int, config: LawnConfig) -> tuple[int, int]:
    cell_width = config.width / config.columns
    cell_height = config.height / config.rows
    center_x = int(col * cell_width + cell_width / 2)
    center_y = int(row * cell_height + cell_height / 2)
    return center_x, center_y           #Will be used for plant placement on the grid


def get_cell_bounds(row: int, col: int, config: LawnConfig) -> tuple[int, int, int, int]:
    cell_width = config.width / config.columns
    cell_height = config.height / config.rows
    x1 = int(col * cell_width)
    y1 = int(row * cell_height)
    x2 = int(x1 + cell_width)
    y2 = int(y1 + cell_height)
    return x1, y1, x2, y2


# Zombie spawning + movement
def spawn_zombie(state: LawnState, config: LawnConfig):
    row = random.randint(0, config.rows - 1)
    start_x = config.width - 50

    if random.random() < 0.2:
        zombie = {
            "row": row,
            "x": start_x,
            "type": "big",
            "health": config.larger_zombie_health,
            "speed": -1.2,
            "eating": False,
            "bite_cooldown": 0
        }
    else:
        zombie = {
            "row": row,
            "x": start_x,
            "type": "normal",
            "health": config.zombie_health,
            "speed": -2,
            "eating": False,
            "bite_cooldown": 0
        }

    state.zombies.append(zombie)

# Zombie state, moving/eating logic
def move_zombies(state: LawnState):
    for zombie in state.zombies:
        if not zombie["eating"]:
            zombie["x"] += zombie["speed"]


# Peashooter projectiles
def spawn_peas(state: LawnState, config: LawnConfig):
    if state.pea_cooldown > 0:
        state.pea_cooldown -= 1
        return

    for (row, col), plant in state.plants.items():
        if plant["type"] == "peashooter":
            x = col * (config.width / config.columns) + 40
            state.peas.append({"row": row, "x": x})

    state.pea_cooldown = 20


def move_peas(state: LawnState):
    for pea in state.peas:
        pea["x"] += 8

    state.peas = [p for p in state.peas if p["x"] < 1400]



# Collision detection
def rects_overlap(a, b):
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    return not (ax2 < bx1 or ax1 > bx2 or ay2 < by1 or ay1 > by2)


def check_collisions(state: LawnState, config: LawnConfig):
    UI_HEIGHT = 80

    # Reset eating state each frame
    for zombie in state.zombies:
        zombie["eating"] = False

    # Decrement bite cooldown when not eating
    for zombie in state.zombies:
        if not zombie["eating"] and zombie["bite_cooldown"] > 0:
            zombie["bite_cooldown"] -= 1

    # Zombie to Plant damage
    for zombie in state.zombies:
        row = zombie["row"]
        zx = zombie["x"]

        cell_height = config.height / config.rows
        zy = int(row * cell_height + cell_height / 2 + UI_HEIGHT)

        half = 30 if zombie["type"] == "big" else 20
        zombie_box = (zx - half, zy - half, zx + half, zy + half)

        for (prow, pcol), plant in list(state.plants.items()):
            px1, py1, px2, py2 = get_cell_bounds(prow, pcol, config)
            py1 += UI_HEIGHT
            py2 += UI_HEIGHT
            plant_box = (px1, py1, px2, py2)

            if rects_overlap(zombie_box, plant_box):

                zombie["eating"] = True

                # Bite every 12 frames (~0.4 seconds)
                if zombie["bite_cooldown"] <= 0:
                    plant["health"] -= config.zombie_damage
                    zombie["bite_cooldown"] = 12

                # Remove plant if dead
                if plant["health"] <= 0:
                    state.plants.pop((prow, pcol), None)
                    zombie["eating"] = False
                    zombie["bite_cooldown"] = 0


    # Pea to Zombie damage
    peas_to_remove = []
    zombies_to_remove = []

    for pea in state.peas:
        prow = pea["row"]
        px = pea["x"]

        for zombie in state.zombies:
            if zombie["row"] != prow:
                continue

            half = 30 if zombie["type"] == "big" else 20
            zx = zombie["x"]

            if zx - half <= px <= zx + half:
                zombie["health"] -= config.pea_shooter_damage
                peas_to_remove.append(pea)

                if zombie["health"] <= 0:
                    zombies_to_remove.append(zombie)

    for pea in peas_to_remove:
        if pea in state.peas:
            state.peas.remove(pea)

    for zombie in zombies_to_remove:
        if zombie in state.zombies:
            state.zombies.remove(zombie)
            state.zombies_killed += 1