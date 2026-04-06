import random
import pygame

from pvz_view import redraw
from pvz_model import (
LawnConfig, LawnState,
check_collisions, move_zombies,
get_cell_from_xy, spawn_zombie)


def on_click(state, x, y, config):
        cell = get_cell_from_xy(x, y, config)
        if cell is not None:
            state.toggle_cell(cell)
        return state


#starts game and contains the main game loop
def startgame(screen: pygame.Surface, config: LawnConfig):
    state  = LawnState()
    clock  = pygame.time.Clock()

    while state.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Left-click → place / remove a plant
                mx, my = event.pos
                state = on_click(state, mx, my, config)

        move_zombies(state)
        check_collisions(state, config)

        # Randomly spawn a zombie
        if random.random() < 0.01:
            spawn_zombie(state, config)

        redraw(screen, state, config)

        clock.tick(30)

    pygame.quit()
