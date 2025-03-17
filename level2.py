import pygame # type: ignore
import random
import sys
import world_select
import json

# Initialize PyGame
pygame.init()

# Screen settings

BASE_WIDTH = 1920
BASE_HEIGHT = 1080

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h # Will only work with resolutions 1920 x 1080 or better

TILE_SIZE = 40  # Adjusted for better layout

scale_factor = HEIGHT / BASE_HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Level 2")

ground_tile = pygame.image.load("./images/ground.png")
ground_tile = pygame.transform.scale(ground_tile, (TILE_SIZE, TILE_SIZE))

floating_ground = ground_tile

platform_tile = pygame.image.load("./images/platform.png")
platform_tile = pygame.transform.scale(platform_tile, (TILE_SIZE, TILE_SIZE))

dirt_tile = pygame.image.load("./images/dirt.png")
dirt_tile = pygame.transform.scale(dirt_tile, (TILE_SIZE, TILE_SIZE))

background = pygame.image.load("./images/background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Scale to screen size

invisible_platform = None

tree = pygame.image.load("./images/tree.png")
tree = pygame.transform.scale(tree, (TILE_SIZE * 2, TILE_SIZE * 3))  # Resize tree to fit properly

double_jump_boots = pygame.image.load("./images/boots.png")
double_jump_boots = pygame.transform.scale(double_jump_boots, (TILE_SIZE, TILE_SIZE))

speed_boots = pygame.image.load("./images/speed_boots.png")
speed_boots = pygame.transform.scale(speed_boots, (TILE_SIZE, TILE_SIZE))

house = pygame.image.load("./images/house.png")
house = pygame.transform.scale(house, (TILE_SIZE * 5, TILE_SIZE * 3))

thorn = pygame.image.load("./images/thorn.png")
thorn = pygame.transform.scale(thorn, (TILE_SIZE, TILE_SIZE))

flag = pygame.image.load("./images/flag.png")
flag = pygame.transform.scale(flag, (TILE_SIZE, TILE_SIZE))

super_speed_powerup = pygame.image.load("./images/super_speed_powerup.png")
super_speed_powerup = pygame.transform.scale(super_speed_powerup, (TILE_SIZE, TILE_SIZE))

dash_powerup = pygame.image.load("./images/dash_powerup.png")
dash_powerup = pygame.transform.scale(dash_powerup, (TILE_SIZE, TILE_SIZE))

up_dash = pygame.transform.rotate(dash_powerup, 90)
left_dash = pygame.transform.flip(dash_powerup, True, False)

coin = pygame.image.load("./images/coin.png")
coin = pygame.transform.scale(coin, (TILE_SIZE, TILE_SIZE))

fence = pygame.image.load("./images/fence.png")
fence = pygame.transform.scale(fence, (TILE_SIZE, TILE_SIZE // 2))

sign = pygame.image.load("./images/sign.png")
sign = pygame.transform.scale(sign, (TILE_SIZE, TILE_SIZE))

rock = pygame.image.load("./images/rock.png")
rock = pygame.transform.scale(rock, (TILE_SIZE, TILE_SIZE // 2))

background_tree = pygame.image.load("./images/background_tree.png")
background_tree = pygame.transform.scale(background_tree, (TILE_SIZE * 1.5, TILE_SIZE * 2))

water = pygame.image.load("./images/water.png")
water = pygame.transform.scale(water, (TILE_SIZE, TILE_SIZE))

walkway = pygame.image.load("./images/walkway.png")
walkway = pygame.transform.scale(walkway, (TILE_SIZE * 4, TILE_SIZE * 2))
flipped_walkway = pygame.transform.flip(walkway, True, False)  # Flip horizontally (True), no vertical flip (False)

ice_tile = pygame.image.load("./images/ice.png")
ice_tile = pygame.transform.scale(ice_tile, (TILE_SIZE, TILE_SIZE))
flipped_ice = pygame.transform.flip(ice_tile, False, True)

windmill = pygame.image.load("./images/windmill.png")
windmill = pygame.transform.scale(windmill, (TILE_SIZE * 3, TILE_SIZE * 4))

jump_reset = pygame.image.load("./images/bubble.png")
jump_reset = pygame.transform.scale(jump_reset, (TILE_SIZE, TILE_SIZE))

spring = pygame.image.load("./images/spring.png")
spring= pygame.transform.scale(spring, (TILE_SIZE, TILE_SIZE))

# Set up the level with a width of 200 and a height of 27 rows
level_width = 280
level_height = HEIGHT // TILE_SIZE  # Adjust level height according to user's resolution

level_map = [[0] * level_width for _ in range(level_height)]  # Start with air

GROUND = level_height - 2 #Constant for the ground level
SURFACE = GROUND - 1 #Constant for the surface level

# This is for the snowflake animations
WHITE = (255, 255, 255)
NUM_SNOWFLAKES = 200
snowflakes = []

#This for loop is also for snowflakes
for _ in range(NUM_SNOWFLAKES):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    size = random.randint(2, 6)  # Random size
    speed = random.uniform(10, 12)  # Falling speed
    x_speed = random.uniform(-2, 2)  # Small horizontal drift
    snowflakes.append([x, y, size, speed, x_speed])

for row_index in range(GROUND, level_height):  # Only draw ground from row 23 down
    row = [1] * level_width  # Default to full ground row
    if row_index >= 12:  # At row 10 and below, create a pit
        for col_index in range(8, 18):  # Remove ground in columns 8-18
            row[col_index] = 0  # Set to air (pit)
        for col_index in range(25, 36):
            row[col_index] = 0
        for col_index in range(66, 86):
            row[col_index] = 0
        for col_index in range(96, 101):
            row[col_index] = 0
        for col_index in range(115, 120):
            row[col_index] = 0
        for col_index in range(125, 135):
            row[col_index] = 0
        for col_index in range(135, 140):
            row[col_index] = 0
        for col_index in range(145, 166):
            row[col_index] = 0
        for col_index in range(167, 176):
            row[col_index] = 0
        for col_index in range(186, 190):
            row[col_index] = 0
        for col_index in range(191, 195):
            row[col_index] = 0
        for col_index in range(196, 200):
            row[col_index] = 0
        for col_index in range(210, 260):
            row[col_index] = 0
    level_map[row_index] = row  # Add row to level map

# Add solid ground at the very bottom
level_map.append([1] * level_width)

for row_index in range(SURFACE - 6, GROUND): #Raised Ground
    level_map[row_index][30] = 1
for row_index in range(SURFACE - 4, GROUND): #Raised Ground
    level_map[row_index][18:25] = [1] * 7
for row_index in range(SURFACE - 1, GROUND): #Raised Ground
    level_map[row_index][36:45] = [1] * 9
for row_index in range(SURFACE - 3, GROUND): #Raised Ground
    level_map[row_index][45:50] = [1] * 5
for row_index in range(SURFACE - 5, GROUND): #Raised Ground
    level_map[row_index][50:60] = [1] * 10
for row_index in range(SURFACE - 7, GROUND): #Raised Ground
    level_map[row_index][60:65] = [1] * 5
for row_index in range(SURFACE - 13, GROUND): #Raised Ground
    level_map[row_index][65] = 1
for row_index in range(SURFACE - 13, GROUND): #Raised Ground
    level_map[row_index][86:96] = [1] * 10
for row_index in range(SURFACE - 8, GROUND): #Raised Ground
    level_map[row_index][120:125] = [1] * 5
for row_index in range(0, SURFACE - 4):
    level_map[row_index][101:115] = [14] * 14
for row_index in range(GROUND, level_height-1):
    level_map[row_index][125:135] = [16] * 10
    level_map[row_index][140:145] = [16] * 5
for row_index in range(GROUND+1, level_height):
    level_map[row_index][125:135] = [17] * 10
    level_map[row_index][140:145] = [17] * 5
for row_index in range(SURFACE - 4, GROUND): #Raised Ground
    level_map[row_index][176:186] = [1] * 10
for row_index in range(SURFACE - 5, GROUND): #Raised Ground
    level_map[row_index][190] = 1
for row_index in range(SURFACE - 5, GROUND): #Raised Ground
    level_map[row_index][195] = 1
for row_index in range(SURFACE - 10, GROUND): #Raised Ground
    level_map[row_index][200:210] = [1] * 10
for row_index in range(SURFACE - 5, SURFACE - 4):
    level_map[row_index][215:220] = [16] * 5
for row_index in range(SURFACE - 4, SURFACE - 3):
    level_map[row_index][215:220] = [17] * 5
for row_index in range(SURFACE - 6, SURFACE - 5):
    level_map[row_index][225:227] = [16] * 2
for row_index in range(SURFACE - 5, SURFACE - 4):
    level_map[row_index][225:227] = [17] * 2
for row_index in range(SURFACE - 8, SURFACE - 7):
    level_map[row_index][232:234] = [16] * 2
for row_index in range(SURFACE - 7, SURFACE - 6):
    level_map[row_index][232:234] = [17] * 2
for row_index in range(SURFACE - 10, GROUND): #Raised Ground
    level_map[row_index][260:280] = [1] * 20


# Make terrain before this line. The next code block calculates the ground levels

# Find the ground level for each column
ground_levels = [len(level_map)] * len(level_map[0])
for row_index, row in enumerate(level_map):
    for col_index, tile in enumerate(row):
        if tile == 1 and ground_levels[col_index] == len(level_map):
            ground_levels[col_index] = row_index

# All code after this line should be for props, npcs, gadgets, and powerups. Terrain should not be made here.

level_map[SURFACE-16][0:10] = [2] * 10 # Platform
level_map[SURFACE-15][15] = 2 # Platform
level_map[SURFACE-17][5:10] = [6] * 5 # Thorn
level_map[SURFACE-18][1] = 12 # Coin

level_map[SURFACE-2][12] = 20 # Jump Reset

level_map[SURFACE-5][23] = 13 # Super Speed Powerup
level_map[SURFACE-2][39] = 13 # Super Speed Powerup

level_map[SURFACE-10][21:23] = [2] * 2 # Platform
level_map[SURFACE-8][62] = 3 # Double Jump Boots
level_map[SURFACE-13][30:65] = [5] * 35 # Floating Ground
level_map[SURFACE-7][30] = 6 # Thorn

level_map[SURFACE-14][55], level_map[SURFACE-9][122], level_map[SURFACE-11][206] = 7, 7, 7 # Flag
level_map[SURFACE-14][63] = 11 # Speed Boots

level_map[SURFACE-14][66] = 8 # Walkway
level_map[SURFACE-13][66:70] = [10] * 4
level_map[SURFACE-14][82] = 9 # Flipped Walkway
level_map[SURFACE-13][82:86] = [10] * 4

level_map[SURFACE-14][92:96] = [6] * 4 # Thorn
level_map[SURFACE][101:104] = [6] * 3 # Thorn

level_map[level_height-1][66:86] = [4] * 20 # Water
level_map[level_height-1][96:101] = [4] * 5 # Water

level_map[SURFACE-3][118] = 21 # Upwards Dash Powerup
level_map[6][145] = 22 #Left Dash Powerup
level_map[10][135] = 12 # Coin

level_map[SURFACE-2][149] = 2 # Platform
level_map[SURFACE-4][150] = 16 # Ice tile
level_map[SURFACE-3][150] = 17 # Flipped ice tile

level_map[SURFACE-7][153] = 2 # Platform
level_map[SURFACE-9][154] = 16 # Ice tile
level_map[SURFACE-8][154] = 17 # Flipped ice tile

level_map[SURFACE-12][150] = 2 # Platform
level_map[SURFACE-14][149] = 16 # Ice tile
level_map[SURFACE-13][149] = 17 # Flipped ice tile

level_map[SURFACE-17][153] = 2 # Platform
level_map[SURFACE-19][154] = 16 # Ice tile
level_map[SURFACE-18][154] = 17 # Flipped ice tile

level_map[SURFACE][166] = 23 # Spring

level_map[SURFACE-5][178] = 3 # Double Jump Boots
level_map[SURFACE-11][208] = 11 # Super Speed Boots

level_map[SURFACE-6][190], level_map[SURFACE-6][195] = 6, 6 # Thorns

level_map[SURFACE-5][197] = 20 # Jump Reset
level_map[SURFACE-10][242] = 20 # Jump Reset
level_map[SURFACE-10][252] = 20 # Jump Reset

level_map[SURFACE-13][262] = 18 # House
level_map[SURFACE-14][270] = 19 # Windmill


# Dictionary containing which tile corresponds to what
tiles = {1: ground_tile, 2: platform_tile, 3: double_jump_boots, 4: water, 5: floating_ground, 6: thorn, 7: flag, 8: walkway, 9: flipped_walkway, 10: invisible_platform,
         11: speed_boots, 12: coin, 13: super_speed_powerup, 14: dirt_tile, 15: dash_powerup, 16: ice_tile, 17: flipped_ice, 18: house, 19: windmill, 20: jump_reset,
         21: up_dash, 22: left_dash, 23: spring}

rocks = {43, 55, 107} # Column numbers for all the rocks
trees = {20, 51, 201, 276} # Column numbers for all the trees
background_trees = {46, 88, 180, 274} # Column numbers for all the background trees

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

def show_level_completed_screen(slot: int):
    # Display the background image
    screen.blit(background, (0, 0))

    # Set fonts for the text
    title_font = pygame.font.Font('PixelifySans.ttf', 100)
    menu_font = pygame.font.Font('PixelifySans.ttf', 60)

    # Render the "Level Completed" text
    level_completed_text = title_font.render("Level Completed", True, (255, 255, 255))
    select_level_text = menu_font.render("Back to Select Level", True, (255, 255, 255))

    # Position the texts
    level_completed_rect = level_completed_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    select_level_rect = select_level_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 120))

    # Create box around the text
    box_padding = 20
    level_end_screen_box = pygame.Rect(level_completed_rect.left - box_padding, level_completed_rect.top - box_padding, level_completed_rect.width + box_padding*2, level_completed_rect.height + (box_padding*2) + 80)
    pygame.draw.rect(screen, (0, 0, 255), level_end_screen_box, 10)
    
    # Draw the texts
    screen.blit(level_completed_text, level_completed_rect)
    screen.blit(select_level_text, select_level_rect)

    pygame.display.flip()

    # Wait for player to either press a key or click the button
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    waiting = False  # You could also go back to level select here

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if select_level_rect.collidepoint(mouse_x, mouse_y):
                    world_select.World_Selector(slot)
                    sys.exit()  # Go back to level select


def read_data(slot: int):
    with open(f"./User Saves/save{str(slot)}.json", "r") as file:
        data = json.load(file)
    return data.get("character")

# Function to run the tutorial level
def level_2(slot: int):
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
    player_speed = 6.5 * scale_factor # Adjust player speed according to their resolution

    player_vel_y = 0 # Vertical velocity for jumping
    gravity = 1.2 / scale_factor # Gravity effect (Greater number means stronger gravity)
    jump_power = -21 / scale_factor # Jump strength (Bigger negative number means higher jump)
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

    #-----Declared variables for Dash power-up to avoid undefined variable error
    dash_respawn_time = 0 
    dash_pickup_time = 0
    dash_duration = 0
    dashing = False

    checkpoints = [(player_x, player_y), (calculate_x_coordinate(55), calculate_y_coordinate(SURFACE-14)), (calculate_x_coordinate(122), calculate_y_coordinate(SURFACE-9)),
                   (calculate_x_coordinate(206), calculate_y_coordinate(SURFACE-11))]
    checkpoint_bool = [False] * len(checkpoints)
    checkpoint_bool[0] = True
    checkpoint_idx = 0
    dying = False
    death_count = 0
    collidable_tiles = {1, 2, 5, 10, 14, 16, 17, 23}

    coin_count = 0

    running = True
    while running:
        screen.blit(background, (0, 0))

        level_name_font = pygame.font.Font('PixelifySans.ttf', 48)  # Larger font for level name
        level_name_text = level_name_font.render("Level 2", True, (255, 255, 255))  # White text

        screen.blit(level_name_text, (20, 20))  # Position at (20, 20)
        # Draw level using tile images
        for row_index, row in enumerate(level_map):
            for col_index, tile in enumerate(row):
                x, y = col_index * TILE_SIZE - camera_x, row_index * TILE_SIZE
                if tile == 0 or tile == 10: # Continue if the tile is an air block or invisible platform
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
                
                
                # This code picks up the double jump boots
                if tile == 3:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
                        level_map[row_index][col_index] = 0  # Remove the boots from screen
                        doubleJumpBoots = True
                        doubleJumped = False

                # If player touches water
                if tile == 4 or tile == 6:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
                        
                        dying = True

                # This code picks up the speed boots
                if tile == 11:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
                        level_map[row_index][col_index] = 0  # Remove the boots from screen
                        player_speed = player_speed * 1.25 # Up the player speed
                        speedBoots = True

                # Super Speed Powerup
                if tile == 13: 
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):

                        level_map[row_index][col_index] = 0
                        player_speed *= 2  # Double the speed
                        super_speed_effects.append({"end_time": pygame.time.get_ticks() + 2000})  # 2 sec effect
                        super_speed_respawns[(row_index, col_index)] = pygame.time.get_ticks() + 5000  # 5 sec respawn

                # Coin
                if tile == 12:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):

                        coin_count += 1
                        level_map[row_index][col_index] = 0

                # Dash (Modify so that it's all dashes regardless of direction)
                if tile == 15:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):

                        dash_pickup_time = pygame.time.get_ticks()
                        dash_respawn_time = dash_pickup_time + 5000
                        level_map[row_index][col_index] = 0 
                        player_speed = player_speed * 2
                        dash_duration = pygame.time.get_ticks() + 200
                        dashing = True

        # Inside the game loop
        current_time = pygame.time.get_ticks()

        # Apply speed effects from multiple power-ups
        for effect in super_speed_effects[:]:  # Iterate over a copy of the list
            if current_time >= effect["end_time"]:  # Check if effect expired
                player_speed /= 2
                super_speed_effects.remove(effect)

        # Respawn power-ups after 5 seconds
        to_remove = []
        for pos, respawn_time in super_speed_respawns.items():
            if current_time >= respawn_time:
                level_map[pos[0]][pos[1]] = 13  # Respawn power-up
                to_remove.append(pos)  # Mark for removal

        # Remove respawned power-ups from tracking
        for pos in to_remove:
            del super_speed_respawns[pos]

        # # Apply dash powerup
        # if dashing:
        #     player_x += player_speed
        #     if (pygame.time.get_ticks() >= dash_duration) and (dash_duration != 0):
        #         player_speed = player_speed / 2
        #         dashing = False
        #         dash_duration = 0

        # #-----Respawns Dash power-up after 5 seconds
        # if (dash_respawn_time > 0 ) and (pygame.time.get_ticks() >= dash_respawn_time):
        #     level_map[SURFACE-2][113] = 9
        #     dash_respawn_time = 0

        if player_x + TILE_SIZE >= level_width * TILE_SIZE:  # If player reaches the end of the level
            show_level_completed_screen(slot)
            running = False
        

        if player_x <= 0: # Ensure player is within the bounds of the level and does not go to the left
            player_x = 0

        if player_y + TILE_SIZE >= level_height * TILE_SIZE:
            dying = True

        if dying:
            player_x, player_y = checkpoints[checkpoint_idx][0], checkpoints[checkpoint_idx][1]
            death_count += 1
            dying = False

        for k, checkpoint in enumerate(checkpoints):
            x, y = checkpoint
            if player_x >= x and not checkpoint_bool[k]:
                checkpoint_idx += 1
                checkpoint_bool[k] = True
                if checkpoint_idx == 2:
                    doubleJumpBoots = False # Remove their double jump boots
                    player_speed = player_speed / 1.25 # Revert their speed back to normal

        # Camera follows player
        camera_x = max(0, min(player_x - WIDTH // 2, (level_width * TILE_SIZE) - WIDTH))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()  # Update display

if __name__ == "__main__":
    level_2()
    pygame.quit()