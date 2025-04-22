import pygame # type: ignore
import random
import sys
import world_select
from saves_handler import *
from firework_level_end import show_level_complete_deaths
from pause_menu import PauseMenu  # Import the PauseMenu class

from NPCs.level_5_npc_1 import handle_level_5_npc_1_dialogue  # Import the functionality of the first NPC from level 5
from NPCs.level_5_npc_2 import handle_level_5_npc_2_dialogue  # Import the functionality of the second NPC from level 5
from NPCs.level_5_npc_3 import handle_level_5_npc_3_dialogue  # Import the functionality of the third NPC from level 5
from NPCs.level_5_npc_4 import handle_level_5_npc_4_dialogue  # Import the functionality of the fourth NPC from level 5

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

# Pop Balloon sound
pop_balloon_sound = pygame.mixer.Sound("Audio/PopBalloon.mp3")

# Screen settings
BASE_WIDTH = 1920
BASE_HEIGHT = 1080

SAVE_DIR = "User Saves"

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h # Will only work with resolutions 1920 x 1080 or better

TILE_SIZE = HEIGHT // 30  # Readjusted according to user resolution

scale_factor = HEIGHT / BASE_HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Level 5")

ground_tile = pygame.image.load("./desert_images/ground.png")
ground_tile = pygame.transform.scale(ground_tile, (TILE_SIZE, TILE_SIZE))

floating_ground = ground_tile

background = pygame.image.load("./desert_images/background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

platform_tile = pygame.image.load("./desert_images/platform.png")
platform_tile = pygame.transform.scale(platform_tile, (TILE_SIZE, TILE_SIZE))

dirt_tile = pygame.image.load("./desert_images/dirt.png")
dirt_tile = pygame.transform.scale(dirt_tile, (TILE_SIZE, TILE_SIZE))

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

floating_sand = sand

coin = pygame.image.load("./desert_images/coin.png")
coin = pygame.transform.scale(coin, (TILE_SIZE, TILE_SIZE))

high_jump = pygame.image.load("./images/high_jump.png")
high_jump = pygame.transform.scale(high_jump, (TILE_SIZE, TILE_SIZE))

speed_boots = pygame.image.load("./images/speed_boots.png")
speed_boots = pygame.transform.scale(speed_boots, (TILE_SIZE, TILE_SIZE))

balloon = pygame.image.load("./images/balloon.png")
balloon = pygame.transform.scale(balloon, (TILE_SIZE, TILE_SIZE))

glider = pygame.image.load("./images/glider.png")
glider = pygame.transform.scale(glider, (TILE_SIZE, TILE_SIZE))

double_jump_boots = pygame.image.load("./images/boots.png")
double_jump_boots = pygame.transform.scale(double_jump_boots, (TILE_SIZE, TILE_SIZE))

spring = pygame.image.load("./images/spring.png")
spring = pygame.transform.scale(spring, (TILE_SIZE, TILE_SIZE))

dash_powerup = pygame.image.load("./images/dash_powerup.png")
dash_powerup = pygame.transform.scale(dash_powerup, (TILE_SIZE, TILE_SIZE))
left_dash = pygame.transform.flip(dash_powerup, True, False)

jump_reset = pygame.image.load("./images/bubble.png")
jump_reset = pygame.transform.scale(jump_reset, (TILE_SIZE, TILE_SIZE))

full_walkway = pygame.image.load("./desert_images/full_walkway.png")
full_walkway = pygame.transform.scale(full_walkway, (TILE_SIZE * 8, TILE_SIZE * 2))

iron_boots = pygame.image.load("./images/iron_boots.png")
iron_boots = pygame.transform.scale(iron_boots, (TILE_SIZE, TILE_SIZE))

invisible_platform = None

sign = pygame.image.load("./desert_images/sign.png")
sign = pygame.transform.scale(sign, (TILE_SIZE, TILE_SIZE))

npc_1 = pygame.image.load("./Character Combinations/black hair_dark_red shirt_brown pants.png")
npc_1 = pygame.transform.scale(npc_1, (TILE_SIZE, TILE_SIZE))

npc_2 = pygame.image.load("./Character Combinations/female ginger hair_white_brown skirt_magenta pants.png")
npc_2 = pygame.transform.scale(npc_2, (TILE_SIZE, TILE_SIZE))

npc_3 = pygame.image.load("./Character Combinations/female brown hair_white_pink skirt_blue pants.png")
npc_3 = pygame.transform.scale(npc_3, (TILE_SIZE, TILE_SIZE))

npc_4 = pygame.image.load("./Character Combinations/ginger hair_white_yellow shirt_brown pants.png")
npc_4 = pygame.transform.scale(npc_4, (TILE_SIZE, TILE_SIZE))






level_almost_complete_popup = pygame.image.load("./images/level_near_completion_pop_up.png")
level_almost_complete_popup = pygame.transform.scale(level_almost_complete_popup, (250, 60))


level_almost_complete_font = pygame.font.Font('PixelifySans.ttf', 10)
keep_heading_right_font = pygame.font.Font('PixelifySans.ttf', 10)
level_almost_complete_text = level_almost_complete_font.render("Level 5 Almost Complete!", True, (255, 255, 255))
keep_heading_right_text = keep_heading_right_font.render("Keep Heading Right!", True, (255, 255, 255))



pop_up_x = WIDTH - (WIDTH * .20)
pop_up_y = HEIGHT - (HEIGHT * .95)



level_almost_complete_rect = level_almost_complete_text.get_rect(center=(pop_up_x + 140, pop_up_y + 18))
keep_heading_right_rect = keep_heading_right_text.get_rect(center=(pop_up_x + 140, pop_up_y + 38))







#-----Gadget inventory images and dictionary

inventory = pygame.image.load("./images/inventory_slot_opacity.png").convert_alpha()
inventory = pygame.transform.scale(inventory, (250, 70))
inventory_x = (WIDTH - 250) // 2
inventory_y = HEIGHT - 100

inventory_jump_boots = pygame.image.load("./images/boots.png")
inventory_jump_boots = pygame.transform.scale(inventory_jump_boots, (42, 50))

inventory_speed_boots = pygame.image.load("./images/speed_boots.png")
inventory_speed_boots = pygame.transform.scale(inventory_speed_boots, (42, 50))

inventory_iron_boots = pygame.image.load("./images/iron_boots.png")
inventory_iron_boots = pygame.transform.scale(inventory_iron_boots, (42, 50))

inventory_glider = pygame.image.load("./images/glider.png")
inventory_glider = pygame.transform.scale(inventory_glider, (42, 50))

INV_SLOT_WIDTH = 42
INV_SLOT_HEIGHT = 45

first_slot = (inventory_x + 5, inventory_y + 10)
second_slot = (inventory_x + INV_SLOT_WIDTH + 10, inventory_y + 10)
third_slot = (inventory_x + (2*INV_SLOT_WIDTH + 20), inventory_y + 10)
fourth_slot = (inventory_x + (3*INV_SLOT_WIDTH + 40), inventory_y + 10)



# Set up the level with a width of 290 and a height of 30 rows
level_width = 290
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

level_map[5][13] = 12  # Coin
level_map[6][133] = 12 # Coin

# Sand storm (dusty mist) particles constants
SAND_PALETTE = [                                           # warm, earthy hues
    (210, 190, 145),  # light tan
    (198, 166, 125),  # ochre
    (174, 142, 108)   # deeper brown
]
STORM_LAYERS = []      # will hold two large scrolling “fog sheets”

SAND_COLOR = (194, 178, 128)   # light‑brown sand
NUM_SAND_PARTICLES = 350       # tweak for more / fewer grains
sand_particles = []            # will be filled in spawn_sandstorm()

# Dictionary containing which tile corresponds to what
tiles = {0: background, 1: ground_tile, 2: platform_tile, 3: dirt_tile,  4: thorns, 5: water, 6: water_block, 7: flag, 8: sand, 9: flipped_thorn, 10: left_thorn,
         11: right_thorn, 12: coin, 13: high_jump, 14: speed_boots, 15: balloon, 16: full_cactus, 17: glider, 18: double_jump_boots, 19: spring, 20: dash_powerup,
         21: left_dash, 22: jump_reset, 23: full_walkway, 24: iron_boots, 25: pyramids, 26: sign, 27: npc_1, 28: npc_2, 29: npc_3, 30: npc_4, 
         31: floating_ground, 32: floating_sand, 33: invisible_platform}

rocks = {13, 55, 106, 149, 218, 240, 247} # Column numbers for all the rocks
cacti = {11, 53, 107, 228, 255, 280} # Column numbers for the cactuses
full_cacti = {87, 111, 141} # Column numbers for the full cactuses
palm_tree_with_rocks = {22} # Column numbers for the palm_tree_with_rock
signs = {51, 152, 258} # Column numbers for signs

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
    # Stop level 5 music
    pygame.mixer.music.stop()

    # Play the level complete sound once when this function runs
    level_complete_sound.play()

    respawn_gadgets() # Respawn all gadgets on the level
    respawn_powerups() # Respawn all powerups on the level

    update_save(slot, {"Level 5 Checkpoint": 0}) # Set checkpoint to 0
    update_save(slot, {"Level 5 Time": 150}) # Reset the time

    current_state = get_unlock_state(slot, "map2")
    current_state[1] = True  # Unlock level 6 (Map 2 index 1 is equiv Map 2 level 6)
    update_unlock_state(slot, current_state, "map2")

    level_name = "Level Five"


    show_level_complete_deaths(slot, 0, death_count, level_name, background)
    
def npc_spawn():
    level_map[SURFACE][6] = 27 # First NPC
    level_map[SURFACE][54] = 28 # Second NPC
    level_map[SURFACE][84] = 29 # Third NPC
    level_map[SURFACE][243] = 30 # Fourth NPC

    # init sand storm particles
    for _ in range(NUM_SAND_PARTICLES):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        size    = random.randint(2, 5)
        speed   = random.uniform(10, 20)
        drift   = random.uniform(-5, 5)
        sand_particles.append([x, y, size, speed, drift])


def show_game_over_screen(slot: int):

    respawn_gadgets() # Respawn all gadgets on the level
    respawn_powerups() # Respawn all powerups on the level
    
    update_save(slot, {"Level 5 Checkpoint": 0}) # Set checkpoint to 0
    update_save(slot, {"Level 5 Time": 150})

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
                    level_5(slot) # Retry the level
                    sys.exit()
                if select_level_rect.collidepoint(mouse_x, mouse_y):
                    world_select.World_Selector(slot)
                    sys.exit()  # Go back to level select

def respawn_terrain():
    for row_index in range(GROUND, level_height):
        row = [1] * level_width  # Default to full ground row
        for col_index in range(25, 30):  # Remove ground in columns [25-30)
            row[col_index] = 0  # Set to air (pit)
        level_map[row_index] = row  # Add row to level map
        for col_index in range(45, 50):  # Remove ground in columns [45-50)
            row[col_index] = 0  # Set to air (pit)
        for col_index in range(60, 80):  # Remove ground in columns [60-80)
            row[col_index] = 0  # Set to air (pit)
        for col_index in range(85, 105):  # Remove ground in columns [85-105)
            row[col_index] = 0  # Set to air (pit)
        for col_index in range(116, 145):  # Remove ground in columns [116-145)
            row[col_index] = 0  # Set to air (pit)
        for col_index in range(160, 190):  # Remove ground in columns [160-190)
            row[col_index] = 0  # Set to air (pit)
        for col_index in range(230, 235):  # Remove ground in columns [230-235)
            row[col_index] = 0  # Set to air (pit)
        for col_index in range(260, 270):  # Remove ground in columns [260-270)
            row[col_index] = 0  # Set to air (pit)
        level_map[row_index] = row  # Add row to level map

    for row_index in range(SURFACE-1, GROUND): # Raised Ground
        level_map[row_index][15:20] = [1] * 5
    for row_index in range(GROUND, level_height): # Sand
        level_map[row_index][85:105] = [8] * 20
    for row_index in range(SURFACE-2, GROUND): # Raised Ground
        level_map[row_index][110:113] = [1] * 3
    for row_index in range(SURFACE-5, GROUND): # Raised Ground
        level_map[row_index][113:116] = [1] * 3
    for row_index in range(GROUND, level_height): # Sand
        level_map[row_index][136:145] = [8] * 9
    for row_index in range(SURFACE, level_height): # Sand
        level_map[row_index][145:160] = [8] * 15
    for row_index in range(GROUND, level_height): # Sand
        level_map[row_index][210:225] = [8] * 15
    for row_index in range(SURFACE-2, level_height): # Sand
        level_map[row_index][225:230] = [8] * 5
    for row_index in range(SURFACE-6, level_height): # Sand
        level_map[row_index][248:253] = [8] * 5
    for row_index in range(SURFACE-10, level_height): # Raised Sand
        level_map[row_index][253:257] = [8] * 4
    for row_index in range(SURFACE-14, level_height): # Raised Sand
        level_map[row_index][257:260] = [8] * 3

    # Make terrain before this line (unless it's floating). The next code block calculates the ground levels.

    # Find the ground level for each column
    global ground_levels
    ground_levels = [len(level_map)] * len(level_map[0])
    # Find the ground level for each column
    for row_index, row in enumerate(level_map):
        for col_index, tile in enumerate(row):
            if (tile == 1 or tile == 8) and ground_levels[col_index] == len(level_map):
                ground_levels[col_index] = row_index

    level_map[7][12:15] = [2] * 3 # Platform Tiles

    level_map[SURFACE-7][25:35] = [31] * 10 # Floating Ground
    level_map[SURFACE-6][25:35] = [3] * 10 # Floating Dirt

    level_map[SURFACE-8][27:31] = [4] * 4 # Thorns

    level_map[SURFACE][37] = 4 # Thorns

    level_map[SURFACE-7][40:50] = [31] * 10 # Floating Ground
    level_map[SURFACE-6][40:50] = [3] * 10 # Floating Dirt

    level_map[SURFACE-8][46:50] = [4] * 4 # Thorns

    level_map[SURFACE-9][43] = 16 # Full Cactus

    level_map[SURFACE-7][55:65] = [31] * 10 # Floating Ground
    level_map[SURFACE-6][55:65] = [3] * 10 # Floating Dirt

    level_map[SURFACE-9][57] = 25 # Pyramids

    level_map[level_height-2][60:80] = [5] * 20 # Water Block
    level_map[level_height-1][60:80] = [6] * 20 # Water Block

    level_map[SURFACE][82] = 7 # Flag

    level_map[SURFACE][91:93] = [4] * 2 # Thorns
    level_map[SURFACE][96:98] = [4] * 2 # Thorns
    level_map[SURFACE][101:103] = [4] * 2 # Thorns

    level_map[4][81:84] = [2] * 3 # Platform Tiles

    for row_index in range(0, SURFACE-13): # Dirt Block
        level_map[row_index][124] = 10
        level_map[row_index][125] = 3
        level_map[row_index][126] = 11
    
    level_map[level_height-2][160:190] = [5] * 30 # Water Block
    level_map[level_height-1][160:190] = [6] * 30 # Water Block

    level_map[SURFACE][190:210] = [4] * 20 # Thorns

    level_map[8][133] = 2 # Platform Tile of Coin

    level_map[7][168] = 2 # Platform Tile
    level_map[SURFACE-12][174] = 2 # Platform Tile
    level_map[7][180] = 2 # Platform Tile

    level_map[SURFACE-1][158] = 19 # Spring

    level_map[SURFACE][212] = 7 # Flag

    level_map[SURFACE][221] = 4 # Thorns

    level_map[SURFACE-6][235:240] = [32] * 5
    level_map[SURFACE-5][235:240] = [3] * 5
    level_map[SURFACE-4][235:240] = [3] * 5
    level_map[SURFACE-3][235:240] = [3] * 5

    level_map[SURFACE-7][240] = 23 # Full Walkway/Bridge
    level_map[SURFACE-6][240:248] = [33] * 8 # Invisible Platform for the Full Walkway

    level_map[SURFACE-1][274] = 25 # Pyramids
    level_map[SURFACE-1][282] = 25 # Pyramids

def respawn_gadgets():
    level_map[3][82] = 14 # Speed Boots

    level_map[SURFACE][58] = 17 # Glider

    level_map[SURFACE-13][174] = 18 # Double Jump Boots

    level_map[SURFACE-5][243] = 18 # Double Jump Boots

    level_map[SURFACE][245] = 24 # Iron Boots

def respawn_powerups():
    level_map[SURFACE-2][18] = 13 # High Jump
    level_map[SURFACE-8][33] = 13 # High Jump
    level_map[SURFACE-6][114] = 15 # Balloon

    level_map[SURFACE-3][147] = 20 # Dash Powerup

    level_map[SURFACE][126] = 22 # Jump Reset
    level_map[SURFACE][132] = 22 # Jump Reset

    level_map[9][139] = 22 # Jump Reset

    level_map[3][152] = 21 # Left Dash Powerup

    level_map[SURFACE-10][197] = 22 # Jump Reset
    level_map[SURFACE-5][232] = 22 # Jump Reset
    level_map[SURFACE-1][232] = 22 # Jump Reset

def init_sandstorm():
    STORM_LAYERS.clear()

    def make_layer(scale_factor, alpha_min, alpha_max):
        # small noise surface, then smoothly scale up → soft, blended shapes
        tiny = pygame.Surface((WIDTH // scale_factor, HEIGHT // scale_factor), pygame.SRCALPHA)
        for x in range(tiny.get_width()):
            for y in range(tiny.get_height()):
                base_col = random.choice(SAND_PALETTE)
                # subtle shade variation
                col = (
                    base_col[0] + random.randint(-8, 8),
                    base_col[1] + random.randint(-8, 8),
                    base_col[2] + random.randint(-8, 8),
                    random.randint(alpha_min, alpha_max)  # per‑pixel alpha
                )
                tiny.set_at((x, y), col)
        # blow it up so tiny specks smear into smoky waves
        return pygame.transform.smoothscale(tiny, (WIDTH * 2, HEIGHT))

    # two depths → parallax & thickness
    front  = make_layer(scale_factor=4, alpha_min=60, alpha_max=95)
    back   = make_layer(scale_factor=6, alpha_min=30, alpha_max=70)

    # store as [surface, x_offset, scroll_speed]
    STORM_LAYERS.append([back,   0, -1.2])   # slow, distant sheet
    STORM_LAYERS.append([front,  0, -3.5])   # fast, near sheet

def spawn_sandstorm():
    sand_particles.clear()
    for _ in range(NUM_SAND_PARTICLES):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        size = random.randint(2, 5)
        # strong leftward push, light vertical wobble
        x_vel = random.uniform(-120, -60) / 60     # px per frame
        y_vel = random.uniform(-20, 20)   / 60
        sand_particles.append([x, y, size, x_vel, y_vel])

def level_5(slot: int):

    respawn_terrain()
    respawn_gadgets()
    respawn_powerups()
    npc_spawn()
    spawn_sandstorm()
    init_sandstorm() 

    # Stop any previously playing music 
    pygame.mixer.music.stop()
    
    # Load the tutorial music
    pygame.mixer.music.load("Audio/Level5.mp3")
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

    checkpoints = [(calculate_x_coordinate(5), calculate_y_coordinate(SURFACE)), (calculate_x_coordinate(82), calculate_y_coordinate(SURFACE)), (calculate_x_coordinate(212), calculate_y_coordinate(SURFACE))]
    checkpoint_bool = [False] * len(checkpoints)
    checkpoint_bool[0] = True
    checkpoint_idx = load_save(slot).get("Level 5 Checkpoint")
    if not checkpoint_idx:
        checkpoint_idx = 0
    for i in range(checkpoint_idx+1):
        checkpoint_bool[i] = True

    # Camera position
    camera_x = 0
    # (5, SURFACE) should be the starting point
    player_x = checkpoints[checkpoint_idx][0]  # Start x position, change this number to spawn in a different place
    player_y = checkpoints[checkpoint_idx][1]  # Start y position, change this number to spawn in a different place

    # 8.5 should be standard speed
    player_speed = 8.5 * scale_factor # Adjust player speed according to their resolution
    player_vel_x = 0 # Horizontal velocity for friction/sliding
    player_vel_y = 0 # Vertical velocity for jumping
    gravity = 1.25 * scale_factor # Gravity effect (Greater number means stronger gravity)
    jump_power = -18 * scale_factor # Jump strength (Bigger negative number means higher jump)
    on_ground = False # Track if player is on the ground

    bubbleJump = False
    higherJumps = False
    hasBalloon = False
    balloon_vel = 0  # Initial vertical velocity

    coin_count = 0



    times_passed_wooden_sign = 0
    time_before_pop_up_disappears = 0



    # FOR KENNY TO USE (gadget booleans)
    doubleJumpBoots = False
    speedBoots = False
    ironBoots = False
    glider = False
    gliderActive = False
    dashed = False
    dash_duration = 0
    balloon_vel = 0
    powerup_respawns = {}

    animation_index = 0  # Alternates between 0 and 1
    animation_timer = 0  # Tracks when to switch frames
    animation_speed = 4  # Adjust this to control animation speed
    direction = 1  # 1 for right, -1 for left

    normal_friction = 0.25
    ice_friction = 0.95  # Lower friction for slippery effect
    on_ice = False

    dying = False
    death_count = load_save(slot).get("Level 5 Deaths")
    if not death_count:
        death_count = 0

    collidable_tiles = {1, 2, 3, 8, 31, 32, 33}
    dying_tiles = {4, 5, 6, 9, 10, 11}

    start_time = load_save(slot).get("Level 5 Time") # Timer resumes from last time they saved
    if not start_time:
        start_time = 150  # Timer starts at 150 seconds
    timer = start_time
    clock = pygame.time.Clock()

    running = True
    while running:
        
        # print(f"Row: SURFACE - {SURFACE - calculate_row(player_y)}")
        # print(f"Column: {calculate_column(player_x)}")

        screen.blit(background, (0, 0))


        for layer in STORM_LAYERS:
            surf, x_off, speed = layer
            x_off += speed              # move left every frame
            if x_off <= -WIDTH:         # seamless wrap
                x_off += WIDTH
            layer[1] = x_off            # save updated offset

            # Each sheet is 2× screen width → draw twice for wrap
            screen.blit(surf, (x_off, 0))
            screen.blit(surf, (x_off + WIDTH * 2, 0))

        # update & draw sand storm
        for p in sand_particles:
            p[0] += p[3]          # x += x_vel
            p[1] += p[4]          # y += y_vel
            # wrap around screen edges to keep storm continuous
            if p[0] < 0:
                p[0] = WIDTH
                p[1] = random.randint(0, HEIGHT)
            if p[1] < 0 or p[1] > HEIGHT:
                p[1] = random.randint(0, HEIGHT)
            pygame.draw.circle(screen, SAND_COLOR, (int(p[0]), int(p[1])), p[2])


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Pass events to the PauseMenu
            result = pause_menu.handle_event(event, slot)
            if result == "restart":
                timer = None
                update_save(slot, {"Level 5 Checkpoint": 0}) # Set checkpoint to 0
                update_save(slot, {"Level 5 Time": 150})
                level_5(slot)
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if bubbleJump and doubleJumpBoots and not doubleJumped:
                    player_vel_y = jump_power  # Double jump
                    bubbleJump = False
                elif doubleJumpBoots and not doubleJumped:
                    player_vel_y = jump_power  # Double jump
                    doubleJumped = True  # Mark double jump as used
        if pause_menu.paused:
            clock.tick(60)
            continue

        # Draw level using tile images
        for row_index, row in enumerate(level_map):
            for col_index, tile in enumerate(row):
                x, y = col_index * TILE_SIZE - camera_x, row_index * TILE_SIZE
                if tile == 0 or tile == 33: # Continue if air or invisible platform
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

                # Check if player is near the first NPC
        npc_x = calculate_x_coordinate(6)  # First NPC's x position
        npc_y = (SURFACE) * TILE_SIZE  # First NPC's y position
        player_rect = pygame.Rect(player_x - camera_x, player_y, TILE_SIZE, TILE_SIZE)
        npc_rect = pygame.Rect(npc_x - camera_x, npc_y, TILE_SIZE, TILE_SIZE)

        # Handle first NPC dialogue
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()  # Get current time in milliseconds
        handle_level_5_npc_1_dialogue(screen, player_rect, npc_rect, keys, current_time)

        # Check if player is near the second NPC
        npc_x = calculate_x_coordinate(54)  # Second NPC's x position
        npc_y = (SURFACE) * TILE_SIZE  # Second NPC's y position
        player_rect = pygame.Rect(player_x - camera_x, player_y, TILE_SIZE, TILE_SIZE)
        npc_rect = pygame.Rect(npc_x - camera_x, npc_y, TILE_SIZE, TILE_SIZE)

        # Handle second NPC dialogue
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()  # Get current time in milliseconds
        handle_level_5_npc_2_dialogue(screen, player_rect, npc_rect, keys, current_time)

        # Check if player is near the third NPC
        npc_x = calculate_x_coordinate(84)  # Third NPC's x position
        npc_y = (SURFACE) * TILE_SIZE  # Third NPC's y position
        player_rect = pygame.Rect(player_x - camera_x, player_y, TILE_SIZE, TILE_SIZE)
        npc_rect = pygame.Rect(npc_x - camera_x, npc_y, TILE_SIZE, TILE_SIZE)

        # Handle third NPC dialogue
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()  # Get current time in milliseconds
        handle_level_5_npc_3_dialogue(screen, player_rect, npc_rect, keys, current_time)

        # Check if player is near the fourth NPC
        npc_x = calculate_x_coordinate(243)  # Fourth NPC's x position
        npc_y = (SURFACE) * TILE_SIZE  # Fourth NPC's y position
        player_rect = pygame.Rect(player_x - camera_x, player_y, TILE_SIZE, TILE_SIZE)
        npc_rect = pygame.Rect(npc_x - camera_x, npc_y, TILE_SIZE, TILE_SIZE)

        # Handle fourth NPC dialogue
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()  # Get current time in milliseconds
        handle_level_5_npc_4_dialogue(screen, player_rect, npc_rect, keys, current_time)  

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
            if latestTile == 8 or latestTile == 32:
                player_vel_x = player_speed * 0.7
            else:
                player_vel_x = player_speed
            moving = True
            direction = 1
        if keys[pygame.K_a]: # If player presses A
            if latestTile == 8 or latestTile == 32:
                player_vel_x = (player_speed * 0.7) * -1
            else:
                player_vel_x = -player_speed
            moving = True
            direction = -1
        # Jumping Logic (Space Pressed)
        if keys[pygame.K_SPACE]:
            if higherJumps:
                player_vel_y = jump_power * 2
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

        # Pop balloon mechanic
        if keys[pygame.K_r]:
            pop_balloon_sound.play()
            hasBalloon = False

        # Apply gravity when needed
        player_vel_y += gravity
        if keys[pygame.K_e] and glider:
            player_vel_y = gravity
        if hasBalloon:
            player_vel_y = 0
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

                    if tile == 33: # If walkway, ignore collision from left and right and from bottom
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

                # High Jump Functionality
                if tile == 13:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
                        level_map[row_index][col_index] = 0  # Remove the boots from screen
                        power_up_sound.play()
                        higherJumps = True
                        powerup_respawns[(row_index, col_index)] = [13, pygame.time.get_ticks() + 5000]

                # Balloon Functionality
                if tile == 15: 
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):

                        level_map[row_index][col_index] = 0  # Remove the balloon from the map
                        power_up_sound.play()
                        hasBalloon = True
                        balloon_vel = -5  # Initial upward speed
                        powerup_respawns[(row_index, col_index)] = [15, pygame.time.get_ticks() + 5000]

                # Jump reset functionality
                if tile == 22: 
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
                        level_map[row_index][col_index] = 0  # Remove the jump reset from screen
                        bubbleJump = True
                        doubleJumped = False
                        powerup_respawns[(row_index, col_index)] = [22, pygame.time.get_ticks() + 5000]

                # Spring functionality
                if tile == 19:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE >= tile_x and player_x <= tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE >= tile_y and player_y <= tile_y + TILE_SIZE):
                        player_vel_y = -50
                        spring_sound.play()
                        player_vel_y = -50 * scale_factor

                # Double Jump Boots
                if tile == 18:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
                        level_map[row_index][col_index] = 0  # Remove the boots from screen
                        gadget_sound.play()
                        doubleJumpBoots = True
                        doubleJumped = False

                # Speed boots
                if tile == 14:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
                        level_map[row_index][col_index] = 0  # Remove the boots from screen
                        gadget_sound.play()
                        player_speed = player_speed * 1.25 # Up the player speed
                        speedBoots = True

                if tile == 20: # Right Dash
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
                        dash_pickup_time = pygame.time.get_ticks()
                        powerup_respawns[(row_index, col_index)] = [20, pygame.time.get_ticks() + 5000]
                        dash_duration = dash_pickup_time + 500
                        dash_sound.play()
                        dashed = True
                        level_map[row_index][col_index] = 0 
                        dash_sound.play()
                        player_speed = player_speed * 2 
                        direction = 1
                        if player_speed < 0:
                            player_speed *= -1

                if tile == 21: # Left Dash
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):

                        dash_pickup_time = pygame.time.get_ticks()
                        powerup_respawns[(row_index, col_index)] = [21, pygame.time.get_ticks() + 5000]
                        dash_duration = dash_pickup_time + 750
                        dash_sound.play()
                        dashed = True
                        level_map[row_index][col_index] = 0 
                        dash_sound.play()
                        player_speed = player_speed * 3.05
                        direction = -1
                        player_vel_y = 0
                        if player_speed < 0:
                            player_speed *= -1

                if tile == 17: # Picked up glider
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

                if tile == 24: # Picked up iron boots
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE

                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
                        
                        level_map[row_index][col_index] = 0
                        gadget_sound.play()
                        collidable_tiles.remove(33)
                        ironBoots = True
                        player_speed = player_speed / 1.25


        level_name_font = pygame.font.Font('PixelifySans.ttf', 48)  # Larger font for level name
        level_name_text = level_name_font.render("Level 5", True, WHITE)  # White text

        screen.blit(level_name_text, (20, 20))  # Position at (20, 20)

        dt = clock.tick(60) / 1000  # Time elapsed per frame in seconds
        timer -= dt  # Decrease timer
        timer_text = level_name_font.render(f"Time: {int(timer)}", True, RED if timer <= 30 else WHITE)
        screen.blit(timer_text, (WIDTH // 2 - 50, 20))

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
            death_sound.play()

        if dying:
            player_x, player_y = checkpoints[checkpoint_idx][0], checkpoints[checkpoint_idx][1]
            death_count += 1
            update_save(slot, {"Level 5 Deaths": death_count})
            dying = False
            if checkpoint_idx == 0:
                glider = False
                level_map[SURFACE][58] = 17 # Glider
                level_map[GROUND][30:35] = [1] * 5
                level_map[GROUND][40:45] = [1] * 5
                for row_index in range(GROUND+1, level_height):
                    level_map[row_index][30:35] = [3] * 5
                    level_map[row_index][40:45] = [3] * 5
            if checkpoint_idx == 1:
                speedBoots = False
                doubleJumpBoots = False
                level_map[3][82] = 14 # Speed Boots
                level_map[SURFACE-13][174] = 18 # Double Jump Boots
            if checkpoint_idx == 2:
                collidable_tiles.add(33)
                ironBoots = False
                doubleJumpBoots = False
                level_map[SURFACE][245] = 24 # Iron Boots
                level_map[SURFACE-5][243] = 18 # Double Jump Boots


        for k, checkpoint in enumerate(checkpoints):
            x, y = checkpoint
            if player_x >= x and player_y <= y and player_y >= (y - (TILE_SIZE * 4)) and not checkpoint_bool[k]:
                checkpoint_idx += 1
                checkpoint_bool[k] = True
                update_save(slot, {"Level 5 Checkpoint": checkpoint_idx})
                update_save(slot, {"Level 5 Time": timer})
                if checkpoint_idx == 1:
                    glider = False
                    level_map[SURFACE][58] = 17 # Glider
                elif checkpoint_idx == 2:
                    doubleJumpBoots = False
                    speedBoots = False
                    level_map[SURFACE-13][174] = 18 # Double Jump Boots
                    level_map[3][82] = 14 # Speed Boots

        # Set speed back for player if dashing
        if dashed:
            # print("Player speed: " + str(player_speed))
            if (current_time >= dash_duration) and (dash_duration != 0):
                player_speed = 8.5 * scale_factor
                dashed = False
                dash_duration = 0

        # Set speed to normal if no boots
        if not speedBoots and not dashed and not ironBoots:
            player_speed = 8.5 * scale_factor
        if hasBalloon:
            player_y += balloon_vel  # Move up
            balloon_vel -= 0.001  # Gradually slow down (simulating air resistance)

            if player_y + TILE_SIZE < 0:  # If the player moves off the top of the screen
                hasBalloon = False  # Pop the balloon
                balloon_vel = 0  # Reset velocity
        
        # Modified powerup respawns to singular function
        powerup_remove = []
        for position, gadget in powerup_respawns.items():
            if current_time >= gadget[1]:
                level_map[position[0]][position[1]] = gadget[0]
                powerup_remove.append(position) # mark for removal

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

        if ironBoots:
            inv_slots.append(inventory_iron_boots)

        if speedBoots:
            inv_slots.append(inventory_speed_boots)

        for x, gadget in enumerate(inv_slots):
            screen.blit(gadget, inv_slot_dimensions[x])
        

        
        
        # print(calculate_column(player_x))
        # Pop up near level completion 
        if (pygame.time.get_ticks() < time_before_pop_up_disappears):
            screen.blit(level_almost_complete_popup, (pop_up_x, pop_up_y))
            screen.blit(level_almost_complete_text, level_almost_complete_rect)
            screen.blit(keep_heading_right_text, keep_heading_right_rect)


        if (calculate_column(player_x) >= 257 and times_passed_wooden_sign < 1):
            times_passed_wooden_sign += 1
            screen.blit(level_almost_complete_popup, (pop_up_x, pop_up_y))
            screen.blit(level_almost_complete_text, level_almost_complete_rect)
            screen.blit(keep_heading_right_text, keep_heading_right_rect)
            time_before_pop_up_disappears = pygame.time.get_ticks() + 5000



    
        pygame.display.flip()  # Update display

if __name__ == "__main__":
    level_5(1)
    pygame.quit()