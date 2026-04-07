import random
import pygame

from pvz_view import redraw
from pvz_model import (
    LawnConfig, LawnState,
    check_collisions, move_zombies,
    get_cell_from_xy, spawn_zombie,
    place_plant, remove_plant, plant_in_cell,
    move_peas, spawn_peas
)


def handle_click(state, x, y, button, config):
    row, col = get_cell_from_xy(x, y, config)

    if button == 1:  # LEFT CLICK → Peashooter
        place_plant(state, row, col, "peashooter")

    elif button == 3:  # RIGHT CLICK → Wall-nut
        place_plant(state, row, col, "wallnut")

    return state


def startgame(screen: pygame.Surface, config: LawnConfig):
    state = LawnState()
    clock = pygame.time.Clock()

    while state.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                state = handle_click(state, mx, my, event.button, config)

        # -------------------------
        # GAME LOGIC
        # -------------------------
        move_zombies(state)
        move_peas(state)          # NEW
        spawn_peas(state, config) # NEW
        check_collisions(state, config)

        # Randomly spawn a zombie
        if random.random() < 0.01:
            spawn_zombie(state, config)

        # -------------------------
        # DRAW EVERYTHING
        # -------------------------
        redraw(screen, state, config)
        clock.tick(30)

    pygame.quit()