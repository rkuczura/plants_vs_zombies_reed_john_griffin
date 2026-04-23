"""Generate game assets using PIL"""
import os
from PIL import Image, ImageDraw, ImageFont

asset_dir = "assets"
os.makedirs(asset_dir, exist_ok=True)

#Background generated here
bg = Image.new('RGB', (1350, 750), color=(34, 139, 34))
bg_draw = ImageDraw.Draw(bg)
# Add some grass texture
for i in range(0, 1350, 50):
    for j in range(0, 750, 50):
        bg_draw.rectangle([i, j, i+50, j+50], outline=(20, 120, 20))
bg.save(os.path.join(asset_dir, "background.png"))
print("✓ Generated background.png")

#Plants generated here

# Peashooter (green circular plant)
peashooter = Image.new('RGBA', (60, 60), color=(0, 0, 0, 0))
draw = ImageDraw.Draw(peashooter)
draw.ellipse([5, 5, 55, 55], fill=(0, 200, 0), outline=(0, 100, 0), width=3)
draw.ellipse([15, 15, 45, 45], fill=(100, 255, 100))
peashooter.save(os.path.join(asset_dir, "peashooter.png"))
print("✓ Generated peashooter.png")

# Wallnut (brown defensive plant)
wallnut = Image.new('RGBA', (60, 60), color=(0, 0, 0, 0))
draw = ImageDraw.Draw(wallnut)
draw.ellipse([5, 5, 55, 55], fill=(139, 69, 19), outline=(80, 40, 10), width=3)
draw.ellipse([15, 10, 45, 30], fill=(200, 100, 50))  # Crack
wallnut.save(os.path.join(asset_dir, "wallnut.png"))
print("✓ Generated wallnut.png")

# Slowflower (purple slowing plant)
slowflower = Image.new('RGBA', (60, 60), color=(0, 0, 0, 0))
draw = ImageDraw.Draw(slowflower)
draw.ellipse([5, 5, 55, 55], fill=(200, 100, 200), outline=(100, 0, 100), width=3)
draw.polygon([(30, 10), (20, 30), (40, 30)], fill=(255, 200, 255))  # Petals
draw.ellipse([24, 24, 36, 36], fill=(100, 50, 100))
slowflower.save(os.path.join(asset_dir, "slowflower.png"))
print("✓ Generated slowflower.png")

# ==================== ZOMBIES ====================

# Normal Zombie (brown humanoid)
zombie = Image.new('RGBA', (50, 60), color=(0, 0, 0, 0))
draw = ImageDraw.Draw(zombie)
draw.ellipse([10, 5, 40, 25], fill=(120, 60, 60), outline=(0, 0, 0), width=2)  # Head
draw.rectangle([12, 25, 38, 45], fill=(100, 50, 50), outline=(0, 0, 0), width=2)  # Body
draw.rectangle([10, 45, 20, 60], fill=(80, 40, 40), outline=(0, 0, 0), width=1)  # Leg
draw.rectangle([30, 45, 40, 60], fill=(80, 40, 40), outline=(0, 0, 0), width=1)  # Leg
draw.ellipse([15, 12, 22, 18], fill=(255, 255, 255))  # Eye
draw.ellipse([28, 12, 35, 18], fill=(255, 255, 255))  # Eye
zombie.save(os.path.join(asset_dir, "zombie.png"))
print("✓ Generated zombie.png")

# Big Zombie (large and armored)
big_zombie = Image.new('RGBA', (70, 80), color=(0, 0, 0, 0))
draw = ImageDraw.Draw(big_zombie)
draw.ellipse([15, 5, 55, 30], fill=(100, 50, 50), outline=(0, 0, 0), width=3)  # Head
draw.rectangle([12, 30, 58, 60], fill=(80, 40, 40), outline=(0, 0, 0), width=3)  # Body
draw.rectangle([10, 60, 25, 80], fill=(60, 30, 30), outline=(0, 0, 0), width=2)  # Leg
draw.rectangle([45, 60, 60, 80], fill=(60, 30, 30), outline=(0, 0, 0), width=2)  # Leg
draw.ellipse([20, 15, 30, 25], fill=(255, 255, 255))  # Eye
draw.ellipse([40, 15, 50, 25], fill=(255, 255, 255))  # Eye
draw.rectangle([20, 35, 50, 40], fill=(100, 50, 50))  # Armor band
big_zombie.save(os.path.join(asset_dir, "big_zombie.png"))
print("✓ Generated big_zombie.png")

# Boss Zombie (very large with extra armor)
boss_zombie = Image.new('RGBA', (100, 120), color=(0, 0, 0, 0))
draw = ImageDraw.Draw(boss_zombie)
draw.ellipse([20, 10, 80, 45], fill=(60, 30, 30), outline=(0, 0, 0), width=4)  # Head
draw.rectangle([15, 45, 85, 90], fill=(50, 25, 25), outline=(0, 0, 0), width=4)  # Body
draw.rectangle([10, 90, 35, 120], fill=(40, 20, 20), outline=(0, 0, 0), width=3)  # Leg
draw.rectangle([65, 90, 90, 120], fill=(40, 20, 20), outline=(0, 0, 0), width=3)  # Leg
draw.ellipse([30, 20, 45, 35], fill=(255, 255, 255))  # Eye
draw.ellipse([55, 20, 70, 35], fill=(255, 255, 255))  # Eye
draw.rectangle([25, 50, 75, 60], fill=(139, 69, 19), width=2)  # Armor
draw.rectangle([25, 65, 75, 75], fill=(139, 69, 19), width=2)  # Armor
boss_zombie.save(os.path.join(asset_dir, "boss_zombie.png"))
print("✓ Generated boss_zombie.png")

# ==================== PROJECTILE ====================

# Pea Projectile - made larger for visibility on 150x150 grid
pea = Image.new('RGBA', (24, 24), color=(0, 0, 0, 0))
draw = ImageDraw.Draw(pea)
draw.ellipse([2, 2, 22, 22], fill=(200, 255, 0), outline=(100, 150, 0), width=2)
draw.ellipse([8, 8, 16, 16], fill=(255, 255, 150))  # Inner highlight
pea.save(os.path.join(asset_dir, "pea.png"))
print("✓ Generated pea.png")

# ==================== SUN ====================

sun = Image.new('RGBA', (60, 60), color=(0, 0, 0, 0))
draw = ImageDraw.Draw(sun)
draw.ellipse([5, 5, 55, 55], fill=(255, 255, 0), outline=(255, 200, 0), width=3)
# Draw sun rays
for angle in range(0, 360, 45):
    import math
    x1 = 30 + 25 * math.cos(math.radians(angle))
    y1 = 30 + 25 * math.sin(math.radians(angle))
    x2 = 30 + 37 * math.cos(math.radians(angle))
    y2 = 30 + 37 * math.sin(math.radians(angle))
    draw.line([(x1, y1), (x2, y2)], fill=(255, 200, 0), width=3)
sun.save(os.path.join(asset_dir, "sun.png"))
print("✓ Generated sun.png")

print("\n✅ All assets generated successfully!")
