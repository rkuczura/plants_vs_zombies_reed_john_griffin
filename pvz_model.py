#defining the config class
class LawnConfig:
    def __init__(self, width:int, height:int, columns:int, rows:int, plant_radius:int):
        self.width: int = width
        self.height: int = height
        self.columns: int = columns
        self.rows: int = rows
        self.plant_radius: int = plant_radius


#defining the game state. 
# 
"""Not sure what else to put in here"""
class LawnState:
    def __init__(self):
        self.round_num: int
        self.zombies_present: int
        self.running: bool
        self.selected_cells: set[tuple[int, int,]] = set()
        self.view

#adds a plant to a cell
def select_cell(state, row: int, col: int):
        state.selected_cells.add((row, col))

#removes a plant from a cell
def deselect_cell(state, row: int, col: int):
        state.selected_cells.discard((row, col))

#
def is_selected(state, row: int, col: int) -> bool:
        return (row, col) in state.selected_cells