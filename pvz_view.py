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

#loads all game images
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
        """Load all image assets"""
        asset_dir = "assets"
        
        try:
            if os.path.exists(os.path.join(asset_dir, "background.png")):
                self.background = pygame.image.load(os.path.join(asset_dir, "background.png"))
            if os.path.exists(os.path.join(asset_dir, "peashooter.png")):
                self.peashooter = pygame.image.load(os.path.join(asset_dir, "peashooter.png"))
            if os.path.exists(os.path.join(asset_dir, "wallnut.png")):
                self.wallnut = pygame.image.load(os.path.join(asset_dir, "wallnut.png"))
            if os.path.exists(os.path.join(asset_dir, "slowflower.png")):
                self.slowflower = pygame.image.load(os.path.join(asset_dir, "slowflower.png"))
            if os.path.exists(os.path.join(asset_dir, "zombie.png")):
                self.zombie = pygame.image.load(os.path.join(asset_dir, "zombie.png"))
            if os.path.exists(os.path.join(asset_dir, "big_zombie.png")):
                self.large_zombie = pygame.image.load(os.path.join(asset_dir, "big_zombie.png"))
            if os.path.exists(os.path.join(asset_dir, "boss_zombie.png")):
                self.boss_zombie = pygame.image.load(os.path.join(asset_dir, "boss_zombie.png"))
            if os.path.exists(os.path.join(asset_dir, "pea.png")):
                self.pea = pygame.image.load(os.path.join(asset_dir, "pea.png"))
            if os.path.exists(os.path.join(asset_dir, "sun.png")):
                self.sun = pygame.image.load(os.path.join(asset_dir, "sun.png"))
        except Exception as e:
            print(f"Warning: Could not load some assets: {e}")


assets = None 


#load sound effects
class SoundAssets:
    def __init__(self):
        self.shoot_sound = None
        self.hit_sound = None
        self.plant_sound = None
        self.sun_sound = None
        self.level_up_sound = None
        self.music = None
        
        self.load_all()
    
    def load_all(self):
        """Load all sounds - using simple beep if files not available"""
        try:
            pygame.mixer.init()
        except:
            pass
    
    def play_shoot(self):
        """Play shoot sound"""
        if self.shoot_sound:
            self.shoot_sound.play()
    
    def play_hit(self):
        """Play hit sound"""
        if self.hit_sound:
            self.hit_sound.play()
    
    def play_plant(self):
        """Play plant placed sound"""
        if self.plant_sound:
            self.plant_sound.play()
    
    def play_sun(self):
        """Play sun collected sound"""
        if self.sun_sound:
            self.sun_sound.play()
    
    def play_level_up(self):
        """Play level up sound"""
        if self.level_up_sound:
            self.level_up_sound.play()


sounds = SoundAssets()



#renders the screen initially
def build_ui(config: LawnConfig) -> pygame.Surface:
    """Initialize pygame and create the game screen"""
    pygame.init()
    screen = pygame.display.set_mode((config.width, config.height + UI_HEIGHT))
    pygame.display.set_caption("Plants vs Zombies - Python Edition")
    
    global assets
    assets = ImageAssets()
    
    return screen


def redraw(screen: pygame.Surface, state: LawnState, config: LawnConfig):
    """Redraw the entire game screen"""
#background
    screen.fill(COLOR_BG)
    if assets and assets.background:
        screen.blit(assets.background, (0, UI_HEIGHT))
    
   #ui panel
    pygame.draw.rect(screen, COLOR_UI_BG, (0, 0, config.width, UI_HEIGHT))
    pygame.draw.line(screen, (100, 100, 100), (0, UI_HEIGHT), (config.width, UI_HEIGHT), 2)
    
#suns
    for sun in state.suns:
        if not sun["collected"]:
            sun_x = int(sun["x"])
            sun_y = int(sun["y"]) + UI_HEIGHT
            
            if assets and assets.sun:
                screen.blit(assets.sun, (sun_x - 30, sun_y - 30))
            else:
                pygame.draw.circle(screen, (255, 255, 0), (sun_x, sun_y), 30)
                pygame.draw.circle(screen, (255, 200, 0), (sun_x, sun_y), 30, 2)
    
    # Sun counter
    font_large = pygame.font.SysFont("arial", 24, bold=True)
    sun_text = font_large.render(f"Suns: {state.sun_count}", True, COLOR_HIGHLIGHT)
    screen.blit(sun_text, (400, 40))
    
  #level indivator
    level_text = font_large.render(f"Level {state.level}", True, COLOR_TEXT)
    screen.blit(level_text, (config.width // 2 - 50, 15))
    
#kill counter in level and required kills to beat level
    kills_text = font_large.render(f"Kills: {state.zombies_killed}/{config.level_targets[state.level]}", True, COLOR_TEXT)
    screen.blit(kills_text, (config.width - 250, 15))
    
    #plant selection panel
    font_small = pygame.font.SysFont("arial", 12)
    
    # calculate card positions
    card_y = 10
    card_width = 70
    card_height = 60
    card_x_start = 20
    
    plant_cards = [
        ("peashooter", "Pea\n100", assets.peashooter if assets else None, (0, 200, 0)),
        ("wallnut", "Wall\n50", assets.wallnut if assets else None, (139, 69, 19)),
        ("slowflower", "Slow\n75", assets.slowflower if assets else None, (200, 100, 200))
    ]
    
    for i, (plant_type, label, img, color) in enumerate(plant_cards):
        card_x = card_x_start + i * (card_width + 10)
        
        # Highlight selected plant
        border_color = COLOR_HIGHLIGHT if state.selected_plant == plant_type else (150, 150, 150)
        border_width = 3 if state.selected_plant == plant_type else 2
        
        pygame.draw.rect(screen, border_color, (card_x, card_y, card_width, card_height), border_width)
        
        # Draw plant image
        if img:
            img_resized = pygame.transform.scale(img, (50, 50))
            screen.blit(img_resized, (card_x + 10, card_y + 5))
        else:
            pygame.draw.circle(screen, color, (card_x + 35, card_y + 30), 20)
        
        # Draw cost text
        cost_text = font_small.render(label, True, COLOR_TEXT)
        screen.blit(cost_text, (card_x + 5, card_y + 45))
    
    # makes grid
    cell_w = config.width // config.columns
    cell_h = config.height // config.rows
    
    for row in range(config.rows + 1):
        y = UI_HEIGHT + row * cell_h
        pygame.draw.line(screen, COLOR_GRID, (0, y), (config.width, y), 1)
    
    for col in range(config.columns + 1):
        x = col * cell_w
        pygame.draw.line(screen, COLOR_GRID, (x, UI_HEIGHT), (x, UI_HEIGHT + config.height), 1)
    
    # Renders plants
    for (row, col), plant in state.plants.items():
        plant_type = plant["type"]
        px1, py1, px2, py2 = get_cell_bounds(row, col, config)
        py1 += UI_HEIGHT
        py2 += UI_HEIGHT
        
        plant_x = px1 + (px2 - px1) // 2
        plant_y = py1 + (py2 - py1) // 2
        
        # Draw plant based on type
        if plant_type == "peashooter" and assets and assets.peashooter:
            img = pygame.transform.scale(assets.peashooter, (50, 50))
            screen.blit(img, (plant_x - 25, plant_y - 25))
        elif plant_type == "wallnut" and assets and assets.wallnut:
            img = pygame.transform.scale(assets.wallnut, (50, 50))
            screen.blit(img, (plant_x - 25, plant_y - 25))
        elif plant_type == "slowflower" and assets and assets.slowflower:
            img = pygame.transform.scale(assets.slowflower, (50, 50))
            screen.blit(img, (plant_x - 25, plant_y - 25))
        
        # Draw health bar
        health_ratio = plant["health"] / 30.0
        health_ratio = max(0, min(1, health_ratio))
        bar_width = (px2 - px1) - 10
        bar_height = 4
        
        pygame.draw.rect(screen, (200, 0, 0), (px1 + 5, py2 - 8, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 200, 0), (px1 + 5, py2 - 8, bar_width * health_ratio, bar_height))
    
    #draw projectiles
    for pea in state.peas:
        pea_x = int(pea["x"])
        pea_y = int(pea["row"] * cell_h + cell_h / 2 + UI_HEIGHT)
        
        if assets and assets.pea:
            screen.blit(assets.pea, (pea_x - 12, pea_y - 12))
        else:
            pygame.draw.circle(screen, (200, 255, 0), (pea_x, pea_y), 8)
    
    # Draw zombies
    for zombie in state.zombies:
        row = zombie["row"]
        zx = int(zombie["x"])
        zy = int(row * cell_h + cell_h / 2 + UI_HEIGHT)
        
        # Select correct zombie image
        if zombie["type"] == "boss" and assets and assets.boss_zombie:
            img = pygame.transform.scale(assets.boss_zombie, (80, 100))
            screen.blit(img, (zx - 40, zy - 50))
        elif zombie["type"] == "large" and assets and assets.large_zombie:
            img = pygame.transform.scale(assets.large_zombie, (60, 75))
            screen.blit(img, (zx - 30, zy - 38))
        elif zombie["type"] == "normal" and assets and assets.zombie:
            img = pygame.transform.scale(assets.zombie, (50, 60))
            screen.blit(img, (zx - 25, zy - 30))
        else:
            # Fallback to colored rect
            if zombie["type"] == "boss":
                size = 40
            elif zombie["type"] == "large":
                size = 30
            else:
                size = 20
            pygame.draw.rect(screen, (120, 60, 60), (zx - size, zy - size, size * 2, size * 2))
        
        # Draw zombie health bar
        health_ratio = max(0, zombie["health"]) / config.zombie_health
        if zombie["type"] == "large":
            health_ratio = max(0, zombie["health"]) / config.large_zombie_health
        elif zombie["type"] == "boss":
            health_ratio = max(0, zombie["health"]) / config.boss_zombie_health
        
        bar_width = 40
        bar_x = zx - bar_width // 2
        
        pygame.draw.rect(screen, (200, 0, 0), (bar_x, zy + 25, bar_width, 4))
        pygame.draw.rect(screen, (0, 200, 0), (bar_x, zy + 25, bar_width * health_ratio, 4))
    
    # show the effect of the slowflower
    cell_width = config.width / config.columns
    cell_height = config.height / config.rows
    
    for (prow, pcol), plant in state.plants.items():
        if plant["type"] == "slowflower":
            px, py = get_cell_center(prow, pcol, config)
            py += UI_HEIGHT
            
            effect_radius = int(max(cell_width, cell_height) * 2)
            pygame.draw.circle(screen, (200, 100, 200), (int(px), int(py)), effect_radius, 1)
    
    pygame.display.flip()


def draw_level_transition(screen: pygame.Surface, config: LawnConfig, level: int):
    """Draw level transition screen"""
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
    """Draw victory screen"""
    screen.fill((10, 80, 10))
    
    font_huge = pygame.font.SysFont("arial", 100, bold=True)
    font_large = pygame.font.SysFont("arial", 40)
    
    text1 = font_huge.render("YOU WIN!", True, COLOR_HIGHLIGHT)
    text2 = font_large.render("All levels completed!", True, COLOR_TEXT)
    
    screen.blit(text1, (config.width // 2 - 200, config.height // 2 - 100))
    screen.blit(text2, (config.width // 2 - 200, config.height // 2 + 50))
    
    pygame.display.flip()

#show game over screen and options to restart
def draw_game_over(screen: pygame.Surface, config: LawnConfig):
    """Draw game over screen with restart options"""
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