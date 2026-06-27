import pygame
import sys
import random
import math
import os

pygame.init()

BLOCK_SIZE = 40  
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
COLS, ROWS = 256, 45  
WORLD_PIXEL_WIDTH = COLS * BLOCK_SIZE
WORLD_PIXEL_HEIGHT = ROWS * BLOCK_SIZE

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("AstroBlocks 2D: Anniversary Update 1.5")
clock = pygame.time.Clock()

# --- GAME STATES & MODES ---
STATE_MAIN_MENU = 0
STATE_WORLD_SELECT = 1
STATE_PLAYING = 2
current_game_state = STATE_MAIN_MENU
selected_world_slot = 1

MODE_CREATIVE = 0
MODE_SURVIVAL = 1
selected_creation_mode = MODE_CREATIVE  
current_world_mode = MODE_CREATIVE      

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
HOE = 50
WHEAT_SEEDS = 51
FARMLAND = 52
WHEAT_STAGE1 = 53
WHEAT_STAGE2 = 54
WHEAT_STAGE3 = 55
WHEAT_STAGE4 = 56
WATER = 57
OBSIDIAN = 58
DIRT_WALL = 59
STONE_WALL = 60
DOOR_CLOSED = 61
DOOR_OPEN = 62
GLASS_PANE = 63
LIGHTNING_ROD = 64
WIND_TURBINE = 65
UMBRELLA = 66

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
    TORCH: (180, 120, 40), CRAFTING_TABLE: (160, 82, 45), FURNACE: (105, 105, 105),
    BED: (220, 20, 60), PORTAL: (0, 240, 255), LEVER: (120, 120, 120),
    PISTON: (140, 110, 80), PISTON_HEAD: (180, 150, 120), RAILS: (192, 192, 192),
    MINECART_ITEM: (112, 128, 144), GREENSTONE_WIRE: (20, 60, 20),
    GREEN_DYNAMITE: (0, 200, 50), CHEST: (139, 105, 20), BOW: (200, 150, 100),
    ARROW: (220, 220, 220), JETPACK: (150, 40, 40), LAVA: (230, 70, 0),
    CHARGER: (60, 70, 90), BOSS_ALTAR: (75, 0, 130), HOE: (120, 90, 60),
    WHEAT_SEEDS: (140, 170, 100), FARMLAND: (90, 55, 30), WHEAT_STAGE1: (40, 140, 40),
    WHEAT_STAGE2: (60, 170, 60), WHEAT_STAGE3: (190, 180, 50), WHEAT_STAGE4: (230, 190, 30),
    WATER: (30, 144, 255), OBSIDIAN: (25, 20, 40), DIRT_WALL: (70, 45, 25), STONE_WALL: (65, 65, 65),
    DOOR_CLOSED: (165, 42, 42), DOOR_OPEN: (120, 30, 30), GLASS_PANE: (220, 245, 255),
    LIGHTNING_ROD: (192, 192, 192), WIND_TURBINE: (240, 240, 240), UMBRELLA: (200, 50, 50)
}

inventory_font = pygame.font.SysFont("Arial", 16)
menu_font = pygame.font.SysFont("Arial", 24)
title_font = pygame.font.SysFont("Arial", 48, bold=True)

torch_anim_frame = 0
turbine_anim_frame = 0

# --- NEW WEATHER & MECHANICS VARIABLES ---
is_raining = False
rain_timer = 0
lightning_flash = 0
active_lightning_signals = set()
custom_spawn_point = None
falling_leaves = []
BLOCK_TEXTURES = {}
LEVER_ACTIVE_TEXTURES = {}
GREENSTONE_ACTIVE_TEXTURES = {}

def generate_textures():
    global BLOCK_TEXTURES
    for block_id, color in BLOCK_COLORS.items():
        surf = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        surf.fill(color)
        
        # Эффект намокания: во время дождя блоки поверхности становятся темнее
        is_wet = is_raining and current_dimension == DIMENSION_EARTH
        
        if block_id == GRASS:
            c_dirt = (95, 50, 25) if is_wet else (120, 75, 40)
            c_grass = (24, 110, 24) if is_wet else (34, 139, 34)
            surf.fill(c_dirt) 
            pygame.draw.rect(surf, c_grass, (0, 0, BLOCK_SIZE, 12)) 
            pygame.draw.rect(surf, (15, 80, 15) if is_wet else (24, 130, 24), (0, 0, BLOCK_SIZE, 4)) 
            for x_offset in range(0, BLOCK_SIZE, 4):
                hang = random.randint(3, 7)
                pygame.draw.rect(surf, c_grass, (x_offset, 12, 2, hang))
            pygame.draw.rect(surf, (70, 35, 15) if is_wet else (95, 55, 25), (4, 24, 4, 4))
            
        elif block_id == DIRT:
            surf.fill((95, 50, 25) if is_wet else (120, 75, 40))
            pygame.draw.rect(surf, (70, 35, 15) if is_wet else (95, 55, 25), (0, 0, BLOCK_SIZE, BLOCK_SIZE), 2)
            pygame.draw.rect(surf, (60, 30, 10) if is_wet else (90, 50, 20), (6, 8, 4, 4))
            
        elif block_id == STONE:
            surf.fill((115, 115, 115))
            pygame.draw.rect(surf, (85, 85, 85), (0, 0, BLOCK_SIZE, BLOCK_SIZE), 2)
            pygame.draw.line(surf, (80, 80, 80), (2, 12), (16, 12), 2)
            pygame.draw.line(surf, (145, 145, 145), (2, 2), (38, 2), 2)

        elif block_id in [COAL_ORE, IRON_ORE, GOLD_ORE, DIAMOND_ORE, REDSTONE_ORE]:
            surf.fill((115, 115, 115))
            pygame.draw.rect(surf, (85, 85, 85), (0, 0, BLOCK_SIZE, BLOCK_SIZE), 2)
            pygame.draw.rect(surf, color, (8, 6, 8, 6))
            pygame.draw.rect(surf, color, (22, 12, 6, 8))
            if block_id == DIAMOND_ORE:
                pygame.draw.rect(surf, (255, 255, 255), (24, 14, 3, 3))

        elif block_id == PLANKS:
            surf.fill((185, 140, 85))
            pygame.draw.rect(surf, (125, 90, 45), (0, 0, BLOCK_SIZE, BLOCK_SIZE), 2)
            pygame.draw.line(surf, (125, 90, 45), (0, 13), (BLOCK_SIZE, 13), 2)

        elif block_id == GLASS:
            surf.fill((170, 225, 245))
            surf.set_alpha(140)
            pygame.draw.rect(surf, (255, 255, 255), (0, 0, BLOCK_SIZE, BLOCK_SIZE), 2)
            pygame.draw.line(surf, (255, 255, 255), (6, 34), (34, 6), 3)

        elif block_id in [BRICK, RED_BRICK]:
            surf.fill(color)
            border_c = (40, 5, 5) if block_id == BRICK else (70, 15, 15)
            pygame.draw.rect(surf, border_c, (0, 0, BLOCK_SIZE, BLOCK_SIZE), 2)

        elif block_id == TORCH:
            surf.fill(SKY_BLUE); surf.set_colorkey(SKY_BLUE)
            pygame.draw.rect(surf, (100, 65, 30), (18, 16, 5, 24))
            pygame.draw.rect(surf, (60, 40, 20), (18, 16, 5, 4))
            pygame.draw.rect(surf, (40, 30, 15), (17, 36, 7, 4))

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

        elif block_id == BED:
            surf.fill((220, 220, 220))
            pygame.draw.rect(surf, (180, 20, 40), (12, 0, BLOCK_SIZE - 12, BLOCK_SIZE))
            pygame.draw.rect(surf, (130, 10, 25), (12, 34, BLOCK_SIZE - 12, 6))
            pygame.draw.rect(surf, (255, 255, 255), (2, 6, 8, 28))

        elif block_id == PORTAL:
            surf.set_alpha(200)
            pygame.draw.rect(surf, (0, 40, 80), (0, 0, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(surf, (0, 230, 255), (4, 4, BLOCK_SIZE - 8, BLOCK_SIZE - 8), 2)

        elif block_id == LEVER:
            pygame.draw.rect(surf, (80, 80, 80), (8, 28, 24, 12))
            pygame.draw.rect(surf, (40, 40, 40), (8, 28, 24, 12), 2)
            pygame.draw.line(surf, (180, 40, 40), (20, 28), (8, 8), 4)
            pygame.draw.circle(surf, (230, 50, 50), (8, 8), 5)
            
            act_surf = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
            act_surf.fill(color); act_surf.set_colorkey(color)
            pygame.draw.rect(act_surf, (80, 80, 80), (8, 28, 24, 12))
            pygame.draw.rect(act_surf, (40, 40, 40), (8, 28, 24, 12), 2)
            pygame.draw.line(act_surf, (40, 180, 80), (20, 28), (32, 8), 4)
            pygame.draw.circle(act_surf, (50, 230, 100), (32, 8), 5)
            LEVER_ACTIVE_TEXTURES[LEVER] = act_surf

        elif block_id == PISTON:
            surf.fill((100, 100, 100))
            pygame.draw.rect(surf, (50, 50, 50), (0, 0, 26, BLOCK_SIZE))
            pygame.draw.rect(surf, (150, 110, 70), (26, 0, 14, BLOCK_SIZE))

        elif block_id == PISTON_HEAD:
            surf.fill(SKY_BLUE); surf.set_colorkey(SKY_BLUE)
            pygame.draw.rect(surf, (140, 140, 140), (0, 15, 26, 10))
            pygame.draw.rect(surf, (150, 110, 70), (26, 0, 14, BLOCK_SIZE))

        elif block_id == RAILS:
            surf.fill(SKY_BLUE); surf.set_colorkey(SKY_BLUE)
            pygame.draw.line(surf, (180, 180, 180), (0, 28), (BLOCK_SIZE, 28), 3)
            pygame.draw.line(surf, (180, 180, 180), (0, 38), (BLOCK_SIZE, 38), 3)

        elif block_id == MINECART_ITEM:
            surf.fill(SKY_BLUE); surf.set_colorkey(SKY_BLUE)
            pygame.draw.rect(surf, (130, 140, 150), (2, 10, 36, 22))
            pygame.draw.circle(surf, (40, 40, 40), (10, 34), 6)
            pygame.draw.circle(surf, (30, 30, 30), (30, 34), 6)

        elif block_id == GREENSTONE_WIRE:
            surf.fill(SKY_BLUE); surf.set_colorkey(SKY_BLUE)
            pygame.draw.rect(surf, (10, 50, 10), (14, 14, 12, 12))
            
            act_surf = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
            act_surf.fill(SKY_BLUE); act_surf.set_colorkey(SKY_BLUE)
            pygame.draw.rect(act_surf, (0, 220, 60), (12, 12, 16, 16))
            GREENSTONE_ACTIVE_TEXTURES[GREENSTONE_WIRE] = act_surf

        elif block_id == GREEN_DYNAMITE:
            surf.fill((10, 130, 40))
            pygame.draw.rect(surf, (240, 240, 240), (0, 14, BLOCK_SIZE, 12))

        elif block_id == CHEST:
            surf.fill((139, 105, 20))
            pygame.draw.rect(surf, (80, 50, 15), (0, 0, BLOCK_SIZE, BLOCK_SIZE), 3)
            pygame.draw.rect(surf, (230, 190, 20), (16, 14, 8, 10))

        elif block_id == BOW:
            surf.fill(SKY_BLUE); surf.set_colorkey(SKY_BLUE)
            pygame.draw.arc(surf, (160, 110, 60), (4, 4, 32, 32), 0.5, 3.8, 4)

        elif block_id == ARROW:
            surf.fill(SKY_BLUE); surf.set_colorkey(SKY_BLUE)
            pygame.draw.line(surf, (140, 110, 80), (4, 20), (32, 20), 2)

        elif block_id == JETPACK:
            surf.fill(SKY_BLUE); surf.set_colorkey(SKY_BLUE)
            pygame.draw.rect(surf, (160, 40, 40), (8, 6, 24, 28))

        elif block_id == LAVA:
            pygame.draw.rect(surf, (230, 70, 0), (0, 0, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(surf, (255, 120, 0), (0, 6, BLOCK_SIZE, 8))

        elif block_id == CHARGER:
            pygame.draw.rect(surf, (40, 45, 55), (0, 0, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.polygon(surf, (0, 255, 200), [(20, 8), (12, 22), (18, 22), (16, 32), (26, 18), (20, 18)])

        elif block_id == BOSS_ALTAR:
            pygame.draw.rect(surf, (40, 0, 70), (0, 0, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.circle(surf, (255, 0, 255), (20, 20), 8)

        elif block_id == HOE:
            surf.fill(SKY_BLUE); surf.set_colorkey(SKY_BLUE)
            pygame.draw.line(surf, (139, 69, 19), (6, 34), (28, 12), 3)

        elif block_id == WHEAT_SEEDS:
            surf.fill(SKY_BLUE); surf.set_colorkey(SKY_BLUE)
            pygame.draw.polygon(surf, (160, 120, 80), [(8, 32), (32, 32), (20, 8)])

        elif block_id == FARMLAND:
            surf.fill((80, 45, 20))
            pygame.draw.rect(surf, (45, 20, 5), (0, 4, BLOCK_SIZE, 6))

        elif block_id == WHEAT_STAGE1:
            surf.fill(SKY_BLUE); surf.set_colorkey(SKY_BLUE)
            pygame.draw.line(surf, (40, 180, 40), (14, 40), (10, 28), 2)

        elif block_id == WHEAT_STAGE2:
            surf.fill(SKY_BLUE); surf.set_colorkey(SKY_BLUE)
            pygame.draw.line(surf, (50, 200, 50), (20, 40), (20, 18), 3)

        elif block_id == WHEAT_STAGE3:
            surf.fill(SKY_BLUE); surf.set_colorkey(SKY_BLUE)
            pygame.draw.line(surf, (210, 190, 60), (20, 40), (20, 10), 3)

        elif block_id == WHEAT_STAGE4:
            surf.fill(SKY_BLUE); surf.set_colorkey(SKY_BLUE)
            pygame.draw.line(surf, (245, 215, 50), (20, 40), (20, 4), 3)

        elif block_id == WATER:
            surf.fill((30, 144, 255))
            surf.set_alpha(170)
            pygame.draw.rect(surf, (70, 180, 255), (0, 0, BLOCK_SIZE, 4))

        elif block_id == OBSIDIAN:
            surf.fill((25, 20, 42))
            pygame.draw.line(surf, (60, 40, 90), (4, 4), (16, 16), 2)

        elif block_id == DIRT_WALL:
            surf.fill((75, 45, 25))
            pygame.draw.rect(surf, (55, 30, 15), (0, 0, BLOCK_SIZE, BLOCK_SIZE), 1)

        elif block_id == STONE_WALL:
            surf.fill((65, 65, 65))
            pygame.draw.rect(surf, (45, 45, 45), (0, 0, BLOCK_SIZE, BLOCK_SIZE), 1)

        elif block_id == DOOR_CLOSED:
            surf.fill((135, 85, 45))
            pygame.draw.rect(surf, (75, 45, 15), (0, 0, BLOCK_SIZE, BLOCK_SIZE), 3)
            pygame.draw.circle(surf, (230, 190, 20), (32, 20), 3)

        elif block_id == DOOR_OPEN:
            surf.fill(SKY_BLUE); surf.set_colorkey(SKY_BLUE)
            pygame.draw.rect(surf, (75, 45, 15), (0, 0, 10, BLOCK_SIZE))
            pygame.draw.rect(surf, (110, 70, 35), (2, 2, 6, BLOCK_SIZE - 4))

        elif block_id == GLASS_PANE:
            surf.fill(SKY_BLUE); surf.set_colorkey(SKY_BLUE)
            pygame.draw.rect(surf, (200, 240, 255), (16, 0, 8, BLOCK_SIZE))
            surf.set_alpha(180)

        elif block_id == LIGHTNING_ROD:
            surf.fill(SKY_BLUE); surf.set_colorkey(SKY_BLUE)
            pygame.draw.rect(surf, (140, 140, 150), (18, 0, 4, BLOCK_SIZE))
            pygame.draw.rect(surf, (200, 200, 210), (14, 0, 12, 6))

        elif block_id == WIND_TURBINE:
            surf.fill((90, 95, 105))
            pygame.draw.rect(surf, (50, 55, 65), (0, 0, BLOCK_SIZE, BLOCK_SIZE), 2)
            pygame.draw.circle(surf, (220, 220, 230), (20, 20), 6)

        elif block_id == UMBRELLA:
            surf.fill(SKY_BLUE); surf.set_colorkey(SKY_BLUE)
            pygame.draw.arc(surf, (220, 40, 40), (4, 4, 32, 24), 0, 3.14, 6)
            pygame.draw.line(surf, (40, 40, 40), (20, 16), (20, 34), 2)
            pygame.draw.arc(surf, (40, 40, 40), (16, 32, 6, 6), 3.14, 6.28, 2)

        BLOCK_TEXTURES[block_id] = surf

generate_textures()
DIMENSION_EARTH = 0
DIMENSION_MOON = 1
current_dimension = DIMENSION_EARTH  

spawned_trees = []
wheat_growth_timer = {}
lunar_droids = []
lunar_lasers = []

player_hp = 100
player_max_hp = 100

def get_world_filename(slot):
    return f"astroblocks_world_{slot}.txt"

def save_world_to_file(slot):
    filename = get_world_filename(slot)
    try:
        with open(filename, "w") as f:
            sp_x = custom_spawn_point[0] if custom_spawn_point else -1
            sp_y = custom_spawn_point[1] if custom_spawn_point else -1
            f.write(f"{player_x},{player_y},{jetpack_fuel},{current_dimension},{current_world_mode},{int(is_raining)},{rain_timer},{sp_x},{sp_y}\n")
            f.write(f"{len(spawned_trees)}\n")
            for t in spawned_trees:
                f.write(f"{t['x']},{t['y']},{t['height']},{t['bl_y']},{t['br_y']}\n")
            f.write(f"{len(wheat_growth_timer)}\n")
            for (r, c), timer in wheat_growth_timer.items():
                f.write(f"{r},{c},{timer}\n")
            for row in range(ROWS):
                f.write(" ".join(map(str, earth_map[row])) + "\n")
            for row in range(ROWS):
                f.write(" ".join(map(str, moon_map[row])) + "\n")
    except Exception as e:
        pass

def load_world_from_file(slot):
    global player_x, player_y, jetpack_fuel, current_dimension, current_world_mode, spawned_trees, wheat_growth_timer, earth_map, moon_map, world_map, player_hp, is_raining, rain_timer, custom_spawn_point
    filename = get_world_filename(slot)
    if not os.path.exists(filename):
        return False
    try:
        with open(filename, "r") as f:
            meta = f.readline().strip().split(",")
            player_x = float(meta[0])
            player_y = float(meta[1])
            jetpack_fuel = float(meta[2])
            current_dimension = int(meta[3])
            current_world_mode = int(meta[4]) if len(meta) > 4 else MODE_CREATIVE
            
            if len(meta) > 8:
                is_raining = bool(int(meta[5]))
                rain_timer = int(meta[6])
                sx, sy = float(meta[7]), float(meta[8])
                custom_spawn_point = (sx, sy) if sx != -1 else None
            else:
                is_raining = False
                rain_timer = 0
                custom_spawn_point = None
            
            spawned_trees.clear()
            num_trees = int(f.readline().strip())
            for _ in range(num_trees):
                t_data = f.readline().strip().split(",")
                spawned_trees.append({
                    "x": float(t_data[0]), "y": float(t_data[1]), "height": int(t_data[2]),
                    "bl_y": float(t_data[3]), "br_y": float(t_data[4])
                })
                
            wheat_growth_timer.clear()
            num_wheat = int(f.readline().strip())
            for _ in range(num_wheat):
                w_data = f.readline().strip().split(",")
                wheat_growth_timer[(int(w_data[0]), int(w_data[1]))] = int(w_data[2])
                
            for r in range(ROWS):
                earth_map[r] = list(map(int, f.readline().strip().split()))
            for r in range(ROWS):
                moon_map[r] = list(map(int, f.readline().strip().split()))
                
        world_map = earth_map if current_dimension == DIMENSION_EARTH else moon_map
        lunar_droids.clear()
        lunar_lasers.clear()
        falling_leaves.clear()
        player_hp = player_max_hp
        generate_textures()
        return True
    except Exception as e:
        return False

def generate_new_world(mode):
    global earth_map, moon_map, world_map, spawned_trees, wheat_growth_timer, current_dimension, player_x, player_y, jetpack_fuel, current_world_mode, player_hp, is_raining, rain_timer, custom_spawn_point
    player_x, player_y = 300, 150
    jetpack_fuel = 100.0
    current_dimension = DIMENSION_EARTH
    current_world_mode = mode
    player_hp = player_max_hp
    is_raining = False
    rain_timer = 0
    custom_spawn_point = None
    spawned_trees.clear()
    wheat_growth_timer.clear()
    falling_leaves.clear()
    
    earth_map = [[AIR for _ in range(COLS)] for _ in range(ROWS)]
    for col in range(COLS):
        ground_level = random.randint(12, 15) 
        for row in range(ROWS):
            if row == ground_level:
                earth_map[row][col] = SAND if random.random() < 0.12 else GRASS 
            elif ground_level < row <= ground_level + 4:
                earth_map[row][col] = DIRT
            elif row > ground_level + 4:
                ore_chance = random.random()
                if row > 35:
                    if ore_chance < 0.08: earth_map[row][col] = LAVA
                    elif ore_chance < 0.09 and col % 25 == 0: earth_map[row][col] = BOSS_ALTAR
                    elif ore_chance < 0.13: earth_map[row][col] = DIAMOND_ORE
                    elif ore_chance < 0.16: earth_map[row][col] = EMERALD
                    else: earth_map[row][col] = BLACKSTONE
                elif row > 24:
                    if ore_chance < 0.03: earth_map[row][col] = GOLD_ORE
                    elif ore_chance < 0.06: earth_map[row][col] = REDSTONE_ORE
                    elif ore_chance < 0.10: earth_map[row][col] = COPPER
                    else: earth_map[row][col] = STONE
                else:
                    if ore_chance < 0.08: earth_map[row][col] = IRON_ORE
                    elif ore_chance < 0.14: earth_map[row][col] = COAL_ORE
                    else: earth_map[row][col] = STONE

    cave_mask = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    for r in range(16, ROWS):
        for c in range(COLS):
            if random.random() < 0.44: cave_mask[r][c] = 1
                
    for _ in range(3):
        new_mask = [[cave_mask[r][c] for c in range(COLS)] for r in range(ROWS)]
        for r in range(17, ROWS - 1):
            for c in range(1, COLS - 1):
                count = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]: count += cave_mask[r + dr][c + dc]
                if count > 4: new_mask[r][c] = 1
                elif count < 4: new_mask[r][c] = 0
        cave_mask = new_mask

    for r in range(16, ROWS):
        for c in range(COLS):
            if cave_mask[r][c] == 1 and earth_map[r][c] not in [PORTAL, BOSS_ALTAR, LAVA]:
                old_block = earth_map[r][c]
                if old_block in [STONE, COAL_ORE, IRON_ORE, GOLD_ORE, DIAMOND_ORE, REDSTONE_ORE, COPPER, BLACKSTONE]:
                    earth_map[r][c] = STONE_WALL
                elif old_block == DIRT:
                    earth_map[r][c] = DIRT_WALL
                if random.random() < 0.04 and earth_map[r][c] in [STONE_WALL, DIRT_WALL] and r > 20:
                    if earth_map[r-1][c] not in [STONE_WALL, DIRT_WALL, AIR]:
                        earth_map[r][c] = WATER

    for col in range(8, COLS - 8):
        for row in range(ROWS):
            if earth_map[row][col] == GRASS:
                if random.random() < 0.15:
                    t_height = random.randint(140, 200)
                    spawned_trees.append({
                        "x": col * BLOCK_SIZE + 16, "y": row * BLOCK_SIZE, "height": t_height,
                        "bl_y": t_height * random.uniform(0.4, 0.5), "br_y": t_height * random.uniform(0.6, 0.7)
                    })
                break

    moon_map = [[AIR for _ in range(COLS)] for _ in range(ROWS)]
    for col in range(COLS):
        moon_ground = random.randint(10, 14)
        for row in range(ROWS):
            if row >= moon_ground: moon_map[row][col] = AMETHYST if random.random() < 0.08 else STONE

    for col in range(15, COLS - 15, 35):
        if random.random() < 0.7:
            d_row = random.randint(20, 32)
            d_w, d_h = random.randint(10, 14), random.randint(5, 7)
            for r in range(d_row, min(ROWS, d_row + d_h)):
                for c in range(col, min(COLS, col + d_w)):
                    if r == d_row or r == d_row + d_h - 1 or c == col or c == col + d_w - 1: moon_map[r][c] = QUARTZ
                    else: moon_map[r][c] = AIR
            if d_row + d_h - 2 < ROWS and col + d_w // 2 < COLS: moon_map[d_row + d_h - 2][col + d_w // 2] = CHEST

    world_map = earth_map
    generate_textures()

earth_map = [[AIR for _ in range(COLS)] for _ in range(ROWS)]
moon_map = [[AIR for _ in range(COLS)] for _ in range(ROWS)]
world_map = earth_map
player_x, player_y = 300, 150
player_w, player_h = 30, 50  
player_speed = 4
vel_y = 0  
is_grounded = False
camera_x = 0  
camera_y = 0  

player_direction = 1  
walk_frame = 0.0      
is_moving = False     

time_of_day = 0       
DAY_LENGTH = 18000    
current_sky_color = (135, 206, 235)  
night_darkness = 0    

jetpack_fuel = 100.0
boss_active = False
boss_x, boss_y = 0, 0
boss_hp = 1000
boss_max_hp = 1000
boss_projectiles = []
boss_shoot_timer = 0
boss_facing_right = True

clouds = [{"x": random.randint(0, SCREEN_WIDTH * 3), "y": random.randint(20, 150), "speed": random.uniform(0.2, 0.5), "width": random.randint(60, 120)} for _ in range(12)]
stars = [{"x": random.randint(0, SCREEN_WIDTH), "y": random.randint(0, SCREEN_HEIGHT), "size": random.randint(1, 3), "blink_speed": random.uniform(0.02, 0.07), "phase": random.uniform(0, 6.28)} for _ in range(60)]

creative_items = [
    PICKAXE, HOE, WHEAT_SEEDS, GRASS, DIRT, STONE, WOOD, LEAVES,
    COAL_ORE, IRON_ORE, GOLD_ORE, DIAMOND_ORE, REDSTONE_ORE, GLASS,
    BRICK, WOOL, PLANKS, SAND, NEON, AMETHYST, EMERALD, LAPIS, COPPER, 
    QUARTZ, COAL_BLOCK, IRON_BLOCK, GOLD_BLOCK, BLACKSTONE, TERRACOTTA, 
    GLOWSTONE, RED_BRICK, BLUE_WOOL, GREEN_WOOL, TORCH, CRAFTING_TABLE, 
    FURNACE, BED, PORTAL, LEVER, PISTON, RAILS, MINECART_ITEM, GREENSTONE_WIRE, 
    GREEN_DYNAMITE, CHEST, BOW, ARROW, JETPACK, LAVA, CHARGER, BOSS_ALTAR,
    WATER, OBSIDIAN, DIRT_WALL, STONE_WALL, DOOR_CLOSED, GLASS_PANE,
    LIGHTNING_ROD, WIND_TURBINE, UMBRELLA
]
current_hand = PICKAXE  
show_inventory = False
show_pause_menu = False
DIFFICULTY_EASY, DIFFICULTY_HARD = 0, 1
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
chest_inventory = [AMETHYST, AMETHYST, NEON, ARROW, ARROW, ARROW] + [AIR]*12

def draw_organic_tree(tree):
    scr_x = tree["x"] - camera_x
    scr_y = tree["y"] - camera_y
    h = tree["height"]
    if -150 < scr_x < SCREEN_WIDTH + 150 and -250 < scr_y < SCREEN_HEIGHT + h:
        for i in range(0, int(h), 4):
            cy = scr_y - i
            th = 10 + int(6 * (1.0 - i / h))
            if i < 24: th += int(16 * (1.0 - i / 24))
            pygame.draw.rect(screen, (101, 67, 33), (scr_x - th // 2, cy, th, 4))
        by1 = scr_y - tree["bl_y"]
        pygame.draw.line(screen, (101, 67, 33), (scr_x, by1), (scr_x - 25, by1 - 15), 5)
        by2 = scr_y - tree["br_y"]
        pygame.draw.line(screen, (101, 67, 33), (scr_x, by2), (scr_x + 25, by2 - 15), 5)
        for cx, cy, rad in [(scr_x - 25, by1 - 15, 24), (scr_x + 25, by2 - 15, 24), (scr_x, scr_y - h, 36), (scr_x - 14, scr_y - h + 12, 26), (scr_x + 14, scr_y - h + 12, 26)]:
            pygame.draw.circle(screen, (24, 115, 24), (int(cx), int(cy)), rad)
            pygame.draw.circle(screen, (34, 155, 34), (int(cx), int(cy) - 3), rad - 2)

def draw_player(x, y):
    screen_x = x - camera_x
    screen_y = y - camera_y
    leg_swing = math.sin(walk_frame) * 8 if (is_moving and is_grounded) else (4 if not is_grounded else 0)
    arm_swing = math.sin(walk_frame) * 6 if (is_moving and is_grounded) else 0
    pygame.draw.rect(screen, (100, 50, 0), (screen_x + 6, screen_y, 18, 6)) 
    pygame.draw.rect(screen, (255, 224, 189), (screen_x + 6, screen_y + 6, 18, 12)) 
    ex = screen_x + 18 if player_direction == 1 else screen_x + 10
    pygame.draw.rect(screen, (0, 0, 0), (ex, screen_y + 10, 2, 2)) 
    pygame.draw.rect(screen, (0, 150, 255), (screen_x + 6, screen_y + 18, 18, 18)) 
    pygame.draw.rect(screen, (50, 50, 200), (screen_x + 6 + int(leg_swing), screen_y + 36, 7, 14)) 
    pygame.draw.rect(screen, (40, 40, 180), (screen_x + 17 - int(leg_swing), screen_y + 36, 7, 14)) 
    pygame.draw.rect(screen, (255, 224, 189), (screen_x + 2 + int(arm_swing), screen_y + 20, 4, 10)) 
    pygame.draw.rect(screen, (255, 224, 189), (screen_x + 24 - int(arm_swing), screen_y + 20, 4, 10))

def draw_zombie(x, y):
    screen_x = x - camera_x
    screen_y = y - camera_y
    pygame.draw.rect(screen, (30, 20, 0), (screen_x + 6, screen_y, 18, 6)) 
    pygame.draw.rect(screen, (60, 140, 60), (screen_x + 6, screen_y + 6, 18, 12)) 
    pygame.draw.rect(screen, (255, 0, 0), (screen_x + 14, screen_y + 10, 2, 2)) 
    pygame.draw.rect(screen, (100, 30, 150), (screen_x + 3, screen_y + 18, 24, 18)) 
    pygame.draw.rect(screen, (30, 30, 100), (screen_x + 4, screen_y + 36, 10, 14)) 

def draw_lunar_droid(x, y):
    screen_x = x - camera_x
    screen_y = y - camera_y
    pygame.draw.circle(screen, (150, 160, 175), (int(screen_x + 15), int(screen_y + 15)), 14)
    pygame.draw.circle(screen, (100, 110, 125), (int(screen_x + 15), int(screen_y + 15)), 14, 2)
    pygame.draw.rect(screen, (0, 240, 255), (screen_x + 10, screen_y + 12, 10, 6))
    pygame.draw.line(screen, (80, 80, 80), (screen_x + 15, screen_y + 1), (screen_x + 15, screen_y - 6), 2)
    pygame.draw.circle(screen, (255, 0, 50), (int(screen_x + 15), int(screen_y - 7)), 2)

def draw_boss(x, y):
    sx, sy = x - camera_x, y - camera_y
    pygame.draw.rect(screen, (20, 0, 40), (sx + 12, sy, 66, 18))
    pygame.draw.rect(screen, (110, 30, 180), (sx + 12, sy + 18, 66, 36))
    pygame.draw.rect(screen, (255, 0, 0), (sx + 30, sy + 30, 10, 10))
    pygame.draw.rect(screen, (255, 0, 0), (sx + 50, sy + 30, 10, 10))
    pygame.draw.rect(screen, (40, 10, 80), (sx, sy + 54, 90, 66))
    pygame.draw.rect(screen, (20, 5, 40), (sx + 15, sy + 120, 24, 30))
    pygame.draw.rect(screen, (20, 5, 40), (sx + 51, sy + 120, 24, 30))

def draw_pickaxe(x, y):
    pygame.draw.line(screen, (139, 69, 19), (x + 5, y + 30), (x + 30, y + 5), 4) 
    pygame.draw.arc(screen, (150, 150, 150), (x + 15, y, 20, 20), 0.5, 3.14, 5) 

def draw_minecart(x, y):
    sx, sy = x - camera_x, y - camera_y
    pygame.draw.rect(screen, (100, 110, 120), (sx + 2, sy + 16, 36, 20))
    pygame.draw.circle(screen, (30, 30, 30), (sx + 10, sy + 34), 5)
    pygame.draw.circle(screen, (30, 30, 30), (sx + 30, sy + 34), 5)

def draw_live_arrow(x, y, vx):
    sx, sy = x - camera_x, y - camera_y
    pygame.draw.line(screen, (100, 100, 100), (sx, sy), (sx + (15 if vx >= 0 else -15), sy), 2)
while True:
    clock.tick(60)
    
    phase = time_of_day / DAY_LENGTH
    torch_anim_frame = (torch_anim_frame + 1) % 30
    turbine_anim_frame = (turbine_anim_frame + (5 if is_raining else 1)) % 360

    if current_game_state == STATE_PLAYING:
        if not show_pause_menu:
            time_of_day = (time_of_day + 1) % DAY_LENGTH  
            
            # --- СИСТЕМА ПОГОДЫ (Дождь раз в 2 дня) ---
            rain_timer += 1
            if not is_raining and rain_timer >= 36000:  # 2 игровых дня без дождя
                if random.random() < 0.05:  # Шанс начала шторма
                    is_raining = True
                    rain_timer = 0
                    generate_textures()  # Обновляем текстуры на влажные
            elif is_raining and rain_timer >= 2400:  # Дождь идёт около 40 секунд
                is_raining = False
                rain_timer = 0
                generate_textures()  # Возвращаем сухие текстуры
                
            # Эффект падающих листьев во время шторма
            if is_raining and current_dimension == DIMENSION_EARTH and random.random() < 0.15:
                for col in range(start_col, end_col):
                    for row in range(start_row, end_row):
                        if 0 <= row < ROWS and 0 <= col < COLS and world_map[row][col] == LEAVES:
                            if random.random() < 0.01:
                                falling_leaves.append({"x": col * BLOCK_SIZE + 20, "y": row * BLOCK_SIZE + 20, "vx": random.uniform(-1.5, -0.5), "vy": random.uniform(1.0, 2.0)})
        
        # Корректировка цвета неба при шторме
        if current_dimension == DIMENSION_EARTH:
            if is_raining:
                r1, g1, b1 = 45, 55, 70
                r2, g2, b2 = 25, 30, 45
                night_darkness = 120
            else:
                if phase < 0.25:  
                    progress = phase / 0.25
                    night_darkness = int(180 * (1 - progress))
                    r1, g1, b1 = int(10 + (135 - 10) * progress), int(15 + (206 - 15) * progress), int(30 + (235 - 30) * progress)
                    r2, g2, b2 = int(5 + (70 - 5) * progress), int(10 + (130 - 10) * progress), int(20 + (180 - 20) * progress)
                elif phase < 0.5:  
                    night_darkness = 0
                    r1, g1, b1, r2, g2, b2 = 135, 206, 235, 70, 130, 180
                elif phase < 0.75:  
                    progress = (phase - 0.5) / 0.25
                    night_darkness = int(180 * progress)
                    r1, g1, b1 = int(135 - (135 - 10) * progress), int(206 - (206 - 15) * progress), int(235 - (235 - 30) * progress)
                    r2, g2, b2 = int(70 - (70 - 5) * progress), int(130 - (130 - 10) * progress), int(180 - (180 - 20) * progress)
                else:  
                    night_darkness = 180
                    r1, g1, b1, r2, g2, b2 = 10, 15, 30, 5, 10, 20
        else:
            night_darkness = 100 if phase < 0.5 else 160
            r1, g1, b1, r2, g2, b2 = 15, 10, 25, 5, 5, 12

        for y in range(0, SCREEN_HEIGHT, 15):
            factor = y / SCREEN_HEIGHT
            curr_r = int(r1 + (r2 - r1) * factor)
            curr_g = int(g1 + (g2 - g1) * factor)
            curr_b = int(b1 + (b2 - b1) * factor)
            pygame.draw.rect(screen, (curr_r, curr_g, curr_b), (0, y, SCREEN_WIDTH, 15))

        if current_dimension == DIMENSION_EARTH and night_darkness > 40 and not is_raining:
            for star in stars:
                if not show_pause_menu: star["phase"] += star["blink_speed"]
                pygame.draw.circle(screen, (255, 255, 255), (star["x"], star["y"]), star["size"])

        if current_dimension == DIMENSION_MOON:
            for star in stars:
                if not show_pause_menu: star["phase"] += star["blink_speed"]
                pygame.draw.circle(screen, (240, 240, 255), (star["x"], star["y"]), star["size"])

        if current_dimension == DIMENSION_EARTH and night_darkness < 140 and not is_raining:
            for cloud in clouds:
                if not show_pause_menu:
                    cloud["x"] -= cloud["speed"]
                    if cloud["x"] + cloud["width"] < 0: cloud["x"] = WORLD_PIXEL_WIDTH
                c_screen_x = cloud["x"] - camera_x
                if -150 < c_screen_x < SCREEN_WIDTH + 50:
                    pygame.draw.ellipse(screen, (245, 250, 255, 180), (c_screen_x, cloud["y"], cloud["width"], 25))
        if not show_pause_menu and clock.get_fps() != 0:
            if is_raining and current_dimension == DIMENSION_EARTH and random.random() < 0.3:
                rc = random.randint(start_col, end_col - 1)
                if 0 <= rc < COLS:
                    for rr in range(ROWS):
                        if world_map[rr][rc] not in [AIR, WATER, DIRT_WALL, STONE_WALL, DOOR_OPEN, GLASS_PANE, TORCH]:
                            if rr - 1 >= 0 and world_map[rr - 1][rc] == AIR and rr > 10:
                                pass
                            break
            if is_raining and current_dimension == DIMENSION_EARTH and random.random() < 0.005:
                lightning_flash = 12
                lc = random.randint(0, COLS - 1)
                for lr in range(ROWS):
                    if world_map[lr][lc] != AIR:
                        if world_map[lr][lc] == LIGHTNING_ROD: active_lightning_signals.add((lr, lc))
                        break
            if random.random() < 0.4:  
                for row in range(ROWS - 2, -1, -1):
                    for col in range(COLS):
                        block = world_map[row][col]
                        if block in [WATER, LAVA]:
                            is_obsidian = False
                            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                                nr, nc = row + dr, col + dc
                                if 0 <= nr < ROWS and 0 <= nc < COLS:
                                    neighbor = world_map[nr][nc]
                                    if (block == WATER and neighbor == LAVA) or (block == LAVA and neighbor == WATER):
                                        world_map[row][col] = OBSIDIAN
                                        world_map[nr][nc] = OBSIDIAN
                                        is_obsidian = True
                                        break
                            if is_obsidian: continue
                            down = world_map[row + 1][col]
                            if down in [AIR, DIRT_WALL, STONE_WALL, DOOR_OPEN]:
                                world_map[row + 1][col] = block
                                world_map[row][col] = AIR
                            else:
                                sides = []
                                if col > 0 and world_map[row][col - 1] in [AIR, DIRT_WALL, STONE_WALL, DOOR_OPEN]: sides.append(col - 1)
                                if col < COLS - 1 and world_map[row][col + 1] in [AIR, DIRT_WALL, STONE_WALL, DOOR_OPEN]: sides.append(col + 1)
                                if sides:
                                    target_col = random.choice(sides)
                                    world_map[row][target_col] = block
                                    if random.random() < 0.2: world_map[row][col] = AIR
        if lightning_flash > 0: lightning_flash -= 1
        if not show_pause_menu:
            next_leaves = []
            for leaf in falling_leaves:
                leaf["x"] += leaf["vx"]; leaf["y"] += leaf["vy"]
                l_c, l_r = int(leaf["x"] // BLOCK_SIZE), int(leaf["y"] // BLOCK_SIZE)
                if 0 <= l_r < ROWS and 0 <= l_c < COLS and world_map[l_r][l_c] in [AIR, DIRT_WALL, STONE_WALL, WATER]: next_leaves.append(leaf)
            falling_leaves = next_leaves
            growth_speed = 3 if (is_raining and current_dimension == DIMENSION_EARTH) else 1
            for key in list(wheat_growth_timer.keys()):
                wheat_growth_timer[key] += growth_speed
                if wheat_growth_timer[key] >= 400:  
                    wheat_growth_timer[key] = 0; w_r, w_c = key
                    if 0 <= w_r < ROWS and 0 <= w_c < COLS:
                        curr_crop = world_map[w_r][w_c]
                        if curr_crop == WHEAT_STAGE1: world_map[w_r][w_c] = WHEAT_STAGE2
                        elif curr_crop == WHEAT_STAGE2: world_map[w_r][w_c] = WHEAT_STAGE3
                        elif curr_crop == WHEAT_STAGE3: world_map[w_r][w_c] = WHEAT_STAGE4
                        else: del wheat_growth_timer[key]
        for row in range(ROWS - 4):
            for col in range(COLS - 3):
                if (world_map[row][col] == STONE and world_map[row][col+1] == STONE and world_map[row][col+2] == STONE and world_map[row][col+3] == STONE and
                    world_map[row+4][col] == STONE and world_map[row+4][col+1] == STONE and world_map[row+4][col+2] == STONE and world_map[row+4][col+3] == STONE and
                    world_map[row+1][col] == STONE and world_map[row+2][col] == STONE and world_map[row+3][col] == STONE and
                    world_map[row+1][col+3] == STONE and world_map[row+2][col+3] == STONE and world_map[row+3][col+3] == STONE):
                    if world_map[row+1][col+1] == AIR: world_map[row+1][col+1] = PORTAL
                    if world_map[row+1][col+2] == AIR: world_map[row+1][col+2] = PORTAL
                    if world_map[row+2][col+1] == AIR: world_map[row+2][col+1] = PORTAL
                    if world_map[row+2][col+2] == AIR: world_map[row+2][col+2] = PORTAL
                    if world_map[row+3][col+1] == AIR: world_map[row+3][col+1] = PORTAL
                    if world_map[row+3][col+2] == AIR: world_map[row+3][col+2] = PORTAL
        p_col = int((player_x + player_w / 2) // BLOCK_SIZE); p_row = int((player_y + player_h / 2) // BLOCK_SIZE)
        if 0 <= p_row < ROWS and 0 <= p_col < COLS and world_map[p_row][p_col] == PORTAL:
            if current_dimension == DIMENSION_EARTH:
                current_dimension = DIMENSION_MOON
                for r_offset in range(5):
                    for c_offset in range(4):
                        if p_row-2+r_offset < ROWS and p_col-1+c_offset < COLS: moon_map[p_row-2+r_offset][p_col-1+c_offset] = earth_map[p_row-2+r_offset][p_col-1+c_offset]
                world_map = moon_map
            else: current_dimension = DIMENSION_EARTH; world_map = earth_map
            player_y -= 40; vel_y = -3; zombies.clear(); minecarts.clear(); arrows.clear(); boss_active = False; lunar_droids.clear(); lunar_lasers.clear()
        active_greenstone.clear(); queue = list(active_levers)
        for row in range(ROWS):
            for col in range(COLS):
                if world_map[row][col] == WIND_TURBINE and is_raining and current_dimension == DIMENSION_EARTH: queue.append((row, col))
                if (row, col) in active_lightning_signals: queue.append((row, col))
        visited = set(queue)
        while queue:
            curr_row, curr_col = queue.pop(0)
            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                nr, nc = curr_row + dr, curr_col + dc
                if 0 <= nr < ROWS and 0 <= nc < COLS and world_map[nr][nc] == GREENSTONE_WIRE and (nr, nc) not in visited: visited.add((nr, nc)); active_greenstone.add((nr, nc)); queue.append((nr, nc))
        exploded_dynamites = []
        for row in range(ROWS):
            for col in range(COLS):
                if world_map[row][col] == GREEN_DYNAMITE:
                    is_triggered = False
                    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < ROWS and 0 <= nc < COLS and ((nr, nc) in active_levers or (nr, nc) in active_greenstone or (nr, nc) in active_lightning_signals): is_triggered = True; break
                    if is_triggered: exploded_dynamites.append((row, col))
        for r_det, c_det in exploded_dynamites:
            for dr in range(-2, 3):
                for dc in range(-2, 3):
                    nr, nc = r_det + dr, c_det + dc
                    if 0 <= nr < ROWS and 0 <= nc < COLS and world_map[nr][nc] != PORTAL:
                        if (nr, nc) in active_levers: active_levers.remove((nr, nc))
                        world_map[nr][nc] = AIR
        for row in range(ROWS):
            for col in range(COLS):
                if world_map[row][col] == PISTON:
                    should_activate = False
                    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < ROWS and 0 <= nc < COLS and ((nr, nc) in active_levers or (nr, nc) in active_greenstone or (nr, nc) in active_lightning_signals): should_activate = True; break
                    if should_activate:
                        if col + 1 < COLS and world_map[row][col+1] in [AIR, DIRT_WALL, STONE_WALL]:
                            if col + 2 < COLS and world_map[row][col+2] not in [AIR, PISTON_HEAD]: world_map[row][col+2] = world_map[row][col+1]
                            world_map[row][col+1] = PISTON_HEAD
                    else:
                        if col + 1 < COLS and world_map[row][col+1] == PISTON_HEAD: world_map[row][col+1] = AIR
        camera_x = player_x - SCREEN_WIDTH // 2
        if camera_x < 0: camera_x = 0
        if camera_x > WORLD_PIXEL_WIDTH - SCREEN_WIDTH: camera_x = WORLD_PIXEL_WIDTH - SCREEN_WIDTH
        camera_y = player_y - SCREEN_HEIGHT // 2
        if camera_y < 0: camera_y = 0
        if camera_y > WORLD_PIXEL_HEIGHT - SCREEN_HEIGHT: camera_y = WORLD_PIXEL_HEIGHT - SCREEN_HEIGHT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if current_game_state == STATE_PLAYING: save_world_to_file(selected_world_slot)
            pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN:
            if current_game_state == STATE_PLAYING:
                if event.key == pygame.K_ESCAPE:
                    show_pause_menu = not show_pause_menu; show_inventory = False; show_chest = False
                if event.key == pygame.K_i and not show_pause_menu and not show_chest and current_world_mode == MODE_CREATIVE:
                    show_inventory = not show_inventory
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if current_game_state == STATE_MAIN_MENU:
                btn_play = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
                if btn_play.collidepoint(mouse_x, mouse_y): current_game_state = STATE_WORLD_SELECT
            elif current_game_state == STATE_WORLD_SELECT:
                btn_mode_toggle = pygame.Rect(SCREEN_WIDTH // 2 - 150, 100, 300, 40)
                if btn_mode_toggle.collidepoint(mouse_x, mouse_y): selected_creation_mode = MODE_SURVIVAL if selected_creation_mode == MODE_CREATIVE else MODE_CREATIVE
                for slot in range(1, 4):
                    slot_y = SCREEN_HEIGHT // 2 - 80 + slot * 60
                    btn_slot = pygame.Rect(SCREEN_WIDTH // 2 - 150, slot_y, 300, 45)
                    if btn_slot.collidepoint(mouse_x, mouse_y):
                        selected_world_slot = slot
                        if not load_world_from_file(slot): generate_new_world(selected_creation_mode); save_world_to_file(slot)
                        current_game_state = STATE_PLAYING
                btn_back = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT - 70, 150, 40)
                if btn_back.collidepoint(mouse_x, mouse_y): current_game_state = STATE_MAIN_MENU
            elif current_game_state == STATE_PLAYING:
                if show_pause_menu:
                    mid_x, mid_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
                    if pygame.Rect(mid_x - 100, mid_y - 60, 200, 40).collidepoint(mouse_x, mouse_y): show_pause_menu = False
                    elif pygame.Rect(mid_x - 100, mid_y - 10, 200, 40).collidepoint(mouse_x, mouse_y): current_difficulty = DIFFICULTY_HARD if current_difficulty == DIFFICULTY_EASY else DIFFICULTY_EASY
                    elif pygame.Rect(mid_x - 100, mid_y + 40, 200, 40).collidepoint(mouse_x, mouse_y):
                        save_world_to_file(selected_world_slot); show_pause_menu = False; current_game_state = STATE_MAIN_MENU
                elif show_chest:
                    ch_x, ch_y = SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 100
                    for idx in range(18):
                        r_idx, c_idx = idx // 6, idx % 6
                        if pygame.Rect(ch_x + 20 + c_idx * 55, ch_y + 50 + r_idx * 55, 45, 45).collidepoint(mouse_x, mouse_y): chest_inventory[idx], current_hand = current_hand, chest_inventory[idx]
                    if not pygame.Rect(ch_x, ch_y, 360, 230).collidepoint(mouse_x, mouse_y): show_chest = False
                elif show_inventory and current_world_mode == MODE_CREATIVE:
                    inv_x, inv_y = SCREEN_WIDTH // 2 - 190, SCREEN_HEIGHT // 2 - 210
                    for idx, item in enumerate(creative_items):
                        row_idx, col_idx = idx // 8, idx % 8
                        if pygame.Rect(inv_x + 20 + col_idx * 43, inv_y + 50 + row_idx * 43, 38, 38).collidepoint(mouse_x, mouse_y): current_hand = item; show_inventory = False
                else:
                    block_col = int((mouse_x + camera_x) // BLOCK_SIZE); block_row = int((mouse_y + camera_y) // BLOCK_SIZE)
                    if 0 <= block_col < COLS and 0 <= block_row < ROWS:
                        if event.button == 1:
                            if current_hand == BOW: arrows.append({"x": player_x + 15, "y": player_y + 20, "vx": 10.0 if mouse_x >= SCREEN_WIDTH // 2 else -10.0})
                            elif current_hand == HOE and world_map[block_row][block_col] in [GRASS, DIRT]: world_map[block_row][block_col] = FARMLAND
                            elif current_hand == WHEAT_SEEDS and current_world_mode == MODE_CREATIVE:
                                if block_row - 1 >= 0 and world_map[block_row][block_col] == FARMLAND and world_map[block_row - 1][block_col] == AIR: world_map[block_row - 1][block_col] = WHEAT_STAGE1; wheat_growth_timer[(block_row - 1, block_col)] = 0
                            elif current_hand == PICKAXE:
                                if world_map[block_row][block_col] == BOSS_ALTAR: boss_active = True; boss_x = block_col * BLOCK_SIZE - 25; boss_y = block_row * BLOCK_SIZE - 100; boss_hp = boss_max_hp
                                if world_map[block_row][block_col] in [WHEAT_STAGE1, WHEAT_STAGE2, WHEAT_STAGE3, WHEAT_STAGE4] and (block_row, block_col) in wheat_growth_timer: del wheat_growth_timer[(block_row, block_col)]
                                if world_map[block_row][block_col] == PISTON and block_col + 1 < COLS and world_map[block_row][block_col + 1] == PISTON_HEAD: world_map[block_row][block_col + 1] = AIR
                                if (block_row, block_col) in active_levers: active_levers.remove((block_row, block_col))
                                if block_row > 15:
                                    if world_map[block_row][block_col] in [STONE, COAL_ORE, IRON_ORE, GOLD_ORE, DIAMOND_ORE, REDSTONE_ORE, COPPER, BLACKSTONE]: world_map[block_row][block_col] = STONE_WALL
                                    elif world_map[block_row][block_col] == DIRT: world_map[block_row][block_col] = DIRT_WALL
                                    else: world_map[block_row][block_col] = AIR
                                else: world_map[block_row][block_col] = AIR
                        elif event.button == 3:
                            if world_map[block_row][block_col] == DOOR_CLOSED: world_map[block_row][block_col] = DOOR_OPEN
                            elif world_map[block_row][block_col] == DOOR_OPEN: world_map[block_row][block_col] = DOOR_CLOSED
                            elif world_map[block_row][block_col] == BED:
                                custom_spawn_point = (player_x, player_y)
                                if current_dimension == DIMENSION_EARTH and (phase >= 0.75 or phase < 0.25): time_of_day = 4500
                            elif world_map[block_row][block_col] == LEVER:
                                if (block_row, block_col) in active_levers: active_levers.remove((block_row, block_col))
                                else: active_levers.add((block_row, block_col))
                            elif world_map[block_row][block_col] == CHEST: show_chest = True; current_chest_pos = (block_row, block_col)
                            elif world_map[block_row][block_col] == BOSS_ALTAR: world_map[block_row][block_col] = AIR; boss_active = True; boss_x = block_col * BLOCK_SIZE - 25; boss_y = block_row * BLOCK_SIZE - 100; boss_hp = boss_max_hp
                            elif current_hand == MINECART_ITEM and world_map[block_row][block_col] == RAILS: minecarts.append({"x": block_col * BLOCK_SIZE, "y": block_row * BLOCK_SIZE, "vx": 0, "vy": 0})
                            elif current_hand not in [PICKAXE, MINECART_ITEM, HOE, WHEAT_SEEDS] and world_map[block_row][block_col] in [AIR, DIRT_WALL, STONE_WALL, DOOR_OPEN] and current_world_mode == MODE_CREATIVE: world_map[block_row][block_col] = current_hand
    if current_game_state == STATE_PLAYING and not show_pause_menu:
        def is_charger_powered(r, c):
            if world_map[r][c] == CHARGER:
                for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < ROWS and 0 <= nc < COLS and (world_map[nr][nc] in active_greenstone or world_map[nr][nc] in active_levers): return True
            return False

        p_center_col = int((player_x + player_w / 2) // BLOCK_SIZE)
        p_center_row = int((player_y + player_h / 2) // BLOCK_SIZE)
        is_in_water = False
        if 0 <= p_center_row < ROWS and 0 <= p_center_col < COLS and world_map[p_center_row][p_center_col] == WATER: is_in_water = True

        if is_in_water: gravity, jump_force, current_speed = 0.08, -3.5, player_speed * 0.6
        elif current_hand == UMBRELLA and vel_y > 0: gravity, jump_force, current_speed = 0.04, -11, player_speed
        else: gravity, jump_force, current_speed = (0.15 if current_dimension == DIMENSION_MOON else 0.5), (-6.5 if current_dimension == DIMENSION_MOON else -11), player_speed

        is_moving = False
        if not show_inventory and not show_chest:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] and player_x > 0: player_x -= current_speed; player_direction = -1; is_moving = True
            if keys[pygame.K_d] and player_x < WORLD_PIXEL_WIDTH - player_w: player_x += current_speed; player_direction = 1; is_moving = True
            walk_frame = (walk_frame + 0.12) if (is_moving and is_grounded) else 0

            if keys[pygame.K_SPACE] and current_hand == JETPACK and jetpack_fuel > 0: vel_y = -3.5 if is_in_water else -6.0; is_grounded = False; jetpack_fuel -= 0.4
            elif keys[pygame.K_SPACE] and is_grounded: vel_y = jump_force; is_grounded = False
            
            if not (keys[pygame.K_SPACE] and current_hand == JETPACK and jetpack_fuel > 0): vel_y += gravity
            if is_in_water and vel_y > 2.0: vel_y = 2.0
            if current_hand == UMBRELLA and vel_y > 1.2: vel_y = 1.2
            player_y += vel_y

            foot_row = int((player_y + player_h) // BLOCK_SIZE); center_col = int((player_x + player_w / 2) // BLOCK_SIZE)
            if 0 <= foot_row < ROWS and 0 <= center_col < COLS:
                if world_map[foot_row][center_col] not in [AIR, WATER, DIRT_WALL, STONE_WALL, DOOR_OPEN, GLASS_PANE, TORCH]:
                    if world_map[foot_row][center_col] == LAVA:
                        player_y -= 20; vel_y = -4; is_grounded = False
                        if current_world_mode == MODE_SURVIVAL: player_hp -= 1.5
                    else:
                        player_y = foot_row * BLOCK_SIZE - player_h; vel_y = 0; is_grounded = True
                        ch_c = int((player_x + player_w / 2) // BLOCK_SIZE); ch_r = int((player_y + player_h - 5) // BLOCK_SIZE); ch_ur = int((player_y + player_h + 5) // BLOCK_SIZE)
                        if 0 <= ch_c < COLS:
                            if 0 <= ch_r < ROWS and world_map[ch_r][ch_c] == CHARGER:
                                if any((ch_r + dr, ch_c + dc) in active_greenstone or (ch_r + dr, ch_c + dc) in active_levers for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]):
                                    jetpack_fuel = min(100.0, jetpack_fuel + 4.0)
                            if 0 <= ch_ur < ROWS and world_map[ch_ur][ch_c] == CHARGER:
                                if any((ch_ur + dr, ch_c + dc) in active_greenstone or (ch_ur + dr, ch_c + dc) in active_levers for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]):
                                    jetpack_fuel = min(100.0, jetpack_fuel + 4.0)
                else: is_grounded = False
            else: is_grounded = False
        if boss_active:
            boss_x += 1.0 if boss_x < player_x else -1.0
            boss_facing_right = boss_x < player_x
            boss_y += 0.5 if boss_y < player_y - 40 else -0.5
            b_c, b_r = int((boss_x + 45) // BLOCK_SIZE), int((boss_y + 100) // BLOCK_SIZE)
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    nr, nc = b_r + dr, b_c + dc
                    if 0 <= nr < ROWS and 0 <= nc < COLS and world_map[nr][nc] in [DIRT, GRASS, LEAVES, WOOD]: world_map[nr][nc] = AIR
            boss_shoot_timer += 1
            if boss_shoot_timer >= 90: boss_shoot_timer = 0; boss_projectiles.append({"x": boss_x + 45, "y": boss_y + 40, "vx": 6.0 if boss_facing_right else -6.0})

        next_projectiles = []
        for p in boss_projectiles:
            p["x"] += p["vx"]; p_rect = pygame.Rect(p["x"], p["y"], 8, 8); p_hit = False
            if pygame.Rect(player_x, player_y, player_w, player_h).colliderect(p_rect):
                p_hit = True
                if current_world_mode == MODE_SURVIVAL: player_hp -= 20
            if 0 < p["x"] < WORLD_PIXEL_WIDTH and not p_hit: next_projectiles.append(p)
        boss_projectiles = next_projectiles

        if current_dimension == DIMENSION_MOON:
            zombie_spawn_timer += 1
            if zombie_spawn_timer >= 240 and len(lunar_droids) < 4:
                zombie_spawn_timer = 0; spawn_x = player_x + random.choice([-200, SCREEN_WIDTH + 100]); spawn_y = player_y + random.randint(-100, 100)
                if 0 < spawn_x < WORLD_PIXEL_WIDTH and 0 < spawn_y < WORLD_PIXEL_HEIGHT: lunar_droids.append({"x": spawn_x, "y": spawn_y, "shoot_t": random.randint(0, 60)})
        else: lunar_droids.clear(); lunar_lasers.clear()

        for d in lunar_droids:
            dx, dy = player_x - d["x"], player_y - d["y"]; dist = math.hypot(dx, dy)
            if dist > 5: d["x"] += (dx / dist) * 1.2; d["y"] += (dy / dist) * 1.2
            d["shoot_t"] += 1
            if d["shoot_t"] >= 120 and dist < 400: d["shoot_t"] = 0; lunar_lasers.append({"x": d["x"] + 15, "y": d["y"] + 15, "vx": (dx / dist) * 5.0, "vy": (dy / dist) * 5.0})

        next_lasers = []
        for l in lunar_lasers:
            l["x"] += l["vx"]; l["y"] += l["vy"]; l_rect = pygame.Rect(l["x"], l["y"], 6, 6); l_hit = False
            if pygame.Rect(player_x, player_y, player_w, player_h).colliderect(l_rect):
                l_hit = True
                if current_world_mode == MODE_SURVIVAL: player_hp -= 10
            if 0 < l["x"] < WORLD_PIXEL_WIDTH and 0 < l["y"] < WORLD_PIXEL_HEIGHT and not l_hit: next_lasers.append(l)
        lunar_lasers = next_lasers

        arrows_to_keep = []
        for arrow_obj in arrows:
            arrow_obj["x"] += arrow_obj["vx"]; arrow_hit = False; arrow_rect = pygame.Rect(arrow_obj["x"], arrow_obj["y"], 15, 4)
            if boss_active and arrow_rect.colliderect(pygame.Rect(boss_x, boss_y, 90, 150)):
                boss_hp -= 35; arrow_hit = True
                if boss_hp <= 0:
                    boss_active = False
                    for _ in range(5):
                        r_col = int(boss_x // BLOCK_SIZE) + random.randint(0, 2); r_row = int(boss_y // BLOCK_SIZE) + random.randint(0, 3)
                        if 0 <= r_row < ROWS and 0 <= r_col < COLS: world_map[r_row][r_col] = GOLD_BLOCK if random.random() < 0.3 else EMERALD
            for d in list(lunar_droids):
                if arrow_rect.colliderect(pygame.Rect(d["x"], d["y"], 30, 30)): lunar_droids.remove(d); arrow_hit = True; break
            for z in list(zombies):
                if arrow_rect.colliderect(pygame.Rect(z["x"], z["y"], player_w, player_h)): zombies.remove(z); arrow_hit = True; break
            if 0 < arrow_obj["x"] < WORLD_PIXEL_WIDTH and not arrow_hit: arrows_to_keep.append(arrow_obj)
        arrows = arrows_to_keep

        for cart in minecarts:
            cart["vy"] += 0.5; cart["y"] += cart["vy"]; c_col = int((cart["x"] + BLOCK_SIZE // 2) // BLOCK_SIZE); c_row = int((cart["y"] + BLOCK_SIZE - 2) // BLOCK_SIZE)
            if 0 <= c_row < ROWS and 0 <= c_col < COLS and world_map[c_row][c_col] == RAILS: cart["y"] = c_row * BLOCK_SIZE; cart["vy"] = 0
            cart["vx"] *= 0.95; cart["x"] += cart["vx"]
            if pygame.Rect(player_x, player_y, player_w, player_h).colliderect(pygame.Rect(cart["x"], cart["y"] + 12, BLOCK_SIZE, 20)): cart["vx"] = 4.0 if player_x < cart["x"] else -4.0

        if current_dimension == DIMENSION_EARTH and current_difficulty == DIFFICULTY_HARD and phase >= 0.75:
            zombie_spawn_timer += 1
            if zombie_spawn_timer >= 180 and len(zombies) < 5:
                zombie_spawn_timer = 0; spawn_x = player_x + random.choice([-150, SCREEN_WIDTH + 50])
                if 0 < spawn_x < WORLD_PIXEL_WIDTH:
                    z_col = int(spawn_x // BLOCK_SIZE); z_row = 5
                    for r in range(ROWS):
                        if world_map[r][z_col] not in [AIR, WATER, DIRT_WALL, STONE_WALL, DOOR_OPEN, GLASS_PANE]: z_row = r - 1; break
                    zombies.append({"x": spawn_x, "y": z_row * BLOCK_SIZE, "vel_y": 0})
        if phase < 0.75 or current_dimension == DIMENSION_MOON: zombies.clear()
        for z in zombies:
            z["vel_y"] += 0.5; z["y"] += z["vel_y"]; z_fr, z_cc = int((z["y"] + player_h) // BLOCK_SIZE), int((z["x"] + player_w / 2) // BLOCK_SIZE)
            if 0 <= z_fr < ROWS and 0 <= z_cc < COLS and world_map[z_fr][z_cc] not in [AIR, WATER, DIRT_WALL, STONE_WALL, DOOR_OPEN, GLASS_PANE]: z["y"] = z_fr * BLOCK_SIZE - player_h; z["vel_y"] = 0
            if pygame.Rect(player_x, player_y, player_w, player_h).colliderect(pygame.Rect(z["x"], z["y"], player_w, player_h)):
                if current_world_mode == MODE_SURVIVAL: player_hp -= 0.5
            z["x"] += zombie_speed if z["x"] < player_x else -zombie_speed

        if current_world_mode == MODE_SURVIVAL and player_hp <= 0:
            if custom_spawn_point: player_x, player_y = custom_spawn_point[0], custom_spawn_point[1]
            else: player_x, player_y = 300, 150
            vel_y = 0; player_hp = player_max_hp; current_dimension = DIMENSION_EARTH; world_map = earth_map; zombies.clear(); lunar_droids.clear(); lunar_lasers.clear()
    if current_game_state == STATE_PLAYING:
        start_col = max(0, int(camera_x // BLOCK_SIZE))
        end_col = min(COLS, int((camera_x + SCREEN_WIDTH) // BLOCK_SIZE) + 1)
        start_row = max(0, int(camera_y // BLOCK_SIZE))
        end_row = min(ROWS, int((camera_y + SCREEN_HEIGHT) // BLOCK_SIZE) + 1)

        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                if 0 <= row < ROWS and 0 <= col < COLS:
                    block = world_map[row][col]
                    rect = pygame.Rect(col * BLOCK_SIZE - camera_x, row * BLOCK_SIZE - camera_y, BLOCK_SIZE, BLOCK_SIZE)
                    if block in [AIR, WATER, TORCH, DOOR_OPEN, GLASS_PANE, WIND_TURBINE, LIGHTNING_ROD]:
                        if row > 24: screen.blit(BLOCK_TEXTURES[STONE_WALL], rect)
                        elif row > 15: screen.blit(BLOCK_TEXTURES[DIRT_WALL], rect)

        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                if 0 <= row < ROWS and 0 <= col < COLS:
                    block = world_map[row][col]
                    if block != AIR:
                        rect = pygame.Rect(col * BLOCK_SIZE - camera_x, row * BLOCK_SIZE - camera_y, BLOCK_SIZE, BLOCK_SIZE)
                        if block == LEVER and (row, col) in active_levers: screen.blit(LEVER_ACTIVE_TEXTURES[LEVER], rect)
                        elif block == GREENSTONE_WIRE and (row, col) in active_greenstone: screen.blit(GREENSTONE_ACTIVE_TEXTURES[GREENSTONE_WIRE], rect)
                        else: screen.blit(BLOCK_TEXTURES[block], rect)
                        
                        if block == TORCH:
                            fx, fy = rect.x + 20, rect.y + 14
                            fire_offset = int(math.sin(torch_anim_frame * 0.4) * 2)
                            pygame.draw.circle(screen, (255, 69, 0), (fx, fy - 4 + fire_offset), 5)
                            pygame.draw.circle(screen, (255, 215, 0), (fx, fy - 3 + fire_offset), 3)
                            
                        elif block == WIND_TURBINE:
                            tx, ty = rect.x + 20, rect.y + 20
                            rad = 18
                            ang_step = 2.094
                            for i in range(3):
                                cur_ang = math.radians(turbine_anim_frame) + i * ang_step
                                bx = tx + int(math.cos(cur_ang) * rad)
                                by = ty + int(math.sin(cur_ang) * rad)
                                pygame.draw.line(screen, (200, 200, 210), (tx, ty), (bx, by), 3)
                        
                        if block not in [WATER, DIRT_WALL, STONE_WALL, TORCH, DOOR_OPEN, GLASS_PANE]:
                            if row - 1 >= 0 and world_map[row - 1][col] != block: pygame.draw.line(screen, (0, 0, 0), rect.topleft, rect.topright, 1)
                            if row + 1 < ROWS and world_map[row + 1][col] != block: pygame.draw.line(screen, (0, 0, 0), rect.bottomleft, rect.bottomright, 1)
                            if col - 1 >= 0 and world_map[row][col - 1] != block: pygame.draw.line(screen, (0, 0, 0), rect.topleft, rect.bottomleft, 1)
                            if col + 1 < COLS and world_map[row][col + 1] != block: pygame.draw.line(screen, (0, 0, 0), rect.topright, rect.bottomright, 1)

        if current_dimension == DIMENSION_EARTH:
            for tree in spawned_trees: draw_organic_tree(tree)

        for arrow_obj in arrows: draw_live_arrow(arrow_obj["x"], arrow_obj["y"], arrow_obj["vx"])

        for p in boss_projectiles:
            p_screen_x, p_screen_y = p["x"] - camera_x, p["y"] - camera_y
            pygame.draw.circle(screen, (255, 69, 0), (int(p_screen_x), int(p_screen_y)), 8)
            pygame.draw.circle(screen, (255, 215, 0), (int(p_screen_x), int(p_screen_y)), 4)

        if current_dimension == DIMENSION_MOON:
            for d in lunar_droids: draw_lunar_droid(d["x"], d["y"])
            for l in lunar_lasers:
                l_scr_x, l_scr_y = l["x"] - camera_x, l["y"] - camera_y
                pygame.draw.circle(screen, (0, 240, 255), (int(l_scr_x), int(l_scr_y)), 5)
                pygame.draw.circle(screen, (255, 255, 255), (int(l_scr_x), int(l_scr_y)), 2)

        for cart in minecarts: draw_minecart(cart["x"], cart["y"])
        for z in zombies: draw_zombie(z["x"], z["y"])
        if boss_active: draw_boss(boss_x, boss_y)
        
        for leaf in falling_leaves:
            pygame.draw.rect(screen, (34, 115, 34) if is_raining else (46, 115, 46), (leaf["x"] - camera_x, leaf["y"] - camera_y, 4, 4))
            
        draw_player(player_x, player_y)
        
        if is_raining and current_dimension == DIMENSION_EARTH:
            for _ in range(6):
                rx = random.randint(0, SCREEN_WIDTH)
                ry = random.randint(0, SCREEN_HEIGHT)
                pygame.draw.line(screen, (100, 150, 255, 120), (rx, ry), (rx - 4, ry + 12), 1)

        if night_darkness > 0 or current_dimension == DIMENSION_MOON or (is_raining and current_dimension == DIMENSION_EARTH):
            base_darkness = night_darkness if current_dimension == DIMENSION_EARTH else 130
            if is_raining and current_dimension == DIMENSION_EARTH: base_darkness = max(base_darkness, 110)
            base_darkness = max(0, base_darkness - (lightning_flash * 15))
            
            if base_darkness > 0:
                light_mask = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                light_mask.fill((10, 10, 25, base_darkness))
                for row in range(start_row, end_row):
                    for col in range(start_col, end_col):
                        if 0 <= row < ROWS and 0 <= col < COLS and world_map[row][col] == TORCH:
                            ts_x = (col * BLOCK_SIZE + BLOCK_SIZE // 2) - camera_x
                            ts_y = (row * BLOCK_SIZE + BLOCK_SIZE // 2) - camera_y
                            for radius in range(160, 0, -20):
                                current_alpha = max(0, base_darkness - int(base_darkness * (1 - radius / 160)))
                                pygame.draw.circle(light_mask, (10, 10, 25, current_alpha), (ts_x, ts_y), radius)
                screen.blit(light_mask, (0, 0))
        pygame.draw.rect(screen, (0, 0, 0), (10, 10, 120, 50), 2)
        text = inventory_font.render("In Hand:", True, (0, 0, 0))
        screen.blit(text, (15, 25))
        if current_hand == PICKAXE: draw_pickaxe(75, 15)
        else:
            screen.blit(BLOCK_TEXTURES[current_hand], (80, 15))
            pygame.draw.rect(screen, (0, 0, 0), (80, 15, 35, 35), 1)

        pygame.draw.rect(screen, (0, 0, 0), (140, 10, 150, 20), 2)
        fuel_w = int(146 * (jetpack_fuel / 100.0))
        if fuel_w > 0: pygame.draw.rect(screen, (0, 200, 255), (142, 12, fuel_w, 16))
        fuel_text = inventory_font.render(f"Fuel: {int(jetpack_fuel)}%", True, (0, 0, 0))
        screen.blit(fuel_text, (145, 12))

        if current_world_mode == MODE_SURVIVAL:
            num_hearts = 5
            hp_per_heart = 20
            for i in range(num_hearts):
                hx = 15 + i * 22
                hy = 68
                if player_hp >= (i + 1) * hp_per_heart:
                    pygame.draw.polygon(screen, (220, 20, 60), [(hx+8, hy+14), (hx, hy+6), (hx+4, hy), (hx+8, hy+4), (hx+12, hy), (hx+16, hy+6)])
                elif player_hp > i * hp_per_heart:
                    pygame.draw.polygon(screen, (150, 10, 40), [(hx+8, hy+14), (hx, hy+6), (hx+4, hy), (hx+8, hy+4), (hx+12, hy), (hx+16, hy+6)])
                    pygame.draw.polygon(screen, (220, 20, 60), [(hx+8, hy+14), (hx, hy+6), (hx+4, hy), (hx+4, hy+4), (hx+8, hy+4)])
                else:
                    pygame.draw.polygon(screen, (60, 60, 60), [(hx+8, hy+14), (hx, hy+6), (hx+4, hy), (hx+8, hy+4), (hx+12, hy), (hx+16, hy+6)])
                pygame.draw.polygon(screen, (0, 0, 0), [(hx+8, hy+14), (hx, hy+6), (hx+4, hy), (hx+8, hy+4), (hx+12, hy), (hx+16, hy+6)], 1)

        if boss_active:
            pygame.draw.rect(screen, (0, 0, 0), (SCREEN_WIDTH // 2 - 200, 15, 400, 25), 3)
            pygame.draw.rect(screen, (60, 0, 100), (SCREEN_WIDTH // 2 - 197, 18, 394, 19))
            boss_bar_w = int(394 * (boss_hp / boss_max_hp))
            if boss_bar_w > 0: pygame.draw.rect(screen, (160, 0, 255), (SCREEN_WIDTH // 2 - 197, 18, boss_bar_w, 19))
            screen.blit(inventory_font.render("ANCIENT UNDERGROUND GUARDIAN", True, (255, 255, 255)), (SCREEN_WIDTH // 2 - 120, 19))

        if show_inventory and not show_pause_menu and not show_chest and current_world_mode == MODE_CREATIVE:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); overlay.set_alpha(150); overlay.fill((0, 0, 0)); screen.blit(overlay, (0, 0))
            inv_w, inv_h = 380, 420; inv_x = SCREEN_WIDTH // 2 - inv_w // 2; inv_y = SCREEN_HEIGHT // 2 - inv_h // 2
            pygame.draw.rect(screen, (220, 220, 220), (inv_x, inv_y, inv_w, inv_h))
            pygame.draw.rect(screen, (50, 50, 50), (inv_x, inv_y, inv_w, inv_h), 3)
            screen.blit(inventory_font.render("Creative Menu (I)", True, (0, 0, 0)), (inv_x + 20, inv_y + 15))
            for idx, item in enumerate(creative_items):
                row_idx, col_idx = idx // 8, idx % 8
                slot_rect = pygame.Rect(inv_x + 20 + col_idx * 43, inv_y + 50 + row_idx * 43, 38, 38)
                if slot_rect.collidepoint(pygame.mouse.get_pos()): pygame.draw.rect(screen, (255, 255, 150), slot_rect)
                else: pygame.draw.rect(screen, (190, 190, 190), slot_rect)
                pygame.draw.rect(screen, (0, 0, 0), slot_rect, 1)
                if item == PICKAXE: draw_pickaxe(inv_x + 23 + col_idx * 43, inv_y + 52 + row_idx * 43)
                else:
                    scaled_tex = pygame.transform.scale(BLOCK_TEXTURES[item], (32, 32))
                    screen.blit(scaled_tex, (inv_x + 23 + col_idx * 43, inv_y + 53 + row_idx * 43))

    elif current_game_state == STATE_MAIN_MENU:
        screen.fill((15, 15, 30))
        for star in stars: pygame.draw.circle(screen, (240, 240, 255), (star["x"], star["y"]), star["size"])
        for cloud in clouds: pygame.draw.ellipse(screen, (40, 45, 70), (cloud["x"] % SCREEN_WIDTH, cloud["y"] + 150, cloud["width"], 25))
        logo = title_font.render("AstroBlocks", True, (0, 230, 255))
        screen.blit(logo, (SCREEN_WIDTH // 2 - logo.get_width() // 2, SCREEN_HEIGHT // 3 - 40))
        btn_play = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
        pygame.draw.rect(screen, (50, 50, 70), btn_play); pygame.draw.rect(screen, (255, 255, 255), btn_play, 2)
        txt_play = menu_font.render("PLAY", True, (255, 255, 255))
        screen.blit(txt_play, (SCREEN_WIDTH // 2 - txt_play.get_width() // 2, SCREEN_HEIGHT // 2 + 10))

    elif current_game_state == STATE_WORLD_SELECT:
        screen.fill((20, 20, 40))
        for star in stars: pygame.draw.circle(screen, (200, 200, 220), (star["x"], star["y"]), star["size"])
        title_sel = menu_font.render("SELECT WORLD SLOT", True, (255, 255, 255))
        screen.blit(title_sel, (SCREEN_WIDTH // 2 - title_sel.get_width() // 2, 40))
        btn_mode_toggle = pygame.Rect(SCREEN_WIDTH // 2 - 150, 100, 300, 40)
        pygame.draw.rect(screen, (60, 60, 90), btn_mode_toggle); pygame.draw.rect(screen, (255, 255, 255), btn_mode_toggle, 2)
        mode_str = "NEW WORLD MODE: SURVIVAL" if selected_creation_mode == MODE_SURVIVAL else "NEW WORLD MODE: CREATIVE"
        txt_mode = inventory_font.render(mode_str, True, (255, 255, 100) if selected_creation_mode == MODE_SURVIVAL else (100, 255, 255))
        screen.blit(txt_mode, (SCREEN_WIDTH // 2 - txt_mode.get_width() // 2, 112))
        for slot in range(1, 4):
            slot_y = SCREEN_HEIGHT // 2 - 80 + slot * 60
            btn_slot = pygame.Rect(SCREEN_WIDTH // 2 - 150, slot_y, 300, 45)
            has_save = os.path.exists(f"astroblocks_world_{slot}.txt")
            btn_color = (40, 90, 50) if has_save else (70, 70, 80)
            pygame.draw.rect(screen, btn_color, btn_slot); pygame.draw.rect(screen, (255, 255, 255), btn_slot, 2)
            status_text = f"World Slot {slot} (LOAD)" if has_save else f"World Slot {slot} (GENERATE NEW)"
            txt_slot = inventory_font.render(status_text, True, (255, 255, 255))
            screen.blit(txt_slot, (SCREEN_WIDTH // 2 - txt_slot.get_width() // 2, slot_y + 12))
        btn_back = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT - 70, 150, 40)
        pygame.draw.rect(screen, (120, 40, 40), btn_back); pygame.draw.rect(screen, (255, 255, 255), btn_back, 2)
        txt_back = inventory_font.render("BACK", True, (255, 255, 255))
        screen.blit(txt_back, (SCREEN_WIDTH // 2 - txt_back.get_width() // 2, SCREEN_HEIGHT - 60))
    if current_game_state == STATE_PLAYING:
        if show_chest and not show_pause_menu:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); overlay.set_alpha(150); overlay.fill((0, 0, 0)); screen.blit(overlay, (0, 0))
            inv_w, inv_h = 360, 230; inv_x = SCREEN_WIDTH // 2 - inv_w // 2; inv_y = SCREEN_HEIGHT // 2 - inv_h // 2
            pygame.draw.rect(screen, (220, 220, 220), (inv_x, inv_y, inv_w, inv_h))
            pygame.draw.rect(screen, (50, 50, 50), (inv_x, inv_y, inv_w, inv_h), 3)
            screen.blit(inventory_font.render("Chest Storage (Right-click outside to close)", True, (0, 0, 0)), (inv_x + 20, inv_y + 15))
            for idx in range(18):
                row_idx, col_idx = idx // 6, idx % 6
                slot_rect = pygame.Rect(inv_x + 20 + col_idx * 55, inv_y + 50 + row_idx * 55, 45, 45)
                if slot_rect.collidepoint(pygame.mouse.get_pos()): pygame.draw.rect(screen, (255, 255, 150), slot_rect)
                else: pygame.draw.rect(screen, (190, 190, 190), slot_rect)
                pygame.draw.rect(screen, (0, 0, 0), slot_rect, 1)
                item = chest_inventory[idx]
                if item != AIR:
                    if item == PICKAXE: draw_pickaxe(inv_x + 27 + col_idx * 55, inv_y + 55 + row_idx * 55)
                    else:
                        screen.blit(BLOCK_TEXTURES[item], (inv_x + 22 + col_idx * 55, inv_y + 52 + row_idx * 55))
                        pygame.draw.rect(screen, (0, 0, 0), (inv_x + 22 + col_idx * 55, inv_y + 52 + row_idx * 55, 35, 35), 1)

        if show_pause_menu:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); overlay.set_alpha(200); overlay.fill((20, 20, 30)); screen.blit(overlay, (0, 0))
            mid_x, mid_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
            screen.blit(inventory_font.render("GAME PAUSED", True, (255, 255, 255)), (mid_x - 50, mid_y - 110))
            for b_y, b_text, b_col in [(-60, "Resume Game", (80,80,90)), (-10, "Difficulty: HARD" if current_difficulty == DIFFICULTY_HARD else "Difficulty: EASY", (80,80,90)), (40, "Exit Game", (150,50,50))]:
                btn = pygame.Rect(mid_x - 100, mid_y + b_y, 200, 40)
                pygame.draw.rect(screen, b_col, btn); pygame.draw.rect(screen, (255, 255, 255), btn, 2)
                screen.blit(inventory_font.render(b_text, True, (255, 255, 255)), (mid_x - 45, mid_y + b_y + 10))

    pygame.display.flip()
