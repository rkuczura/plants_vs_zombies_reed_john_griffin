import pygame
from pvz_model import LawnConfig, LawnState, get_cell_bounds

#Color options for the game
COLOR_BG         = (0, 128, 0)    # green lawn background
COLOR_GRID       = (0, 0, 0)      # black grid lines
COLOR_PLANT_FILL = (0, 128, 128)  # teal plant body
COLOR_PLANT_OUT  = (128, 0, 128)  # purple plant outline
COLOR_ZOMBIE_FILL = (139, 69, 19) # brown zombie body
COLOR_ZOMBIE_OUT  = (0, 0, 0)     # black zombie outline

#creates pygame window and pushes to surface
def build_ui(config: LawnConfig) -> pygame.Surface:
    pygame.init()
    screen = pygame.display.set_mode((config.width, config.height))
    pygame.display.set_caption("Plants vs Zombies")
    return screen

#redraw function which redraws the screen every frame:
#must remove then add everything
def redraw(screen: pygame.Surface, state: LawnState, config: LawnConfig):
    screen.fill(COLOR_BG)

    cell_w = config.width  // config.columns
    cell_h = config.height // config.rows
    for row in range(config.rows + 1):
        y = row * cell_h
        pygame.draw.line(screen, COLOR_GRID, (0, y), (config.width, y))
    for col in range(config.columns + 1):
        x = col * cell_w
        pygame.draw.line(screen, COLOR_GRID, (x, 0), (x, config.height))

#draws the plants
    for (row, col) in state.selected_cells:
        x1, y1, x2, y2 = get_cell_bounds(row, col, config)
        rect = pygame.Rect(x1 + 10, y1 + 10, (x2 - x1) - 20, (y2 - y1) - 20)
        #body
        pygame.draw.ellipse(screen, COLOR_PLANT_FILL, rect)       
        #outline 
        pygame.draw.ellipse(screen, COLOR_PLANT_OUT,  rect, 3)    

    #draws zombies
    for zombie in state.zombies:
        row = zombie["row"]
        zx  = int(zombie["x"])

        cell_height = config.height / config.rows
        zy = int(row * cell_height + cell_height / 2)

        zombie_rect = pygame.Rect(zx - 20, zy - 20, 40, 40)
        pygame.draw.rect(screen, COLOR_ZOMBIE_FILL, zombie_rect)
        pygame.draw.rect(screen, COLOR_ZOMBIE_OUT,  zombie_rect, 2)

#pushes everything to the display. All of this was made on a backgroud screen and is then put on the front screen or "flipped" when its ready
    pygame.display.flip()