import pygame # type: ignore
import random
import json
import sys
import world_select
from NPCs.level_4_npc_1 import handle_level_4_npc_1_dialogue  # Import the functionality of the first NPC from level 4
from NPCs.level_4_npc_2 import handle_level_4_npc_2_dialogue  # Import the functionality of the second NPC from level 4
from NPCs.level_4_npc_3 import handle_level_4_npc_3_dialogue  # Import the functionality of the third NPC from level 4
from NPCs.level_4_npc_4 import handle_level_4_npc_4_dialogue  # Import the functionality of the fourth NPC from level 4


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
pygame.display.set_caption("Level 4")

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
down_dash = pygame.transform.rotate(dash_powerup, -90)

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

spring = pygame.image.load("./images/spring.png")
spring= pygame.transform.scale(spring, (TILE_SIZE, TILE_SIZE))

speed_boots = pygame.image.load("./images/speed_boots.png")
speed_boots = pygame.transform.scale(speed_boots, (TILE_SIZE, TILE_SIZE))

dash_gadget = pygame.image.load("./images/jett_dash.png")
dash_gadget = pygame.transform.scale(dash_gadget, (TILE_SIZE, TILE_SIZE))

balloon = pygame.image.load("./images/balloon.png")
balloon = pygame.transform.scale(balloon, (TILE_SIZE, TILE_SIZE))

npc_1 = pygame.image.load("./Character Combinations/ginger hair_dark_red shirt_blue pants.png")
npc_1 = pygame.transform.scale(npc_1, (TILE_SIZE, TILE_SIZE))
flipped_npc_1 = pygame.transform.flip(npc_1, True, False)  # Flip horizontally (True), no vertical flip (False)

npc_2 = pygame.image.load("./Character Combinations/brown hair_white_yellow shirt_black pants.png")
npc_2 = pygame.transform.scale(npc_2, (TILE_SIZE, TILE_SIZE))
flipped_npc_2 = pygame.transform.flip(npc_2, True, False)  # Flip horizontally (True), no vertical flip (False)

npc_3 = pygame.image.load("./Character Combinations/black hair_dark_yellow shirt_blue pants.png")
npc_3 = pygame.transform.scale(npc_3, (TILE_SIZE, TILE_SIZE))
flipped_npc_3 = pygame.transform.flip(npc_3, True, False)  # Flip horizontally (True), no vertical flip (False)

npc_4 = pygame.image.load("./Character Combinations/ginger hair_white_yellow shirt_brown pants.png")
npc_4 = pygame.transform.scale(npc_4, (TILE_SIZE, TILE_SIZE))
flipped_npc_4 = pygame.transform.flip(npc_4, True, False)  # Flip horizontally (True), no vertical flip (False)

# Set up the level with a width of 300 and a height of 30 rows
level_width = 300
level_height = HEIGHT // TILE_SIZE  # Adjust level height according to user's resolution

level_map = [[0] * level_width for _ in range(level_height)]  # Start with air

GROUND = level_height - 4 #Constant for the ground level
SURFACE = GROUND - 1 #Constant for the surface level

# This is for the snowflake animations
WHITE = (255, 255, 255)
RED = (255, 0, 0) # For timer
BLUE = (0, 0, 255) # For hover
NUM_SNOWFLAKES = 300
snowflakes = []

#This for loop is also for snowflakes
for _ in range(NUM_SNOWFLAKES):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    size = random.randint(2, 6)  # Random size
    speed = random.uniform(15, 20)  # Falling speed
    x_speed = random.uniform(-20, -10)  # Small horizontal drift
    snowflakes.append([x, y, size, speed, x_speed])

for row_index in range(GROUND, level_height):
    row = [1] * level_width  # Default to full ground row
    for col_index in range(15, 25):  # Remove ground in columns 15-24
        row[col_index] = 0  # Set to air (pit)
    for col_index in range(37, 41):  # Remove ground in columns 37-40
        row[col_index] = 0  # Set to air (pit)
    for col_index in range(42, 100):  # Remove ground in columns 42-99
        row[col_index] = 0  # Set to air (pit)
    for col_index in range(121, 150):  # Remove ground in columns 121-149
        row[col_index] = 0  # Set to air (pit)
    for col_index in range(170, level_width-20):  # Remove ground in columns 170-level_width-20
        row[col_index] = 0  # Set to air (pit)
    level_map[row_index] = row  # Add row to level map

# Add solid ground at the very bottom
level_map.append([1] * level_width)

for row_index in range(SURFACE-1, GROUND): # Raised Ground
    level_map[row_index][25:28] = [1] * 3
for row_index in range(SURFACE-2, GROUND): # Raised Ground
    level_map[row_index][28:32] = [1] * 4
for row_index in range(SURFACE-4, GROUND): # Raised Ground
    level_map[row_index][32:37] = [1] * 5
for row_index in range(SURFACE-6, GROUND): # Raised Ground
    level_map[row_index][41] = 1
for row_index in range(SURFACE-17, SURFACE-12): # Upside Down Dirt
    level_map[row_index][41] = 9
level_map[SURFACE-18][37:70] = [6] * 33
for row_index in range(SURFACE-17, SURFACE-8): # Upside Down Dirt
    level_map[row_index][69] = 9
for row_index in range(SURFACE-3, GROUND): # Raised Ground
    level_map[row_index][69] = 1
level_map[SURFACE-18][20:24] = [21] * 4 # Ice
level_map[SURFACE-17][20:24] = [22] * 4 # Flipped ice
level_map[GROUND][75] = 2 # Platform for spring

level_map[SURFACE-18][88:113] = [21] * 25
for row_index in range(SURFACE-17, SURFACE-4): # Huge Ice Block
    level_map[row_index][88:113] = [28] * 25
level_map[SURFACE-4][88:113] = [22] * 25
level_map[0][95:101] = [9] * 6

for row_index in range(4, SURFACE-18): # Upside Down Dirt
    level_map[row_index][106] = 9

for row_index in range(0, SURFACE-18): # Upside Down Dirt
    level_map[row_index][112] = 9

level_map[GROUND][75] = 2 # Platform for spring
level_map[SURFACE-9][113:117] = [2] * 4 # Platform
level_map[SURFACE-18][116:120] = [2] * 4 # Platform
level_map[SURFACE-18][120] = 6 # Floating Ground Tile
for row_index in range(SURFACE-17, SURFACE-3):
    level_map[row_index][120] = 9 # Dirt Tiles
for row_index in range(SURFACE-18, GROUND):
    level_map[row_index][150:160] = [1] * 10
for col_index in range(121, 146, 8):
    level_map[SURFACE-18][col_index:col_index+3] = [21] * 3 # Platform
for col_index in range(125, 146, 8):
    level_map[SURFACE-13][col_index:col_index+3] = [21] * 3 # Platform
for col_index in range(121, 146, 8):
    level_map[SURFACE-9][col_index:col_index+3] = [21] * 3 # Platform
for row_index in range(SURFACE-16, GROUND):
    level_map[row_index][160:165] = [1] * 5
for row_index in range(SURFACE-9, GROUND):
    level_map[row_index][165:170] = [1] * 5
level_map[SURFACE-18][184:189] = [6] * 5
for row_index in range(SURFACE-18, GROUND):
    level_map[row_index][184] = 1 # Raised Ground
level_map[SURFACE-18][185:190] = [6] * 5
level_map[SURFACE-11][190:201] = [6] * 11
for row_index in range(0, SURFACE-11):
    level_map[row_index][195] = 9 # Dirt Tiles
level_map[SURFACE-18][201:206] = [6] * 5
for row_index in range(SURFACE-18, GROUND):
    level_map[row_index][206] = 1 # Raised Ground
for row_index in range(SURFACE-16, GROUND):
    level_map[row_index][280:level_width] = [1] * (level_width-280) # Raised Ground

# Make terrain before this line. The next code block calculates the ground levels

# Find the ground level for each column
ground_levels = [len(level_map)] * len(level_map[0])
for row_index, row in enumerate(level_map):
    for col_index, tile in enumerate(row):
        if tile == 1 and ground_levels[col_index] == len(level_map):
            ground_levels[col_index] = row_index

# All code after this line should be for props, npcs, gadgets, and powerups. Terrain should not be made here.

level_map[SURFACE][13] = 31 # Dash Gadget

level_map[level_height-3][15:level_width] = [3] * (level_width-15) # Water
level_map[level_height-2][15:level_width] = [11] * (level_width-15) # Water Block
level_map[level_height-1][15:level_width] = [11] * (level_width-15) # Water Block

level_map[SURFACE-7][41] = 7 # Thorn
level_map[SURFACE-12][41] = 17 # Flipped Thorn

level_map[SURFACE-5][44] = 4 # Jump Reset

level_map[SURFACE-5][48:52] = [2] * 4 # Platform 
level_map[SURFACE-6][50:52] = [7] * 2 # Thorns

level_map[SURFACE-8][54] = 4 # Super Speed Powerup

level_map[SURFACE-3][61:65] = [2] * 4 # Platform
level_map[SURFACE-4][61] = 7 # Thorn
level_map[SURFACE-4][64] = 7 # Thorn

level_map[SURFACE-8][69] = 17 # Flipped Thorn
level_map[SURFACE-4][69] = 7 # Thorn

level_map[SURFACE-19][65:70] = [7] * 5 # Thorns on top
level_map[SURFACE-19][39] = 16 # Double Jump Boots
# level_map[SURFACE-19][38] = 20 # Super Speed Powerup
level_map[SURFACE-19][21] = 10 # Frost Walking Boots

#level_map[SURFACE-2][72] = 5 # Dash Powerup
level_map[SURFACE][75] = 29 # Spring

level_map[SURFACE-19][88:90] = [7] * 2 # Thorns
level_map[SURFACE-19][95:101] = [7] * 6 # Thorns
level_map[1][95:101] = [17] * 6 # Thorns

level_map[SURFACE][102] = 8 # First Checkpoint (Flag)
level_map[SURFACE][107] = 30 # Speed Boots

for row_index in range(4, SURFACE-18):
    level_map[row_index][105] = 18 # Left Thorns
    level_map[row_index][107] = 19 # Right Thorns

level_map[5][110] = 12 # Coin

level_map[SURFACE][118] = 23 # High Jump
level_map[SURFACE-10][114] = 23 # High Jump

for col_index in range(126, 143, 8):
    level_map[4][col_index] = 32 # Down Dash
for col_index in range(130, 139, 8):
    level_map[SURFACE-16][col_index] = 5 # Right Dash
for col_index in range(126, 143, 8):
    level_map[SURFACE-8][col_index] = 4 # Jump Reset
level_map[SURFACE-12][122] = 4 # Jump Reset
level_map[SURFACE-16][142] = 4 # Jump Reset

level_map[SURFACE-11][146] = 12 # Coin

level_map[SURFACE-19][152] = 8 # Second Checkpoint (Flag)

level_map[SURFACE-17][185:190] = [17] * 5 # Flipped Thorns
level_map[SURFACE-17][201:206] = [17] * 5 # Flipped Thorns
level_map[SURFACE-10][190:201] = [17] * 11 # Flipped Thorns
level_map[SURFACE-11][201] = 19 # Right Thorn
level_map[SURFACE-12][196:201] = [7] * 5 # Thorns   

level_map[SURFACE-10][168] = 33 # Balloon
level_map[SURFACE-12][191] = 33 # Balloon
level_map[SURFACE-3][187] = 4 # Jump Reset
level_map[SURFACE-1][193] = 33 # Balloon
level_map[SURFACE-19][205] = 30 # Speed Boots

level_map[SURFACE-14][214:218] = [21] * 4 # Ice Tile
level_map[SURFACE-13][214:218] = [22] * 4 # Flipped Ice Tile

level_map[SURFACE-10][226:230] = [21] * 4 # Ice Tile
level_map[SURFACE-9][226:230] = [22] * 4 # Flipped Ice Tile

level_map[SURFACE-6][238:242] = [21] * 4 # Ice Tile
level_map[SURFACE-5][238:242] = [22] * 4 # Flipped Ice Tile

level_map[SURFACE-2][250:254] = [21] * 4 # Ice Tile
level_map[SURFACE-1][250:254] = [22] * 4 # Flipped Ice Tile

level_map[SURFACE-3][253] = 33 # Balloon

level_map[SURFACE-5][35] = 34 # First NPC - (Placed next to the first sign of the map)
level_map[SURFACE-19][151] = 35 # Second NPC - (Placed next to the second checkpoint flag of the map)
level_map[SURFACE-19][202] = 36 # Third NPC - (Placed next to the second speed boots)
level_map[SURFACE-17][291] = 37 # Fourth NPC - (Placed next to the last sign of the map)

# Dictionary containing which tile corresponds to what
tiles = {0: background, 1: ground_tile, 2: platform_tile, 3: water, 4: jump_reset, 5: dash_powerup, 6: floating_ground, 7: thorn, 8: flag, 9: dirt_tile, 10: frost_walking_boots,
         11: water_block, 12: coin, 13: walkway, 14: flipped_walkway, 15: invisible_platform, 16: double_jump_boots, 17: flipped_thorn, 18: left_thorn, 19: right_thorn, 20: super_speed_powerup,
         21: ice_tile, 22: flipped_ice, 23: high_jump, 24: up_dash, 25: house, 26: tree, 27: background_tree, 28: ice_block, 29: spring, 30: speed_boots,
         31: dash_gadget, 32: down_dash, 33: balloon, 34: npc_1, 35: npc_2, 36: npc_3, 37: npc_4}

rocks = {26, 112, 296} # Column numbers for all the rocks
trees = {7, 115, 154, 281, 289} # Column numbers for all the trees
background_trees = {29, 157, 286} # Column numbers for all the background trees
signs = {33, 162, 293} # Column numbers for all the signs

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

    level_map[SURFACE][13] = 31 # Dash Gadget
    level_map[SURFACE-5][44] = 4 # Jump Reset
    level_map[SURFACE-8][53] = 20 # Super Speed Powerup

    level_map[SURFACE-19][39] = 16 # Double Jump Boots
    level_map[SURFACE-19][38] = 20 # Super Speed Powerup
    level_map[SURFACE-19][21] = 10 # Frost Walking Boots

    level_map[SURFACE-2][72] = 5 # Dash Powerup

    level_map[SURFACE][107] = 30 # Speed Boots

    level_map[SURFACE][118] = 23 # High Jump
    level_map[SURFACE-10][114] = 23 # High Jump

    for col_index in range(126, 143, 8):
        level_map[4][col_index] = 32 # Down Dash
    for col_index in range(130, 139, 8):
        level_map[SURFACE-16][col_index] = 5 # Right Dash
    for col_index in range(126, 143, 8):
        level_map[SURFACE-8][col_index] = 4 # Jump Reset
    level_map[SURFACE-12][122] = 4 # Jump Reset
    level_map[SURFACE-16][142] = 4 # Jump Reset

    level_map[SURFACE-10][168] = 33 # Balloon
    level_map[SURFACE-12][191] = 33 # Balloon
    level_map[SURFACE-3][187] = 4 # Jump Reset
    level_map[SURFACE-1][193] = 33 # Balloon
    level_map[SURFACE-19][205] = 30 # Speed Boots

    level_map[SURFACE-3][253] = 33 # Balloon

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

def show_game_over_screen(slot: int):

    level_map[5][110] = 12 # Coin
    level_map[SURFACE-11][146] = 12 # Coin

    level_map[SURFACE][13] = 31 # Dash Gadget
    level_map[SURFACE-5][44] = 4 # Jump Reset
    level_map[SURFACE-8][53] = 20 # Super Speed Powerup

    level_map[SURFACE-19][39] = 16 # Double Jump Boots
    level_map[SURFACE-19][38] = 20 # Super Speed Powerup
    level_map[SURFACE-19][21] = 10 # Frost Walking Boots

    level_map[SURFACE-2][72] = 5 # Dash Powerup

    level_map[SURFACE][107] = 30 # Speed Boots

    level_map[SURFACE][118] = 23 # High Jump
    level_map[SURFACE-10][114] = 23 # High Jump

    for col_index in range(126, 143, 8):
        level_map[4][col_index] = 32 # Down Dash
    for col_index in range(130, 139, 8):
        level_map[SURFACE-16][col_index] = 5 # Right Dash
    for col_index in range(126, 143, 8):
        level_map[SURFACE-8][col_index] = 4 # Jump Reset
    level_map[SURFACE-12][122] = 4 # Jump Reset
    level_map[SURFACE-16][142] = 4 # Jump Reset

    level_map[SURFACE-10][168] = 33 # Balloon
    level_map[SURFACE-12][191] = 33 # Balloon
    level_map[SURFACE-3][187] = 4 # Jump Reset
    level_map[SURFACE-1][193] = 33 # Balloon
    level_map[SURFACE-19][205] = 30 # Speed Boots

    level_map[SURFACE-3][253] = 33 # Balloon

    # Wait for player to click the button
    waiting = True
    while waiting:

        screen.blit(background, (0, 0))

        # Set fonts for the text
        title_font = pygame.font.Font('PixelifySans.ttf', 100)
        sub_font = pygame.font.Font('PixelifySans.ttf', 60)
        sub_font_hover = pygame.font.Font('PixelifySans.ttf', 65)  # Larger for hover

        # Render hover effect dynamically
        restart_hover = False
        select_level_hover = False

        # Render the "Game Over" text
        game_over_text = title_font.render("Game Over", True, WHITE)
        restart_text = sub_font.render("Retry", True, WHITE)
        select_level_text = sub_font.render("Back to Select Level", True, WHITE)

        # Position the texts
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        restart_over_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 120))
        select_level_rect = select_level_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 240))

        # Check if mouse is hovering
        if restart_over_rect.collidepoint(pygame.mouse.get_pos()):
            restart_hover = True
        if select_level_rect.collidepoint(pygame.mouse.get_pos()):
            select_level_hover = True

        # If hovering, change text size dynamically
        if restart_hover:
            restart_text = sub_font_hover.render("Retry", True, BLUE)
            restart_over_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 120))  # Recalculate position
        if select_level_hover:
            select_level_text = sub_font_hover.render("Back to Select Level", True, BLUE)
            select_level_rect = select_level_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 240))  # Recalculate position

        # Create box around the text
        box_padding = 100
        game_over_screen_box = pygame.Rect(game_over_rect.left - box_padding, game_over_rect.top, game_over_rect.width + box_padding*2, game_over_rect.height + (box_padding*2) + 40)
        pygame.draw.rect(screen, BLUE, game_over_screen_box, 10)
        
        # Draw the texts
        screen.blit(game_over_text, game_over_rect)
        screen.blit(restart_text, restart_over_rect)
        screen.blit(select_level_text, select_level_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if restart_over_rect.collidepoint(mouse_x, mouse_y):
                    level_4(slot) # Retry the level
                    sys.exit()
                if select_level_rect.collidepoint(mouse_x, mouse_y):
                    world_select.World_Selector(slot)
                    sys.exit()  # Go back to level select

def level_4(slot: int):
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
    speedBoots = False # Track if player has speed boots
    dashGadget = False # Track if player has the dash gadget

    # State Variables for Gadgets
    bubbleJump = False
    bubbleJump_respawns = {}
    dash_respawns = {}
    dashing = False
    dash_duration = 0
    dashed = False
    super_speed_effects = []
    super_speed_respawns = {}
    higherJumps = False
    higherJumps_respawns = {}
    up_dash_respawns = {}
    down_dash_respawns = {}
    hasBalloon = False
    balloon_vel = 0  # Initial vertical velocity
    balloon_respawns = {}

    animation_index = 0  # Alternates between 0 and 1
    animation_timer = 0  # Tracks when to switch frames
    animation_speed = 4  # Adjust this to control animation speed
    direction = 1  # 1 for right, -1 for left

    normal_friction = 0.25
    ice_friction = 0.95  # Lower friction for slippery effect
    on_ice = False

    checkpoints = [(player_x, player_y), (calculate_x_coordinate(102), calculate_y_coordinate(SURFACE)), (calculate_x_coordinate(152), calculate_y_coordinate(SURFACE-19))]
    checkpoint_bool = [False] * len(checkpoints)
    checkpoint_bool[0] = True
    checkpoint_idx = 0
    dying = False
    death_count = 0
    collidable_tiles = {1, 2, 3, 6, 9, 15, 21, 22, 28}
    dying_tiles = {3, 11, 18, 19, 7, 17} 

    coin_count = 0

    start_time = 180  # Timer starts at 180 seconds
    timer = start_time
    clock = pygame.time.Clock()

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
        npc_x = calculate_x_coordinate(35)  # First NPC's x position
        npc_y = (SURFACE-5) * TILE_SIZE  # First NPC's y position
        player_rect = pygame.Rect(player_x - camera_x, player_y, TILE_SIZE, TILE_SIZE)
        npc_rect = pygame.Rect(npc_x - camera_x, npc_y, TILE_SIZE, TILE_SIZE)

        # Handle first NPC dialogue
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()  # Get current time in milliseconds
        handle_level_4_npc_1_dialogue(screen, player_rect, npc_rect, keys, current_time)

        # Check if player is near the second NPC
        npc_x = calculate_x_coordinate(151)  # Second NPC's x position
        npc_y = (SURFACE - 19) * TILE_SIZE  # Second NPC's y position
        player_rect = pygame.Rect(player_x - camera_x, player_y, TILE_SIZE, TILE_SIZE)
        npc_rect = pygame.Rect(npc_x - camera_x, npc_y, TILE_SIZE, TILE_SIZE)

        # Handle second NPC dialogue
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()  # Get current time in milliseconds
        handle_level_4_npc_2_dialogue(screen, player_rect, npc_rect, keys, current_time)

        # Check if player is near the third NPC
        npc_x = calculate_x_coordinate(202)  # Third NPC's x position
        npc_y = (SURFACE - 19) * TILE_SIZE  # Third NPC's y position
        player_rect = pygame.Rect(player_x - camera_x, player_y, TILE_SIZE, TILE_SIZE)
        npc_rect = pygame.Rect(npc_x - camera_x, npc_y, TILE_SIZE, TILE_SIZE)

        # Handle third NPC dialogue
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()  # Get current time in milliseconds
        handle_level_4_npc_3_dialogue(screen, player_rect, npc_rect, keys, current_time)

        # Check if player is near the fourth NPC
        npc_x = calculate_x_coordinate(291)  # Fourth NPC's x position
        npc_y = (SURFACE-17) * TILE_SIZE  # Fourth NPC's y position
        player_rect = pygame.Rect(player_x - camera_x, player_y, TILE_SIZE, TILE_SIZE)
        npc_rect = pygame.Rect(npc_x - camera_x, npc_y, TILE_SIZE, TILE_SIZE)

        # Handle fourth NPC dialogue
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()  # Get current time in milliseconds
        handle_level_4_npc_4_dialogue(screen, player_rect, npc_rect, keys, current_time)  

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
                elif event.key == pygame.K_e:
                    if dashGadget:
                        dashing = True
                        dash_duration = 15  # Dash lasts for 15 frames
                        dash_velocity = player_vel_x * 2  # Boost speed temporarily
                        dash_timer = dash_duration
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
        level_name_text = level_name_font.render("Level 4", True, WHITE)  # White text

        screen.blit(level_name_text, (20, 20))  # Position at (20, 20)

        dt = clock.tick(60) / 1000  # Time elapsed per frame in seconds
        timer -= dt  # Decrease timer

        timer_text = level_name_font.render(f"Time: {int(timer)}", True, RED if timer <= 30 else WHITE)
        screen.blit(timer_text, (WIDTH // 2 - 50, 20))

        # Apply gravity
        if not hasBalloon:
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
                
                #  High Jump
                if tile == 23:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
                        level_map[row_index][col_index] = 0  # Remove the boots from screen
                        higherJumps = True
                        higherJumps_respawns[(row_index, col_index)] = pygame.time.get_ticks() + 5000

                # Dash
                if tile == 31:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
                            dashGadget = True
                            level_map[row_index][col_index] = 0 

                # Super Speed Powerups
                if tile == 20: 
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):

                        level_map[row_index][col_index] = 0
                        player_speed *= 4  # Double the speed
                        super_speed_effects.append({"end_time": pygame.time.get_ticks() + 1600})  # 1.6 sec effect
                        super_speed_respawns[(row_index, col_index)] = pygame.time.get_ticks() + 5000  # 5 sec respawn
                
                # Spring
                if tile == 29:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE >= tile_x and player_x <= tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE >= tile_y and player_y <= tile_y + TILE_SIZE):
                        player_vel_y = -50

                # Double Jump Boots
                if tile == 16:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
                        level_map[row_index][col_index] = 0  # Remove the boots from screen
                        doubleJumpBoots = True
                        doubleJumped = False

                # Ice boots
                if tile == 10:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
                        level_map[row_index][col_index] = 0  # Remove the boots from screen
                        frostWalkBoots = True

                # Dash
                if tile == 5:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):

                        dash_pickup_time = pygame.time.get_ticks()
                        dash_respawns[(row_index, col_index)] = pygame.time.get_ticks() + 5000
                        dash_duration = dash_pickup_time + 500
                        dashed = True
                        level_map[row_index][col_index] = 0 
                        player_speed = player_speed * 2 
                        direction = 1
                        if player_speed < 0:
                            player_speed *= -1
                        
                
                # This code picks up the speed boots
                if tile == 30:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
                        level_map[row_index][col_index] = 0  # Remove the boots from screen
                        player_speed = player_speed * 1.25 # Up the player speed
                        speedBoots = True

                # Down dash
                if tile == 32:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
                        level_map[row_index][col_index] = 0  # Remove the boots from screen
                        player_vel_y += 15
                        down_dash_respawns[(row_index, col_index)] = pygame.time.get_ticks() + 5000

                if tile == 33:  # Balloon pickup
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):

                        level_map[row_index][col_index] = 0  # Remove the balloon from the map
                        hasBalloon = True
                        balloon_vel = -5  # Initial upward speed
                        balloon_respawns[(row_index, col_index)] = pygame.time.get_ticks() + 5000

        
        if player_x + TILE_SIZE >= level_width * TILE_SIZE:  # If player reaches the end of the level
            show_level_completed_screen(slot, death_count)
            running = False

        if timer <= 0:
            timer = 0  # Prevent negative values
            show_game_over_screen(slot)
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
                doubleJumpBoots = False
                dashGadget = False
                level_map[SURFACE-19][21] = 10 # Frost Walking Boots
                level_map[SURFACE-19][39] = 16 # Double Jump Boots
                level_map[SURFACE][13] = 31 # Dash Gadget
            elif checkpoint_idx == 1:
                speedBoots = False
                level_map[SURFACE][107] = 30 # Speed Boots
            elif checkpoint_idx == 2:
                speedBoots = False
                level_map[SURFACE-19][205] = 30 # Speed Boots


        for k, checkpoint in enumerate(checkpoints):
            x, y = checkpoint
            if player_x >= x and player_y <= y and player_y >= (y - (TILE_SIZE * 4)) and not checkpoint_bool[k]:
                checkpoint_idx += 1
                checkpoint_bool[k] = True
                if checkpoint_idx == 1:
                    frostWalkBoots = False
                    doubleJumpBoots = False
                    dashGadget = False
                elif checkpoint_idx == 2:
                    speedBoots = False
                    
        # Camera follows player
        camera_x = max(0, min(player_x - WIDTH // 2, (level_width * TILE_SIZE) - WIDTH))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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

        # Respawn power-ups after 5 seconds
        to_remove = []
        for pos, respawn_time in super_speed_respawns.items():
            if current_time >= respawn_time:
                level_map[pos[0]][pos[1]] = 20  # Respawn power-up
                to_remove.append(pos)  # Mark for removal

        # Apply speed effects from multiple power-ups
        for effect in super_speed_effects[:]:  # Iterate over a copy of the list
            if current_time >= effect["end_time"]:  # Check if effect expired
                player_speed /= 4
                super_speed_effects.remove(effect)

        up_dash_removes = []
        for pos, respawn_time in dash_respawns.items():
            if current_time >= respawn_time:
                level_map[pos[0]][pos[1]] = 5  # Respawn power-up
                up_dash_removes.append(pos)  # Mark for removal

        down_dash_removes = []
        for pos, respawn_time in down_dash_respawns.items():
            if current_time >= respawn_time:
                level_map[pos[0]][pos[1]] = 32  # Respawn power-up
                down_dash_removes.append(pos)  # Mark for removal

        balloon_removes = []
        for pos, respawn_time in balloon_respawns.items():
            if current_time >= respawn_time:
                level_map[pos[0]][pos[1]] = 33  # Respawn power-up
                balloon_removes.append(pos)  # Mark for removal

        # Gliding Dash Mechanic
        if dashing and dash_gadget:
            t = 1 - (dash_timer / dash_duration)  # Progress of dash (0 to 1)
            ease_t = 1 - (1 - t) ** 3  # Ease-out effect
            player_x += dash_velocity * ease_t  # Smooth transition

            dash_timer -= 1
            if dash_timer <= 0:
                dashing = False  # Stop dashing

        # Set speed back for player if dashing
        if dashed:
            if (current_time >= dash_duration) and (dash_duration != 0):
                player_speed = 8.5 * scale_factor
                dashed = False
                dash_duration = 0

        # Set speed to normal if no boots
        if not speedBoots:
            player_speed = 8.5 * scale_factor

        if hasBalloon:
            player_y += balloon_vel  # Move up
            balloon_vel -= 0.001  # Gradually slow down (simulating air resistance)

            if player_y + TILE_SIZE < 0:  # If the player moves off the top of the screen
                hasBalloon = False  # Pop the balloon
                balloon_vel = 0  # Reset velocity

        pygame.display.flip()  # Update display

if __name__ == "__main__":
    level_4(1)
    pygame.quit()