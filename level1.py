import pygame  # type: ignore
import random
import sys
import time
import world_select
import json
from NPCs.level_1_npc_1 import handle_level_1_npc_1_dialogue  # Import the functionality of the first NPC from level 1
from NPCs.level_1_npc_2 import handle_level_1_npc_2_dialogue  # Import the functionality of the second NPC from level 1
from NPCs.level_1_npc_3 import handle_level_1_npc_3_dialogue  # Import the functionality of the third NPC from level 1

# Initialize Pygame
pygame.init()
pygame.mixer.init() # Initialize Pygame Audio Mixer

# Load the level complete sound 
level_complete_sound = pygame.mixer.Sound("Audio/LevelComplete.mp3")
# pygame.mixer.music.set_volume(1.0)  # start at 100% volume 

# Gadget pick up sound 
gadget_sound = pygame.mixer.Sound("Audio/GadgetPickUp.mp3")

# Death sound 
death_sound = pygame.mixer.Sound("Audio/Death.mp3")

# Screen Resolution 
BASE_WIDTH = 1920
BASE_HEIGHT = 1080
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h 
TILE_SIZE = 40 
scale_factor = HEIGHT / BASE_HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Level One")

# --------------------------
# Tiles and Ground Elements
# --------------------------
ground_tile = pygame.image.load("./images/ground.png")
ground_tile = pygame.transform.scale(ground_tile, (TILE_SIZE, TILE_SIZE))

platform_tile = pygame.image.load("./images/platform.png")
platform_tile = pygame.transform.scale(platform_tile, (TILE_SIZE * 1.1, TILE_SIZE * 1.1))
flipped_platform_tile = pygame.transform.flip(platform_tile, False, True)

dirt_tile = pygame.image.load("./images/dirt.png")
dirt_tile = pygame.transform.scale(dirt_tile, (TILE_SIZE, TILE_SIZE))

# --------------------------
# Background and Environment
# --------------------------
background = pygame.image.load("./images/background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT)) 

tree = pygame.image.load("./images/tree.png")
tree = pygame.transform.scale(tree, (TILE_SIZE * 2, TILE_SIZE * 3))  

background_tree = pygame.image.load("./images/background_tree.png")
background_tree = pygame.transform.scale(background_tree, (TILE_SIZE * 1.5, TILE_SIZE * 2))

house = pygame.image.load("./images/house.png")
house = pygame.transform.scale(house, (TILE_SIZE * 5, TILE_SIZE * 3))

mushroom = pygame.image.load ("./images/mushroom.png")
mushroom = pygame.transform.scale(mushroom, (TILE_SIZE * 6, TILE_SIZE * 6))

walkway = pygame.image.load("./images/walkway.png")
walkway = pygame.transform.scale(walkway, (TILE_SIZE * 3.0, TILE_SIZE * 2.2))

flipped_walkway = pygame.transform.flip(walkway, True, False)  # Flip horizontally (True), no vertical flip (False)
flipped_walkway = pygame.transform.scale(flipped_walkway, (TILE_SIZE * 3.0, TILE_SIZE * 2.2))

water = pygame.image.load("./images/water.png")
water = pygame.transform.scale(water, (TILE_SIZE, TILE_SIZE))

windmill = pygame.image.load("./images/windmill.png")
windmill = pygame.transform.scale(windmill, (TILE_SIZE * 5, TILE_SIZE * 6))

jump_reset = pygame.image.load("./images/bubble.png")
jump_reset = pygame.transform.scale(jump_reset, (TILE_SIZE, TILE_SIZE))

spring = pygame.image.load("./images/spring.png")
spring= pygame.transform.scale(spring, (TILE_SIZE, TILE_SIZE))

invisible_platform = None

floating_ground = ground_tile

ice_tile = pygame.image.load("./images/ice.png")
ice_tile = pygame.transform.scale(ice_tile, (TILE_SIZE, TILE_SIZE))
flipped_ice = pygame.transform.flip(ice_tile, False, True)

windmill = pygame.image.load("./images/windmill.png")
windmill = pygame.transform.scale(windmill, (TILE_SIZE * 5, TILE_SIZE * 6))

# --------------------------
# Items and Power-ups
# --------------------------
boots = pygame.image.load("./images/boots.png")
boots = pygame.transform.scale(boots, (TILE_SIZE, TILE_SIZE))

speed_boots = pygame.image.load("./images/speed_boots.png")
speed_boots = pygame.transform.scale(speed_boots, (TILE_SIZE, TILE_SIZE))

super_speed_powerup = pygame.image.load("./images/super_speed_powerup.png")
super_speed_powerup = pygame.transform.scale(super_speed_powerup, (TILE_SIZE, TILE_SIZE))

dash_powerup = pygame.image.load("./images/dash_powerup.png")
dash_powerup = pygame.transform.scale(dash_powerup, (TILE_SIZE, TILE_SIZE))

coin = pygame.image.load("./images/coin.png")
coin = pygame.transform.scale(coin, (TILE_SIZE, TILE_SIZE))

# --------------------------
# Obstacles and Decorations
# --------------------------
thorn = pygame.image.load("./images/thorn.png")
thorn = pygame.transform.scale(thorn, (TILE_SIZE, TILE_SIZE))
flipped_thorn = pygame.transform.flip(thorn, False, True)
thorn_rotated = pygame.transform.rotate(thorn, 180)
thorn_left = pygame.transform.rotate(thorn, 90)
thorn_right = pygame.transform.rotate(thorn, -90)

flag = pygame.image.load("./images/flag.png")
flag = pygame.transform.scale(flag, (TILE_SIZE, TILE_SIZE))

fence = pygame.image.load("./images/fence.png")
fence = pygame.transform.scale(fence, (TILE_SIZE, TILE_SIZE // 2))

sign = pygame.image.load("./images/sign.png")
sign = pygame.transform.scale(sign, (TILE_SIZE, TILE_SIZE))

rock = pygame.image.load("./images/rock.png")
rock = pygame.transform.scale(rock, (TILE_SIZE, TILE_SIZE // 2))

# --------------------------
# NPC Characters
# --------------------------
npc_1 = pygame.image.load("./Character Combinations/black hair_dark_blue shirt_black pants.png")
npc_1 = pygame.transform.scale(npc_1, (TILE_SIZE, TILE_SIZE))
flipped_npc_1 = pygame.transform.flip(npc_1, True, False)  

npc_2 = pygame.image.load("./Character Combinations/brown hair_white_blue shirt_blue pants.png")
npc_2 = pygame.transform.scale(npc_2, (TILE_SIZE, TILE_SIZE))
flipped_npc_2 = pygame.transform.flip(npc_2, True, False)  

npc_3 = pygame.image.load("./Character Combinations/ginger hair_white_blue shirt_black pants.png")
npc_3 = pygame.transform.scale(npc_3, (TILE_SIZE, TILE_SIZE))
flipped_npc_3 = pygame.transform.flip(npc_3, True, False)  

npc_4 = pygame.image.load("./Character Combinations/black hair_dark_blue shirt_brown pants.png")
npc_4 = pygame.transform.scale(npc_4, (TILE_SIZE, TILE_SIZE))
flipped_npc_4 = pygame.transform.flip(npc_4, True, False)  

# -------------------------------
# Level Setup and Constants
# -------------------------------
level_width = 140
level_height = HEIGHT // TILE_SIZE  

level_map = [[0] * level_width for _ in range(level_height)]  

GROUND = level_height - 4 
SURFACE = GROUND - 1 

# -------------------------------
# Snowflake Animation Setup
# -------------------------------
WHITE = (255, 255, 255)
NUM_SNOWFLAKES = 100
snowflakes = []

for _ in range(NUM_SNOWFLAKES):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    size = random.randint(2, 6)  
    speed = random.uniform(1, 6)  
    x_speed = random.uniform(-0.5, 0.5)  
    snowflakes.append([x, y, size, speed, x_speed])

# -------------------------------
# Terrain Generation
# -------------------------------
# Add solid ground at the very bottom
level_map.append([1] * level_width)

for row_index in range(SURFACE - 8, SURFACE):
    for col in range(0, 5):
        level_map[row_index][col] = 1

for row_index in range(SURFACE - 8, SURFACE):
    for col in range(9, 21):
        level_map[row_index][col] = 1

for col in range(25, level_width):
    step_down = (col - 25) // 3
    ground_start = min((SURFACE - 6) + step_down, GROUND)
    for row_index in range(ground_start, level_height):
        level_map[row_index][col] = 1


for col in range(40, 60):
    for row in range(level_height):
        level_map[row][col] = 0


for row_index in range(SURFACE - 2, SURFACE):
    for col in range(60, 70):
        level_map[row_index][col] = 1

for col in range(70, 80):
    for row in range(level_height):
        level_map[row][col] = 0

for row_index in range(SURFACE - 12, SURFACE):
    for col in range(80, 85):
        level_map[row_index][col] = 1

for col in range(85, 120):
    for row in range(level_height):
        level_map[row][col] = 0

for col in range(120, 140):
    for row in range(level_height):
        level_map[row][col] = 0

for row_index in range(0, SURFACE - 4):
     level_map[row_index][120:130] = [27] * 14

for row_index in range(SURFACE - 1, SURFACE):
    for col in range(120, 134):
        level_map[row_index][col] = 28

for col in range(134, level_width):
    level_map[SURFACE][col] = 28




# -------------------------------
# Ground Level Calculation
# -------------------------------
ground_levels = [len(level_map)] * len(level_map[0])
for row_index, row in enumerate(level_map):
    for col_index, tile in enumerate(row):
        if tile == 1 and ground_levels[col_index] == len(level_map):
            ground_levels[col_index] = row_index

# -------------------------------------
# Props, NPCs, and Power-ups Setup
# (Terrain should not be created here)
# -------------------------------------
tiles = {
    1: ground_tile,
    2: platform_tile,
    3: boots,
    4: flipped_npc_1,
    5: house,
    6: thorn,
    7: flag,
    8: super_speed_powerup,
    9: dash_powerup,
    10: fence,
    11: sign,
    12: npc_1,
    13: speed_boots,
    14: coin,
    15: npc_2,
    16: npc_3,
    17: flipped_npc_2,
    18: flipped_npc_3,
    19: npc_4,
    20: flipped_npc_4,
    21: mushroom,
    22: walkway,
    23: flipped_walkway,
    24: dirt_tile,
    25: water,
    26: invisible_platform,
    27: dirt_tile,
    28: ice_tile,
    29: flipped_ice,
    30: windmill,
    31: spring,
    32: floating_ground,
    33: flipped_thorn,
    34: flipped_platform_tile,
    35: thorn_rotated,
    36: thorn_left,
    37: thorn_right,
    38: jump_reset
}

deadly_tiles = {6, 25, 33, 35, 36, 37}

# -----------------------------------
# Special Objects and NPC Placement
# -----------------------------------
# Thorns placement
# level_map[SURFACE][98:104], level_map[SURFACE][113:115] = [6] * 6, [6] * 2 

# Flag placement
# level_map[SURFACE-5][37], level_map[SURFACE][87] = 7, 7 

# Power ups placement
# level_map[SURFACE][0] = 8 
# level_map[SURFACE-2][113] = 9 
level_map[SURFACE - 3][39] = 3  # Jump Boots (moved to show at the beginning temporarily)
#level_map[SURFACE - 7][26] = 8  # Super Speed Powerup (moved to show at the beginning temporarily)
level_map[SURFACE-8][76] = 38 # Jump Reset

# Fences and sign placement
# level_map[SURFACE-6][122:124] = [10] * 2 
# level_map[SURFACE-7][135:140] = [10] * 5 
# level_map[SURFACE-7][130] = 11 

# Wooden house placement
level_map[SURFACE - 9][9] = 6 # Thorn 
level_map[SURFACE - 11][10] = 5 # Wooden House

# Mushroom house placement 
level_map[SURFACE - 14][14] = 21 # Mushroom House
level_map[SURFACE - 9][20] = 6 # Thorn 

# Sign placement
level_map[SURFACE - 9][1] = 11 # Wooden House

# Walkway placement
level_map[SURFACE - 3][40] = 22 # Walkway Bridge
level_map[SURFACE - 2][40:44] = [26] * 4

level_map[SURFACE - 3][70] = 22
level_map[SURFACE - 2][70:74] = [26] * 4

# Flipped placement 
level_map[SURFACE - 3][57] = 23 # Flipped Walkway Bridge
level_map[SURFACE - 2][56:60] = [26] * 4 

# Thorns placement 
# level_map[SURFACE - 7][25] = 6 # Removed Spikes 
level_map[SURFACE - 6][28] = 6
level_map[SURFACE - 5][31] = 6
level_map[SURFACE - 4][34] = 6
level_map[SURFACE - 3][37] = 6

# level_map[SURFACE - 3][60] = 6
level_map[SURFACE - 3][61] = 6 # Thorns
level_map[SURFACE - 3][62] = 6
level_map[SURFACE - 3][63] = 6
level_map[SURFACE - 3][64] = 6
level_map[SURFACE - 3][65] = 6
level_map[SURFACE - 3][66] = 6
level_map[SURFACE - 3][67] = 6
level_map[SURFACE - 3][68] = 6
# level_map[SURFACE - 3][69] = 6
# level_map[SURFACE - 3][70] = 6

# Water placement
level_map[level_height-1][40:60] = [25] * 20 # Water
level_map[level_height-1][70:200] = [25] * 80 # Water


# Windmill placement
level_map[SURFACE - 18][80] = 30 # Windmill
level_map[SURFACE - 1][79] = 36 # Thorns on left side of Windmill terrain
level_map[SURFACE - 2][79] = 36
level_map[SURFACE - 3][79] = 36
level_map[SURFACE - 4][79] = 36
level_map[SURFACE - 5][79] = 36
level_map[SURFACE - 6][79] = 36
level_map[SURFACE - 7][79] = 36 
level_map[SURFACE - 8][79] = 36
level_map[SURFACE - 9][79] = 36
level_map[SURFACE - 10][79] = 36
level_map[SURFACE - 11][79] = 36
level_map[SURFACE - 12][79] = 36

level_map[SURFACE - 1][85] = 37 # Thorns on right side of Windmill terrain
level_map[SURFACE - 2][85] = 37
level_map[SURFACE - 3][85] = 37
level_map[SURFACE - 4][85] = 37
level_map[SURFACE - 5][85] = 37
level_map[SURFACE - 6][85] = 37
level_map[SURFACE - 7][85] = 37 
level_map[SURFACE - 8][85] = 37
level_map[SURFACE - 9][85] = 37
level_map[SURFACE - 10][85] = 37
level_map[SURFACE - 11][85] = 37
level_map[SURFACE - 12][85] = 37


level_map[SURFACE - 23][119] = 36
level_map[SURFACE - 22][119] = 36
level_map[SURFACE - 21][119] = 36
level_map[SURFACE - 20][119] = 36
level_map[SURFACE - 19][119] = 36
level_map[SURFACE - 18][119] = 36
level_map[SURFACE - 17][119] = 36
level_map[SURFACE - 16][119] = 36
level_map[SURFACE - 15][119] = 36
level_map[SURFACE - 14][119] = 36
level_map[SURFACE - 13][119] = 36
level_map[SURFACE - 12][119] = 36
level_map[SURFACE - 11][119] = 36
level_map[SURFACE - 10][119] = 36
level_map[SURFACE - 9][119] = 36
level_map[SURFACE - 8][119] = 36
level_map[SURFACE - 7][119] = 36
level_map[SURFACE - 6][119] = 36
level_map[SURFACE - 6][119] = 36

# Platform & Thorn placement 
level_map[SURFACE - 18][90] = 34 # Flipped Platform
level_map[SURFACE - 17][90] = 33 # Flipped Thorn on platform
level_map[SURFACE - 12][90] = 2 # Platform
level_map[SURFACE - 8][90] = 2 # Platform
level_map[SURFACE - 9][90] = 6 # Thorn on platform

level_map[SURFACE - 8][95] = 2 # Platform
level_map[SURFACE - 9][95] = 6 # Thorn on platform
level_map[SURFACE - 18][95] = 34 # Flipped Platform
level_map[SURFACE - 17][95] = 33 # Flipped Thorn on platform


level_map[SURFACE - 18][100] = 34 # Flipped Platform
level_map[SURFACE - 17][100] = 33 # Flipped Thorn on platform
level_map[SURFACE - 12][100] = 2 # Platform
level_map[SURFACE - 8][100] = 2 # Platform
level_map[SURFACE - 9][100] = 6 # Thorn on platform


level_map[SURFACE - 8][105] = 2 # Platform
level_map[SURFACE - 9][105] = 6 # Thorn on platform
level_map[SURFACE - 18][105] = 34 # Flipped Platform
level_map[SURFACE - 17][105] = 33 # Flipped Thorn on platform
level_map[SURFACE - 8][105] = 2 # Platform
level_map[SURFACE - 9][105] = 6 # Thorn on platform


level_map[SURFACE - 18][110] = 34 # Flipped Platform
level_map[SURFACE - 17][110] = 33 # Flipped Thorn on platform
level_map[SURFACE - 12][110] = 2 # Platform
level_map[SURFACE - 8][110] = 2 # Platform
level_map[SURFACE - 9][110] = 6 # Thorn on platform

# NPCs Placement
level_map[SURFACE - 9][12] = 12 # First NPC
level_map[SURFACE - 9][18] = 15 # Second NPC
level_map[SURFACE - 3][58] = 16 # Third NPC

rocks = {}           
trees = {}                     
background_trees = {}     

# --------------------------------------------
# Helper Functions for Coordinate Conversion
# --------------------------------------------
def calculate_column(x): 
    return int(x // TILE_SIZE)

def calculate_x_coordinate(column):
    return int(column * TILE_SIZE)

def calculate_row(y):
    return int(y // TILE_SIZE)

def calculate_y_coordinate(row):
    return int(row * TILE_SIZE)


def show_level_completed_screen(slot: int):

    # Stop tutorial music
    pygame.mixer.music.stop()

    # Play the level complete sound once when this function runs
    level_complete_sound.play()

    screen.blit(background, (0, 0))
    level_map[SURFACE][28] = 3  # Respawn double jump boots
    level_map[SURFACE-5][55] = 13  # Respawn speed boots
    level_map[SURFACE-1][68] = 0   # Despawn coin
    level_map[SURFACE-2][79:81] = [0] * 2  # Despawn platforms after getting coin

    title_font = pygame.font.Font('PixelifySans.ttf', 100)
    menu_font = pygame.font.Font('PixelifySans.ttf', 60)
    level_completed_text = title_font.render("Level Completed", True, (255, 255, 255))
    select_level_text = menu_font.render("Back to Select Level", True, (255, 255, 255))

    level_completed_rect = level_completed_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    select_level_rect = select_level_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 120))
    box_padding = 20
    level_end_screen_box = pygame.Rect(level_completed_rect.left - box_padding, level_completed_rect.top - box_padding, level_completed_rect.width + box_padding*2, level_completed_rect.height + (box_padding*2) + 80)
    pygame.draw.rect(screen, (0, 0, 255), level_end_screen_box, 10)
    
    screen.blit(level_completed_text, level_completed_rect)
    screen.blit(select_level_text, select_level_rect)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    waiting = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if select_level_rect.collidepoint(mouse_x, mouse_y):
                    world_select.World_Selector(slot)
                    sys.exit()



def read_data(slot: int):
    with open(f"./User Saves/save{str(slot)}.json", "r") as file:
        data = json.load(file)
    return data.get("character")

# -----------------------------------
# Level One Game Loop
# -----------------------------------
def level_1(slot: int):

    # Stop any previously playing music 
    pygame.mixer.music.stop()
    
    # Load the tutorial music
    pygame.mixer.music.load("Audio/Level1.mp3")
    pygame.mixer.music.play(-1)  # -1 loops forever

    level_map[SURFACE - 3][39] = 3   # Jump Boots

    # Grab the sprite that was customized
    sprite = read_data(slot)

    # Load all the images into their respective variables
    player = pygame.image.load(f"./Assets/Character Sprites/standing/{sprite}")
    player = pygame.transform.scale(player, (TILE_SIZE, TILE_SIZE))
    flipped_player = pygame.transform.flip(player, True, False)

    run = pygame.image.load(f"./Assets/Character Sprites/running/{sprite}")
    run = pygame.transform.scale(run, (TILE_SIZE, TILE_SIZE))
    flipped_run = pygame.transform.flip(run, True, False)

    run_frames = [
        pygame.image.load(f"./Assets/Character Sprites/walking/{sprite}"),
        pygame.image.load(f"./Assets/Character Sprites/running/{sprite}")
    ]

    run_frames = [pygame.transform.scale(frame, (TILE_SIZE, TILE_SIZE)) for frame in run_frames]

    # Camera position
    camera_x = 0
    player_x = 150  # Start position, change this number to spawn in a different place
    player_y = HEIGHT - 560
    player_speed = 6.5 * scale_factor # Adjust player speed according to their resolution

    player_vel_y = 0 # Vertical velocity for jumping
    gravity = 1.0 / scale_factor # Gravity effect (Greater number means stronger gravity)
    jump_power = -21 / scale_factor # Jump strength (Bigger negative number means higher jump)
    on_ground = False # Track if player is on the ground
    doubleJumpBoots = False # Track if player has double jump boots
    doubleJumped = False # Track if player double jumped already
    speedBoots = False

    animation_index = 0  # Alternates between 0 and 1
    animation_timer = 0  # Tracks when to switch frames
    animation_speed = 4  # Adjust this to control animation speed
    direction = 1  # 1 for right, -1 for left

    super_speed_bool = False
    super_speed_respawn_time = 0
    super_speed_pickup_time = 0
    super_speed_effect_off_time = 0

    dash_respawn_time = 0 
    dash_pickup_time = 0
    dash_duration = 0
    dashing = False

    checkpoints = [(150, HEIGHT-600)]
    checkpoint_bool = [True]
    checkpoint_idx = 0
    dying = False
    death_count = 0
    coin_count = 0
    collidable_tiles = {1, 2, 32, 26, 27, 28, 29, 31}

    # State Variables for Gadgets
    bubbleJump = False
    bubbleJump_respawns = {}

    running = True
    while running:
        screen.blit(background, (0, 0))

        level_name_font = pygame.font.Font('PixelifySans.ttf', 48)  # Larger font for level name
        level_name_text = level_name_font.render("Level 1", True, (255, 255, 255))  # White text

        screen.blit(level_name_text, (20, 20))  # Position at (20, 20)
        # Draw level using tile images
        for row_index, row in enumerate(level_map):
            for col_index, tile in enumerate(row):
                x, y = col_index * TILE_SIZE - camera_x, row_index * TILE_SIZE
                if tile == 0 or tile == 26: # Continue if the tile is an air block or invisible platform
                    continue
                else: # Draw according to the dictionary
                    screen.blit(tiles.get(tile), (x, y))

        # Draw dirt below ground
        for col_index, ground_y in enumerate(ground_levels):
            for row_index in range(ground_y + 1, len(level_map) + 10):  # Extra depth
                x, y = col_index * TILE_SIZE - camera_x, row_index * TILE_SIZE
                screen.blit(dirt_tile, (x, y))  # Draw dirt using image

        for i in trees:  # Adding trees
            x = i * TILE_SIZE - camera_x
            y = (ground_levels[i] - 3) * TILE_SIZE  # Place tree 3 tiles above the ground
            screen.blit(tree, (x, y))

        for i in background_trees:  # Adding background trees
            x = i * TILE_SIZE - camera_x
            y = (ground_levels[i] - 2) * TILE_SIZE  # Place background trees 2 tiles above the ground
            screen.blit(background_tree, (x, y))

        for i in rocks:  # Adding rocks
            x = i * TILE_SIZE - camera_x
            y = (ground_levels[i] - 1) * TILE_SIZE  # Place rocks 1 tile above the ground
            screen.blit(rock, (x, y + TILE_SIZE // 2))

        for i, snowflake in enumerate(snowflakes):
            x, y, size, speed, x_speed = snowflake  # Unpack snowflake data
            
            # Move snowflake downward and drift sideways
            y += speed  
            x += x_speed  # Drift slightly left/right
            
            # Reset snowflake when it reaches the bottom or moves too far left/right
            if y > HEIGHT:
                y = 0
                x = random.randint(0, WIDTH)  # Respawn at a new x position
            if x < 0 or x > WIDTH:  # Keep it within screen bounds
                x = random.randint(0, WIDTH)

            # Update snowflake position in the list
            snowflakes[i] = [x, y, size, speed, x_speed]

            # Draw snowflake
            pygame.draw.circle(screen, WHITE, (int(x), int(y)), size)
        
        # Check if player is near the first NPC
        npc_x = calculate_x_coordinate(12)  # First NPC's x position
        npc_y = (SURFACE - 9) * TILE_SIZE  # First NPC's y position
        player_rect = pygame.Rect(player_x - camera_x, player_y, TILE_SIZE, TILE_SIZE)
        npc_rect = pygame.Rect(npc_x - camera_x, npc_y, TILE_SIZE, TILE_SIZE)

        # Handle first NPC dialogue
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()  # Get current time in milliseconds
        handle_level_1_npc_1_dialogue(screen, player_rect, npc_rect, keys, current_time)

        # Check if player is near the second NPC
        npc_x = calculate_x_coordinate(18)  # Second NPC's x position
        npc_y = (SURFACE - 9) * TILE_SIZE  # Second NPC's y position
        player_rect = pygame.Rect(player_x - camera_x, player_y, TILE_SIZE, TILE_SIZE)
        npc_rect = pygame.Rect(npc_x - camera_x, npc_y, TILE_SIZE, TILE_SIZE)

        # Handle second NPC dialogue
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()  # Get current time in milliseconds
        handle_level_1_npc_2_dialogue(screen, player_rect, npc_rect, keys, current_time)

        # Check if player is near the third NPC
        npc_x = calculate_x_coordinate(58)  # Third NPC's x position
        npc_y = (SURFACE - 3) * TILE_SIZE  # Third NPC's y position
        player_rect = pygame.Rect(player_x - camera_x, player_y, TILE_SIZE, TILE_SIZE)
        npc_rect = pygame.Rect(npc_x - camera_x, npc_y, TILE_SIZE, TILE_SIZE)

        # Handle NPC 3 dialogue
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()  # Get current time in milliseconds
        handle_level_1_npc_3_dialogue(screen, player_rect, npc_rect, keys, current_time)

        # Handle events
        keys = pygame.key.get_pressed()
        moving = False
        if keys[pygame.K_d]: # If player presses D
            player_x += player_speed
            moving = True
            direction = 1
        if keys[pygame.K_a]: # If player presses A
            player_x -= player_speed        
            moving = True
            direction = -1
        if keys[pygame.K_SPACE] and on_ground: # If player presses Spacebar
            player_vel_y = jump_power # Apply jump force
            on_ground = False # Player is now airborne
        if moving:
            animation_timer += 1
            if animation_timer >= animation_speed:  
                animation_timer = 0
                animation_index = 1 - animation_index  # Alternate between 0 and 1

        current_frame = run_frames[animation_index]

        if direction == -1:  # Flip when moving left
            current_frame = pygame.transform.flip(current_frame, True, False)

        if moving: # Animate the player running if they are moving
            if not on_ground and direction == 1: # If they are airborne and moving right
                screen.blit(run, (player_x - camera_x, player_y))
            elif not on_ground and direction == -1: # If they are airborne and moving left
                screen.blit(flipped_run, (player_x - camera_x, player_y))
            else: # On ground
                screen.blit(current_frame, (player_x - camera_x, player_y))
        else: # Draw the player in an idle position
            if direction == 1: # Right
                screen.blit(player, (player_x - camera_x, player_y))
            else: # Left
                screen.blit(flipped_player, (player_x - camera_x, player_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Jumping Logic (Space Pressed)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if on_ground:
                        player_vel_y = jump_power  # Normal jump
                        on_ground = False
                        doubleJumped = False  # Reset double jump when landing
                    elif doubleJumpBoots and not doubleJumped:
                        player_vel_y = jump_power  # Double jump
                        doubleJumped = True  # Mark double jump as used
                    elif bubbleJump:
                        player_vel_y = jump_power  # jump again
                        bubbleJump = False
            
        # Apply gravity
        player_vel_y += gravity
        player_y += player_vel_y

        on_ground = False
        for row_index, row in enumerate(level_map):
            for col_index, tile in enumerate(row):
                if tile in collidable_tiles:  # Ground, platform, floating ground, invisible platform tiles, Dirt
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE

                    # This code block prevents the player from falling through solid ground
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and  
                    player_y + TILE_SIZE <= tile_y + player_vel_y and  # Only land if falling down
                    player_y + TILE_SIZE > tile_y):  # Ensures overlap
                        player_y = tile_y - TILE_SIZE
                        player_vel_y = 0
                        on_ground = True  # Player lands
                        doubleJumped = False # Reset double jump

                    # This code block prevents collision with solid blocks from the left and right
                    if (player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):  # If the player is at the same height as the block
                        if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and player_x + TILE_SIZE - player_speed <= tile_x):  
                            # Moving right into a block
                            player_x = tile_x - TILE_SIZE  

                        elif (player_x < tile_x + TILE_SIZE and player_x + TILE_SIZE > tile_x and player_x + player_speed >= tile_x + TILE_SIZE):  
                            # Moving left into a block
                            player_x = tile_x + TILE_SIZE

                    # This code block prevents collision with solid blocks above their head
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and  
                        player_y < tile_y + TILE_SIZE and player_y - player_vel_y >= tile_y + TILE_SIZE):

                        player_y = tile_y + TILE_SIZE  # Align player below the ceiling
                        player_vel_y = 0  # Stop upward motion 
                
                
                
                if tile == 3:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
                        level_map[row_index][col_index] = 0  # Remove the boots from screen
                        gadget_sound.play() # Play gadget pick up sound when picking up
                        doubleJumpBoots = True
                        doubleJumped = False

                # If player touches water or thorn
                if tile in deadly_tiles:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
                        death_sound.play() # Play death sound when player touches water or thorn
                        dying = True

                
                if tile == 13:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
                        level_map[row_index][col_index] = 0  # Remove the boots from screen
                        player_speed = player_speed * 1.25 # Up the player speed
                        speedBoots = True

                if tile == 8:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):

                        super_speed_pickup_time = pygame.time.get_ticks()
                        super_speed_effect_off_time = super_speed_pickup_time + 2000
                        super_speed_bool = True
                        level_map[SURFACE][95] = 0
                        super_speed_respawn_time = super_speed_pickup_time + 5000
                        player_speed = player_speed * 2

                if tile == 9:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):

                        dash_pickup_time = pygame.time.get_ticks()
                        dash_respawn_time = dash_pickup_time + 5000
                        level_map[SURFACE-2][113] = 0 
                        player_speed = player_speed * 2
                        dash_duration = pygame.time.get_ticks() + 200
                        dashing = True

                if tile == 14:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):

                        coin_count += 1
                        level_map[SURFACE-1][68] = 0
                        level_map[SURFACE-2][79:81] = [2] * 2   # Platform 

                if tile == 28:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and  
                        player_y + TILE_SIZE == tile_y):  # Feet touching top of ice
                        on_ice = True

                # This code handles jump reset
                if tile == 38:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
                        level_map[row_index][col_index] = 0  # Remove the jump reset from screen
                        bubbleJump = True
                        doubleJumped = False
                        bubbleJump_respawns[(row_index, col_index)] = pygame.time.get_ticks() + 5000

        # Respawn power-ups after 5 seconds
        bubble_removes = []
        for pos, respawn_time in bubbleJump_respawns.items():
            if current_time >= respawn_time:
                level_map[pos[0]][pos[1]] = 38  # Respawn power-up
                bubble_removes.append(pos)  # Mark for removal

        # Apply super-speed powerup
        if (super_speed_bool == True) and (pygame.time.get_ticks() >= super_speed_effect_off_time):
            player_speed = player_speed / 2
            super_speed_bool = False
            super_speed_pickup_time = 0

        #-----Respawns super-speed power-up after 5 seconds
        if (super_speed_respawn_time > 0) and (pygame.time.get_ticks() >= super_speed_respawn_time): 
            level_map[SURFACE-5][23] = 13
            super_speed_respawn_time = 0

        # Apply dash powerup
        if dashing:
            player_x += player_speed
            if (pygame.time.get_ticks() >= dash_duration) and (dash_duration != 0):
                player_speed = player_speed / 2
                dashing = False
                dash_duration = 0

        #-----Respawns Dash power-up after 5 seconds
        if (dash_respawn_time > 0 ) and (pygame.time.get_ticks() >= dash_respawn_time):
            level_map[SURFACE-2][113] = 9
            dash_respawn_time = 0

        if player_x + TILE_SIZE >= level_width * TILE_SIZE:  # If player reaches the end of the level
            show_level_completed_screen(slot)
            running = False
        

        if player_x <= 0: # Ensure player is within the bounds of the level and does not go to the left
            player_x = 0

        # When player falls past bottom of level = dies
        if player_y + TILE_SIZE >= level_height * TILE_SIZE:
            dying = True
            death_sound.play() # Play death sound when player touches water or thorn

        if dying:
            player_x, player_y = checkpoints[checkpoint_idx][0], checkpoints[checkpoint_idx][1]
            death_count += 1
            dying = False
            level_map[SURFACE - 3][39] = 3
            # Reset the player’s flags so re-collect
            doubleJumpBoots = False
            if checkpoint_idx == 0 and doubleJumpBoots:
                doubleJumpBoots = False
                level_map[SURFACE][28] = 3
            elif checkpoint_idx == 1 and speedBoots:
                level_map[SURFACE-5][55] = 13
                speedBoots = False
                player_speed = player_speed / 1.25

        for k, checkpoint in enumerate(checkpoints):
            x, y = checkpoint
            if player_x >= x and not checkpoint_bool[k]:
                checkpoint_idx += 1
                checkpoint_bool[k] = True
                if checkpoint_idx == 2:
                    doubleJumpBoots = False 
                    player_speed = player_speed / 1.25 
                    level_map[SURFACE-1][68] = 14  

       
        camera_x = max(0, min(player_x - WIDTH // 2, (level_width * TILE_SIZE) - WIDTH))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()  



if __name__ == "__main__":
    level_1(1)
    pygame.quit()
