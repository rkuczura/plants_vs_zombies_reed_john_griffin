import pygame
import os
from pvz_model import LawnConfig, LawnState, get_cell_bounds, get_cell_center

UI_HEIGHT = 80

# Color Pallet
COLOR_BG = (34, 139, 34)  # Forest green lawn
COLOR_GRID = (0, 0, 0)    # Black grid
COLOR_UI_BG = (20, 100, 20)  # Darker green UI
COLOR_TEXT = (255, 255, 255)  # White text
COLOR_HIGHLIGHT = (255, 255, 0)  # Yellow highlight

# ---------------------------------------------------------
# IMAGE ASSETS
# ---------------------------------------------------------
class ImageAssets:
    def __init__(self):
        self.background = None
        self.peashooter = None
        self.wallnut = None
        self.slowflower = None
        self.zombie = None
        self.large_zombie = None
        self.boss_zombie = None
        self.pea = None
        self.sun = None
        
        self.load_all()
    
    def load_all(self):
        asset_dir = "assets"
        
        try:
            def load_if_exists(name):
                path = os.path.join(asset_dir, name)
                return pygame.image.load(path) if os.path.exists(path) else None

            self.background = load_if_exists("background.png")
            self.peashooter = load_if_exists("peashooter.png")
            self.wallnut = load_if_exists("wallnut.png")
            self.slowflower = load_if_exists("slowflower.png")
            self.zombie = load_if_exists("zombie.png")
            self.large_zombie = load_if_exists("big_zombie.png")
            self.boss_zombie = load_if_exists("boss_zombie.png")
            self.pea = load_if_exists("pea.png")
            self.sun = load_if_exists("sun.png")

        except Exception as e:
            print(f"Warning: Could not load some assets: {e}")


assets = None 


# ---------------------------------------------------------
# SOUND ASSETS (music handled in VIEW per assignment)
# ---------------------------------------------------------
class SoundAssets:
    def __init__(self):
        self.shoot_sound = None
        self.hit_sound = None
        self.plant_sound = None
        self.sun_sound = None
        self.level_up_sound = None
        
        self.load_all()
    
    def load_all(self):
        """Initialize mixer and load background music."""
        try:
            pygame.mixer.init()
        except:
            pass

        # Load background music
        music_path = os.path.join("assets", "music.mp3")
        if os.path.exists(music_path):
            try:
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(0.5)
            except:
                print("Could not load music file.")

    # Sound effect helpers (optional)
    def play_shoot(self):
        if self.shoot_sound:
            self.shoot_sound.play()
    
    def play_hit(self):
        if self.hit_sound:
            self.hit_sound.play()
    
    def play_plant(self):
        if self.plant_sound:
            self.plant_sound.play()
    
    def play_sun(self):
        if self.sun_sound:
            self.sun_sound.play()
    
    def play_level_up(self):
        if self.level_up_sound:
            self.level_up_sound.play()


sounds = SoundAssets()


# ---------------------------------------------------------
# BUILD UI (START MUSIC HERE — REQUIRED BY ASSIGNMENT)
# ---------------------------------------------------------
def build_ui(config: LawnConfig) -> pygame.Surface:
    pygame.init()
    screen = pygame.display.set_mode((config.width, config.height + UI_HEIGHT))
    pygame.display.set_caption("Plants vs Zombies - Python Edition")
    
    global assets
    assets = ImageAssets()

    # Start background music (assignment requirement: music in view)
    try:
        pygame.mixer.music.play(-1)  # loop forever
    except:
        print("Music failed to play.")

    return screen


# ---------------------------------------------------------
# REDRAW EVERYTHING
# ---------------------------------------------------------
def redraw(screen: pygame.Surface, state: LawnState, config: LawnConfig):
    screen.fill(COLOR_BG)
    if assets and assets.background:
        screen.blit(assets.background, (0, UI_HEIGHT))
    
    # UI panel
    pygame.draw.rect(screen, COLOR_UI_BG, (0, 0, config.width, UI_HEIGHT))
    pygame.draw.line(screen, (100, 100, 100), (0, UI_HEIGHT), (config.width, UI_HEIGHT), 2)
    
    # Suns
    for sun in state.suns:
        if not sun["collected"]:
            sun_x = int(sun["x"])
            sun_y = int(sun["y"]) + UI_HEIGHT
            
            if assets.sun:
                screen.blit(assets.sun, (sun_x - 30, sun_y - 30))
            else:
                pygame.draw.circle(screen, (255, 255, 0), (sun_x, sun_y), 30)
    
    # Sun counter
    font_large = pygame.font.SysFont("arial", 24, bold=True)
    sun_text = font_large.render(f"Suns: {state.sun_count}", True, COLOR_HIGHLIGHT)
    screen.blit(sun_text, (400, 40))
    
    # Level indicator
    level_text = font_large.render(f"Level {state.level}", True, COLOR_TEXT)
    screen.blit(level_text, (config.width // 2 - 50, 15))
    
    # Kill counter
    kills_text = font_large.render(f"Kills: {state.zombies_killed}/{config.level_targets[state.level]}", True, COLOR_TEXT)
    screen.blit(kills_text, (config.width - 250, 15))
    
    # Plant selection cards
    font_small = pygame.font.SysFont("arial", 12)
    card_y = 10
    card_width = 70
    card_height = 60
    card_x_start = 20
    
    plant_cards = [
        ("peashooter", "Pea\n100", assets.peashooter, (0, 200, 0)),
        ("wallnut", "Wall\n50", assets.wallnut, (139, 69, 19)),
        ("slowflower", "Slow\n75", assets.slowflower, (200, 100, 200))
    ]
    
    for i, (plant_type, label, img, color) in enumerate(plant_cards):
        card_x = card_x_start + i * (card_width + 10)
        
        border_color = COLOR_HIGHLIGHT if state.selected_plant == plant_type else (150, 150, 150)
        border_width = 3 if state.selected_plant == plant_type else 2
        
        pygame.draw.rect(screen, border_color, (card_x, card_y, card_width, card_height), border_width)
        
        if img:
            img_resized = pygame.transform.scale(img, (50, 50))
            screen.blit(img_resized, (card_x + 10, card_y + 5))
        else:
            pygame.draw.circle(screen, color, (card_x + 35, card_y + 30), 20)
        
        cost_text = font_small.render(label, True, COLOR_TEXT)
        screen.blit(cost_text, (card_x + 5, card_y + 45))
    
    # Grid
    cell_w = config.width // config.columns
    cell_h = config.height // config.rows
    
    for row in range(config.rows + 1):
        y = UI_HEIGHT + row * cell_h
        pygame.draw.line(screen, COLOR_GRID, (0, y), (config.width, y), 1)
    
    for col in range(config.columns + 1):
        x = col * cell_w
        pygame.draw.line(screen, COLOR_GRID, (x, UI_HEIGHT), (x, UI_HEIGHT + config.height), 1)
    
    # Plants
    for (row, col), plant in state.plants.items():
        plant_type = plant["type"]
        px1, py1, px2, py2 = get_cell_bounds(row, col, config)
        py1 += UI_HEIGHT
        py2 += UI_HEIGHT
        
        plant_x = px1 + (px2 - px1) // 2
        plant_y = py1 + (py2 - py1) // 2
        
        img = None
        if plant_type == "peashooter":
            img = assets.peashooter
        elif plant_type == "wallnut":
            img = assets.wallnut
        elif plant_type == "slowflower":
            img = assets.slowflower
        
        if img:
            img = pygame.transform.scale(img, (50, 50))
            screen.blit(img, (plant_x - 25, plant_y - 25))
        
        # Health bar
        if "max_health" in plant:
            max_health = plant["max_health"]
        elif plant_type == "peashooter":
            max_health = 20
        elif plant_type == "wallnut":
            max_health = 35
        elif plant_type == "slowflower":
            max_health = 12
        else:
            max_health = 30

        health_ratio = plant["health"] / max_health
        health_ratio = max(0, min(1, health_ratio))
        bar_width = (px2 - px1) - 10
        bar_height = 4

        pygame.draw.rect(screen, (200, 0, 0), (px1 + 5, py2 - 8, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 200, 0), (px1 + 5, py2 - 8, bar_width * health_ratio, bar_height))
    
    # Peas
    for pea in state.peas:
        pea_x = int(pea["x"])
        pea_y = int(pea["row"] * cell_h + cell_h / 2 + UI_HEIGHT)
        
        if assets.pea:
            screen.blit(assets.pea, (pea_x - 12, pea_y - 12))
        else:
            pygame.draw.circle(screen, (200, 255, 0), (pea_x, pea_y), 8)
    
    # Zombies
    for zombie in state.zombies:
        row = zombie["row"]
        zx = int(zombie["x"])
        zy = int(row * cell_h + cell_h / 2 + UI_HEIGHT)
        
        img = None
        if zombie["type"] == "boss":
            img = assets.boss_zombie
        elif zombie["type"] == "large":
            img = assets.large_zombie
        else:
            img = assets.zombie
        
        if img:
            size = (80, 100) if zombie["type"] == "boss" else (60, 75) if zombie["type"] == "large" else (50, 60)
            img = pygame.transform.scale(img, size)
            screen.blit(img, (zx - size[0] // 2, zy - size[1] // 2))
        else:
            pygame.draw.rect(screen, (120, 60, 60), (zx - 20, zy - 20, 40, 40))
        
        # Health bar
        if zombie["type"] == "large":
            max_hp = config.large_zombie_health
        elif zombie["type"] == "boss":
            max_hp = config.boss_zombie_health
        else:
            max_hp = config.zombie_health
        
        health_ratio = max(0, zombie["health"]) / max_hp
        bar_width = 40
        bar_x = zx - bar_width // 2
        
        pygame.draw.rect(screen, (200, 0, 0), (bar_x, zy + 25, bar_width, 4))
        pygame.draw.rect(screen, (0, 200, 0), (bar_x, zy + 25, bar_width * health_ratio, 4))
    
    # Slowflower effect
    cell_width = config.width / config.columns
    cell_height = config.height / config.rows
    
    for (prow, pcol), plant in state.plants.items():
        if plant["type"] == "slowflower":
            px, py = get_cell_center(prow, pcol, config)
            py += UI_HEIGHT
            
            effect_radius = int(max(cell_width, cell_height) * 2)
            pygame.draw.circle(screen, (200, 100, 200), (int(px), int(py)), effect_radius, 1)
    
    pygame.display.flip()


# ---------------------------------------------------------
# LEVEL TRANSITION / VICTORY / GAME OVER
# ---------------------------------------------------------
def draw_level_transition(screen: pygame.Surface, config: LawnConfig, level: int):
    overlay = pygame.Surface((config.width, config.height + UI_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    font_huge = pygame.font.SysFont("arial", 100, bold=True)
    text = font_huge.render(f"LEVEL {level}", True, COLOR_HIGHLIGHT)
    text_rect = text.get_rect(center=(config.width // 2, (config.height + UI_HEIGHT) // 2))
    screen.blit(text, text_rect)
    
    pygame.display.flip()


def draw_victory(screen: pygame.Surface, config: LawnConfig):
    screen.fill((10, 80, 10))
    
    font_huge = pygame.font.SysFont("arial", 100, bold=True)
    font_large = pygame.font.SysFont("arial", 40)
    
    text1 = font_huge.render("YOU WIN!", True, COLOR_HIGHLIGHT)
    text2 = font_large.render("All levels completed!", True, COLOR_TEXT)
    
    screen.blit(text1, (config.width // 2 - 200, config.height // 2 - 100))
    screen.blit(text2, (config.width // 2 - 200, config.height // 2 + 50))
    
    pygame.display.flip()


def draw_game_over(screen: pygame.Surface, config: LawnConfig):
    screen.fill((100, 0, 0))
    
    font_huge = pygame.font.SysFont("arial", 100, bold=True)
    font_large = pygame.font.SysFont("arial", 40)
    font_medium = pygame.font.SysFont("arial", 30)
    
    text1 = font_huge.render("GAME OVER", True, COLOR_TEXT)
    text2 = font_large.render("A zombie reached your house!", True, COLOR_TEXT)
    text3 = font_medium.render("Press 'R' to restart level or 'G' for Game Start", True, COLOR_HIGHLIGHT)
    
    screen.blit(text1, (config.width // 2 - 250, config.height // 2 - 150))
    screen.blit(text2, (config.width // 2 - 250, config.height // 2 - 30))
    screen.blit(text3, (config.width // 2 - 350, config.height // 2 + 100))
    
    pygame.display.flip()
