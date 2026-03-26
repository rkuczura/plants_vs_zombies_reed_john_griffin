from logging import config, root
import random

from pvz_view import build_ui, redraw
from pvz_model import LawnConfig, LawnState, check_collisions, move_zombies, select_cell, is_selected, get_cell_from_xy, spawn_zombie
import tkinter as tk

#for right now(phase 1) this is just used to place a "plant" or circle on any grid square that is
def on_click(state, event, canvas, config):
        cell = get_cell_from_xy(event.x, event.y, config)
        if cell is not None:
            state.toggle_cell(cell)
            redraw(canvas, state, config)
        return state

def startgame(root: tk.Tk, config: LawnConfig):
    canvas, view_ids = build_ui(root, config)
    state = LawnState()

    def lclick_handler(event):
        nonlocal state
        state = on_click(state, event, canvas, config)

    canvas.bind("<ButtonPress-1>", lclick_handler)

    def game_loop():
        move_zombies(state)
        check_collisions(state, config)
        redraw(canvas, state, config)

        if random.random() < 0.01:
            spawn_zombie(state, config)

        root.after(30, game_loop)  # <-- reschedule from inside

    game_loop()