import pygame # type: ignore
import random
import json
import sys
import world_select
from collections import deque
from NPCs.level_3_npc_1 import handle_level_3_npc_1_dialogue  # Import the functionality of the NPC from level 3
from NPCs.level_3_npc_2 import handle_level_3_npc_2_dialogue  # Import the functionality of the NPC from level 3
from NPCs.level_3_npc_3 import handle_level_3_npc_3_dialogue  # Import the functionality of the NPC from level 3
from NPCs.level_3_npc_4 import handle_level_3_npc_4_dialogue  # Import the functionality of the NPC from level 3

# Initialize PyGame
pygame.init()

# Screen settings

BASE_WIDTH = 1920
BASE_HEIGHT = 1080

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h # Will only work with resolutions 1920 x 1080 or better

TILE_SIZE = HEIGHT // 30  # Readjusted according to user resolution

scale_factor = HEIGHT / BASE_HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Level 3")

ground_tile = pygame.image.load("./images/ground.png")
ground_tile = pygame.transform.scale(ground_tile, (TILE_SIZE, TILE_SIZE))

floating_ground = ground_tile

platform_tile = pygame.image.load("./images/platform.png")
platform_tile = pygame.transform.scale(platform_tile, (TILE_SIZE, TILE_SIZE))

dirt_tile = pygame.image.load("./images/dirt.png")
dirt_tile = pygame.transform.scale(dirt_tile, (TILE_SIZE, TILE_SIZE))

background = pygame.image.load("./images/background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

tree = pygame.image.load("./images/tree.png")
tree = pygame.transform.scale(tree, (TILE_SIZE * 2, TILE_SIZE * 3))  # Resize tree to fit properly

rock = pygame.image.load("./images/rock.png")
rock = pygame.transform.scale(rock, (TILE_SIZE, TILE_SIZE // 2))

background_tree = pygame.image.load("./images/background_tree.png")
background_tree = pygame.transform.scale(background_tree, (TILE_SIZE * 1.5, TILE_SIZE * 2))

water = pygame.image.load("./images/water.png")
water = pygame.transform.scale(water, (TILE_SIZE, TILE_SIZE))

water_block = pygame.image.load("./images/water_block.png")
water_block = pygame.transform.scale(water_block, (TILE_SIZE, TILE_SIZE))

ice_tile = pygame.image.load("./images/ice.png")
ice_tile = pygame.transform.scale(ice_tile, (TILE_SIZE, TILE_SIZE))
flipped_ice = pygame.transform.flip(ice_tile, False, True)

ice_block = pygame.image.load("./images/ice_block.png")
ice_block = pygame.transform.scale(ice_block, (TILE_SIZE, TILE_SIZE))

jump_reset = pygame.image.load("./images/bubble.png")
jump_reset = pygame.transform.scale(jump_reset, (TILE_SIZE, TILE_SIZE))

dash_powerup = pygame.image.load("./images/dash_powerup.png")
dash_powerup = pygame.transform.scale(dash_powerup, (TILE_SIZE, TILE_SIZE))
up_dash = pygame.transform.rotate(dash_powerup, 90)

thorn = pygame.image.load("./images/thorn.png")
thorn = pygame.transform.scale(thorn, (TILE_SIZE, TILE_SIZE))
flipped_thorn = pygame.transform.flip(thorn, False, True)
left_thorn = pygame.transform.rotate(thorn, 90)
right_thorn = pygame.transform.rotate(thorn, -90)

flag = pygame.image.load("./images/flag.png")
flag = pygame.transform.scale(flag, (TILE_SIZE, TILE_SIZE))

frost_walking_boots = pygame.image.load("./images/ice_boots.png")
frost_walking_boots = pygame.transform.scale(frost_walking_boots, (TILE_SIZE, TILE_SIZE))

coin = pygame.image.load("./images/coin.png")
coin = pygame.transform.scale(coin, (TILE_SIZE, TILE_SIZE))

walkway = pygame.image.load("./images/walkway.png")
walkway = pygame.transform.scale(walkway, (TILE_SIZE * 4, TILE_SIZE * 2))
flipped_walkway = pygame.transform.flip(walkway, True, False)  # Flip horizontally (True), no vertical flip (False)

invisible_platform = None

double_jump_boots = pygame.image.load("./images/boots.png")
double_jump_boots = pygame.transform.scale(double_jump_boots, (TILE_SIZE, TILE_SIZE))

super_speed_powerup = pygame.image.load("./images/super_speed_powerup.png")
super_speed_powerup = pygame.transform.scale(super_speed_powerup, (TILE_SIZE, TILE_SIZE))

high_jump = pygame.image.load("./images/high_jump.png")
high_jump = pygame.transform.scale(high_jump, (TILE_SIZE, TILE_SIZE))

house = pygame.image.load("./images/house.png")
house = pygame.transform.scale(house, (TILE_SIZE * 10, TILE_SIZE * 6))

sign = pygame.image.load("./images/sign.png")
sign = pygame.transform.scale(sign, (TILE_SIZE, TILE_SIZE))

npc_1 = pygame.image.load("./Character Combinations/black hair_dark_yellow shirt_black pants.png")
npc_1 = pygame.transform.scale(npc_1, (TILE_SIZE, TILE_SIZE))
flipped_npc_1 = pygame.transform.flip(npc_1, True, False)  # Flip horizontally (True), no vertical flip (False)

npc_2 = pygame.image.load("./Character Combinations/brown hair_white_red shirt_brown pants.png")
npc_2 = pygame.transform.scale(npc_2, (TILE_SIZE, TILE_SIZE))
flipped_npc_2 = pygame.transform.flip(npc_2, True, False)  # Flip horizontally (True), no vertical flip (False)

npc_3 = pygame.image.load("./Character Combinations/ginger hair_white_yellow shirt_brown pants.png")
npc_3 = pygame.transform.scale(npc_3, (TILE_SIZE, TILE_SIZE))
flipped_npc_3 = pygame.transform.flip(npc_3, True, False)  # Flip horizontally (True), no vertical flip (False)

npc_4 = pygame.image.load("./Character Combinations/black hair_dark_blue shirt_brown pants.png")
npc_4 = pygame.transform.scale(npc_4, (TILE_SIZE, TILE_SIZE))
flipped_npc_4 = pygame.transform.flip(npc_4, True, False)  

# Set up the level with a width of 250 and a height of 30 rows
level_width = 250
level_height = HEIGHT // TILE_SIZE  # Adjust level height according to user's resolution

level_map = [[0] * level_width for _ in range(level_height)]  # Start with air

GROUND = level_height - 4 #Constant for the ground level
SURFACE = GROUND - 1 #Constant for the surface level

# This is for the snowflake animations
WHITE = (255, 255, 255)
RED = (255, 0, 0) # For timer
BLUE = (0, 0, 255) # For hover
NUM_SNOWFLAKES = 200
snowflakes = []

#This for loop is also for snowflakes
for _ in range(NUM_SNOWFLAKES):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    size = random.randint(2, 6)  # Random size
    speed = random.uniform(3, 6)  # Falling speed
    x_speed = random.uniform(-2, 2)  # Small horizontal drift
    snowflakes.append([x, y, size, speed, x_speed])

for row_index in range(GROUND, level_height):
    row = [1] * level_width  # Default to full ground row
    for col_index in range(15, 35):  # Remove ground in columns 15-35
        row[col_index] = 0  # Set to air (pit)
    for col_index in range(55, 75):  # Remove ground in columns 55-75
        row[col_index] = 0  # Set to air (pit)
    for col_index in range(95, 130):  # Remove ground in columns 95-130
        row[col_index] = 0  # Set to air (pit)
    for col_index in range(135, 150):  # Remove ground in columns 130-150
        row[col_index] = 0  # Set to air (pit)
    for col_index in range(160, level_width-20):  # Remove ground in columns 160-level_width-20
        row[col_index] = 0  # Set to air (pit)
    level_map[row_index] = row  # Add row to level map

# Add solid ground at the very bottom
level_map.append([1] * level_width)

for row_index in range(SURFACE-2, GROUND): # Raised Ground
    level_map[row_index][40:45] = [1] * 5
for row_index in range(SURFACE-4, GROUND): # Raised Ground
    level_map[row_index][45:55] = [1] * 10
for row_index in range(SURFACE-4, GROUND): # Raised Ground
    level_map[row_index][75:85] = [1] * 10
for row_index in range(SURFACE-3, GROUND): # Raised Ground
    level_map[row_index][85:90] = [1] * 5
for row_index in range(SURFACE-1, GROUND): # Raised Ground
    level_map[row_index][90:95] = [1] * 5
for row_index in range(SURFACE-5, GROUND): # Raised Ground
    level_map[row_index][110] = 1
for row_index in range(0, 14): # Upside down dirt block
    level_map[row_index][110] = 9
for row_index in range(SURFACE-12, GROUND): # Raised Ground
    level_map[row_index][120] = 1
for row_index in range(0, 14): # Upside down dirt block
    level_map[row_index][130] = 9
for row_index in range(SURFACE-3, GROUND): # Raised Ground
    level_map[row_index][150:160] = [1] * 10
for row_index in range(8, 18): # Floating dirt block
    level_map[row_index][176] = 9
for row_index in range(0, 16): # Upside down dirt block
    level_map[row_index][195] = 9
for row_index in range(0, 20): # Upside down dirt block
    level_map[row_index][224] = 9
for row_index in range(SURFACE-13, GROUND): # Raised Ground
    level_map[row_index][230:level_width] = [1] * 20

# Make terrain before this line. The next code block calculates the ground levels

# Find the ground level for each column
ground_levels = [len(level_map)] * len(level_map[0])
for row_index, row in enumerate(level_map):
    for col_index, tile in enumerate(row):
        if tile == 1 and ground_levels[col_index] == len(level_map):
            ground_levels[col_index] = row_index

for row_index in range(0, 6):
    level_map[row_index][26] = 9

# All code after this line should be for props, npcs, gadgets, and powerups. Terrain should not be made here.

row = SURFACE - 3
col = 12
for i in range(6):
    level_map[row][col] = 4 # Jump Reset
    row -= 3
    col = col - 4 if i % 2 == 0 else col + 4
level_map[row][col] = 5

level_map[6][20:33] = [6] * 13 # Floating Ground
level_map[5][24] = 10 # Frost Walking Boots
level_map[4][28] = 12 # Coin
level_map[10][36] = 4 # Jump Reset
level_map[14][43] = 4 # Jump Reset

level_map[level_height-3][15:35] = [3] * 20 # Water
level_map[level_height-2][15:35] = [11] * 20 # Water Block
level_map[level_height-1][15:35] = [11] * 20 # Water Block

level_map[SURFACE-2][57] = 4 # Jump Reset

level_map[SURFACE][39] = 7 # Thorn

level_map[SURFACE-5][55] = 13 # Walkway
level_map[SURFACE-4][55:59] = [15] * 4 # Invisible Platforms to ensure collision with walkway

level_map[SURFACE-8][61] = 5 # Dash Powerup

level_map[level_height-3][55:75] = [3] * 20 # Water
level_map[level_height-2][55:75] = [11] * 20 # Water Block
level_map[level_height-1][55:75] = [11] * 20 # Water Block

level_map[SURFACE-5][77] = 8 # Flag
level_map[SURFACE-5][82] = 16 # Double Jump Boots

level_map[level_height-3][95:130] = [3] * 35 # Water
level_map[level_height-2][95:130] = [11] * 35 # Water Block
level_map[level_height-1][95:130] = [11] * 35 # Water Block

level_map[SURFACE-7][105] = 4 # Jump Reset
level_map[SURFACE-7][115] = 4 # Jump Reset
level_map[SURFACE-14][115] = 4 # Jump Reset
level_map[SURFACE-3][125] = 4 # Jump Reset
level_map[SURFACE-6][130] = 20 # Super Speed Powerup

level_map[SURFACE-6][110] = 7 # Thorn
level_map[14][110] = 17 # Flipped Thorn
for row_index in range(13, GROUND+1):
    level_map[row_index][119] = 18 # Left Thorn
for row_index in range(13, GROUND+1):
    level_map[row_index][121] = 19 # Right Thorn
level_map[12][120] = 7 # Thorn
level_map[14][130] = 17 # Flipped Thorn
level_map[SURFACE][130:135] = [7] * 5 # Thorns

level_map[level_height-3][135:150] = [3] * 35 # Water
level_map[level_height-2][135:150] = [11] * 35 # Water Block
level_map[level_height-1][135:150] = [11] * 35 # Water Block

level_map[SURFACE-4][146] = 14 # Flipped Walkway
level_map[SURFACE-3][146:150] = [15] * 4 # Invisible Platforms to ensure collision with walkway

level_map[SURFACE-4][153] = 8 # Flag

level_map[SURFACE-5][165:170] = [21] * 5 # Ice
level_map[SURFACE-4][165:170] = [22] * 5 # Flipped ice

level_map[SURFACE-6][167] = 20 # Super Speed Powerup
level_map[SURFACE-6][169] = 23 # High Jump Powerup

level_map[SURFACE-7][182:187] = [21] * 5 # Ice
level_map[SURFACE-6][182:187] = [22] * 5 # Flipped ice

level_map[7][176] = 7 # Thorn
level_map[18][176] = 17 # Flipped Thorn
for row_index in range(8, 18):
    level_map[row_index][175] = 18 # Left Thorn
for row_index in range(8, 18):
    level_map[row_index][177] = 19 # Right Thorn

level_map[SURFACE-9][193:196] = [2] * 3 # Platform

level_map[12][191] = 14 # Flipped Walkway
level_map[13][191:195] = [15] * 4 # Invisible Platforms to ensure collision with walkway
level_map[9][191] = 14 # Flipped Walkway
level_map[10][191:195] = [15] * 4 # Invisible Platforms to ensure collision with walkway
level_map[6][191] = 14 # Flipped Walkway
level_map[7][191:195] = [15] * 4 # Invisible Platforms to ensure collision with walkway

level_map[3][186] = 12 # Coin

level_map[SURFACE-3][193] = 4 # Jump Reset
level_map[SURFACE-5][198] = 4 # Jump Reset

level_map[SURFACE-9][198] = 24 # Up Dash Powerup

level_map[12][202:219] = [6] * 17 # Floating Ground
level_map[12][201] = 18 # Left Thorn
level_map[12][219] = 19 # Right Thorn
level_map[13][202:219] = [17] * 17 # Upside Down Thorn
level_map[4][203:206] = [2] * 3 # Platform
level_map[4][215:218] = [2] * 3 # Platform
level_map[11][210] = 23 # High Jump Powerup
level_map[3][204] = 10 # Frost Walking Boots
level_map[3][216] = 16 # Double Jump Boots

level_map[20][224] = 17 # Flipped Thorn

level_map[SURFACE-8][227] = 4 # Jump Reset

level_map[SURFACE-19][235] = 25 # House

level_map[level_height-6][160:level_width-20] = [3] * (level_width-180) # Water
for row_index in range(level_height-5, level_height):
    level_map[row_index][160:level_width-20] = [11] * (level_width-180) # Water Block

# Dictionary containing which tile corresponds to what
tiles = {0: background, 1: ground_tile, 2: platform_tile, 3: water, 4: jump_reset, 5: dash_powerup, 6: floating_ground, 7: thorn, 8: flag, 9: dirt_tile, 10: frost_walking_boots,
         11: water_block, 12: coin, 13: walkway, 14: flipped_walkway, 15: invisible_platform, 16: double_jump_boots, 17: flipped_thorn, 18: left_thorn, 19: right_thorn, 20: super_speed_powerup,
         21: ice_tile, 22: flipped_ice, 23: high_jump, 24: up_dash, 25: house, 26: tree, 27: background_tree, 28: ice_block, 29: npc_1, 30: npc_2, 31: npc_3, 32: npc_4}

level_map[9][203] = 26 # Tree
level_map[9][216] = 26 # Tree

level_map[10][206] = 27 # Background Tree
level_map[10][213] = 27 # Background Tree

# NPCs placements
level_map[SURFACE][8] = 29 # First NPC (Placed at the start of the map)
level_map[SURFACE-5][52] = 30 # Second NPC - (Placed at the bridge at the start of the lake)
level_map[11][208] = 31 # Third NPC - (Placed next to the high jump boost)
level_map[SURFACE-14][237] = 32 # Fourth NPC - (Placed at the house at the end of the map)

rocks = {3, 36, 41, 91, 246} # Column numbers for all the rocks
trees = {48, 157, 247} # Column numbers for all the trees
background_trees = {6, 86, 232} # Column numbers for all the background trees
signs = {10, 94, 230} # Column numbers for all the signs

# Converts the x coordinates to the column on the map
def calculate_column(x): 
    return int(x // TILE_SIZE)

# Converts the column number to the x-coordinate
def calculate_x_coordinate(column):
    return int(column * TILE_SIZE)

# Converts the y coordinate to the row on the map
def calculate_row(y):
    return int(y // TILE_SIZE)

# Converts the row number to the y-coordinate
def calculate_y_coordinate(row):
    return int(row * TILE_SIZE)

def read_data(slot: int):
    with open(f"./User Saves/save{str(slot)}.json", "r") as file:
        data = json.load(file)
    return data.get("character")

def show_level_completed_screen(slot: int, death_count: int):

    level_map[5][24] = 10 # Frost Walking Boots
    level_map[SURFACE-5][82] = 16 # Double Jump Boots
    level_map[3][204] = 10 # Frost Walking Boots
    level_map[3][216] = 16 # Double Jump Boots

    # Wait for player to click the button
    waiting = True
    while waiting:
        # Display the background image
        screen.blit(background, (0, 0))

        # Set fonts for the text
        title_font = pygame.font.Font('PixelifySans.ttf', 100)
        menu_font = pygame.font.Font('PixelifySans.ttf', 60)
        menu_font_hover = pygame.font.Font('PixelifySans.ttf', 65)  # Larger for hover

        # Render hover effect dynamically
        select_level_hover = False

        # Render the "Level Completed" text
        level_completed_text = title_font.render("Level Completed", True, WHITE)
        death_count_text = title_font.render(f"Deaths: {death_count}", True, WHITE)
        select_level_text = menu_font.render("Back to Select Level", True, WHITE)

        # Position the texts
        level_completed_rect = level_completed_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        death_count_rect = death_count_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 120))
        select_level_rect = select_level_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 240))

        # Check if mouse is hovering
        if select_level_rect.collidepoint(pygame.mouse.get_pos()):
            select_level_hover = True

        # If hovering, change text size dynamically
        if select_level_hover:
            select_level_text = menu_font_hover.render("Back to Select Level", True, BLUE)
            select_level_rect = select_level_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 240))  # Recalculate position

        # Create box around the text
        box_padding = 20
        level_end_screen_box = pygame.Rect(level_completed_rect.left - box_padding, level_completed_rect.top - box_padding, level_completed_rect.width + box_padding*2, level_completed_rect.height + (box_padding*2) + 200)
        pygame.draw.rect(screen, BLUE, level_end_screen_box, 10)
        
        # Draw the texts
        screen.blit(level_completed_text, level_completed_rect)
        screen.blit(death_count_text, death_count_rect)
        screen.blit(select_level_text, select_level_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if select_level_rect.collidepoint(mouse_x, mouse_y):
                    world_select.World_Selector(slot)
                    sys.exit()  # Go back to level select

def level_3(slot: int):
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

    # (5, SURFACE) should be the starting point
    player_x = calculate_x_coordinate(5)  # Start position, change this number to spawn in a different place
    player_y = calculate_y_coordinate(SURFACE)
    
    # 8.5 should be standard speed
    player_speed = 8.5 * scale_factor # Adjust player speed according to their resolution
    player_vel_x = 0 # Horizontal velocity for friction/sliding
    player_vel_y = 0 # Vertical velocity for jumping
    gravity = 1.25 * scale_factor # Gravity effect (Greater number means stronger gravity)
    jump_power = -18 * scale_factor # Jump strength (Bigger negative number means higher jump)
    on_ground = False # Track if player is on the ground
    doubleJumpBoots = False # Track if player has double jump boots
    doubleJumped = False # Track if player double jumped already
    frostWalkBoots = False # Track if player has frost walk boots

    animation_index = 0  # Alternates between 0 and 1
    animation_timer = 0  # Tracks when to switch frames
    animation_speed = 4  # Adjust this to control animation speed
    direction = 1  # 1 for right, -1 for left

    normal_friction = 0.25
    ice_friction = 0.95  # Lower friction for slippery effect
    on_ice = False

    checkpoints = [(player_x, player_y), (calculate_x_coordinate(77), calculate_y_coordinate(SURFACE-5)), (calculate_x_coordinate(153), calculate_y_coordinate(SURFACE-4))]
    checkpoint_bool = [False] * len(checkpoints)
    checkpoint_bool[0] = True
    checkpoint_idx = 0
    dying = False
    death_count = 0
    collidable_tiles = {1, 2, 3, 6, 9, 15, 21, 22}
    dying_tiles = {3, 7, 11, 17, 18, 19}

    coin_count = 0

    # State Variables for Gadgets
    bubbleJump = False
    bubbleJump_respawns = {}
    dash_respawns = {}
    dashing = False
    dash_duration = 0
    super_speed_effects = []
    super_speed_respawns = {}
    higherJumps = False
    higherJumps_respawns = {}
    up_dash_respawns = {}

    running = True
    while running:
        
        screen.blit(background, (0, 0))
        # Draw level using tile images
        for row_index, row in enumerate(level_map):
            for col_index, tile in enumerate(row):
                x, y = col_index * TILE_SIZE - camera_x, row_index * TILE_SIZE
                if tile == 0 or tile == 15: # Continue if the tile is an air block or invisible platform
                    continue
                screen.blit(tiles.get(tile), (x, y)) # Draw according to the dictionary

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

        for i in signs:  # Adding signs
            x = i * TILE_SIZE - camera_x
            y = (ground_levels[i] - 1) * TILE_SIZE  # Place rocks 1 tile above the ground
            screen.blit(sign, (x, y))

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
        npc_x = calculate_x_coordinate(8)  # First NPC's x position
        npc_y = (SURFACE) * TILE_SIZE  # First NPC's y position
        player_rect = pygame.Rect(player_x - camera_x, player_y, TILE_SIZE, TILE_SIZE)
        npc_rect = pygame.Rect(npc_x - camera_x, npc_y, TILE_SIZE, TILE_SIZE)

        # Handle first NPC dialogue
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()  # Get current time in milliseconds
        handle_level_3_npc_1_dialogue(screen, player_rect, npc_rect, keys, current_time)

        # Check if player is near the second NPC
        npc_x = calculate_x_coordinate(52)  # Second NPC's x position
        npc_y = (SURFACE - 5) * TILE_SIZE  # Second NPC's y position
        player_rect = pygame.Rect(player_x - camera_x, player_y, TILE_SIZE, TILE_SIZE)
        npc_rect = pygame.Rect(npc_x - camera_x, npc_y, TILE_SIZE, TILE_SIZE)

        # Handle second NPC dialogue
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()  # Get current time in milliseconds
        handle_level_3_npc_2_dialogue(screen, player_rect, npc_rect, keys, current_time)

        # Check if player is near the third NPC
        npc_x = calculate_x_coordinate(208)  # Third NPC's x position
        npc_y = 11 * TILE_SIZE  # Third NPC's y position
        player_rect = pygame.Rect(player_x - camera_x, player_y, TILE_SIZE, TILE_SIZE)
        npc_rect = pygame.Rect(npc_x - camera_x, npc_y, TILE_SIZE, TILE_SIZE)

        # Handle third NPC dialogue
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()  # Get current time in milliseconds
        handle_level_3_npc_3_dialogue(screen, player_rect, npc_rect, keys, current_time)

        # Check if player is near the fourth NPC
        npc_x = calculate_x_coordinate(237)  # Fourth NPC's x position
        npc_y = (SURFACE - 14) * TILE_SIZE  # Fourth NPC's y position
        player_rect = pygame.Rect(player_x - camera_x, player_y, TILE_SIZE, TILE_SIZE)
        npc_rect = pygame.Rect(npc_x - camera_x, npc_y, TILE_SIZE, TILE_SIZE)

        # Handle fourth NPC dialogue
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()  # Get current time in milliseconds
        handle_level_3_npc_4_dialogue(screen, player_rect, npc_rect, keys, current_time)   

        acceleration = 0.5  # Slower acceleration on ice
        friction = normal_friction if not on_ice else ice_friction

        # Handle events
        keys = pygame.key.get_pressed()
        moving = False
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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Jumping Logic (Space Pressed)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if higherJumps:
                        player_vel_y = jump_power * 2
                        higherJumps = False
                    elif on_ground:
                        player_vel_y = jump_power  # Normal jump
                        on_ground = False
                        doubleJumped = False  # Reset double jump when landing
                    elif doubleJumpBoots and not doubleJumped:
                        player_vel_y = jump_power  # Double jump
                        doubleJumped = True  # Mark double jump as used
                    elif bubbleJump:
                        player_vel_y = jump_power  # jump again
                        bubbleJump = False


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

        level_name_font = pygame.font.Font('PixelifySans.ttf', 48)  # Larger font for level name
        level_name_text = level_name_font.render("Level 3", True, WHITE)  # White text

        screen.blit(level_name_text, (20, 20))  # Position at (20, 20)

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

                    if tile == 15: # If walkway, ignore collision from left and right and from bottom
                        continue
                    # This code block ensures collision with solid blocks from the left and right
                    if (player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):  # If the player is at the same height as the block
                        if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and player_x + TILE_SIZE - player_speed <= tile_x):  
                            # Moving right into a block
                            player_x = tile_x - TILE_SIZE  

                        elif (player_x < tile_x + TILE_SIZE and player_x + TILE_SIZE > tile_x and player_x + player_speed >= tile_x + TILE_SIZE):  
                            # Moving left into a block
                            player_x = tile_x + TILE_SIZE

                    # This code block ensures collision with solid blocks above their head
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and  
                        player_y < tile_y + TILE_SIZE and player_y - player_vel_y >= tile_y + TILE_SIZE):

                        player_y = tile_y + TILE_SIZE  # Align player below the ceiling
                        player_vel_y = 0  # Stop upward motion

                # If player dies
                if tile in dying_tiles:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE >= tile_x and player_x <= tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE >= tile_y and player_y <= tile_y + TILE_SIZE):
                        # Ice boots functionality - change water to ice
                        if frostWalkBoots and tile == 3:
                            current_x = calculate_column(player_x)
                            current_y = calculate_row(player_y)+1
                            level_map[current_y][current_x] = 21  # Turn the starting tile into ice
                        else:
                            dying = True

                # Coin
                if tile == 12:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):

                        coin_count += 1
                        level_map[row_index][col_index] = 0

                if tile == 21 or tile == 22 or tile == 28:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and  
                        player_y + TILE_SIZE == tile_y):  # Feet touching top of ice
                        on_ice = True

                # -------------------------------- Gadget/Powerup Pickup Functionality -------------------------------- #
                # Bubble jump reset
                if tile == 4: 
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
                        level_map[row_index][col_index] = 0  # Remove the jump reset from screen
                        bubbleJump = True
                        doubleJumped = False
                        bubbleJump_respawns[(row_index, col_index)] = pygame.time.get_ticks() + 5000

                # Dash
                if tile == 5:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):

                        dash_pickup_time = pygame.time.get_ticks()
                        dash_respawns[(row_index, col_index)] = pygame.time.get_ticks() + 5000
                        dash_duration = dash_pickup_time + 700
                        dashing = True
                        level_map[row_index][col_index] = 0 
                        player_speed = player_speed * 3
                        direction = 1
                        if player_speed < 0:
                            player_speed *= -1

                # Ice boots
                if tile == 10:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
                        level_map[row_index][col_index] = 0  # Remove the boots from screen
                        frostWalkBoots = True
                        
                if tile == 16:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
                        level_map[row_index][col_index] = 0  # Remove the boots from screen
                        doubleJumpBoots = True
                        doubleJumped = False

                # Super Speed Powerup
                if tile == 20: 
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):

                        level_map[row_index][col_index] = 0
                        player_speed *= 2.5  # Double the speed
                        super_speed_effects.append({"end_time": pygame.time.get_ticks() + 1600})  # 1.6 sec effect
                        super_speed_respawns[(row_index, col_index)] = pygame.time.get_ticks() + 5000  # 5 sec respawn

                # High Jump
                if tile == 23:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
                        level_map[row_index][col_index] = 0  # Remove the boots from screen
                        higherJumps = True
                        higherJumps_respawns[(row_index, col_index)] = pygame.time.get_ticks() + 5000

                # Up Dash
                if tile == 24:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
                        level_map[row_index][col_index] = 0 
                        player_vel_y = -30
                        up_dash_respawns[(row_index, col_index)] = pygame.time.get_ticks() + 5000


        
        if player_x + TILE_SIZE >= level_width * TILE_SIZE:  # If player reaches the end of the level
            show_level_completed_screen(slot, death_count)
            running = False

        if player_x <= 0: # Ensure player is within the bounds of the level and does not go to the left
            player_x = 0

        if player_y + TILE_SIZE >= level_height * TILE_SIZE:
            dying = True

        if dying:
            player_x, player_y = checkpoints[checkpoint_idx][0], checkpoints[checkpoint_idx][1]
            death_count += 1
            dying = False
            if checkpoint_idx == 0:
                frostWalkBoots = False
                level_map[5][24] = 10 # Frost Walking Boots
            elif checkpoint_idx == 1:
                doubleJumpBoots = False
                level_map[SURFACE-5][82] = 16 # Double Jump Boots
            elif checkpoint_idx == 2:
                frostWalkBoots = False
                doubleJumpBoots = False
                level_map[3][204] = 10 # Frost Walking Boots
                level_map[3][216] = 16 # Double Jump Boots

        for k, checkpoint in enumerate(checkpoints):
            x, y = checkpoint
            if player_x >= x and player_y <= y and not checkpoint_bool[k]:
                checkpoint_idx += 1
                checkpoint_bool[k] = True
                if checkpoint_idx == 1 and frostWalkBoots: # Remove Frost Walk Boots Effect
                    frostWalkBoots = False
                elif checkpoint_idx == 2 and doubleJumpBoots: # Remove Double Jump Boots Effect
                    doubleJumpBoots = False

        # ------------------------------- Power-up Respawns ---------------------------------- #
        current_time = pygame.time.get_ticks()
        # Respawn bubble jump reset after 5 seconds
        bubble_removes = []
        for pos, respawn_time in bubbleJump_respawns.items():
            if current_time >= respawn_time:
                level_map[pos[0]][pos[1]] = 4  # Respawn power-up
                bubble_removes.append(pos)  # Mark for removal

        # Respawn higher jump reset after 5 seconds
        jumps_removes = []
        for pos, respawn_time in higherJumps_respawns.items():
            if current_time >= respawn_time:
                level_map[pos[0]][pos[1]] = 23  # Respawn power-up
                jumps_removes.append(pos)  # Mark for removal

        # Set speed back for player if dashing
        if dashing:
            if (current_time >= dash_duration) and (dash_duration != 0):
                player_speed = 8.5 * scale_factor
                dashing = False
                dash_duration = 0

        # Respawn dash powerup after 5 seconds
        dash_remove = []
        for pos, respawn_time in dash_respawns.items():
            if current_time >= respawn_time:
                level_map[pos[0]][pos[1]] = 5  # Respawn power-up
                dash_remove.append(pos)  # Mark for removal

        # Respawn power-ups after 5 seconds
        to_remove = []
        for pos, respawn_time in super_speed_respawns.items():
            if current_time >= respawn_time:
                level_map[pos[0]][pos[1]] = 20  # Respawn power-up
                to_remove.append(pos)  # Mark for removal

        # Apply speed effects from multiple power-ups
        for effect in super_speed_effects[:]:  # Iterate over a copy of the list
            if current_time >= effect["end_time"]:  # Check if effect expired
                player_speed /= 2.5
                super_speed_effects.remove(effect)

        up_dash_removes = []
        for pos, respawn_time in up_dash_respawns.items():
            if current_time >= respawn_time:
                level_map[pos[0]][pos[1]] = 24  # Respawn power-up
                up_dash_removes.append(pos)  # Mark for removal
                    
        # Camera follows player
        camera_x = max(0, min(player_x - WIDTH // 2, (level_width * TILE_SIZE) - WIDTH))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()  # Update display

if __name__ == "__main__":
    level_3(1)
    pygame.quit()