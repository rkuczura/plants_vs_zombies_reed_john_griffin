import tkinter as tk
from pvz_model import LawnConfig, LawnState, get_cell_from_xy, get_cell_center, get_cell_bounds, plant_in_cell

class LawnViewIds:
    def __init__(self):
        self.plant_id: int
        self.sun_count_id: int


def build_ui(root: tk.Tk, config: LawnConfig) -> tuple[tk.Canvas, LawnViewIds]:
    canvas = tk.Canvas(
        root,
        width=config.width,
        height=config.height,
        bg="green"
    )
    canvas.pack()

    view_ids = LawnViewIds()

    row_step = config.height // config.rows
    column_step = config.width // config.columns

    # Draw grid
    for y in range(0, config.height, row_step):
        canvas.create_line(0, y, config.width, y, fill="black")

    for x in range(0, config.width, column_step):
        canvas.create_line(x, 0, x, config.height, fill="black")

    return canvas, view_ids

def redraw(canvas, state: LawnState, config: LawnConfig):
    canvas.delete("plant")
    canvas.delete("zombie")

    # draw plants
    for (row, col) in state.selected_cells:
        x0, y0, x1, y1 = get_cell_bounds(row, col, config)
        canvas.create_oval(
            x0 + 10, y0 + 10, x1 - 10, y1 - 10,
            fill="teal",
            outline="purple",
            tags="plant"
        )

    # draw zombies
    for zombie in state.zombies:
        row = zombie["row"]
        x = zombie["x"]

        cell_height = config.height / config.rows
        y = int(row * cell_height + cell_height / 2)

        canvas.create_rectangle(
            x - 20, y - 20, x + 20, y + 20,
            fill="brown",
            outline="black",
            tags="zombie"
        )