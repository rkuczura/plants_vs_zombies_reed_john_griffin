import tkinter as tk
from pvz_model import LawnConfig, LawnState

class LawnViewIds:
    def __init__(self):
        self.plant_id: int
        self.sun_count_id: int


def build_ui(root: tk.Tk, config:LawnConfig) ->tuple[tk.Canvas, LawnViewIds]:
    canvas = tk.Canvas(
        root,
        width = config.width,
        height = config.height,
        bg = "green"
    )

    canvas.pack()
    view_ids = LawnViewIds()

    row_step = config.height//config.rows

    column_step = config.width//config.columns

    for hzontal_line_y in range(0, config.height, row_step):
        canvas.create_line(
            0,
            hzontal_line_y,
            config.width,
            hzontal_line_y,
            fill = "black"
        )
    for vtical_line_x in range(0,config.width,column_step):
        canvas.create_line(
            vtical_line_x,
            0,
            vtical_line_x,
            config.height,
            fill = "black"

        )
    return (canvas, view_ids)
