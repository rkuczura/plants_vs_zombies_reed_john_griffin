
import pygame
from pvz_view import (
    redraw, draw_victory, draw_game_over, draw_level_transition, UI_HEIGHT
)
from pvz_model import (
    LawnConfig, LawnState,
    check_collisions, move_zombies, move_peas, spawn_peas,
    get_cell_from_xy, spawn_zombie, place_plant, collect_sun,
    spawn_sun, move_suns, update_game_state, check_game_over,
    should_spawn_zombie, reset_level, reset_game
)

#mouse click handler
def handle_click(state: LawnState, x: int, y: int, config: LawnConfig) -> bool:
    # Check if click is on UI panel
    if y < UI_HEIGHT:
        # Plant selection cards at y=10
        card_y = 10
        card_width = 70
        card_height = 60
        card_x_start = 20

        plant_cards = ["peashooter", "wallnut", "slowflower"]

        for i, plant_type in enumerate(plant_cards):
            card_x = card_x_start + i * (card_width + 10)
            if (card_x <= x <= card_x + card_width and 
                card_y <= y <= card_y + card_height):
                state.selected_plant = plant_type
                return False

        return False

    # Check if click is on a sun
    sun_y = y - UI_HEIGHT
    if collect_sun(state, x, sun_y, config):
        return False

    # Click is on game board - try to place a plant
    row, col = get_cell_from_xy(x, y - UI_HEIGHT, config)

    # Validate grid coordinates
    if row < 0 or row >= config.rows or col < 0 or col >= config.columns:
        return False

    # Try to place the selected plant
    success = place_plant(state, row, col, state.selected_plant, config)
    return success


def handle_keypress(state: LawnState, key: int):
    """Handle keyboard input"""
    if key == pygame.K_r:
        # Restart current level
        reset_level(state)
        state.running = True
        state.game_over = False
    elif key == pygame.K_g:
        # Restart game from Level 1
        reset_game(state)
        state.running = True


def update_game(state: LawnState, config: LawnConfig):
    """
    Main game update loop - handle all game logic
    """
    # Spawn suns
    spawn_sun(state, config)
    move_suns(state, config)

    # Spawn zombies if conditions are met
    if should_spawn_zombie(state, config):
        spawn_zombie(state, config)
        state.zombies_spawned += 1

    # Move all entities
    move_zombies(state, config)
    move_peas(state)
    spawn_peas(state, config)

    # Check all collisions
    check_collisions(state, config)

    # Check if any zombie reached the left side (LOSE condition)
    if check_game_over(state):
        return

    # Update overall game state
    update_game_state(state, config)


def startgame(screen: pygame.Surface, config: LawnConfig):
    """Main game loop"""
    state = LawnState()
    clock = pygame.time.Clock()

    # Main game loop
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            elif event.type == pygame.MOUSEBUTTONDOWN and state.running:
                mx, my = event.pos
                handle_click(state, mx, my, config)

            elif event.type == pygame.KEYDOWN and not state.running:
                handle_keypress(state, event.key)

        # Update game state if running
        if state.running:
            update_game(state, config)

        # Render appropriate screen
        if state.game_won:
            draw_victory(screen, config)
            pygame.display.flip()
            pygame.time.wait(3000)
            pygame.quit()
            return
        elif state.game_over:
            draw_game_over(screen, config)
        elif state.show_level_transition:
            draw_level_transition(screen, config, state.level)
        else:
            redraw(screen, state, config)

        clock.tick(30)  # 30 FPS
