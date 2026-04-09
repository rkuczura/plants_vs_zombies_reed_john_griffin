import random
import pygame

#Imports viewmodels for plants and game screen
from pvz_view import redraw, PEASHOOTER_CARD, WALLNUT_CARD, draw_victory, draw_level_2_message, draw_game_over
#Imports game physics for zombie movement and spawns
from pvz_model import (
    LawnConfig, LawnState,
    check_collisions, move_zombies,
    get_cell_from_xy, spawn_zombie,
    place_plant, remove_plant, plant_in_cell,
    move_peas, spawn_peas
)



def handle_click(state, x, y, button, config):              #Creates the UI for the plant selection and placement
    if y < 80:
        if PEASHOOTER_CARD.collidepoint(x, y):
            state.selected_plant = "peashooter"             # Selects peashooter
        elif WALLNUT_CARD.collidepoint(x, y):
            state.selected_plant = "wallnut"                # Selects wallnut
        return state

    row, col = get_cell_from_xy(x, y - 80, config)

    if button == 1:
        place_plant(state, row, col, state.selected_plant)  # Places the selected plant on the grid

    return state



def startgame(screen: pygame.Surface, config: LawnConfig):
    state = LawnState()
    clock = pygame.time.Clock()

    #Inital state of the game loop
    while state.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                state = handle_click(state, mx, my, event.button, config)

        # Game Logic
        move_zombies(state)
        move_peas(state)          # NEW
        spawn_peas(state, config) # NEW
        check_collisions(state, config)

        # Randomly spawn a zombie
        spawn_rate = 0.01 if state.level == 1 else 0.02

        if random.random() < spawn_rate:
            spawn_zombie(state, config)
            state.zombies_spawned += 1
        
        # Check if any zombie reached the left side
        for zombie in state.zombies:
            if zombie["x"] < 0:
                state.game_over = True
                state.running = False
        
        # Creates the second level after killing enough zombies
        if state.zombies_killed >= state.level_target[state.level] and not state.zombies:
            if state.level == 1:
                state.level = 2
                state.zombies_killed = 0
                state.zombies_spawned = 0
                state.peas.clear()
                state.level_2_shown = False
            else:
                state.victory = True
                state.running = False
        
        # Display screen messages
        if state.game_over:
            draw_game_over(screen, config)
            pygame.time.wait(3000)
        elif state.level == 2 and not state.level_2_shown:
            draw_level_2_message(screen, config)
            pygame.time.wait(2000)
            state.level_2_shown = True
            # Continue to normal redraw after level message
            redraw(screen, state, config)
        elif state.victory:
            draw_victory(screen, config)
            pygame.time.wait(3000)
        else:
            # Draw everything normally
            redraw(screen, state, config)
        
        clock.tick(30)

        

    pygame.quit()