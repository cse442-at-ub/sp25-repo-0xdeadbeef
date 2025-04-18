import pygame # type: ignore
import sys
import world_select
from saves_handler import *
from firework_level_end import show_level_complete_deaths
from pause_menu import PauseMenu  # Import the PauseMenu class

from NPCs.level_6_npc_1 import handle_level_6_npc_1_dialogue  # Import the functionality of the first NPC from level 6
from NPCs.level_6_npc_2 import handle_level_6_npc_2_dialogue  # Import the functionality of the second NPC from level 6
from NPCs.level_6_npc_3 import handle_level_6_npc_3_dialogue  # Import the functionality of the third NPC from level 6
from NPCs.level_6_npc_4 import handle_level_6_npc_4_dialogue  # Import the functionality of the fourth NPC from level 6

# Initialize PyGame
pygame.init()

pygame.mixer.init() # Initialize Pygame Audio Mixer

# Load the level complete sound 
level_complete_sound = pygame.mixer.Sound("Audio/LevelComplete.mp3")

# Gadget pick up sound 
gadget_sound = pygame.mixer.Sound("Audio/GadgetPickUp.mp3")

# Death sound 
death_sound = pygame.mixer.Sound("Audio/Death.mp3")

# Super speed power up sound
super_speed_sound = pygame.mixer.Sound("Audio/SuperSpeed.mp3")

# Dash power up sound
dash_sound = pygame.mixer.Sound("Audio/Dash.mp3")

# Power up sound (global)
power_up_sound = pygame.mixer.Sound("Audio/PowerUpPickUp.mp3") 

# Spring sound 
spring_sound = pygame.mixer.Sound("Audio/Spring.mp3")

# Coin pick up sound 
coin_sound = pygame.mixer.Sound("Audio/Coin.mp3")

# Screen settings
BASE_WIDTH = 1920
BASE_HEIGHT = 1080

SAVE_DIR = "User Saves"

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h # Will only work with resolutions 1920 x 1080 or better

TILE_SIZE = HEIGHT // 30  # Readjusted according to user resolution

scale_factor = HEIGHT / BASE_HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Level 6")

ground_tile = pygame.image.load("./desert_images/ground.png")
ground_tile = pygame.transform.scale(ground_tile, (TILE_SIZE, TILE_SIZE))

floating_ground = ground_tile

transparent_ground = pygame.image.load("./desert_images/ground.png").convert_alpha()
transparent_ground = pygame.transform.scale(transparent_ground, (TILE_SIZE, TILE_SIZE))
transparent_ground.set_alpha(50)  # 0 = fully transparent, 255 = fully opaque

background = pygame.image.load("./desert_images/background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

platform_tile = pygame.image.load("./desert_images/platform.png")
platform_tile = pygame.transform.scale(platform_tile, (TILE_SIZE, TILE_SIZE))

transparent_platform = pygame.image.load("./desert_images/platform.png").convert_alpha()
transparent_platform = pygame.transform.scale(transparent_platform, (TILE_SIZE, TILE_SIZE))  # 0 = fully transparent, 255 = fully opaque
transparent_platform.set_alpha(50)  # 0 = fully transparent, 255 = fully opaque

dirt_tile = pygame.image.load("./desert_images/dirt.png")
dirt_tile = pygame.transform.scale(dirt_tile, (TILE_SIZE, TILE_SIZE))

transparent_dirt = pygame.image.load("./desert_images/dirt.png").convert_alpha()
transparent_dirt = pygame.transform.scale(transparent_dirt, (TILE_SIZE, TILE_SIZE))
transparent_dirt.set_alpha(50)  # 0 = fully transparent, 255 = fully opaque

background_dead_tree = pygame.image.load("./desert_images/background_dead_tree.png")
background_dead_tree = pygame.transform.scale(background_dead_tree, (TILE_SIZE, TILE_SIZE))

cactus_with_rock = pygame.image.load("./desert_images/cactus_with_rock.png")
cactus_with_rock = pygame.transform.scale(cactus_with_rock, (TILE_SIZE, TILE_SIZE))

cactus = pygame.image.load("./desert_images/cactus.png")
cactus = pygame.transform.scale(cactus, (TILE_SIZE, TILE_SIZE))

dead_tree = pygame.image.load("./desert_images/dead_tree.png")
dead_tree = pygame.transform.scale(dead_tree, (TILE_SIZE, TILE_SIZE))

full_cactus = pygame.image.load("./desert_images/full_cactus.png")
full_cactus = pygame.transform.scale(full_cactus, (TILE_SIZE * 1.5, TILE_SIZE * 2))

palm_tree_with_rock = pygame.image.load("./desert_images/palm_tree_with_rock.png")
palm_tree_with_rock = pygame.transform.scale(palm_tree_with_rock, (TILE_SIZE * 2.5, TILE_SIZE * 3))

pyramids = pygame.image.load("./desert_images/pyramids.png")
pyramids = pygame.transform.scale(pyramids, (TILE_SIZE * 6, TILE_SIZE * 2))

rock = pygame.image.load("./desert_images/rock.png")
rock = pygame.transform.scale(rock, (TILE_SIZE, TILE_SIZE // 2))

thorns = pygame.image.load("./desert_images/thorns.png")
thorns = pygame.transform.scale(thorns, (TILE_SIZE, TILE_SIZE))
flipped_thorn = pygame.transform.flip(thorns, False, True)
left_thorn = pygame.transform.rotate(thorns, 90)
right_thorn = pygame.transform.rotate(thorns, -90)

water = pygame.image.load("./desert_images/water.png")
water = pygame.transform.scale(water, (TILE_SIZE, TILE_SIZE))

water_block = pygame.image.load("./images/water_block.png")
water_block = pygame.transform.scale(water_block, (TILE_SIZE, TILE_SIZE))

flag = pygame.image.load("./images/flag.png")
flag = pygame.transform.scale(flag, (TILE_SIZE, TILE_SIZE))

sand = pygame.image.load("./desert_images/sand.png")
sand = pygame.transform.scale(sand, (TILE_SIZE, TILE_SIZE))

coin = pygame.image.load("./desert_images/coin.png")
coin = pygame.transform.scale(coin, (TILE_SIZE, TILE_SIZE))

high_jump = pygame.image.load("./images/high_jump.png")
high_jump = pygame.transform.scale(high_jump, (TILE_SIZE, TILE_SIZE))

transparent_high_jump = pygame.image.load("./images/high_jump.png").convert_alpha()
transparent_high_jump = pygame.transform.scale(transparent_high_jump, (TILE_SIZE, TILE_SIZE))  # 0 = fully transparent, 255 = fully opaque
transparent_high_jump.set_alpha(50)  # 0 = fully transparent, 255 = fully opaque

speed_boots = pygame.image.load("./images/speed_boots.png")
speed_boots = pygame.transform.scale(speed_boots, (TILE_SIZE, TILE_SIZE))

balloon = pygame.image.load("./images/balloon.png")
balloon = pygame.transform.scale(balloon, (TILE_SIZE, TILE_SIZE))

jump_reset = pygame.image.load("./images/bubble.png")
jump_reset = pygame.transform.scale(jump_reset, (TILE_SIZE, TILE_SIZE))

double_jump_boots = pygame.image.load("./images/boots.png")
double_jump_boots = pygame.transform.scale(double_jump_boots, (TILE_SIZE, TILE_SIZE))

spring = pygame.image.load("./images/spring.png")
spring = pygame.transform.scale(spring, (TILE_SIZE, TILE_SIZE))

transparent_spring = pygame.image.load("./images/spring.png").convert_alpha()
transparent_spring = pygame.transform.scale(transparent_spring, (TILE_SIZE, TILE_SIZE))  # 0 = fully transparent, 255 = fully opaque
transparent_spring.set_alpha(50)  # 0 = fully transparent, 255 = fully opaque

button = pygame.image.load("./images/button.png")
button = pygame.transform.scale(button, (TILE_SIZE, TILE_SIZE))
flipped_button = pygame.transform.flip(button, False, True)

super_speed_powerup = pygame.image.load("./images/super_speed_powerup.png")
super_speed_powerup = pygame.transform.scale(super_speed_powerup, (TILE_SIZE, TILE_SIZE))

sand_boots = pygame.image.load("./desert_images/sand_boots.png")
sand_boots = pygame.transform.scale(sand_boots, (TILE_SIZE, TILE_SIZE))

glider = pygame.image.load("./images/glider.png")
glider = pygame.transform.scale(glider, (TILE_SIZE, TILE_SIZE))

high_jump = pygame.image.load("./images/high_jump.png")
high_jump = pygame.transform.scale(high_jump, (TILE_SIZE, TILE_SIZE))

right_dash = pygame.image.load("./images/dash_powerup.png")
right_dash = pygame.transform.scale(right_dash, (TILE_SIZE, TILE_SIZE))
up_dash = pygame.transform.rotate(right_dash, 90)
left_dash = pygame.transform.flip(right_dash, True, False)

walkway = pygame.image.load("./desert_images/walkway.png")
walkway = pygame.transform.scale(walkway, (TILE_SIZE * 4, TILE_SIZE * 2))
flipped_walkway = pygame.transform.flip(walkway, True, False)  # Flip horizontally (True), no vertical flip (False)

invisible_platform = None
invisible_button = None

sign = pygame.image.load("./desert_images/sign.png")
sign = pygame.transform.scale(sign, (TILE_SIZE, TILE_SIZE))

npc_1 = pygame.image.load("./Character Combinations/black hair_dark_red shirt_brown pants.png")
npc_1 = pygame.transform.scale(npc_1, (TILE_SIZE, TILE_SIZE))

npc_2 = pygame.image.load("./Character Combinations/ginger hair_dark_yellow shirt_black pants.png")
npc_2 = pygame.transform.scale(npc_2, (TILE_SIZE, TILE_SIZE))

npc_3 = pygame.image.load("./Character Combinations/brown hair_white_red shirt_brown pants.png")
npc_3 = pygame.transform.scale(npc_3, (TILE_SIZE, TILE_SIZE))

npc_4 = pygame.image.load("./Character Combinations/ginger hair_white_yellow shirt_brown pants.png")
npc_4 = pygame.transform.scale(npc_4, (TILE_SIZE, TILE_SIZE))


#-----Gadget inventory images and dictionary

inventory = pygame.image.load("./images/inventory_slot.png").convert_alpha()
inventory = pygame.transform.scale(inventory, (250, 70))
inventory_x = (WIDTH - 250) // 2
inventory_y = HEIGHT - 100

inventory_jump_boots = pygame.image.load("./images/boots.png")
inventory_jump_boots = pygame.transform.scale(inventory_jump_boots, (42, 50))

inventory_sand_boots = pygame.image.load("./desert_images/sand_boots.png")
inventory_sand_boots = pygame.transform.scale(inventory_sand_boots, (42, 50))

inventory_glider = pygame.image.load("./images/glider.png")
inventory_glider = pygame.transform.scale(inventory_glider, (42, 50))

INV_SLOT_WIDTH = 42
INV_SLOT_HEIGHT = 45

first_slot = (inventory_x + 5, inventory_y + 10)
second_slot = (inventory_x + INV_SLOT_WIDTH + 10, inventory_y + 10)
third_slot = (inventory_x + (2*INV_SLOT_WIDTH + 20), inventory_y + 10)
fourth_slot = (inventory_x + (3*INV_SLOT_WIDTH + 40), inventory_y + 10)

# Set up the level with a width of 300 and a height of 30 rows
level_width = 300
level_height = HEIGHT // TILE_SIZE  # Adjust level height according to user's resolution

level_map = [[0] * level_width for _ in range(level_height)]  # Start with air
# Add solid ground at the very bottom
level_map.append([1] * level_width)
ground_levels = None

GROUND = level_height - 4 #Constant for the ground level
SURFACE = GROUND - 1 #Constant for the surface level

WHITE = (255, 255, 255)
RED = (255, 0, 0) # For timer
BLUE = (0, 0, 255) # For hover

# Initialize the PauseMenu
pause_menu = PauseMenu(screen)

level_map[SURFACE-6][56] = 12 # Coin
level_map[2][196] = 12 # Coin

# Dictionary containing which tile corresponds to what
tiles = {0: background, 1: ground_tile, 2: platform_tile, 3: dirt_tile,  4: thorns, 5: water, 6: water_block, 7: flag, 8: sand, 9: flipped_thorn, 10: left_thorn,
         11: right_thorn, 12: coin, 13: high_jump, 14: speed_boots, 15: balloon, 16: full_cactus, 17: jump_reset, 18: double_jump_boots, 19: spring, 20: button,
         21: flipped_button, 22: super_speed_powerup, 23: sand_boots, 24: glider, 25: high_jump, 26: right_dash, 27: up_dash, 28: left_dash, 29: walkway, 30: flipped_walkway,
         31: transparent_ground, 32: transparent_dirt, 33: transparent_high_jump, 34: pyramids, 35: npc_1, 36: npc_2, 37: npc_3, 38: npc_4, 39: floating_ground, 40: sign,
         41: full_cactus, 42: invisible_platform, 43: transparent_spring, 44: transparent_platform, 45: invisible_button}

rocks = {61, 118, 196} # Column numbers for all the rocks
cacti = {64, 167} # Column number for the cactuses
full_cacti = {9, 183, 284} # Column number for the full cactuses
palm_tree_with_rocks = {86, 104} # Column number for the palm_tree_with_rock
signs = {282} # Column numbers for signs

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

def show_level_completed_screen(slot: int, death_count: int):
    # Stop level 6 music
    pygame.mixer.music.stop()

    # Play the level complete sound once when this function runs
    level_complete_sound.play()

    respawn_gadgets() # Respawn all gadgets on the level
    respawn_powerups() # Respawn all powerups on the level

    update_save(slot, {"Level 6 Checkpoint": 0}) # Set checkpoint to 0

    level_name = "Level Six"
    
    show_level_complete_deaths(slot, 0, death_count, level_name)

def show_game_over_screen(slot: int):
    
    respawn_gadgets() # Respawn all gadgets on the level
    respawn_powerups() # Respawn all powerups on the level

    update_save(slot, {"Level 6 Checkpoint": 0}) # Set checkpoint to 0

def respawn_terrain():
    for row_index in range(GROUND, level_height):
        row = [1] * level_width  # Default to full ground row
        for col_index in range(15, 60):  # Remove ground in columns [15 - 60)
            row[col_index] = 0  # Set to air (pit)
        for col_index in range(80, 85):  # Remove ground in columns [80 - 85)
            row[col_index] = 0  # Set to air (pit)
        for col_index in range(90, 103):  # Remove ground in columns [90 - 103)
            row[col_index] = 0  # Set to air (pit)
        for col_index in range(110, 115):  # Remove ground in columns [110 - 115)
            row[col_index] = 0  # Set to air (pit)
        for col_index in range(125, 160):  # Remove ground in columns [125 - 160)
            row[col_index] = 0  # Set to air (pit)
        for col_index in range(200, 280):  # Remove ground in columns [200 - 280)
            row[col_index] = 0  # Set to air (pit)
        level_map[row_index] = row  # Add row to level map

    for row_index in range(SURFACE-3, GROUND): # Raised Ground
        level_map[row_index][0:15] = [1] * 15
    for row_index in range(SURFACE-5, level_height): # Raised Ground
        level_map[row_index][30] = 1
    for row_index in range(SURFACE, level_height): # Raised Ground
        level_map[row_index][37] = 1
    for row_index in range(SURFACE-12, SURFACE-5): # Floating Dirt Block
        level_map[row_index][37] = 3
    for row_index in range(SURFACE-13, level_height): # Raised Ground
        level_map[row_index][59] = 1
    for row_index in range(SURFACE-7, level_height): # Raised Ground
        level_map[row_index][53] = 1
    level_map[level_height-1][56] = 1 # Platform for Spring
    level_map[GROUND][70:80] = [8] * 10
    for row_index in range(GROUND+1, level_height): # Sand
        level_map[row_index][70:80] = [3] * 10
    for row_index in range(0, SURFACE-11): # Dirt
        level_map[row_index][95] = 3
    for row_index in range(0, SURFACE-5): # Dirt
        level_map[row_index][104] = 3
    for row_index in range(5, GROUND): # Raised Ground
        level_map[row_index][120:125] = [1] * 5
    for row_index in range(0, SURFACE-14): # Dirt
        level_map[row_index][132] = 3
    for row_index in range(5, GROUND): # Raised Ground
        level_map[row_index][160:165] = [1] * 5
    for row_index in range(0, GROUND): # Dirt
        level_map[row_index][189] = 3
    level_map[GROUND][155:160] = [31] * 5 # Transparent Ground
    for row_index in range(GROUND+1, level_height): # Transparent Dirt
        level_map[row_index][155:160] = [32] * 5

    # Make terrain before this line (unless it's floating). The next code block calculates the ground levels.

    # Find the ground level for each column
    global ground_levels
    ground_levels = [len(level_map)] * len(level_map[0])
    # Find the ground level for each column
    for row_index, row in enumerate(level_map):
        for col_index, tile in enumerate(row):
            if (tile == 1) and ground_levels[col_index] == len(level_map):
                ground_levels[col_index] = row_index

    level_map[SURFACE-4][13:15] = [4] * 2 # Thorns

    level_map[SURFACE-12][20] = 2 # Platform Tile
    level_map[SURFACE-16][22] = 2 # Platform Tile

    level_map[SURFACE-13][30:59] = [39] * 29 # Floating Ground
    level_map[SURFACE-1][20] = 2 # Platform Tile

    level_map[SURFACE-6][30] = 4 # Thorn
    for row_index in range(SURFACE-5, level_height):
        level_map[row_index][29] = 10 # Left Thorns
        level_map[row_index][31] = 11 # Right Thorns

    level_map[7][53:56] = [44] * 3 # Platform Tiles
    level_map[level_height-1][34] = 31 # Ground
    level_map[level_height-2][34] = 43 # Spring --------------------------------------------------------------

    level_map[7][30:32] = [2] * 2 # Platform Tiles
    level_map[7][38:41] = [2] * 3 # Platform Tiles

    level_map[SURFACE-14][30:60] = [4] * 30 # Thorns
    level_map[SURFACE-5][37] = 9 # Flipped Thorn
    for row_index in range(SURFACE-12, SURFACE-5):
        level_map[row_index][36] = 10 # Left Thorns
        level_map[row_index][38] = 11 # Right Thorns
    level_map[SURFACE-1][37] = 4 # Thorn

    for row_index in range(SURFACE-7, level_height):
        level_map[row_index][52] = 10 # Left Thorns
        level_map[row_index][54] = 11 # Right Thorns
    level_map[level_height-2][56] = 19 # Spring

    for row_index in range(SURFACE-12, level_height):
        level_map[row_index][58] = 10 # Left Thorns

    level_map[6][31] = 4 # Thorn
    level_map[6][38] = 4 # Thorn

    level_map[SURFACE-12][48] = 21 # Flipped Button
    level_map[SURFACE][66] = 7 # Flag

    level_map[SURFACE][70] = 40 # Sign
    level_map[SURFACE-1][72] = 41 # Full Cactus

    level_map[SURFACE-5][80:90] = [8] * 10 # Second Layer of Sand
    level_map[SURFACE-5][95:105] = [8] * 10 # Second Layer of Sand

    level_map[SURFACE-11][89:96] = [8] * 7 # Third Layer of Sand

    level_map[SURFACE-6][89] = 4 # Thorn
    level_map[4][96:99] = [39] * 3 # Floating Ground
    level_map[SURFACE][109] = 4 # Thorn

    level_map[4][116] = 30 # Flipped Walkway
    level_map[5][116:120] = [42] * 4 # Invisible Platform to be walked on

    level_map[4][122] = 7 # Flag

    level_map[4][125] = 29 # Walkway
    level_map[5][125:129] = [42] * 4 # Invisible Platform to be walked on

    level_map[SURFACE-14][125:129] = [45] * 4 # Invisible Button

    level_map[9][128] = 30 # Flipped Walkway
    level_map[10][128:132] = [42] * 4 # Invisible Platform to be walked on

    level_map[4][156] = 30 # Flipped Walkway
    level_map[5][156:160] = [42] * 4 # Invisible Platform to be walked on

    level_map[4][162] = 7 # Flag

    row = 5
    col = 165
    for i in range(4):
        level_map[row][col:col+20] = [39] * 20 # Ground
        row += 5
        col = col + 4 if i % 2 == 0 else col - 4

    level_map[4][175] = 4 # Thorn
    level_map[SURFACE-16][175] = 4 # Thorn
    level_map[SURFACE-11][175] = 4 # Thorn
    level_map[SURFACE-6][175] = 4 # Thorn
    level_map[SURFACE][175] = 4 # Thorn

    level_map[4][167] = 20 # Button

    level_map[SURFACE][193] = 7 # Flag

    level_map[SURFACE-2][215] = 2 # Platform Tile
    level_map[SURFACE-5][215] = 2 # Platform Tile

    level_map[6][207] = 8 # Sand
    level_map[6][204] = 39 # Platform containing thorn
    level_map[5][204] = 4 # Thorn
    level_map[9][202] = 8 # Sand

    level_map[4][196] = 8 # Sand

    level_map[7][240] = 2 # Platform Tile

    level_map[SURFACE-1][289] = 34 # Pyramid

def respawn_gadgets():
    level_map[SURFACE-2][20] = 18 # Double Jump Boots
    level_map[SURFACE-12][93] = 23 # Sand Boots
    level_map[3][97] = 24 # Glider

    level_map[6][240] = 24 # Glider

def respawn_powerups():
    level_map[SURFACE-10][11] = 17 # Jump Reset

    level_map[SURFACE][17] = 17 # Jump Reset
    level_map[SURFACE-5][26] = 17 # Jump Reset
    level_map[SURFACE][34] = 17 # Jump Reset
    level_map[SURFACE-2][42] = 17 # Jump Reset
    level_map[SURFACE-7][48] = 17 # Jump Reset

    level_map[6][40] = 22 # Super Speed Powerup

    level_map[SURFACE-3][117] = 27 # Up Dash
    level_map[SURFACE-8][117] = 27 # Up Dash
    level_map[SURFACE-13][117] = 27 # Up Dash
    level_map[SURFACE-18][117] = 27 # Up Dash

    # Past the 1st Flag
    level_map[SURFACE-2][75] = 17 # Jump Reset
    level_map[SURFACE-4][77] = 17 # Jump Reset

    level_map[SURFACE-8][85] = 17 # Jump Reset
    level_map[SURFACE-10][87] = 17 # Jump Reset

    level_map[SURFACE-6][102] = 25 # High Jump
    
    for col_index in range(130, 150, 6):
        level_map[SURFACE-5][col_index] = 17 # Jump Reset
    level_map[SURFACE-9][133] = 17 # Jump Reset
    level_map[SURFACE-9][139] = 17 # Jump Reset
    level_map[SURFACE-8][148] = 28 # Left Dash

    level_map[4][171] = 22 # Super Speed Powerup
    level_map[9][179] = 22 # Super Speed Powerup
    level_map[SURFACE-11][171] = 22 # Super Speed Powerup
    level_map[SURFACE-6][179] = 22 # Super Speed Powerup
    level_map[SURFACE][171] = 22 # Super Speed Powerup

    level_map[SURFACE][198] = 22 # Super Speed Powerup

    level_map[SURFACE-1][211] = 17 # Jump Reset

    level_map[SURFACE-6][215] = 25 # High Jump

    level_map[6][199] = 17 # Jump Reset

    level_map[8][223] = 17 # Jump Reset
    level_map[5][226] = 26 # Right Dash

    level_map[8][236] = 17 # Jump Reset

    level_map[SURFACE][157] = 33 # Transparent High Jump
    level_map[7][157] = 17 # Jump Reset

def respawn_npcs():
    level_map[SURFACE-4][7] = 35       # First NPC
    level_map[SURFACE][68] = 36        # Second NPC
    level_map[SURFACE-21][124] = 37    # Third NPC
    level_map[SURFACE][194] = 38       # Fourth NPC
    
timer = None

def button_spawn(btn_idx):
    global timer
    if btn_idx == 1: # Spawns in the ground and the spring and the platform to proceed
        level_map[7][53:56] = [2] * 3 # Platform Tiles
        level_map[level_height-1][34] = 1 # Ground
        level_map[level_height-2][34] = 19 # Spring
    elif btn_idx == 2: # Supposed to wait 10 seconds after pressing this invisible button then spawn in the transparent ground
        timer = 10
    elif btn_idx == 3: # Despawns the dirt and turns it into air
        for row_index in range(SURFACE-4, GROUND): # Dirt
            level_map[row_index][189] = 0 # Air
        timer = 15

def button_despawn():
    level_map[7][53:56] = [44] * 3 # Transparent Platform Tiles
    level_map[level_height-1][34] = 31 # Transparent Ground
    level_map[level_height-2][34] = 43 # Transparent Spring

    level_map[GROUND][155:160] = [31] * 5 # Transparent Ground
    for row_index in range(GROUND+1, level_height): # Transparent Dirt
        level_map[row_index][155:160] = [32] * 5
    level_map[SURFACE][157] = 33 # Transparent High Jump
    for row_index in range(SURFACE-4, GROUND): # Air currently
        level_map[row_index][189] = 3 # Set back to dirt

def level_6(slot: int):

    respawn_terrain()
    respawn_gadgets()
    respawn_powerups()
    respawn_npcs()

    # Stop any previously playing music 
    pygame.mixer.music.stop()
    
    # Load the tutorial music
    pygame.mixer.music.load("Audio/Level6.mp3")
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

    checkpoints = [(calculate_x_coordinate(5), calculate_y_coordinate(SURFACE-4)), (calculate_x_coordinate(66), calculate_y_coordinate(SURFACE)),
                   (calculate_x_coordinate(122), calculate_y_coordinate(4)), (calculate_x_coordinate(162), calculate_y_coordinate(4)), (calculate_x_coordinate(193), calculate_y_coordinate(SURFACE))]
    checkpoint_bool = [False] * len(checkpoints)
    checkpoint_bool[0] = True
    checkpoint_idx = load_save(slot).get("Level 6 Checkpoint")
    if not checkpoint_idx:
        checkpoint_idx = 0
    for i in range(checkpoint_idx+1):
        checkpoint_bool[i] = True

    # Camera position
    camera_x = 0
    # (5, SURFACE-4) should be the starting point
    player_x = checkpoints[checkpoint_idx][0]  # Start x position, change this number to spawn in a different place
    player_y = checkpoints[checkpoint_idx][1]  # Start y position, change this number to spawn in a different place

    # 8.5 should be standard speed
    player_speed = 8.5 * scale_factor # Adjust player speed according to their resolution
    default_speed = player_speed
    player_vel_x = 0 # Horizontal velocity for friction/sliding
    player_vel_y = 0 # Vertical velocity for jumping
    gravity = 1.25 * scale_factor # Gravity effect (Greater number means stronger gravity)
    jump_power = -18 * scale_factor # Jump strength (Bigger negative number means higher jump)
    on_ground = False # Track if player is on the ground

    bubbleJump = False
    higherJumps = False

    doubleJumpBoots = False
    sandBoots = False
    glider = False
    powerup_respawns = {}
    super_speed_effects = []
    current_x = 0
    current_y = 0
    latestTile = 0
    dashed = False
    dash_duration = 0

    coin_count = 0

    animation_index = 0  # Alternates between 0 and 1
    animation_timer = 0  # Tracks when to switch frames
    animation_speed = 4  # Adjust this to control animation speed
    direction = 1  # 1 for right, -1 for left

    normal_friction = 0.25
    ice_friction = 0.95  # Lower friction for slippery effect
    on_ice = False

    dying = False
    death_count = load_save(slot).get("Level 6 Deaths")
    if not death_count:
        death_count = 0

    collidable_tiles = {1, 2, 3, 8, 39, 42}
    dying_tiles = {4, 5, 6, 9, 10, 11}

    clock = pygame.time.Clock()

    running = True
    while running:
        
        #print(f"Row: SURFACE - {SURFACE - calculate_row(player_y)}")
        #print(f"Column: {calculate_column(player_x)}")

        screen.blit(background, (0, 0))

                        # Check if player is near the first NPC
        npc_x = calculate_x_coordinate(7)  # First NPC's x position
        npc_y = (SURFACE-4) * TILE_SIZE  # First NPC's y position
        player_rect = pygame.Rect(player_x - camera_x, player_y, TILE_SIZE, TILE_SIZE)
        npc_rect = pygame.Rect(npc_x - camera_x, npc_y, TILE_SIZE, TILE_SIZE)

        # Handle first NPC dialogue
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()  # Get current time in milliseconds
        handle_level_6_npc_1_dialogue(screen, player_rect, npc_rect, keys, current_time)

        # Check if player is near the second NPC
        npc_x = calculate_x_coordinate(68)  # Second NPC's x position
        npc_y = (SURFACE) * TILE_SIZE  # Second NPC's y position
        player_rect = pygame.Rect(player_x - camera_x, player_y, TILE_SIZE, TILE_SIZE)
        npc_rect = pygame.Rect(npc_x - camera_x, npc_y, TILE_SIZE, TILE_SIZE)

        # Handle second NPC dialogue
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()  # Get current time in milliseconds
        handle_level_6_npc_2_dialogue(screen, player_rect, npc_rect, keys, current_time)

        # Check if player is near the third NPC
        npc_x = calculate_x_coordinate(124)  # Third NPC's x position
        npc_y = (SURFACE-22) * TILE_SIZE  # Third NPC's y position
        player_rect = pygame.Rect(player_x - camera_x, player_y, TILE_SIZE, TILE_SIZE)
        npc_rect = pygame.Rect(npc_x - camera_x, npc_y, TILE_SIZE, TILE_SIZE)

        # Handle third NPC dialogue
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()  # Get current time in milliseconds
        handle_level_6_npc_3_dialogue(screen, player_rect, npc_rect, keys, current_time)

        # Check if player is near the fourth NPC
        npc_x = calculate_x_coordinate(194)  # Fourth NPC's x position
        npc_y = (SURFACE) * TILE_SIZE  # Fourth NPC's y position
        player_rect = pygame.Rect(player_x - camera_x, player_y, TILE_SIZE, TILE_SIZE)
        npc_rect = pygame.Rect(npc_x - camera_x, npc_y, TILE_SIZE, TILE_SIZE)

        # Handle fourth NPC dialogue
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()  # Get current time in milliseconds
        handle_level_6_npc_4_dialogue(screen, player_rect, npc_rect, keys, current_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Pass events to the PauseMenu
            pause_menu.handle_event(event, slot)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if bubbleJump and doubleJumpBoots and not doubleJumped:
                    player_vel_y = jump_power  # Double jump
                    bubbleJump = False
                elif doubleJumpBoots and not doubleJumped:
                    player_vel_y = jump_power  # Double jumpit
                    doubleJumped = True  # Mark double jump as used
        if pause_menu.paused:
            clock.tick(60)
            continue

        # Draw level using tile images
        for row_index, row in enumerate(level_map):
            for col_index, tile in enumerate(row):
                x, y = col_index * TILE_SIZE - camera_x, row_index * TILE_SIZE
                if tile == 0 or tile == 42 or tile == 45: # Continue if the tile is an air block or invisible platform/button
                    continue
                screen.blit(tiles.get(tile), (x, y)) # Draw according to the dictionary

        # Draw dirt below ground
        for col_index, ground_y in enumerate(ground_levels):
            for row_index in range(ground_y + 1, len(level_map) + 10):  # Extra depth
                x, y = col_index * TILE_SIZE - camera_x, row_index * TILE_SIZE
                screen.blit(dirt_tile, (x, y))  # Draw dirt using image

        for i in rocks:  # Adding rocks
            x = i * TILE_SIZE - camera_x
            y = (ground_levels[i] - 1) * TILE_SIZE  # Place rocks 1 tile above the ground
            screen.blit(rock, (x, y + TILE_SIZE // 2))

        for i in cacti:  # Adding cactuses
            x = i * TILE_SIZE - camera_x
            y = (ground_levels[i] - 1) * TILE_SIZE
            screen.blit(cactus, (x, y))

        for i in full_cacti:  # Adding cactuses
            x = i * TILE_SIZE - camera_x
            y = (ground_levels[i] - 2) * TILE_SIZE
            screen.blit(full_cactus, (x, y))

        for i in palm_tree_with_rocks:  # Adding palm trees with rocks
            x = i * TILE_SIZE - camera_x
            y = (ground_levels[i] - 3) * TILE_SIZE
            screen.blit(palm_tree_with_rock, (x, y))

        for i in signs:  # Adding signs
            x = i * TILE_SIZE - camera_x
            y = (ground_levels[i] - 1) * TILE_SIZE
            screen.blit(sign, (x, y))

        acceleration = 0.5  # Slower acceleration on ice
        friction = normal_friction if not on_ice else ice_friction

        # Handle events
        keys = pygame.key.get_pressed()
        moving = False
        # if keys[pygame.K_w]:
        #     player_y -= player_speed
        # if keys[pygame.K_s]:
        #     player_y += player_speed
        current_x = calculate_column(player_x)
        current_y = calculate_row(player_y)+1
        currentTile = level_map[current_y][current_x]
        if currentTile > 0:
            latestTile = currentTile
        if keys[pygame.K_d]: # If player presses D
            if latestTile == 8 and not sandBoots:
                player_vel_x = player_speed * 0.7
            elif sandBoots:
                player_vel_x = player_speed
            else:
                player_vel_x = player_speed
            moving = True
            direction = 1
        if keys[pygame.K_a]: # If player presses A
            if latestTile == 8 and not sandBoots:
                player_vel_x = (player_speed * 0.7) * -1
            elif sandBoots:
                player_vel_x = -player_speed
            else:
                player_vel_x = -player_speed
            moving = True
            direction = -1
        # Jumping Logic (Space Pressed)
        if keys[pygame.K_SPACE]:
            if higherJumps:
                player_vel_y = jump_power * 2.25
                higherJumps = False
            elif on_ground:
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

        # Apply gravity when needed
        player_vel_y += gravity
        if keys[pygame.K_e] and glider:
            player_vel_y = gravity
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

                    if tile == 42: # If invisible platform, ignore collision from left and right and from bottom
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
                    
                        dying = True
                        death_sound.play()

                # Coin
                if tile == 12:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
                        coin_count += 1
                        # counter_for_coin_increment = 0 
                        eclipse_increment(slot, 1)
                        level_map[row_index][col_index] = 0
                        coin_sound.play()

                # Jump reset functionality
                if tile == 17: 
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
                        level_map[row_index][col_index] = 0  # Remove the jump reset from screen
                        bubbleJump = True
                        doubleJumped = False
                        powerup_respawns[(row_index, col_index)] = [17, pygame.time.get_ticks() + 5000]

                # Double Jump Boots
                if tile == 18:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
                        level_map[row_index][col_index] = 0  # Remove the boots from screen
                        gadget_sound.play()
                        doubleJumpBoots = True
                        doubleJumped = False

                # Spring functionality
                if tile == 19:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE >= tile_x and player_x <= tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE >= tile_y and player_y <= tile_y + TILE_SIZE):
                        player_vel_y = -38 * scale_factor
                        doubleJumped = False
                        spring_sound.play()

                # Button functionality
                if tile == 20:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE >= tile_x and player_x <= tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE >= tile_y and player_y <= tile_y + TILE_SIZE):
                        
                        button_spawn(3)

                # Flipped button functionality
                if tile == 21:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE >= tile_x and player_x <= tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE >= tile_y and player_y <= tile_y + TILE_SIZE):
                        
                        button_spawn(1)

                # High Jump Functionality
                if tile == 25:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
                        level_map[row_index][col_index] = 0  # Remove the boots from screen
                        power_up_sound.play()
                        higherJumps = True
                        powerup_respawns[(row_index, col_index)] = [25, pygame.time.get_ticks() + 5000]

                # Super Speed Powerup
                if tile == 22: 
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
                        super_speed_sound.play()
                        level_map[row_index][col_index] = 0
                        power_up_sound.play()

                        if len(super_speed_effects) == 0:
                            player_speed *= 2.5  # Double the speed
                        super_speed_effects.append({"end_time": pygame.time.get_ticks() + 1600})  # 1.6 sec effect
                        powerup_respawns[(row_index, col_index)] = [22, pygame.time.get_ticks() + 5000]  # 5 sec respawn

                if tile == 24: # Picked up glider (For Kenny to do)
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE

                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
                    
                        level_map[row_index][col_index] = 0
                        gadget_sound.play()
                        glider = True
                        for row_index in range(GROUND, level_height):
                            level_map[row_index][30:35] = [0] * 5
                            level_map[row_index][40:45] = [0] * 5
                        ground_levels[30:35] = [level_height] * 5
                        ground_levels[40:45] = [level_height] * 5

                # Up Dash
                if tile == 27:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
                        level_map[row_index][col_index] = 0 
                        player_vel_y = -25 * scale_factor
                        dash_sound.play()
                        powerup_respawns[(row_index, col_index)] = [27, pygame.time.get_ticks() + 5000]

                # Sand Boots
                if tile == 23:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
                        level_map[row_index][col_index] = 0 
                        gadget_sound.play()
                        sandBoots = True

                if tile == 26: # Right Dash
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
                        dash_pickup_time = pygame.time.get_ticks()
                        powerup_respawns[(row_index, col_index)] = [26, pygame.time.get_ticks() + 5000]
                        dash_duration = dash_pickup_time + 1000
                        dash_sound.play()
                        dashed = True
                        level_map[row_index][col_index] = 0 
                        dash_sound.play()
                        player_speed = player_speed * 2 
                        direction = 1
                        if player_speed < 0:
                            player_speed *= -1

                if tile == 28: # Left Dash
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
                        dash_pickup_time = pygame.time.get_ticks()
                        powerup_respawns[(row_index, col_index)] = [28, pygame.time.get_ticks() + 5000]
                        dash_duration = dash_pickup_time + 750
                        dash_sound.play()
                        dashed = True
                        level_map[row_index][col_index] = 0 
                        dash_sound.play()
                        player_speed = player_speed * 3.05
                        direction = -1
                        if player_speed < 0:
                            player_speed *= -1

                # Flipped button functionality
                if tile == 45:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE >= tile_x and player_x <= tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE >= tile_y and player_y <= tile_y + TILE_SIZE):
                        
                        button_spawn(2)

        level_name_font = pygame.font.Font('PixelifySans.ttf', 48)  # Larger font for level name

        global timer
        if timer and timer > 0:
            dt = clock.tick(60) / 1000  # Time elapsed per frame in seconds
            timer -= dt  # Decrease timer
            timer_text = level_name_font.render(f"{int(timer)}", True, WHITE)
            screen.blit(timer_text, (WIDTH // 2 - 50, 20))
        elif timer and timer <= 0:
            timer = None
            button_despawn()
            level_map[SURFACE][157] = 25 # High Jump
            level_map[GROUND][155:160] = [1] * 5 # Ground
            for row_index in range(GROUND+1, level_height): # Dirt
                level_map[row_index][155:160] = [3] * 5

        level_name_font = pygame.font.Font('PixelifySans.ttf', 48)  # Larger font for level name
        level_name_text = level_name_font.render("Level 6", True, WHITE)  # White text

        screen.blit(level_name_text, (20, 20))  # Position at (20, 20)

        if player_x + TILE_SIZE >= level_width * TILE_SIZE:  # If player reaches the end of the level
            show_level_completed_screen(slot, death_count)
            running = False

        if player_x <= 0: # Ensure player is within the bounds of the level and does not go to the left
            player_x = 0

        if player_y + TILE_SIZE >= level_height * TILE_SIZE:
            dying = True
            death_sound.play()

        if dying:
            timer = None
            player_x, player_y = checkpoints[checkpoint_idx][0], checkpoints[checkpoint_idx][1]
            death_count += 1
            update_save(slot, {"Level 6 Deaths": death_count})
            respawn_powerups()
            button_despawn()
            if (SURFACE, 157) in powerup_respawns:
                del powerup_respawns[(SURFACE, 157)]
            dying = False
            higherJumps = False
            player_vel_y = 0 # Instantly stops any vertical movement
            if checkpoint_idx == 0:
                doubleJumpBoots = False
                level_map[SURFACE-2][20] = 18 # Double Jump Boots
            elif checkpoint_idx == 1:
                sandBoots = False
                glider = False
                level_map[SURFACE-12][93] = 23 # Sand Boots
                level_map[3][97] = 24 # Glider
            elif checkpoint_idx == 4:
                glider = False
                level_map[6][240] = 24 # Glider
            if super_speed_effects:
                player_speed = default_speed  # Reset to normal speed
                super_speed_effects.clear()   # Remove all ongoing effects

        for k, checkpoint in enumerate(checkpoints):
            x, y = checkpoint
            if player_x >= x and player_y <= y and player_y >= (y - (TILE_SIZE * 4)) and not checkpoint_bool[k]:
                checkpoint_idx += 1
                checkpoint_bool[k] = True
                update_save(slot, {"Level 6 Checkpoint": checkpoint_idx})
                if checkpoint_idx == 1:
                    doubleJumpBoots = False
                    level_map[SURFACE-2][20] = 18 # Double Jump Boots
                elif checkpoint_idx == 2:
                    sandBoots = False
                    glider = False
                    level_map[SURFACE-12][93] = 23 # Sand Boots
                    level_map[3][97] = 24 # Glider

        current_time = pygame.time.get_ticks()

        # Apply speed effects from multiple power-ups
        for effect in super_speed_effects[:]:  # Iterate over a copy of the list
            if current_time >= effect["end_time"]:  # Check if effect expired
                super_speed_effects.remove(effect)
            if len(super_speed_effects) == 0:
                player_speed /= 2.5
         
        # Modified powerup respawns to singular function
        powerup_remove = []
        for position, gadget in powerup_respawns.items():
            if current_time >= gadget[1]:
                level_map[position[0]][position[1]] = gadget[0]
                powerup_remove.append(position) # mark for removal

        # This creates the dashing affect on the player
        if dashed:
            # print("Player speed: " + str(player_speed))
            if (current_time >= dash_duration) and (dash_duration != 0):
                player_speed = 8.5 * scale_factor
                dashed = False
                dash_duration = 0

        # Camera follows player
        camera_x = max(0, min(player_x - WIDTH // 2, (level_width * TILE_SIZE) - WIDTH))


        #-----Inventory Fill-up logic

        screen.blit(inventory, (inventory_x, inventory_y))

        inv_slots = []

        inv_slot_dimensions = [first_slot, second_slot, third_slot, fourth_slot]

        if glider:
            inv_slots.append(inventory_glider)

        if doubleJumpBoots:
            inv_slots.append(inventory_jump_boots)

        if sandBoots:
            inv_slots.append(inventory_sand_boots)


        for x, gadget in enumerate(inv_slots):
            screen.blit(gadget, inv_slot_dimensions[x])
    
        pygame.display.flip()  # Update display

if __name__ == "__main__":
    level_6(1)
    pygame.quit()