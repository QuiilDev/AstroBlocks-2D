import pygame
import sys
import random
import math

pygame.init()

BLOCK_SIZE = 40  
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
COLS, ROWS = 256, 45  
WORLD_PIXEL_WIDTH = COLS * BLOCK_SIZE
WORLD_PIXEL_HEIGHT = ROWS * BLOCK_SIZE

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("AstroBlocks 2D")
clock = pygame.time.Clock()

AIR = 0
GRASS = 1
DIRT = 2
STONE = 3
WOOD = 4
LEAVES = 5
COAL_ORE = 6
IRON_ORE = 7
GOLD_ORE = 8
DIAMOND_ORE = 9
REDSTONE_ORE = 10
GLASS = 11
BRICK = 12
WOOL = 13
PLANKS = 14
SAND = 15
NEON = 16
AMETHYST = 17
EMERALD = 18
LAPIS = 19
COPPER = 20
QUARTZ = 21
COAL_BLOCK = 22
IRON_BLOCK = 23
GOLD_BLOCK = 24
BLACKSTONE = 25
TERRACOTTA = 26
GLOWSTONE = 27
RED_BRICK = 28
BLUE_WOOL = 29
GREEN_WOOL = 30
TORCH = 31
CRAFTING_TABLE = 32
FURNACE = 33
BED = 34
PORTAL = 35  
LEVER = 36
PISTON = 37
PISTON_HEAD = 38
RAILS = 39
MINECART_ITEM = 40
GREENSTONE_WIRE = 41
GREEN_DYNAMITE = 42
CHEST = 43
BOW = 44
ARROW = 45
JETPACK = 46
LAVA = 47
CHARGER = 48
BOSS_ALTAR = 49

PICKAXE = 99  

SKY_BLUE = (135, 206, 235)
BLOCK_COLORS = {
    GRASS: (34, 139, 34), DIRT: (139, 69, 19), STONE: (120, 120, 120),
    WOOD: (101, 67, 33), LEAVES: (46, 115, 46), COAL_ORE: (60, 60, 60),
    IRON_ORE: (210, 180, 140), GOLD_ORE: (255, 215, 0), DIAMOND_ORE: (0, 255, 255),
    REDSTONE_ORE: (255, 0, 0), GLASS: (200, 240, 255), BRICK: (178, 34, 34),
    WOOL: (240, 240, 240), PLANKS: (222, 184, 135), SAND: (238, 214, 175),
    NEON: (0, 255, 128), AMETHYST: (153, 50, 204), EMERALD: (0, 201, 87),
    LAPIS: (25, 25, 112), COPPER: (184, 115, 51), QUARTZ: (245, 245, 245),
    COAL_BLOCK: (30, 30, 30), IRON_BLOCK: (220, 220, 220), GOLD_BLOCK: (255, 215, 0),
    BLACKSTONE: (45, 45, 48), TERRACOTTA: (210, 105, 30), GLOWSTONE: (255, 236, 139),
    RED_BRICK: (165, 42, 42), BLUE_WOOL: (0, 0, 205), GREEN_WOOL: (0, 128, 0),
    TORCH: (255, 165, 0), CRAFTING_TABLE: (160, 82, 45), FURNACE: (105, 105, 105),
    BED: (220, 20, 60), PORTAL: (0, 240, 255), LEVER: (120, 120, 120),
    PISTON: (140, 110, 80), PISTON_HEAD: (180, 150, 120), RAILS: (192, 192, 192),
    MINECART_ITEM: (112, 128, 144), GREENSTONE_WIRE: (20, 60, 20),
    GREEN_DYNAMITE: (0, 200, 50), CHEST: (139, 105, 20), BOW: (200, 150, 100),
    ARROW: (220, 220, 220), JETPACK: (150, 40, 40), LAVA: (230, 70, 0),
    CHARGER: (60, 70, 90), BOSS_ALTAR: (75, 0, 130)
}

inventory_font = pygame.font.SysFont("Arial", 16)
BLOCK_TEXTURES = {}
LEVER_ACTIVE_TEXTURES = {}
GREENSTONE_ACTIVE_TEXTURES = {}

def generate_textures():
    for block_id, color in BLOCK_COLORS.items():
        surf = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        surf.fill(color)
        
        if block_id == GRASS:
            surf.fill((135, 80, 45)) 
            pygame.draw.rect(surf, (34, 155, 34), (0, 0, BLOCK_SIZE, 12)) 
            pygame.draw.rect(surf, (24, 120, 24), (0, 0, BLOCK_SIZE, 4)) 
            pygame.draw.line(surf, (55, 180, 55), (2, 11), (5, 14), 2)
            pygame.draw.line(surf, (55, 180, 55), (12, 11), (14, 16), 2)
            pygame.draw.line(surf, (55, 180, 55), (22, 11), (25, 15), 2)
            pygame.draw.line(surf, (55, 180, 55), (32, 11), (34, 17), 2)
            pygame.draw.rect(surf, (100, 60, 30), (4, 22, 4, 4))
            pygame.draw.rect(surf, (100, 60, 30), (24, 28, 5, 3))
            
        elif block_id == DIRT:
            surf.fill((135, 80, 45))
            pygame.draw.rect(surf, (105, 60, 30), (0, 0, BLOCK_SIZE, BLOCK_SIZE), 2)
            pygame.draw.rect(surf, (100, 60, 30), (6, 8, 5, 5))
            pygame.draw.rect(surf, (100, 60, 30), (22, 24, 6, 4))
            pygame.draw.rect(surf, (160, 100, 65), (14, 16, 4, 4))
            
        elif block_id == STONE:
            surf.fill((110, 110, 110))
            pygame.draw.rect(surf, (80, 80, 80), (0, 0, BLOCK_SIZE, BLOCK_SIZE), 2)
            pygame.draw.line(surf, (75, 75, 75), (4, 10), (14, 10), 2)
            pygame.draw.line(surf, (75, 75, 75), (14, 10), (18, 22), 2)
            pygame.draw.line(surf, (140, 140, 140), (2, 2), (38, 2), 2)
            pygame.draw.line(surf, (140, 140, 140), (2, 2), (2, 38), 2)
            pygame.draw.rect(surf, (90, 90, 90), (25, 25, 6, 6))

        elif block_id in [COAL_ORE, IRON_ORE, GOLD_ORE, DIAMOND_ORE, REDSTONE_ORE]:
            surf.fill((110, 110, 110))
            pygame.draw.rect(surf, (80, 80, 80), (0, 0, BLOCK_SIZE, BLOCK_SIZE), 2)
            pygame.draw.line(surf, (140, 140, 140), (2, 2), (38, 2), 1)
            pygame.draw.line(surf, (140, 140, 140), (2, 2), (2, 38), 1)
            pygame.draw.rect(surf, color, (8, 6, 8, 6))
            pygame.draw.rect(surf, color, (22, 12, 6, 8))
            pygame.draw.rect(surf, color, (6, 24, 10, 6))
            pygame.draw.rect(surf, color, (24, 26, 8, 8))
            pygame.draw.rect(surf, (255, 255, 255) if block_id == DIAMOND_ORE else color, (26, 14, 3, 3))

        elif block_id == PLANKS:
            surf.fill((190, 145, 90))
            pygame.draw.rect(surf, (130, 95, 50), (0, 0, BLOCK_SIZE, BLOCK_SIZE), 2)
            pygame.draw.line(surf, (130, 95, 50), (0, 13), (BLOCK_SIZE, 13), 2)
            pygame.draw.line(surf, (130, 95, 50), (0, 26), (BLOCK_SIZE, 26), 2)
            pygame.draw.line(surf, (130, 95, 50), (16, 0), (16, 13), 2)
            pygame.draw.line(surf, (130, 95, 50), (28, 13), (28, 26), 2)
            pygame.draw.line(surf, (130, 95, 50), (12, 26), (12, 40), 2)
            pygame.draw.line(surf, (215, 175, 120), (2, 2), (38, 2), 1)

        elif block_id == GLASS:
            surf.fill((160, 220, 240))
            surf.set_alpha(150)
            pygame.draw.rect(surf, (255, 255, 255), (0, 0, BLOCK_SIZE, BLOCK_SIZE), 2)
            pygame.draw.line(surf, (255, 255, 255), (6, 34), (34, 6), 3)
            pygame.draw.line(surf, (255, 255, 255), (16, 34), (34, 16), 1)

        elif block_id in [BRICK, RED_BRICK]:
            surf.fill(color)
            pygame.draw.rect(surf, (50, 10, 10) if block_id == BRICK else (80, 20, 20), (0, 0, BLOCK_SIZE, BLOCK_SIZE), 2)
            pygame.draw.line(surf, (210, 210, 210), (0, 13), (BLOCK_SIZE, 13), 2)
            pygame.draw.line(surf, (210, 210, 210), (0, 26), (BLOCK_SIZE, 26), 2)
            pygame.draw.line(surf, (210, 210, 210), (14, 0), (14, 13), 2)
            pygame.draw.line(surf, (210, 210, 210), (26, 13), (26, 26), 2)
            pygame.draw.line(surf, (210, 210, 210), (18, 26), (18, 40), 2)
        elif block_id == CRAFTING_TABLE:
            surf.fill((140, 90, 45))
            pygame.draw.rect(surf, (75, 45, 15), (0, 0, BLOCK_SIZE, BLOCK_SIZE), 3)
            pygame.draw.rect(surf, (190, 145, 90), (4, 4, BLOCK_SIZE - 8, 8))
            pygame.draw.rect(surf, (60, 35, 10), (6, 18, 12, 16))
            pygame.draw.rect(surf, (100, 100, 100), (24, 20, 10, 10))

        elif block_id == FURNACE:
            surf.fill((90, 90, 90))
            pygame.draw.rect(surf, (50, 50, 50), (0, 0, BLOCK_SIZE, BLOCK_SIZE), 3)
            pygame.draw.rect(surf, (130, 130, 130), (3, 3, BLOCK_SIZE - 6, 8))
            pygame.draw.rect(surf, (25, 25, 25), (8, 18, 24, 16))
            pygame.draw.rect(surf, (230, 90, 10), (12, 22, 16, 10))
            pygame.draw.rect(surf, (255, 200, 30), (15, 25, 10, 5))

        elif block_id == BED:
            surf.fill((220, 220, 220))
            pygame.draw.rect(surf, (180, 20, 40), (12, 0, BLOCK_SIZE - 12, BLOCK_SIZE))
            pygame.draw.rect(surf, (130, 10, 25), (12, 34, BLOCK_SIZE - 12, 6))
            pygame.draw.rect(surf, (255, 255, 255), (2, 6, 8, 28))

        elif block_id == PORTAL:
            surf.set_alpha(200)
            pygame.draw.rect(surf, (0, 40, 80), (0, 0, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(surf, (0, 230, 255), (4, 4, BLOCK_SIZE - 8, BLOCK_SIZE - 8), 2)
            pygame.draw.line(surf, (255, 255, 255), (6, 6), (34, 34), 2)
            pygame.draw.line(surf, (255, 255, 255), (6, 34), (34, 6), 2)

        elif block_id == LEVER:
            pygame.draw.rect(surf, (80, 80, 80), (8, 28, 24, 12))
            pygame.draw.rect(surf, (40, 40, 40), (8, 28, 24, 12), 2)
            pygame.draw.line(surf, (180, 40, 40), (20, 28), (8, 8), 4)
            pygame.draw.circle(surf, (230, 50, 50), (8, 8), 5)
            
            act_surf = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
            act_surf.fill(color)
            act_surf.set_colorkey(color)
            pygame.draw.rect(act_surf, (80, 80, 80), (8, 28, 24, 12))
            pygame.draw.rect(act_surf, (40, 40, 40), (8, 28, 24, 12), 2)
            pygame.draw.line(act_surf, (40, 180, 80), (20, 28), (32, 8), 4)
            pygame.draw.circle(act_surf, (50, 230, 100), (32, 8), 5)
            LEVER_ACTIVE_TEXTURES[LEVER] = act_surf

        elif block_id == PISTON:
            surf.fill((100, 100, 100))
            pygame.draw.rect(surf, (50, 50, 50), (0, 0, 26, BLOCK_SIZE))
            pygame.draw.rect(surf, (150, 110, 70), (26, 0, 14, BLOCK_SIZE))
            pygame.draw.rect(surf, (100, 70, 40), (26, 0, 14, BLOCK_SIZE), 2)

        elif block_id == PISTON_HEAD:
            surf.fill(SKY_BLUE)
            surf.set_colorkey(SKY_BLUE)
            pygame.draw.rect(surf, (140, 140, 140), (0, 15, 26, 10))
            pygame.draw.rect(surf, (150, 110, 70), (26, 0, 14, BLOCK_SIZE))
            pygame.draw.rect(surf, (100, 70, 40), (26, 0, 14, BLOCK_SIZE), 2)

        elif block_id == RAILS:
            surf.fill(SKY_BLUE)
            surf.set_colorkey(SKY_BLUE)
            pygame.draw.rect(surf, (90, 60, 30), (4, 30, 8, 8))
            pygame.draw.rect(surf, (90, 60, 30), (28, 30, 8, 8))
            pygame.draw.line(surf, (180, 180, 180), (0, 28), (BLOCK_SIZE, 28), 3)
            pygame.draw.line(surf, (180, 180, 180), (0, 38), (BLOCK_SIZE, 38), 3)

        elif block_id == MINECART_ITEM:
            surf.fill(SKY_BLUE)
            surf.set_colorkey(SKY_BLUE)
            pygame.draw.rect(surf, (130, 140, 150), (2, 10, 36, 22))
            pygame.draw.rect(surf, (90, 100, 110), (6, 14, 28, 14))
            pygame.draw.circle(surf, (40, 40, 40), (10, 34), 6)
            pygame.draw.circle(surf, (30, 30, 30), (30, 34), 6)

        elif block_id == GREENSTONE_WIRE:
            surf.fill(SKY_BLUE)
            surf.set_colorkey(SKY_BLUE)
            pygame.draw.rect(surf, (10, 50, 10), (14, 14, 12, 12))
            pygame.draw.rect(surf, (20, 80, 20), (16, 16, 8, 8))
            
            act_surf = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
            act_surf.fill(SKY_BLUE)
            act_surf.set_colorkey(SKY_BLUE)
            pygame.draw.rect(act_surf, (0, 220, 60), (12, 12, 16, 16))
            pygame.draw.rect(act_surf, (180, 255, 200), (15, 15, 10, 10))
            GREENSTONE_ACTIVE_TEXTURES[GREENSTONE_WIRE] = act_surf

        elif block_id == GREEN_DYNAMITE:
            surf.fill((10, 130, 40))
            pygame.draw.rect(surf, (5, 80, 20), (0, 0, BLOCK_SIZE, BLOCK_SIZE), 3)
            pygame.draw.rect(surf, (240, 240, 240), (0, 14, BLOCK_SIZE, 12))
            pygame.draw.line(surf, (200, 200, 200), (20, 0), (20, 8), 2)
            pygame.draw.circle(surf, (255, 160, 10), (20, 0), 4)

        elif block_id == CHEST:
            surf.fill((140, 95, 40))
            pygame.draw.rect(surf, (80, 50, 15), (0, 0, BLOCK_SIZE, BLOCK_SIZE), 3)
            pygame.draw.line(surf, (80, 50, 15), (0, 18), (BLOCK_SIZE, 18), 3)
            pygame.draw.rect(surf, (230, 190, 20), (16, 14, 8, 10))
            pygame.draw.rect(surf, (50, 50, 50), (19, 19, 2, 3))

        elif block_id == BOW:
            surf.fill(SKY_BLUE)
            surf.set_colorkey(SKY_BLUE)
            pygame.draw.arc(surf, (160, 110, 60), (4, 4, 32, 32), 0.5, 3.8, 4)
            pygame.draw.line(surf, (230, 230, 230), (28, 6), (28, 34), 1)

        elif block_id == ARROW:
            surf.fill(SKY_BLUE)
            surf.set_colorkey(SKY_BLUE)
            pygame.draw.line(surf, (140, 110, 80), (4, 20), (32, 20), 2)
            pygame.draw.polygon(surf, (180, 180, 180), [(32, 20), (24, 14), (24, 26)])
            pygame.draw.line(surf, (255, 255, 255), (4, 15), (8, 20), 2)
            pygame.draw.line(surf, (255, 255, 255), (4, 25), (8, 20), 2)

        elif block_id == JETPACK:
            surf.fill(SKY_BLUE)
            surf.set_colorkey(SKY_BLUE)
            pygame.draw.rect(surf, (160, 40, 40), (8, 6, 24, 28))
            pygame.draw.rect(surf, (100, 20, 20), (12, 10, 16, 20))
            pygame.draw.rect(surf, (50, 50, 50), (10, 32, 6, 6))
            pygame.draw.rect(surf, (50, 50, 50), (24, 32, 6, 6))

        elif block_id == LAVA:
            pygame.draw.rect(surf, (255, 120, 0), (0, 0, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(surf, (200, 50, 0), (0, 8, BLOCK_SIZE, 8))
            pygame.draw.rect(surf, (255, 180, 30), (4, 24, 8, 4))
            pygame.draw.rect(surf, (255, 180, 30), (20, 12, 6, 4))

        elif block_id == CHARGER:
            pygame.draw.rect(surf, (40, 45, 55), (0, 0, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(surf, (0, 255, 200), (6, 6, BLOCK_SIZE - 12, BLOCK_SIZE - 12), 2)
            pygame.draw.polygon(surf, (0, 255, 200), [(20, 8), (12, 22), (18, 22), (16, 32), (26, 18), (20, 18)])

        elif block_id == BOSS_ALTAR:
            pygame.draw.rect(surf, (40, 0, 70), (0, 0, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(surf, (140, 0, 255), (4, 4, BLOCK_SIZE - 8, BLOCK_SIZE - 8), 3)
            pygame.draw.circle(surf, (255, 0, 255), (20, 20), 8)

        BLOCK_TEXTURES[block_id] = surf

generate_textures()
DIMENSION_EARTH = 0
DIMENSION_MOON = 1
current_dimension = DIMENSION_EARTH  

earth_map = [[AIR for _ in range(COLS)] for _ in range(ROWS)]
for col in range(COLS):
    ground_level = random.randint(8, 11) 
    for row in range(ROWS):
        if row == ground_level:
            earth_map[row][col] = SAND if random.random() < 0.12 else GRASS 
        elif ground_level < row <= ground_level + 4:
            earth_map[row][col] = DIRT
        elif row > ground_level + 4:
            ore_chance = random.random()
            if row > 35:
                if ore_chance < 0.08:
                    earth_map[row][col] = LAVA
                elif ore_chance < 0.09 and col % 25 == 0:
                    earth_map[row][col] = BOSS_ALTAR
                elif ore_chance < 0.13:
                    earth_map[row][col] = DIAMOND_ORE
                elif ore_chance < 0.16:
                    earth_map[row][col] = EMERALD
                else:
                    earth_map[row][col] = BLACKSTONE
            elif row > 20:
                if ore_chance < 0.03: earth_map[row][col] = GOLD_ORE
                elif ore_chance < 0.06: earth_map[row][col] = REDSTONE_ORE
                elif ore_chance < 0.10: earth_map[row][col] = COPPER
                else: earth_map[row][col] = STONE
            else:
                if ore_chance < 0.08: earth_map[row][col] = IRON_ORE
                elif ore_chance < 0.14: earth_map[row][col] = COAL_ORE
                else: earth_map[row][col] = STONE

for col in range(3, COLS - 3):
    for row in range(ROWS):
        if earth_map[row][col] == GRASS:
            if random.random() < 0.15:
                tree_height = random.randint(3, 5)
                for h in range(1, tree_height + 1):
                    if row - h >= 0:
                        earth_map[row - h][col] = WOOD
                top_row = row - tree_height
                for leaf_row in range(top_row - 2, top_row + 1):
                    for leaf_col in range(col - 2, col + 3):
                        if 0 <= leaf_row < ROWS and 0 <= leaf_col < COLS:
                            if earth_map[leaf_row][leaf_col] == AIR:
                                earth_map[leaf_row][leaf_col] = LEAVES
            break

moon_map = [[AIR for _ in range(COLS)] for _ in range(ROWS)]
for col in range(COLS):
    moon_ground = random.randint(7, 12)
    for row in range(ROWS):
        if row >= moon_ground:
            ore_chance = random.random()
            if row > 30 and ore_chance < 0.06:
                moon_map[row][col] = DIAMOND_ORE  
            elif row > 15 and ore_chance < 0.12:
                moon_map[row][col] = AMETHYST    
            else:
                moon_map[row][col] = STONE

world_map = earth_map
player_x, player_y = 200, 100
player_w, player_h = 30, 50  
player_speed = 4
vel_y = 0  
is_grounded = False
camera_x = 0  
camera_y = 0  

time_of_day = 0       
DAY_LENGTH = 18000    
current_sky_color = (135, 206, 235)  
night_darkness = 0    

jetpack_fuel = 100.0
boss_active = False
boss_x = 0
boss_y = 0
boss_hp = 1000
boss_max_hp = 1000
boss_projectiles = []
boss_shoot_timer = 0
boss_facing_right = True

clouds = []
for _ in range(12):
    clouds.append({
        "x": random.randint(0, SCREEN_WIDTH * 3),
        "y": random.randint(20, 150),
        "speed": random.uniform(0.2, 0.5),
        "width": random.randint(60, 120)
    })

stars = []
for _ in range(60):
    stars.append({
        "x": random.randint(0, SCREEN_WIDTH),
        "y": random.randint(0, SCREEN_HEIGHT),
        "size": random.randint(1, 3),
        "blink_speed": random.uniform(0.02, 0.07),
        "phase": random.uniform(0, 6.28)
    })

creative_items = [
    PICKAXE, GRASS, DIRT, STONE, WOOD, LEAVES,
    COAL_ORE, IRON_ORE, GOLD_ORE, DIAMOND_ORE, REDSTONE_ORE, GLASS,
    BRICK, WOOL, PLANKS, SAND, NEON, AMETHYST,
    EMERALD, LAPIS, COPPER, QUARTZ, COAL_BLOCK, IRON_BLOCK,
    GOLD_BLOCK, BLACKSTONE, TERRACOTTA, GLOWSTONE, RED_BRICK, BLUE_WOOL,
    GREEN_WOOL, TORCH, CRAFTING_TABLE, FURNACE, BED, LEVER,
    PISTON, RAILS, MINECART_ITEM, GREENSTONE_WIRE, GREEN_DYNAMITE,
    CHEST, BOW, ARROW, JETPACK, LAVA, CHARGER, BOSS_ALTAR
]
current_hand = PICKAXE  
show_inventory = False

show_pause_menu = False
DIFFICULTY_EASY = 0
DIFFICULTY_HARD = 1
current_difficulty = DIFFICULTY_EASY  

zombies = []             
zombie_speed = 1.5       
zombie_spawn_timer = 0   

active_levers = set()  
active_greenstone = set()  
minecarts = []         
arrows = []  
show_chest = False
current_chest_pos = None
chest_inventory = [
    AMETHYST, AMETHYST, NEON, ARROW, ARROW, ARROW,
    AIR, AIR, AIR, AIR, AIR, AIR,
    AIR, AIR, AIR, AIR, AIR, AIR
]

def draw_player(x, y):
    screen_x = x - camera_x
    screen_y = y - camera_y
    pygame.draw.rect(screen, (100, 50, 0), (screen_x + 6, screen_y, 18, 6)) 
    pygame.draw.rect(screen, (255, 224, 189), (screen_x + 6, screen_y + 6, 18, 12)) 
    pygame.draw.rect(screen, (0, 0, 0), (screen_x + 18, screen_y + 10, 2, 2)) 
    pygame.draw.rect(screen, (0, 150, 255), (screen_x + 3, screen_y + 18, 24, 18)) 
    pygame.draw.rect(screen, (50, 50, 200), (screen_x + 4, screen_y + 36, 10, 14)) 
    pygame.draw.rect(screen, (50, 50, 200), (screen_x + 16, screen_y + 36, 10, 14)) 

def draw_zombie(x, y):
    screen_x = x - camera_x
    screen_y = y - camera_y
    pygame.draw.rect(screen, (30, 20, 0), (screen_x + 6, screen_y, 18, 6)) 
    pygame.draw.rect(screen, (60, 140, 60), (screen_x + 6, screen_y + 6, 18, 12)) 
    pygame.draw.rect(screen, (255, 0, 0), (screen_x + 14, screen_y + 10, 2, 2)) 
    pygame.draw.rect(screen, (100, 30, 150), (screen_x + 3, screen_y + 18, 24, 18)) 
    pygame.draw.rect(screen, (30, 30, 100), (screen_x + 4, screen_y + 36, 10, 14)) 

def draw_boss(x, y):
    screen_x = x - camera_x
    screen_y = y - camera_y
    pygame.draw.rect(screen, (20, 0, 40), (screen_x + 12, screen_y, 66, 18))
    pygame.draw.rect(screen, (110, 30, 180), (screen_x + 12, screen_y + 18, 66, 36))
    pygame.draw.rect(screen, (255, 0, 0), (screen_x + 30, screen_y + 30, 10, 10))
    pygame.draw.rect(screen, (255, 0, 0), (screen_x + 50, screen_y + 30, 10, 10))
    pygame.draw.rect(screen, (40, 10, 80), (screen_x, screen_y + 54, 90, 66))
    pygame.draw.rect(screen, (20, 5, 40), (screen_x + 15, screen_y + 120, 24, 30))
    pygame.draw.rect(screen, (20, 5, 40), (screen_x + 51, screen_y + 120, 24, 30))

def draw_pickaxe(x, y):
    pygame.draw.line(screen, (139, 69, 19), (x + 5, y + 30), (x + 30, y + 5), 4) 
    pygame.draw.arc(screen, (150, 150, 150), (x + 15, y, 20, 20), 0.5, 3.14, 5) 

def draw_minecart(x, y):
    screen_x = x - camera_x
    screen_y = y - camera_y
    pygame.draw.rect(screen, (100, 110, 120), (screen_x + 2, screen_y + 16, 36, 20))
    pygame.draw.circle(screen, (30, 30, 30), (screen_x + 10, screen_y + 34), 5)
    pygame.draw.circle(screen, (30, 30, 30), (screen_x + 30, screen_y + 34), 5)

def draw_live_arrow(x, y, vx):
    screen_x = x - camera_x
    screen_y = y - camera_y
    if vx >= 0:
        pygame.draw.line(screen, (100, 100, 100), (screen_x, screen_y), (screen_x + 15, screen_y), 2)
        pygame.draw.polygon(screen, (200, 200, 200), [(screen_x + 15, screen_y), (screen_x + 10, screen_y - 4), (screen_x + 10, screen_y + 4)])
    else:
        pygame.draw.line(screen, (100, 100, 100), (screen_x, screen_y), (screen_x - 15, screen_y), 2)
        pygame.draw.polygon(screen, (200, 200, 200), [(screen_x - 15, screen_y), (screen_x - 10, screen_y - 4), (screen_x - 10, screen_y + 4)])
while True:
    clock.tick(60)

    if not show_pause_menu:
        time_of_day = (time_of_day + 1) % DAY_LENGTH  
    
    phase = time_of_day / DAY_LENGTH
    
    if current_dimension == DIMENSION_EARTH:
        if phase < 0.25:  
            progress = phase / 0.25
            night_darkness = int(180 * (1 - progress))
            r1, g1, b1 = int(10 + (135 - 10) * progress), int(15 + (206 - 15) * progress), int(30 + (235 - 30) * progress)
            r2, g2, b2 = int(5 + (70 - 5) * progress), int(10 + (130 - 10) * progress), int(20 + (180 - 20) * progress)
        elif phase < 0.5:  
            night_darkness = 0
            r1, g1, b1 = 135, 206, 235
            r2, g2, b2 = 70, 130, 180
        elif phase < 0.75:  
            progress = (phase - 0.5) / 0.25
            night_darkness = int(180 * progress)
            r1, g1, b1 = int(135 - (135 - 10) * progress), int(206 - (206 - 15) * progress), int(235 - (235 - 30) * progress)
            r2, g2, b2 = int(70 - (70 - 5) * progress), int(130 - (130 - 10) * progress), int(180 - (180 - 20) * progress)
        else:  
            night_darkness = 180
            r1, g1, b1 = 10, 15, 30
            r2, g2, b2 = 5, 10, 20
    else:
        night_darkness = 100 if phase < 0.5 else 160
        r1, g1, b1 = 15, 10, 25
        r2, g2, b2 = 5, 5, 12

    for y in range(0, SCREEN_HEIGHT, 15):
        factor = y / SCREEN_HEIGHT
        curr_r = int(r1 + (r2 - r1) * factor)
        curr_g = int(g1 + (g2 - g1) * factor)
        curr_b = int(b1 + (b2 - b1) * factor)
        pygame.draw.rect(screen, (curr_r, curr_g, curr_b), (0, y, SCREEN_WIDTH, 15))

    if current_dimension == DIMENSION_EARTH and night_darkness > 40:
        for star in stars:
            if not show_pause_menu:
                star["phase"] += star["blink_speed"]
            star_color = (255, 255, 255)
            pygame.draw.circle(screen, star_color, (star["x"], star["y"]), star["size"])

    if current_dimension == DIMENSION_MOON:
        for star in stars:
            if not show_pause_menu:
                star["phase"] += star["blink_speed"]
            pygame.draw.circle(screen, (240, 240, 255), (star["x"], star["y"]), star["size"])

    if current_dimension == DIMENSION_EARTH and night_darkness < 140:
        for cloud in clouds:
            if not show_pause_menu:
                cloud["x"] -= cloud["speed"]
                if cloud["x"] + cloud["width"] < 0:
                    cloud["x"] = WORLD_PIXEL_WIDTH
            c_screen_x = cloud["x"] - camera_x
            if -150 < c_screen_x < SCREEN_WIDTH + 50:
                pygame.draw.ellipse(screen, (245, 250, 255, 180), (c_screen_x, cloud["y"], cloud["width"], 25))
                pygame.draw.ellipse(screen, (245, 250, 255, 180), (c_screen_x + 15, cloud["y"] - 10, cloud["width"] - 20, 25))

    for row in range(ROWS - 4):
        for col in range(COLS - 3):
            if (world_map[row][col] == STONE and world_map[row][col+1] == STONE and 
                world_map[row][col+2] == STONE and world_map[row][col+3] == STONE and
                world_map[row+4][col] == STONE and world_map[row+4][col+1] == STONE and 
                world_map[row+4][col+2] == STONE and world_map[row+4][col+3] == STONE and
                world_map[row+1][col] == STONE and world_map[row+2][col] == STONE and world_map[row+3][col] == STONE and
                world_map[row+1][col+3] == STONE and world_map[row+2][col+3] == STONE and world_map[row+3][col+3] == STONE):
                
                if world_map[row+1][col+1] == AIR: world_map[row+1][col+1] = PORTAL
                if world_map[row+1][col+2] == AIR: world_map[row+1][col+2] = PORTAL
                if world_map[row+2][col+1] == AIR: world_map[row+2][col+1] = PORTAL
                if world_map[row+2][col+2] == AIR: world_map[row+2][col+2] = PORTAL
                if world_map[row+3][col+1] == AIR: world_map[row+3][col+1] = PORTAL
                if world_map[row+3][col+2] == AIR: world_map[row+3][col+2] = PORTAL

    p_col = int((player_x + player_w / 2) // BLOCK_SIZE)
    p_row = int((player_y + player_h / 2) // BLOCK_SIZE)
    if 0 <= p_row < ROWS and 0 <= p_col < COLS:
        if world_map[p_row][p_col] == PORTAL:
            if current_dimension == DIMENSION_EARTH:
                current_dimension = DIMENSION_MOON
                for r_offset in range(5):
                    for c_offset in range(4):
                        if p_row-2+r_offset < ROWS and p_col-1+c_offset < COLS:
                            moon_map[p_row-2+r_offset][p_col-1+c_offset] = earth_map[p_row-2+r_offset][p_col-1+c_offset]
                world_map = moon_map
            else:
                current_dimension = DIMENSION_EARTH
                world_map = earth_map
            player_y -= 40
            vel_y = -3
            zombies.clear()
            minecarts.clear()
            arrows.clear()
            boss_active = False

    active_greenstone.clear()
    queue = list(active_levers)
    visited = set(queue)
    
    while queue:
        curr_row, curr_col = queue.pop(0)
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr, nc = curr_row + dr, curr_col + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                if world_map[nr][nc] == GREENSTONE_WIRE and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    active_greenstone.add((nr, nc))
                    queue.append((nr, nc))

    exploded_dynamites = []
    for row in range(ROWS):
        for col in range(COLS):
            if world_map[row][col] == GREEN_DYNAMITE:
                is_triggered = False
                for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < ROWS and 0 <= nc < COLS:
                        if (nr, nc) in active_levers or (nr, nc) in active_greenstone:
                            is_triggered = True
                            break
                if is_triggered:
                    exploded_dynamites.append((row, col))

    for r_det, c_det in exploded_dynamites:
        for dr in range(-2, 3):
            for dc in range(-2, 3):
                nr, nc = r_det + dr, c_det + dc
                if 0 <= nr < ROWS and 0 <= nc < COLS:
                    if world_map[nr][nc] != PORTAL:
                        if (nr, nc) in active_levers:
                            active_levers.remove((nr, nc))
                        world_map[nr][nc] = AIR

    for row in range(ROWS):
        for col in range(COLS):
            if world_map[row][col] == PISTON:
                should_activate = False
                for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < ROWS and 0 <= nc < COLS:
                        if (nr, nc) in active_levers or (nr, nc) in active_greenstone:
                            should_activate = True
                            break
                
                if should_activate:
                    if col + 1 < COLS and world_map[row][col+1] == AIR:
                        if col + 2 < COLS and world_map[row][col+2] != AIR and world_map[row][col+2] != PISTON_HEAD:
                            world_map[row][col+2] = world_map[row][col+1]
                        world_map[row][col+1] = PISTON_HEAD
                else:
                    if col + 1 < COLS and world_map[row][col+1] == PISTON_HEAD:
                        world_map[row][col+1] = AIR

    camera_x = player_x - SCREEN_WIDTH // 2
    if camera_x < 0: camera_x = 0
    if camera_x > WORLD_PIXEL_WIDTH - SCREEN_WIDTH: camera_x = WORLD_PIXEL_WIDTH - SCREEN_WIDTH

    camera_y = player_y - SCREEN_HEIGHT // 2
    if camera_y < 0: camera_y = 0
    if camera_y > WORLD_PIXEL_HEIGHT - SCREEN_HEIGHT: camera_y = WORLD_PIXEL_HEIGHT - SCREEN_HEIGHT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  
                show_pause_menu = not show_pause_menu
                show_inventory = False  
                show_chest = False
            if event.key == pygame.K_i and not show_pause_menu and not show_chest:  
                show_inventory = not show_inventory

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            if show_pause_menu:
                mid_x, mid_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
                if pygame.Rect(mid_x - 100, mid_y - 60, 200, 40).collidepoint(mouse_x, mouse_y):
                    show_pause_menu = False
                elif pygame.Rect(mid_x - 100, mid_y - 10, 200, 40).collidepoint(mouse_x, mouse_y):
                    if current_difficulty == DIFFICULTY_EASY: current_difficulty = DIFFICULTY_HARD
                    else: current_difficulty = DIFFICULTY_EASY
                elif pygame.Rect(mid_x - 100, mid_y + 40, 200, 40).collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()
                    
            elif show_chest:
                ch_x = SCREEN_WIDTH // 2 - 180
                ch_y = SCREEN_HEIGHT // 2 - 100
                for idx in range(18):
                    r_idx, c_idx = idx // 6, idx % 6
                    slot_rect = pygame.Rect(ch_x + 20 + c_idx * 55, ch_y + 50 + r_idx * 55, 45, 45)
                    if slot_rect.collidepoint(mouse_x, mouse_y):
                        temp = current_hand
                        current_hand = chest_inventory[idx]
                        chest_inventory[idx] = temp
                if not pygame.Rect(ch_x, ch_y, 360, 230).collidepoint(mouse_x, mouse_y):
                    show_chest = False
                    
            elif show_inventory:
                inv_x = SCREEN_WIDTH // 2 - 180
                inv_y = SCREEN_HEIGHT // 2 - 250
                for idx, item in enumerate(creative_items):
                    row_idx, col_idx = idx // 6, idx % 6
                    slot_rect = pygame.Rect(inv_x + 20 + col_idx * 55, inv_y + 50 + row_idx * 55, 45, 45)
                    if slot_rect.collidepoint(mouse_x, mouse_y):
                        current_hand = item
                        show_inventory = False
            else:
                world_click_x = mouse_x + camera_x
                world_click_y = mouse_y + camera_y
                block_col = int(world_click_x // BLOCK_SIZE)
                block_row = int(world_click_y // BLOCK_SIZE)
                
                if 0 <= block_col < COLS and 0 <= block_row < ROWS:
                    if event.button == 1:  
                        if current_hand == BOW:
                            arrow_vx = 10.0 if mouse_x >= SCREEN_WIDTH // 2 else -10.0
                            arrows.append({"x": player_x + 15, "y": player_y + 20, "vx": arrow_vx})
                        elif current_hand == PICKAXE:
                            if world_map[block_row][block_col] == PISTON:
                                if block_col + 1 < COLS and world_map[block_row][block_col + 1] == PISTON_HEAD:
                                    world_map[block_row][block_col + 1] = AIR
                            if (block_row, block_col) in active_levers:
                                active_levers.remove((block_row, block_col))
                            world_map[block_row][block_col] = AIR
                    elif event.button == 3:  
                        if world_map[block_row][block_col] == LEVER:
                            if (block_row, block_col) in active_levers: active_levers.remove((block_row, block_col))
                            else: active_levers.add((block_row, block_col))
                        elif world_map[block_row][block_col] == CHEST:
                            show_chest = True
                            current_chest_pos = (block_row, block_col)
                        elif world_map[block_row][block_col] == BOSS_ALTAR:
                            world_map[block_row][block_col] = AIR
                            boss_active = True
                            boss_x = block_col * BLOCK_SIZE - 25
                            boss_y = block_row * BLOCK_SIZE - 100
                            boss_hp = boss_max_hp
                        elif current_hand == MINECART_ITEM and world_map[block_row][block_col] == RAILS:
                            minecarts.append({"x": block_col * BLOCK_SIZE, "y": block_row * BLOCK_SIZE, "vx": 0, "vy": 0})
                        elif current_hand != PICKAXE and current_hand != MINECART_ITEM and world_map[block_row][block_col] == AIR:
                            world_map[block_row][block_col] = current_hand
    if not show_pause_menu:
        def is_charger_powered(r, c):
            if world_map[r][c] == CHARGER:
                for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < ROWS and 0 <= nc < COLS:
                        if (nr, nc) in active_greenstone or (nr, nc) in active_levers:
                            return True
            return False

        if current_dimension == DIMENSION_MOON:
            gravity = 0.15     
            jump_force = -6.5  
        else:
            gravity = 0.5      
            jump_force = -11   

        if not show_inventory and not show_chest:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] and player_x > 0:
                player_x -= player_speed
            if keys[pygame.K_d] and player_x < WORLD_PIXEL_WIDTH - player_w:
                player_x += player_speed
                
            if keys[pygame.K_SPACE] and current_hand == JETPACK and jetpack_fuel > 0:
                vel_y = -6.0
                is_grounded = False
                jetpack_fuel -= 0.4
            elif keys[pygame.K_SPACE] and is_grounded:
                vel_y = jump_force  
                is_grounded = False

            if not (keys[pygame.K_SPACE] and current_hand == JETPACK and jetpack_fuel > 0):
                vel_y += gravity  
                
            player_y += vel_y

            foot_row = int((player_y + player_h) // BLOCK_SIZE)
            center_col = int((player_x + player_w / 2) // BLOCK_SIZE)
            
            if 0 <= foot_row < ROWS and 0 <= center_col < COLS:
                if world_map[foot_row][center_col] != AIR:
                    if world_map[foot_row][center_col] == LAVA:
                        player_y -= 20
                        vel_y = -4
                        is_grounded = False
                    else:
                        player_y = foot_row * BLOCK_SIZE - player_h  
                        vel_y = 0
                        is_grounded = True
                        
                        check_col = int((player_x + player_w / 2) // BLOCK_SIZE)
                        check_row = int((player_y + player_h - 5) // BLOCK_SIZE)
                        check_under_row = int((player_y + player_h + 5) // BLOCK_SIZE)
                        
                        if 0 <= check_col < COLS:
                            if 0 <= check_row < ROWS:
                                if is_charger_powered(check_row, check_col):
                                    jetpack_fuel = min(100.0, jetpack_fuel + 4.0)
                            if 0 <= check_under_row < ROWS:
                                if is_charger_powered(check_under_row, check_col):
                                    jetpack_fuel = min(100.0, jetpack_fuel + 4.0)
                else:
                    is_grounded = False
            else:
                is_grounded = False

        if boss_active:
            if boss_x < player_x:
                boss_x += 1.0
                boss_facing_right = True
            else:
                boss_x -= 1.0
                boss_facing_right = False
                
            if boss_y < player_y - 40: boss_y += 0.5
            else: boss_y -= 0.5
            
            b_c = int((boss_x + 45) // BLOCK_SIZE)
            b_r = int((boss_y + 100) // BLOCK_SIZE)
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    nr, nc = b_r + dr, b_c + dc
                    if 0 <= nr < ROWS and 0 <= nc < COLS:
                        if world_map[nr][nc] in [DIRT, GRASS, LEAVES, WOOD]:
                            world_map[nr][nc] = AIR

            boss_shoot_timer += 1
            if boss_shoot_timer >= 90:
                boss_shoot_timer = 0
                p_vx = 6.0 if boss_facing_right else -6.0
                boss_projectiles.append({"x": boss_x + 45, "y": boss_y + 40, "vx": p_vx})

        p_to_keep = []
        for p in boss_projectiles:
            p["x"] += p["vx"]
            if 0 < p["x"] < WORLD_PIXEL_WIDTH:
                p_to_keep.append(p)
        boss_projectiles = p_to_keep

        arrows_to_keep = []
        for arrow_obj in arrows:
            arrow_obj["x"] += arrow_obj["vx"]
            arrow_hit = False
            arrow_rect = pygame.Rect(arrow_obj["x"], arrow_obj["y"], 15, 4)
            
            if boss_active:
                b_rect = pygame.Rect(boss_x, boss_y, 90, 150)
                if arrow_rect.colliderect(b_rect):
                    boss_hp -= 35
                    arrow_hit = True
                    if boss_hp <= 0:
                        boss_active = False
                        for _ in range(5):
                            r_col = int(boss_x // BLOCK_SIZE) + random.randint(0, 2)
                            r_row = int(boss_y // BLOCK_SIZE) + random.randint(0, 3)
                            if 0 <= r_row < ROWS and 0 <= r_col < COLS:
                                world_map[r_row][r_col] = GOLD_BLOCK if random.random() < 0.3 else EMERALD
            
            for z in list(zombies):
                z_rect = pygame.Rect(z["x"], z["y"], player_w, player_h)
                if arrow_rect.colliderect(z_rect):
                    zombies.remove(z)
                    arrow_hit = True
                    break
            
            if 0 < arrow_obj["x"] < WORLD_PIXEL_WIDTH and not arrow_hit:
                arrows_to_keep.append(arrow_obj)
        arrows = arrows_to_keep

        for cart in minecarts:
            cart["vy"] += 0.5
            cart["y"] += cart["vy"]
            c_col = int((cart["x"] + BLOCK_SIZE // 2) // BLOCK_SIZE)
            c_row = int((cart["y"] + BLOCK_SIZE - 2) // BLOCK_SIZE)
            if 0 <= c_row < ROWS and 0 <= c_col < COLS and world_map[c_row][c_col] == RAILS:
                cart["y"] = c_row * BLOCK_SIZE
                cart["vy"] = 0
            
            cart["vx"] *= 0.95
            cart["x"] += cart["vx"]
            
            player_rect = pygame.Rect(player_x, player_y, player_w, player_h)
            cart_rect = pygame.Rect(cart["x"], cart["y"] + 12, BLOCK_SIZE, 20)
            if player_rect.colliderect(cart_rect):
                if player_x < cart["x"]: cart["vx"] = 4.0
                elif player_x > cart["x"]: cart["vx"] = -4.0

        if current_dimension == DIMENSION_EARTH and current_difficulty == DIFFICULTY_HARD and phase >= 0.75:
            zombie_spawn_timer += 1
            if zombie_spawn_timer >= 180 and len(zombies) < 5:
                zombie_spawn_timer = 0
                spawn_side = random.choice([-150, SCREEN_WIDTH + 50])
                spawn_x = player_x + spawn_side
                if 0 < spawn_x < WORLD_PIXEL_WIDTH:
                    z_col_idx = int(spawn_x // BLOCK_SIZE)
                    z_row_idx = 5
                    if 0 <= z_col_idx < COLS:
                        for r in range(ROWS):
                            if world_map[r][z_col_idx] != AIR:
                                z_row_idx = r - 1
                                break
                    zombies.append({"x": spawn_x, "y": z_row_idx * BLOCK_SIZE, "vel_y": 0})
        
        if phase < 0.75 or current_dimension == DIMENSION_MOON:
            zombies.clear()

        for z in zombies:
            z["vel_y"] += 0.5
            z["y"] += z["vel_y"]
            z_foot_row = int((z["y"] + player_h) // BLOCK_SIZE)
            z_center_col = int((z["x"] + player_w / 2) // BLOCK_SIZE)
            if 0 <= z_foot_row < ROWS and 0 <= z_center_col < COLS:
                if world_map[z_foot_row][z_center_col] != AIR:
                    z["y"] = z_foot_row * BLOCK_SIZE - player_h
                    z["vel_y"] = 0
            if z["x"] < player_x: z["x"] += zombie_speed
            elif z["x"] > player_x: z["x"] -= zombie_speed
    start_col = max(0, int(camera_x // BLOCK_SIZE))
    end_col = min(COLS, int((camera_x + SCREEN_WIDTH) // BLOCK_SIZE) + 1)
    start_row = max(0, int(camera_y // BLOCK_SIZE))
    end_row = min(ROWS, int((camera_y + SCREEN_HEIGHT) // BLOCK_SIZE) + 1)

    for row in range(start_row, end_row):
        for col in range(start_col, end_col):
            if 0 <= row < ROWS and 0 <= col < COLS:
                block = world_map[row][col]
                if block != AIR:
                    rect = pygame.Rect(col * BLOCK_SIZE - camera_x, row * BLOCK_SIZE - camera_y, BLOCK_SIZE, BLOCK_SIZE)
                    if block == LEVER and (row, col) in active_levers:
                        screen.blit(LEVER_ACTIVE_TEXTURES[LEVER], rect)
                    elif block == GREENSTONE_WIRE and (row, col) in active_greenstone:
                        screen.blit(GREENSTONE_ACTIVE_TEXTURES[GREENSTONE_WIRE], rect)
                    else:
                        screen.blit(BLOCK_TEXTURES[block], rect)
                    pygame.draw.rect(screen, (0, 0, 0), rect, 1) 

    for arrow_obj in arrows:
        draw_live_arrow(arrow_obj["x"], arrow_obj["y"], arrow_obj["vx"])

    for p in boss_projectiles:
        p_screen_x = p["x"] - camera_x
        p_screen_y = p["y"] - camera_y
        pygame.draw.circle(screen, (255, 69, 0), (int(p_screen_x), int(p_screen_y)), 8)
        pygame.draw.circle(screen, (255, 215, 0), (int(p_screen_x), int(p_screen_y)), 4)

    for cart in minecarts: draw_minecart(cart["x"], cart["y"])
    for z in zombies: draw_zombie(z["x"], z["y"])
    if boss_active: draw_boss(boss_x, boss_y)
    draw_player(player_x, player_y)

    if night_darkness > 0:
        light_mask = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        light_mask.fill((10, 10, 25, night_darkness))
        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                if 0 <= row < ROWS and 0 <= col < COLS:
                    if world_map[row][col] == TORCH:
                        torch_screen_x = (col * BLOCK_SIZE + BLOCK_SIZE // 2) - camera_x
                        torch_screen_y = (row * BLOCK_SIZE + BLOCK_SIZE // 2) - camera_y
                        light_radius = 140 
                        for radius in range(light_radius, 0, -20):
                            alpha_reduction = int(night_darkness * (1 - radius / light_radius))
                            current_alpha = max(0, night_darkness - alpha_reduction)
                            pygame.draw.circle(light_mask, (10, 10, 25, current_alpha), (torch_screen_x, torch_screen_y), radius)
        screen.blit(light_mask, (0, 0))
    pygame.draw.rect(screen, (0, 0, 0), (10, 10, 120, 50), 2)
    text = inventory_font.render("In Hand:", True, (0, 0, 0))
    screen.blit(text, (15, 25))
    if current_hand == PICKAXE:
        draw_pickaxe(75, 15)
    else:
        screen.blit(BLOCK_TEXTURES[current_hand], (80, 15))
        pygame.draw.rect(screen, (0, 0, 0), (80, 15, 35, 35), 1)

    pygame.draw.rect(screen, (0, 0, 0), (140, 10, 150, 20), 2)
    fuel_w = int(146 * (jetpack_fuel / 100.0))
    if fuel_w > 0:
        pygame.draw.rect(screen, (0, 200, 255), (142, 12, fuel_w, 16))
    fuel_text = inventory_font.render(f"Fuel: {int(jetpack_fuel)}%", True, (0, 0, 0))
    screen.blit(fuel_text, (145, 12))

    if boss_active:
        pygame.draw.rect(screen, (0, 0, 0), (SCREEN_WIDTH // 2 - 200, 15, 400, 25), 3)
        pygame.draw.rect(screen, (60, 0, 100), (SCREEN_WIDTH // 2 - 197, 18, 394, 19))
        boss_bar_w = int(394 * (boss_hp / boss_max_hp))
        if boss_bar_w > 0:
            pygame.draw.rect(screen, (160, 0, 255), (SCREEN_WIDTH // 2 - 197, 18, boss_bar_w, 19))
        b_name = inventory_font.render("ANCIENT UNDERGROUND GUARDIAN", True, (255, 255, 255))
        screen.blit(b_name, (SCREEN_WIDTH // 2 - 120, 19))

    if show_inventory and not show_pause_menu and not show_chest:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        inv_w, inv_h = 360, 520
        inv_x = SCREEN_WIDTH // 2 - inv_w // 2
        inv_y = SCREEN_HEIGHT // 2 - inv_h // 2
        
        pygame.draw.rect(screen, (220, 220, 220), (inv_x, inv_y, inv_w, inv_h))
        pygame.draw.rect(screen, (50, 50, 50), (inv_x, inv_y, inv_w, inv_h), 3)
        title_text = inventory_font.render("Creative Menu (I)", True, (0, 0, 0))
        screen.blit(title_text, (inv_x + 20, inv_y + 15))
        
        for idx, item in enumerate(creative_items):
            row_idx, col_idx = idx // 6, idx % 6
            slot_rect = pygame.Rect(inv_x + 20 + col_idx * 55, inv_y + 50 + row_idx * 55, 45, 45)
            if slot_rect.collidepoint(pygame.mouse.get_pos()): pygame.draw.rect(screen, (255, 255, 150), slot_rect)
            else: pygame.draw.rect(screen, (190, 190, 190), slot_rect)
            pygame.draw.rect(screen, (0, 0, 0), slot_rect, 1)
            if item == PICKAXE: draw_pickaxe(inv_x + 27 + col_idx * 55, inv_y + 55 + row_idx * 55)
            else:
                screen.blit(BLOCK_TEXTURES[item], (inv_x + 22 + col_idx * 55, inv_y + 52 + row_idx * 55))
                pygame.draw.rect(screen, (0, 0, 0), (inv_x + 22 + col_idx * 55, inv_y + 52 + row_idx * 55, 35, 35), 1)
    if show_chest and not show_pause_menu:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        inv_w, inv_h = 360, 230
        inv_x = SCREEN_WIDTH // 2 - inv_w // 2
        inv_y = SCREEN_HEIGHT // 2 - inv_h // 2
        
        pygame.draw.rect(screen, (220, 220, 220), (inv_x, inv_y, inv_w, inv_h))
        pygame.draw.rect(screen, (50, 50, 50), (inv_x, inv_y, inv_w, inv_h), 3)
        title_text = inventory_font.render("Chest Storage (Right-click outside to close)", True, (0, 0, 0))
        screen.blit(title_text, (inv_x + 20, inv_y + 15))

        for idx in range(18):
            row_idx = idx // 6  
            col_idx = idx % 6
            slot_rect = pygame.Rect(inv_x + 20 + col_idx * 55, inv_y + 50 + row_idx * 55, 45, 45)
            
            if slot_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, (255, 255, 150), slot_rect)
            else:
                pygame.draw.rect(screen, (190, 190, 190), slot_rect)
            pygame.draw.rect(screen, (0, 0, 0), slot_rect, 1)
            
            item = chest_inventory[idx]
            if item != AIR:
                if item == PICKAXE:
                    draw_pickaxe(inv_x + 27 + col_idx * 55, inv_y + 55 + row_idx * 55)
                else:
                    screen.blit(BLOCK_TEXTURES[item], (inv_x + 22 + col_idx * 55, inv_y + 52 + row_idx * 55))
                    pygame.draw.rect(screen, (0, 0, 0), (inv_x + 22 + col_idx * 55, inv_y + 52 + row_idx * 55, 35, 35), 1)

    if show_pause_menu:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((20, 20, 30))
        screen.blit(overlay, (0, 0))
        mid_x, mid_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        menu_title = inventory_font.render("GAME PAUSED", True, (255, 255, 255))
        screen.blit(menu_title, (mid_x - 50, mid_y - 110))
        btn_resume = pygame.Rect(mid_x - 100, mid_y - 60, 200, 40)
        pygame.draw.rect(screen, (80, 80, 90), btn_resume)
        pygame.draw.rect(screen, (255, 255, 255), btn_resume, 2)
        screen.blit(inventory_font.render("Resume Game", True, (255, 255, 255)), (mid_x - 45, mid_y - 50))
        btn_diff = pygame.Rect(mid_x - 100, mid_y - 10, 200, 40)
        pygame.draw.rect(screen, (80, 80, 90), btn_diff)
        pygame.draw.rect(screen, (255, 255, 255), btn_diff, 2)
        diff_str = "Difficulty: EASY" if current_difficulty == DIFFICULTY_EASY else "Difficulty: HARD"
        text_diff = inventory_font.render(diff_str, True, (255, 255, 100) if current_difficulty == DIFFICULTY_HARD else (255, 255, 255))
        screen.blit(text_diff, (mid_x - 55, mid_y))
        btn_exit = pygame.Rect(mid_x - 100, mid_y + 40, 200, 40)
        pygame.draw.rect(screen, (150, 50, 50), btn_exit)
        pygame.draw.rect(screen, (255, 255, 255), btn_exit, 2)
        screen.blit(inventory_font.render("Exit Game", True, (255, 255, 255)), (mid_x - 35, mid_y + 50))

    pygame.display.flip()
