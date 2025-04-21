import pygame  # type: ignore
import random
import sys
import time
import world_select
import json
from NPCs.level_1_npc_1 import handle_level_1_npc_1_dialogue  # Import the functionality of the first NPC from level 1
from NPCs.level_1_npc_2 import handle_level_1_npc_2_dialogue  # Import the functionality of the second NPC from level 1
from NPCs.level_1_npc_3 import handle_level_1_npc_3_dialogue  # Import the functionality of the third NPC from level 1
from saves_handler import *
from firework_level_end import show_level_complete_deaths
from saves_handler import update_unlock_state, get_unlock_state
from pause_menu import PauseMenu  # Import the PauseMenu class

# Initialize Pygame
pygame.init()
pygame.mixer.init() # Initialize Pygame Audio Mixer

# Load the level complete sound 
level_complete_sound = pygame.mixer.Sound("Audio/LevelComplete.mp3")
# pygame.mixer.music.set_volume(1.0)  # start at 100% volume 

# Gadget pick up sound 
gadget_sound = pygame.mixer.Sound("Audio/GadgetPickUp.mp3")

# Super speed power up sound
super_speed_sound = pygame.mixer.Sound("Audio/SuperSpeed.mp3")

# Death sound 
death_sound = pygame.mixer.Sound("Audio/Death.mp3")


# Coin pick up sound 
coin_sound = pygame.mixer.Sound("Audio/Coin.mp3")

counter_for_coin_increment = 0


# Screen Resolution 
BASE_WIDTH = 1920
BASE_HEIGHT = 1080
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h 
TILE_SIZE = HEIGHT // 30 
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
walkway = pygame.transform.scale(walkway, (TILE_SIZE * 4, TILE_SIZE * 2))

flipped_walkway = pygame.transform.flip(walkway, True, False)  # Flip horizontally (True), no vertical flip (False)
flipped_walkway = pygame.transform.scale(flipped_walkway, (TILE_SIZE * 4, TILE_SIZE * 2))

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

npc_2 = pygame.image.load("./Character Combinations/female brown hair_white_pink skirt_magenta pants.png")
npc_2 = pygame.transform.scale(npc_2, (TILE_SIZE, TILE_SIZE))
flipped_npc_2 = pygame.transform.flip(npc_2, True, False)

npc_3 = pygame.image.load("./Character Combinations/ginger hair_white_blue shirt_black pants.png")
npc_3 = pygame.transform.scale(npc_3, (TILE_SIZE, TILE_SIZE))
flipped_npc_3 = pygame.transform.flip(npc_3, True, False)  

npc_4 = pygame.image.load("./Character Combinations/black hair_dark_blue shirt_brown pants.png")
npc_4 = pygame.transform.scale(npc_4, (TILE_SIZE, TILE_SIZE))
flipped_npc_4 = pygame.transform.flip(npc_4, True, False)  



level_almost_complete_popup = pygame.image.load("./images/level_near_completion_pop_up.png")
level_almost_complete_popup = pygame.transform.scale(level_almost_complete_popup, (250, 60))


level_almost_complete_font = pygame.font.Font('PixelifySans.ttf', 10)
keep_heading_right_font = pygame.font.Font('PixelifySans.ttf', 10)
level_almost_complete_text = level_almost_complete_font.render("Level 1 Almost Complete!", True, (255, 255, 255))
keep_heading_right_text = keep_heading_right_font.render("Keep Heading Right!", True, (255, 255, 255))



pop_up_x = WIDTH - (WIDTH * .20)
pop_up_y = HEIGHT - (HEIGHT * .95)



level_almost_complete_rect = level_almost_complete_text.get_rect(center=(pop_up_x + 140, pop_up_y + 18))
keep_heading_right_rect = keep_heading_right_text.get_rect(center=(pop_up_x + 140, pop_up_y + 38))





#-----Gadget inventory images and dictionary

inventory = pygame.image.load("./images/inventory_slot.png").convert_alpha()
inventory = pygame.transform.scale(inventory, (250, 70))
inventory_x = (WIDTH - 250) // 2
inventory_y = HEIGHT - 100

inventory_jump_boots = pygame.image.load("./images/boots.png")
inventory_jump_boots = pygame.transform.scale(inventory_jump_boots, (42, 50))

inventory_speed_boots = pygame.image.load("./images/speed_boots.png")
inventory_speed_boots = pygame.transform.scale(inventory_speed_boots, (42, 50))

INV_SLOT_WIDTH = 42
INV_SLOT_HEIGHT = 45

first_slot = (inventory_x + 5, inventory_y + 10)
second_slot = (inventory_x + INV_SLOT_WIDTH + 10, inventory_y + 10)

# -------------------------------
# Level Setup and Constants
# -------------------------------

level_width = 180
level_height = HEIGHT // TILE_SIZE  

level_map = None
ground_levels = None  

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

rocks = {141, 151, 176}           
trees = {166, 174}                     
background_trees = {146, 171}     

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

def show_level_completed_screen(slot: int, death_count: int):

    # Stop level 1 music
    pygame.mixer.music.stop()

    # Play the level complete sound once when this function runs
    level_complete_sound.play()
    
    respawn_gadgets()
    respawn_powerups()

    update_save(slot, {"Level 1 Checkpoint": 0}) # Set checkpoint to 0

    current_state = get_unlock_state(slot, "map1")
    current_state[2] = True  # Unlock level 2
    update_unlock_state(slot, current_state, "map1")

    level_name = "Level One"

    show_level_complete_deaths(slot, counter_for_coin_increment, death_count, level_name, background)

# Initialize the PauseMenu
pause_menu = PauseMenu(screen)

def respawn_terrain():
    # Add solid ground at the very bottom
    global level_map
    level_map = [[0] * level_width for _ in range(level_height)]
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

    for row_index in range(SURFACE - 1, level_height):
        for col in range(120, 134):
            level_map[row_index][col] = 1

    for row_index in range(SURFACE-2, GROUND): # Raised Ground
        level_map[row_index][145:150] = [1] * 5
    for row_index in range(SURFACE-4, GROUND): # Raised Ground
        level_map[row_index][150:155] = [1] * 5
    for row_index in range(SURFACE-7, GROUND): # Raised Ground
        level_map[row_index][155:158] = [1] * 3
    for row_index in range(SURFACE-12, GROUND): # Raised Ground
        level_map[row_index][158:165] = [1] * 7
    for row_index in range(SURFACE-5, GROUND): # Raised Ground
        level_map[row_index][165:170] = [1] * 5
    for row_index in range(SURFACE-2, GROUND): # Raised Ground
        level_map[row_index][170:173] = [1] * 3
    level_map[SURFACE-10][145:148] = [2] * 3 # Platform Tiles

    # -------------------------------
    # Ground Level Calculation
    # -------------------------------

    global ground_levels
    ground_levels = [len(level_map)] * len(level_map[0])
    for row_index, row in enumerate(level_map):
        for col_index, tile in enumerate(row):
            if tile == 1 and ground_levels[col_index] == len(level_map):
                ground_levels[col_index] = row_index

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
    level_map[SURFACE - 3][56] = 23 # Flipped Walkway Bridge
    level_map[SURFACE - 2][56:60] = [26] * 4 

    # Thorns placement 
    level_map[SURFACE - 6][28] = 6
    level_map[SURFACE - 5][31] = 6
    level_map[SURFACE - 4][34] = 6
    level_map[SURFACE - 3][37] = 6

    level_map[SURFACE-3][61:69] = [6] * 8 # Thorns

    # Water placement
    level_map[level_height-1][40:60] = [25] * 20 # Water
    level_map[level_height-1][70:200] = [25] * 80 # Water

    # Windmill placement
    level_map[SURFACE - 18][80] = 30 # Windmill

    for row_index in range(SURFACE-12, SURFACE):
        level_map[row_index][79] = 36 # Thorns on left side of Windmill terrain
        level_map[row_index][85] = 37 # Thorns on right side of Windmill terrain

    for row_index in range(SURFACE-23, SURFACE-5):
        level_map[row_index][119] = 36 # Thorns on left side of huge dirt block

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

    level_map[SURFACE-2][122] = 7 # Flag

    level_map[SURFACE][144] = 6 # Thorn
    level_map[SURFACE-11][145] = 6 # Thorn on platform
    level_map[SURFACE-13][160:163] = [6] * 3 # Thorns on top of raised ground

    # NPCs Placement
    level_map[SURFACE - 9][12] = 12 # First NPC
    level_map[SURFACE - 9][18] = 15 # Second NPC
    level_map[SURFACE - 3][58] = 16 # Third NPC

def respawn_gadgets():
    level_map[SURFACE-3][39] = 3   # Jump Boots
    level_map[SURFACE-2][127] = 13 # Speed Boots

def respawn_powerups():
    level_map[SURFACE-8][76] = 38 # Jump Reset
    level_map[SURFACE-8][156] = 8 # Super Speed Powerup

# -----------------------------------
# Level One Game Loop
# -----------------------------------
def level_1(slot: int):

    respawn_terrain()
    respawn_gadgets()
    respawn_powerups()

    # Stop any previously playing music 
    pygame.mixer.music.stop()
    
    # Load the tutorial music
    pygame.mixer.music.load("Audio/Level1.mp3")
    pygame.mixer.music.play(-1)  # -1 loops forever

    # Grab the sprite that was customized
    sprite = load_save(slot).get("character")

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

    checkpoints = [(calculate_x_coordinate(3), calculate_y_coordinate(SURFACE-9)), (calculate_x_coordinate(122), calculate_y_coordinate(SURFACE-2))]
    checkpoint_bool = [False] * len(checkpoints)
    checkpoint_idx = load_save(slot).get("Level 1 Checkpoint")
    if not checkpoint_idx:
        checkpoint_idx = 0
    for i in range(checkpoint_idx+1):
        checkpoint_bool[i] = True

    # Camera position
    camera_x = 0
    player_x = checkpoints[checkpoint_idx][0]  # Start x position, change this number to spawn in a different place
    player_y = checkpoints[checkpoint_idx][1]  # Start y position, change this number to spawn in a different place

    player_speed = 8.5 * scale_factor # Adjust player speed according to their resolution
    default_speed = player_speed
    player_vel_x = 0 # Horizontal velocity for friction/sliding
    player_vel_y = 0 # Vertical velocity for jumping
    gravity = 1.25 * scale_factor # Gravity effect (Greater number means stronger gravity)
    jump_power = -18 * scale_factor # Jump strength (Bigger negative number means higher jump)
    on_ground = False # Track if player is on the ground
    doubleJumpBoots = False # Track if player has double jump boots
    doubleJumped = False # Track if player double jumped already
    speedBoots = False

    animation_index = 0  # Alternates between 0 and 1
    animation_timer = 0  # Tracks when to switch frames
    animation_speed = 4  # Adjust this to control animation speed
    direction = 1  # 1 for right, -1 for left

    super_speed_effects = []
    super_speed_respawns = {}

    dash_respawn_time = 0 
    dash_pickup_time = 0
    dash_duration = 0
    dashing = False


    
    times_passed_wooden_sign = 0
    time_before_pop_up_disappears = 0



    normal_friction = 0.25
    ice_friction = 0.95  # Lower friction for slippery effect
    on_ice = False

    #-----Variable to check which gadget was picked up first
    double_first = False
    dying = False
    death_count = load_save(slot).get("Level 1 Deaths")
    if not death_count:
        death_count = 0
    coin_count = 0

    global counter_for_coin_increment
    counter_for_coin_increment = coin_count

    collidable_tiles = {1, 2, 32, 26, 27, 28, 29, 31}

    # State Variables for Gadgets
    bubbleJump = False
    bubbleJump_respawns = {}

    running = True
    while running:

        #print(f"Row: SURFACE - {SURFACE - calculate_row(player_y)}")
        #print(f"Column: {calculate_column(player_x)}")

        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Pass events to the PauseMenu
            result = pause_menu.handle_event(event, slot)
            if result == "restart":
                update_save(slot, {"Level 1 Checkpoint": 0}) # Set checkpoint to 0
                level_1(slot)
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if bubbleJump and doubleJumpBoots and not doubleJumped:
                    player_vel_y = jump_power  # Double jump
                    bubbleJump = False
                elif doubleJumpBoots and not doubleJumped:
                    player_vel_y = jump_power  # Double jump
                    doubleJumped = True  # Mark double jump as used
        if pause_menu.paused:
            continue

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

        acceleration = 0.5  # Slower acceleration on ice
        friction = normal_friction if not on_ice else ice_friction

        # Handle events
        keys = pygame.key.get_pressed()
        moving = False
        # if keys[pygame.K_w]:
        #     player_y -= player_speed
        # if keys[pygame.K_s]:
        #     player_y += player_speed
        if keys[pygame.K_d]: # If player presses D
            if on_ice:
                player_vel_x += acceleration
            else:
                player_vel_x = player_speed
            moving = True
            direction = 1
        if keys[pygame.K_a]: # If player presses A
            if on_ice:
                player_vel_x -= acceleration
            else:
                player_vel_x = -player_speed
            moving = True
            direction = -1
        # Jumping Logic (Space Pressed)
        if keys[pygame.K_SPACE]:
            if on_ground:
                player_vel_y = jump_power  # Normal jump
                on_ground = False
                doubleJumped = False  # Reset double jump when jumping once
            elif bubbleJump:
                player_vel_y = jump_power  # jump again
                bubbleJump = False
        if not moving:
            player_vel_x *= friction
            if abs(player_vel_x) < 0.1:
                player_vel_x = 0
        if moving:
            # Clamp velocity to max speed
            if abs(player_vel_x) > player_speed:
                player_vel_x = player_speed * (1 if player_vel_x > 0 else -1)
            if abs(player_vel_x) < 0.1:
                player_vel_x = 0
            animation_timer += 1
            if animation_timer >= animation_speed:  
                animation_timer = 0
                animation_index = 1 - animation_index  # Alternate between 0 and 1

        player_x += player_vel_x  # Update position
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
            
        # Apply gravity
        player_vel_y += gravity
        player_y += player_vel_y

        on_ground = False
        on_ice = False
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

                    if tile == 26: # Continue if tile is invisible/walkway
                        continue

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
                        gadget_sound.play() # Play gadget pick up sound when picking up
                        player_speed = player_speed * 1.25 # Up the player speed
                        speedBoots = True

                if tile == 8:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
    
                        level_map[row_index][col_index] = 0
                        super_speed_sound.play()
                        player_speed *= 2
                        super_speed_effects.append({"end_time": pygame.time.get_ticks() + 2000})  # 2 sec effect
                        super_speed_respawns[(row_index, col_index)] = pygame.time.get_ticks() + 5000  # 5 sec respawn

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
                        counter_for_coin_increment = 0 
                        eclipse_increment(slot, 1)
                        level_map[SURFACE-1][68] = 0
                        coin_sound.play()
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

        # Apply speed effects from multiple power-ups
        for effect in super_speed_effects[:]:  # Iterate over a copy of the list
            if current_time >= effect["end_time"]:  # Check if effect expired
                player_speed /= 2
                super_speed_effects.remove(effect)

        # Respawn power-ups after 5 seconds
        to_remove = []
        for pos, respawn_time in super_speed_respawns.items():
            if current_time >= respawn_time:
                level_map[pos[0]][pos[1]] = 8  # Respawn super speed power-up
                to_remove.append(pos)  # Mark for removal

        # Respawn power-ups after 5 seconds
        bubble_removes = []
        for pos, respawn_time in bubbleJump_respawns.items():
            if current_time >= respawn_time:
                level_map[pos[0]][pos[1]] = 38  # Respawn power-up
                bubble_removes.append(pos)  # Mark for removal

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
            show_level_completed_screen(slot, death_count)
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
            update_save(slot, {"Level 1 Deaths": death_count})
            dying = False
            respawn_powerups()
            bubbleJump = False
            if checkpoint_idx == 0:
                doubleJumpBoots = False
                level_map[SURFACE - 3][39] = 3 # Respawn Double Jump Boots
            elif checkpoint_idx == 1:
                level_map[SURFACE-2][127] = 13 # Speed Boots
                if speedBoots:
                    speedBoots = False
                    player_speed = default_speed
            if super_speed_effects:
                player_speed = default_speed  # Reset to normal speed
                super_speed_effects.clear()   # Remove all ongoing effects

        for k, checkpoint in enumerate(checkpoints):
            x, y = checkpoint
            if player_x >= x and not checkpoint_bool[k]:
                checkpoint_idx += 1
                checkpoint_bool[k] = True
                update_save(slot, {"Level 1 Checkpoint": checkpoint_idx})
                if checkpoint_idx == 1:
                    doubleJumpBoots = False 
                    level_map[SURFACE - 3][39] = 3 # Respawn Double Jump Boots

       
        camera_x = max(0, min(player_x - WIDTH // 2, (level_width * TILE_SIZE) - WIDTH))

        #-----Inventory Fill-up logic

        screen.blit(inventory, (inventory_x, inventory_y))

        if (doubleJumpBoots):
            if (doubleJumpBoots) and (speedBoots == False):
                double_first = True
                screen.blit(inventory_jump_boots, first_slot)
            elif (doubleJumpBoots) and (speedBoots) and double_first:
                screen.blit(inventory_jump_boots, first_slot)
                screen.blit(inventory_speed_boots, second_slot)


        if (speedBoots):
            if  (speedBoots) and (doubleJumpBoots == False):
                double_first == False
                screen.blit(inventory_speed_boots, first_slot)
            elif (doubleJumpBoots) and (speedBoots) and (double_first == False):
                screen.blit(inventory_speed_boots, first_slot)
                screen.blit(inventory_jump_boots, second_slot)





        # Pop up near level completion 
        # print(calculate_column(player_x))
        if (pygame.time.get_ticks() < time_before_pop_up_disappears):
            screen.blit(level_almost_complete_popup, (pop_up_x, pop_up_y))
            screen.blit(level_almost_complete_text, level_almost_complete_rect)
            screen.blit(keep_heading_right_text, keep_heading_right_rect)


        if (calculate_column(player_x) >= 166 and times_passed_wooden_sign < 1):
            times_passed_wooden_sign += 1
            screen.blit(level_almost_complete_popup, (pop_up_x, pop_up_y))
            screen.blit(level_almost_complete_text, level_almost_complete_rect)
            screen.blit(keep_heading_right_text, keep_heading_right_rect)
            time_before_pop_up_disappears = pygame.time.get_ticks() + 5000





        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()  



if __name__ == "__main__":
    level_1(1)
    pygame.quit()
