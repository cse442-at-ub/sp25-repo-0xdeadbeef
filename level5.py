import pygame # type: ignore
import sys
import world_select
from saves_handler import *
from firework_level_end import show_level_complete_deaths
from pause_menu import PauseMenu  # Import the PauseMenu class

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
pygame.display.set_caption("Level 5")

ground_tile = pygame.image.load("./desert_images/ground.png")
ground_tile = pygame.transform.scale(ground_tile, (TILE_SIZE, TILE_SIZE))

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
pyramids = pygame.transform.scale(pyramids, (TILE_SIZE, TILE_SIZE))

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

coin = pygame.image.load("./images/coin.png")
coin = pygame.transform.scale(coin, (TILE_SIZE, TILE_SIZE))

high_jump = pygame.image.load("./images/high_jump.png")
high_jump = pygame.transform.scale(high_jump, (TILE_SIZE, TILE_SIZE))

speed_boots = pygame.image.load("./images/speed_boots.png")
speed_boots = pygame.transform.scale(speed_boots, (TILE_SIZE, TILE_SIZE))

balloon = pygame.image.load("./images/balloon.png")
balloon = pygame.transform.scale(balloon, (TILE_SIZE, TILE_SIZE))

glider = pygame.image.load("./images/balloon.png")
glider = pygame.transform.scale(glider, (TILE_SIZE, TILE_SIZE))

# Set up the level with a width of 300 and a height of 30 rows
level_width = 300
level_height = HEIGHT // TILE_SIZE  # Adjust level height according to user's resolution

level_map = [[0] * level_width for _ in range(level_height)]  # Start with air
ground_levels = None

GROUND = level_height - 4 #Constant for the ground level
SURFACE = GROUND - 1 #Constant for the surface level

WHITE = (255, 255, 255)
RED = (255, 0, 0) # For timer
BLUE = (0, 0, 255) # For hover

# Initialize the PauseMenu
pause_menu = PauseMenu(screen)

level_map[5][13] = 12  # Coin

# Dictionary containing which tile corresponds to what
tiles = {0: background, 1: ground_tile, 2: platform_tile, 3: dirt_tile,  4: thorns, 5: water, 6: water_block, 7: flag, 8: sand, 9: flipped_thorn, 10: left_thorn,
         11: right_thorn, 12: coin, 13: high_jump, 14: speed_boots, 15: balloon, 16: full_cactus, 17: glider}

rocks = {13, 55, 106} # Column numbers for all the rocks
cacti = {11, 53, 107} # Column number for the cactuses
full_cacti = {87, 111} # Column number for the full cactuses
palm_tree_with_rocks = {22} # Column number for the palm_tree_with_rock

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

    show_level_complete_deaths(slot, 0, death_count)

def show_game_over_screen(slot: int):
    
    update_save(slot, {"Level 5 Checkpoint": 0}) # Set checkpoint to 0
    update_save(slot, {"Level 5 Time": 150})

def respawn_terrain():
    for row_index in range(GROUND, level_height):
        row = [1] * level_width  # Default to full ground row
        for col_index in range(25, 30):  # Remove ground in columns 25-34
            row[col_index] = 0  # Set to air (pit)
        level_map[row_index] = row  # Add row to level map
        for col_index in range(45, 50):  # Remove ground in columns 45-49
            row[col_index] = 0  # Set to air (pit)
        for col_index in range(60, 80):  # Remove ground in columns 60-79
            row[col_index] = 0  # Set to air (pit)
        for col_index in range(85, 105):  # Remove ground in columns 85-104
            row[col_index] = 0  # Set to air (pit)
        for col_index in range(116, 145):  # Remove ground in columns 116-144
            row[col_index] = 0  # Set to air (pit)
        level_map[row_index] = row  # Add row to level map

    # Add solid ground at the very bottom
    level_map.append([1] * level_width)

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

    level_map[SURFACE-7][25:35] = [1] * 10 # Floating Ground
    level_map[SURFACE-6][25:35] = [3] * 10 # Floating Dirt

    level_map[SURFACE-8][27:31] = [4] * 4 # Thorns

    level_map[SURFACE][37] = 4 # Thorns

    level_map[SURFACE-7][40:50] = [1] * 10 # Floating Ground
    level_map[SURFACE-6][40:50] = [3] * 10 # Floating Dirt

    level_map[SURFACE-9][43] = 16 # Full Cactus

    level_map[SURFACE-7][55:65] = [1] * 10 # Floating Ground
    level_map[SURFACE-6][55:65] = [3] * 10 # Floating Dirt

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

def respawn_gadgets():
    level_map[3][82] = 14 # Speed Boots
    level_map[SURFACE][58] = 17 # Glider

def respawn_powerups():
    level_map[SURFACE-2][18] = 13 # High Jump
    level_map[SURFACE-6][114] = 15 # Balloon

def level_5(slot: int):

    respawn_terrain()
    respawn_gadgets()
    respawn_powerups()

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

    checkpoints = [(calculate_x_coordinate(5), calculate_y_coordinate(SURFACE))]
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

    collidable_tiles = {1, 2, 3, 8}
    dying_tiles = {4, 5, 6, 9, 10, 11}

    start_time = load_save(slot).get("Level 5 Time") # Timer resumes from last time they saved
    if not start_time:
        start_time = 150  # Timer starts at 150 seconds
    timer = start_time
    clock = pygame.time.Clock()

    running = True
    while running:
        
        print(f"Row: SURFACE - {SURFACE - calculate_row(player_y)}")
        print(f"Column: {calculate_column(player_x)}")

        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Pass events to the PauseMenu
            pause_menu.handle_event(event, slot)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pass
        if pause_menu.paused:
            clock.tick(60)
            continue

        # Draw level using tile images
        for row_index, row in enumerate(level_map):
            for col_index, tile in enumerate(row):
                x, y = col_index * TILE_SIZE - camera_x, row_index * TILE_SIZE
                if tile == 0:
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

        acceleration = 0.5  # Slower acceleration on ice
        friction = normal_friction if not on_ice else ice_friction

        # Handle events
        keys = pygame.key.get_pressed()
        moving = False
        if keys[pygame.K_w]:
            player_y -= player_speed
        if keys[pygame.K_s]:
            player_y += player_speed
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

        # Apply gravity
        # if not hasBalloon:
        #     player_vel_y += gravity
        #     player_y += player_vel_y

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
                    
                        dying = True
                        death_sound.play()

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

        # Camera follows player
        camera_x = max(0, min(player_x - WIDTH // 2, (level_width * TILE_SIZE) - WIDTH))
    
        pygame.display.flip()  # Update display

if __name__ == "__main__":
    level_5(1)
    pygame.quit()