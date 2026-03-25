from pvz_view import LawnViewIds,build_ui
from pvz_model import LawnConfig, LawnState, select_cell, is_selected, get_cell_from_xy
import tkinter as tk

#for right now(phase 1) this is just used to place a "plant" or circle on any grid square that is
def on_click(state, event):
        cell = get_cell_from_xy(event.x, event.y)
        if cell:
            state._refresh_cell(cell)
            state._update_status()

def startgame(root: tk.Tk, config:LawnConfig):
    canvas, view_ids = build_ui(root, config)
    state = LawnState
    def lclick_handler(event):
            on_click(state,event)
    
    canvas.bind("<ButtonPress-1>", lclick_handler)