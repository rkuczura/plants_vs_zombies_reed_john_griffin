from logging import config
import random



class LawnConfig:
    def __init__(self, width: int, height: int, columns: int, rows: int, plant_radius: int):
        self.width = width
        self.height = height
        self.columns = columns
        self.rows = rows
        self.plant_radius = plant_radius
        self.zombie_speed = -1


class LawnState:
    def __init__(self):
        self.round_num = 1
        self.zombies_present = 0
        self.running = True
        self.selected_cells: set[tuple[int, int]] = set()
        self.zombies = []

    def toggle_cell(self, cell: tuple[int, int]):
        """Add or remove a plant in the given cell."""
        if cell in self.selected_cells:
            self.selected_cells.remove(cell)
        else:
            self.selected_cells.add(cell)


def select_cell(state, row: int, col: int):
    state.selected_cells.add((row, col))


def deselect_cell(state, row: int, col: int):
    state.selected_cells.discard((row, col))


def is_selected(state, row: int, col: int) -> bool:
    return (row, col) in state.selected_cells


def get_cell_from_xy(x: int, y: int, config: LawnConfig) -> tuple[int, int]:
    cell_width = config.width / config.columns
    cell_height = config.height / config.rows
    col = int(x // cell_width)
    row = int(y // cell_height)
    return row, col


def get_cell_center(row: int, col: int, config: LawnConfig) -> tuple[int, int]:
    cell_width = config.width / config.columns
    cell_height = config.height / config.rows
    center_x = int(col * cell_width + cell_width / 2)
    center_y = int(row * cell_height + cell_height / 2)
    return center_x, center_y


def get_cell_bounds(row: int, col: int, config: LawnConfig) -> tuple[int, int, int, int]:
    cell_width = config.width / config.columns
    cell_height = config.height / config.rows
    x1 = int(col * cell_width)
    y1 = int(row * cell_height)
    x2 = int(x1 + cell_width)
    y2 = int(y1 + cell_height)
    return x1, y1, x2, y2


def plant_in_cell(state: LawnState, row: int, col: int) -> bool:
    return (row, col) in state.selected_cells

def spawn_zombie(state: LawnState, config: LawnConfig):
    row = random.randint(0, config.rows - 1)
    start_x = config.width - 50

    zombie = {"row": row, "x": start_x}
    state.zombies.append(zombie)


def move_zombies(state: LawnState):
    for zombie in state.zombies:
        zombie["x"] -= 2

def rects_overlap(a, b):
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    return not (ax2 < bx1 or ax1 > bx2 or ay2 < by1 or ay1 > by2)

def check_collisions(state: LawnState, config: LawnConfig):
    zombies_to_remove = []
    plants_to_remove = []

    for zombie in state.zombies:
        row = zombie["row"]
        zx = zombie["x"]

        # zombie bounding box
        cell_height = config.height / config.rows
        zy = int(row * cell_height + cell_height / 2)

        zombie_box = (zx - 20, zy - 20, zx + 20, zy + 20)

        # check against all plants
        for (prow, pcol) in state.selected_cells:
            px1, py1, px2, py2 = get_cell_bounds(prow, pcol, config)
            plant_box = (px1, py1, px2, py2)

            if rects_overlap(zombie_box, plant_box):
                plants_to_remove.append((prow, pcol))
                zombies_to_remove.append(zombie)

    # apply removals
    for plant in plants_to_remove:
        state.selected_cells.remove(plant)

    for zombie in zombies_to_remove:
        state.zombies.remove(zombie)