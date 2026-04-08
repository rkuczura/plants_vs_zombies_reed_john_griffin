import pygame
from pvz_model import LawnConfig, LawnState, get_cell_bounds

# Color options for the game
COLOR_BG          = (0, 128, 0)     # green lawn background
COLOR_GRID        = (0, 0, 0)       # black grid lines
COLOR_PLANT_FILL  = (0, 128, 128)   # teal plant body
COLOR_PLANT_OUT   = (128, 0, 128)   # purple plant outline
COLOR_ZOMBIE_FILL = (139, 69, 19)   # brown zombie body
COLOR_ZOMBIE_OUT  = (0, 0, 0)       # black zombie outline
UI_HEIGHT = 80
PEASHOOTER_CARD = pygame.Rect(20, 10, 80, 60)
WALLNUT_CARD    = pygame.Rect(120, 10, 80, 60)

def redraw(screen: pygame.Surface, state: LawnState, config: LawnConfig):
    screen.fill(COLOR_BG)

    pygame.draw.rect(screen, (30, 30, 30), (0, 0, config.width, UI_HEIGHT))

    pygame.draw.rect(
        screen,
        (255, 255, 0) if state.selected_plant == "peashooter" else (200, 200, 200),
        PEASHOOTER_CARD, 3
)
    pygame.draw.circle(screen, (0, 200, 0), PEASHOOTER_CARD.center, 20)

    pygame.draw.rect(
        screen,
        (255, 255, 0) if state.selected_plant == "wallnut" else (200, 200, 200),
        WALLNUT_CARD, 3
    )
    pygame.draw.circle(screen, (139, 69, 19), WALLNUT_CARD.center, 22)


    # Draw grid
    cell_w = config.width  // config.columns
    cell_h = config.height // config.rows
    for row in range(config.rows + 1):
        y = UI_HEIGHT + row * cell_h
        pygame.draw.line(screen, COLOR_GRID, (0, y), (config.width, y))
    for col in range(config.columns + 1):
        x = col * cell_w
        pygame.draw.line(screen, COLOR_GRID, (x, UI_HEIGHT), (x, UI_HEIGHT + config.height))

    # draw plants
    for (row, col), plant in state.plants.items():
        plant_type = plant["type"]  # NEW

        x1, y1, x2, y2 = get_cell_bounds(row, col, config)
        y1 += UI_HEIGHT
        y2 += UI_HEIGHT
        w = (x2 - x1)
        h = (y2 - y1)

        if plant_type == "peashooter":
            rect = pygame.Rect(x1 + 12, y1 + 12, w - 24, h - 24)
            pygame.draw.ellipse(screen, (0, 200, 0), rect)
            pygame.draw.ellipse(screen, (0, 100, 0), rect, 3)

        elif plant_type == "wallnut":
            rect = pygame.Rect(x1 + 8, y1 + 8, w - 16, h - 16)
            pygame.draw.ellipse(screen, (139, 69, 19), rect)
            pygame.draw.ellipse(screen, (80, 40, 10), rect, 3)


    # draw zombies
    for pea in state.peas:
        row = pea["row"]
        px = int(pea["x"])

        cell_height = config.height / config.rows
        py = int(row * cell_height + cell_height / 2 + UI_HEIGHT)

        pygame.draw.circle(screen, (255, 255, 0), (px, py), 6)

    
    # draw zombies
    for zombie in state.zombies:
        row = zombie["row"]
        zx  = int(zombie["x"])

        cell_height = config.height / config.rows
        zy = int(row * cell_height + cell_height / 2 + UI_HEIGHT)

        # Big zombie = 60x60, normal = 40x40
        if zombie.get("type") == "big":
            zombie_rect = pygame.Rect(zx - 30, zy - 30, 60, 60)
        else:
            zombie_rect = pygame.Rect(zx - 20, zy - 20, 40, 40)

        pygame.draw.rect(screen, COLOR_ZOMBIE_FILL, zombie_rect)
        pygame.draw.rect(screen, COLOR_ZOMBIE_OUT, zombie_rect, 2)

    pygame.display.flip()


def draw_victory(screen, config):
    screen.fill((10, 80, 10))
    font = pygame.font.SysFont("arial", 72, bold=True)
    text = font.render("YOU WIN!", True, (255, 255, 0))
    screen.blit(text, (config.width//2 - 160, config.height//2 - 40))
    pygame.display.flip()

def draw_level_2_message(screen, config):
    screen.fill((0, 128, 0))
    font = pygame.font.SysFont("arial", 60, bold=True)
    text = font.render("LEVEL 2", True, (255, 255, 0))
    screen.blit(text, (config.width//2 - 120, config.height//2 - 40))
    pygame.display.flip()

def draw_game_over(screen, config):
    screen.fill((128, 0, 0))
    font = pygame.font.SysFont("arial", 72, bold=True)
    text = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(text, (config.width//2 - 200, config.height//2 - 40))
    pygame.display.flip()

def build_ui(config: LawnConfig) -> pygame.Surface:
    pygame.init()
    screen = pygame.display.set_mode((config.width, config.height + UI_HEIGHT))
    pygame.display.set_caption("Plants vs Zombies")
    return screen