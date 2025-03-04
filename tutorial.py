import pygame # type: ignore
import random
import sys

# Initialize PyGame
pygame.init()

# Screen settings

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h # Will only work with resolutions 1920 x 1080 or better
# print(str(WIDTH) + " " + str(HEIGHT))
TILE_SIZE = 40  # Adjusted for better layout

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tutorial Level")

# Load all the images into their respective variables
player = pygame.image.load("./animations/right-stand.png")
player = pygame.transform.scale(player, (TILE_SIZE, TILE_SIZE))
flipped_player = pygame.transform.flip(player, True, False)

run = pygame.image.load("./animations/right-run.png")
run = pygame.transform.scale(run, (TILE_SIZE, TILE_SIZE))
flipped_run = pygame.transform.flip(run, True, False)

run_frames = [
    pygame.image.load("./animations/right-walk.png"),
    pygame.image.load("./animations/right-run.png")
]

run_frames = [pygame.transform.scale(frame, (TILE_SIZE, TILE_SIZE)) for frame in run_frames]

ground_tile = pygame.image.load("./images/ground.png")
ground_tile = pygame.transform.scale(ground_tile, (TILE_SIZE, TILE_SIZE))

platform_tile = pygame.image.load("./images/platform.png")
platform_tile = pygame.transform.scale(platform_tile, (TILE_SIZE, TILE_SIZE))

dirt_tile = pygame.image.load("./images/dirt.png")
dirt_tile = pygame.transform.scale(dirt_tile, (TILE_SIZE, TILE_SIZE))

background = pygame.image.load("./images/background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Scale to screen size

tree = pygame.image.load("./images/tree.png")
tree = pygame.transform.scale(tree, (TILE_SIZE * 2, TILE_SIZE * 3))  # Resize tree to fit properly

boots = pygame.image.load("./images/boots.png")
boots = pygame.transform.scale(boots, (TILE_SIZE, TILE_SIZE))

speed_boots = pygame.image.load("./images/speed_boots.png")
speed_boots = pygame.transform.scale(speed_boots, (TILE_SIZE, TILE_SIZE))

npc = pygame.image.load("./Character Combinations/black hair_dark_blue shirt_black pants.png")
npc = pygame.transform.scale(npc, (TILE_SIZE, TILE_SIZE))
flipped_npc = pygame.transform.flip(npc, True, False)  # Flip horizontally (True), no vertical flip (False)

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

fence = pygame.image.load("./images/fence.png")
fence = pygame.transform.scale(fence, (TILE_SIZE, TILE_SIZE // 2))

sign = pygame.image.load("./images/sign.png")
sign = pygame.transform.scale(sign, (TILE_SIZE, TILE_SIZE))

rock = pygame.image.load("./images/rock.png")
rock = pygame.transform.scale(rock, (TILE_SIZE, TILE_SIZE // 2))

background_tree = pygame.image.load("./images/background_tree.png")
background_tree = pygame.transform.scale(background_tree, (TILE_SIZE * 1.5, TILE_SIZE * 2))

# Set up the level with a width of 140 and a height of 40 rows
level_width = 140
level_height = HEIGHT // TILE_SIZE  # Adjust level height according to user's resolution

level_map = [[0] * level_width for _ in range(level_height)]  # Start with air

GROUND = level_height - 4 #Constant for the ground level
SURFACE = GROUND - 1 #Constant for the surface level

# This is for the snowflake animations
WHITE = (255, 255, 255)
NUM_SNOWFLAKES = 100
snowflakes = []

#This for loop is also for snowflakes
for _ in range(NUM_SNOWFLAKES):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    size = random.randint(2, 6)  # Random size
    speed = random.uniform(1, 6)  # Falling speed
    x_speed = random.uniform(-0.5, 0.5)  # Small horizontal drift
    snowflakes.append([x, y, size, speed, x_speed])

for row_index in range(GROUND, level_height):  # Only draw ground from row 23 down
    row = [1] * level_width  # Default to full ground row
    if row_index >= 10:  # At row 10 and below, create a pit
        for col_index in range(20, 25):  # Remove ground in columns 20-25
            row[col_index] = 0  # Set to air (pit)
        for col_index in range(70, 85):
            row[col_index] = 0  # Set to air (pit)
        for col_index in range(115, 120):
            row[col_index] = 0  # Set to air (pit)
    level_map[row_index] = row  # Add row to level map

# Add solid ground at the very bottom
level_map.append([1] * level_width)

for row_index in range(SURFACE - 4, GROUND): #Raised Ground
    level_map[row_index][35:40] = [1] * 5

level_map[SURFACE - 4][53:58] = [2] * 5   # Platform containing speed boots
level_map[SURFACE - 1][74:76] = [2] * 2   # Platform

for row_index in range(SURFACE - 1, GROUND): #Raised Ground
    level_map[row_index][123:126] = [1] * 3
for row_index in range(SURFACE - 2, GROUND): #Raised Ground
    level_map[row_index][126:128] = [1] * 2
for row_index in range(SURFACE - 6, GROUND): #Raised Ground
    level_map[row_index][128:140] = [1] * 12

level_map[SURFACE - 5][122:124] = [2] * 2 # Platform

# Make terrain before this line. The next code block calculates the ground levels

# Find the ground level for each column
ground_levels = [len(level_map)] * len(level_map[0])
for row_index, row in enumerate(level_map):
    for col_index, tile in enumerate(row):
        if tile == 1 and ground_levels[col_index] == len(level_map):
            ground_levels[col_index] = row_index

# All code after this line should be for props, npcs, gadgets, and powerups. Terrain should not be made here.

# Dictionary containing which tile corresponds to what
tiles = {1: ground_tile, 2: platform_tile, 3: boots, 4: flipped_npc, 5: house, 6: thorn, 7: flag, 8: super_speed_powerup, 9: dash_powerup, 10: fence, 11: sign, 12: npc, 13: speed_boots} 

level_map[SURFACE][28] = 3 # Jump Boots
level_map[SURFACE-5][55] = 13 # Speed Boots
level_map[SURFACE][60] = 4 # NPC 
level_map[SURFACE-2][62] = 5 # House

level_map[SURFACE][98:104] , level_map[SURFACE][113:115]= [6] * 6, [6] * 2 # Thorns
level_map[SURFACE][87] = 7 # Flag

level_map[SURFACE][95] = 8 # Super speed powerup
level_map[SURFACE-2][113] = 9 # Dash powerup

level_map[SURFACE-6][122:124] = [10] * 2 # Fence
level_map[SURFACE-7][135:140] = [10] * 5 # Fence

level_map[SURFACE-7][130] = 11 # Sign

rocks = {14, 33, 45, 68, 108, 124} # Column numbers for all the rocks
trees = {10, 30, 50, 90} # Column numbers for all the trees
background_trees = {16, 42, 55, 93, 133} # Column numbers for all the background trees

# Converts the x coordinates to the column on the map
def calculate_column(x): 
    return int(x // TILE_SIZE)

# Converts the column number to the x-coordinate
def calculate_x_coordinate(column):
    return int(column * TILE_SIZE)

def tutorial_level():

    # Camera position
    camera_x = 0
    player_x = 200  # Start position, change this number to spawn in a different place
    player_y = HEIGHT - 200
    player_speed = (WIDTH // 640) * 2 # Adjust player speed according to their resolution

    player_vel_y = 0 # Vertical velocity for jumping
    gravity = 1.5 # Gravity effect (Greater number means stronger gravity)
    jump_power = -20 # Jump strength (Bigger negative number means higher jump)
    on_ground = False # Track if player is on the ground
    doubleJumpBoots = False # Track if player has double jump boots
    doubleJumped = False # Track if player double jumped already

    animation_index = 0  # Alternates between 0 and 1
    animation_timer = 0  # Tracks when to switch frames
    animation_speed = 4  # Adjust this to control animation speed
    direction = 1  # 1 for right, -1 for left

    #-----Declared variables for speed boost to avoid undefined variable error
    super_speed_bool = False
    super_speed_respawn_time = 0
    super_speed_pickup_time = 0
    super_speed_effect_off_time = 0

    #-----Declared variables for Dash power-up to avoid undefined variable error
    dash_respawn_time = 0 
    dash_pickup_time = 0
    dash_duration = 0
    dashing = False

    # Main loop
    running = True
    while running:
        screen.blit(background, (0, 0))

        #-----Get the current time of the game in milliseconds (for power-up resetting)
        Game_time = pygame.time.get_ticks()

        # Draw level using tile images
        for row_index, row in enumerate(level_map):
            for col_index, tile in enumerate(row):
                x, y = col_index * TILE_SIZE - camera_x, row_index * TILE_SIZE
                if tile == 0: # Continue if the tile is an air block
                    continue
                if tile == 10: #Draw the fence at half size
                    screen.blit(tiles.get(tile), (x, y + TILE_SIZE // 2))
                else: # Draw according to the dictionary
                    screen.blit(tiles.get(tile), (x, y))
                if calculate_column(player_x) >= 60:
                    level_map[SURFACE][60] = 12 # Draw the normal npc
                else:
                    level_map[SURFACE][60] = 4 # Draw the flipped npc

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

        #-----Handle player colliding into Super-Speed Power-up
        if (level_map[calculate_column(player_y)][calculate_column(player_x)]) == level_map[SURFACE][95] and level_map[SURFACE][95] == 8:
            super_speed_pickup_time = pygame.time.get_ticks()
            super_speed_effect_off_time = super_speed_pickup_time + 2000
            super_speed_bool = True
            level_map[SURFACE][95] = 0
            super_speed_respawn_time = super_speed_pickup_time + 10000
            player_speed = player_speed * 2

        #-----Removes super-speed power-up effects after 5 seconds
        if (super_speed_bool == True) and (pygame.time.get_ticks() >= super_speed_effect_off_time):
            player_speed = player_speed / 2
            super_speed_bool = False
            super_speed_pickup_time = 0

        #-----Respawns super-speed power-up after 10 seconds
        if (super_speed_respawn_time > 0) and (pygame.time.get_ticks() >= super_speed_respawn_time): 
            level_map[SURFACE][95] = 8
            super_speed_respawn_time = 0

        #-----Handles player colliding into Dash Power-up
        if (level_map[calculate_column(player_y)][calculate_column(player_x)]) == (level_map[SURFACE-2][113]) and level_map[SURFACE-2][113] == 9:
            dash_pickup_time = pygame.time.get_ticks()
            dash_respawn_time = dash_pickup_time + 5000
            level_map[SURFACE-2][113] = 0 
            player_speed = player_speed * 10
            dash_duration = pygame.time.get_ticks() + 200
            dashing = True
        
        #-----Gives player a "Dash Boost" for approximately a quarter of a second
        if dashing:
            player_x += player_speed
            if (pygame.time.get_ticks() >= dash_duration) and (dash_duration != 0):
                player_speed = player_speed / 10
                dashing = False
                dash_duration = 0

        #-----Respawns Dash power-up after 5 seconds
        if (dash_respawn_time > 0 ) and (pygame.time.get_ticks() >= dash_respawn_time):
            level_map[SURFACE-2][113] = 9
            dash_respawn_time = 0

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
            
            # Jumping Logic (Space/W Pressed)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_w:
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
                if tile in {1, 2}:  # Ground or platform tiles
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

                # This code picks up the speed boots
                if tile == 13:
                    tile_x, tile_y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if (player_x + TILE_SIZE > tile_x and player_x < tile_x + TILE_SIZE and 
                        player_y + TILE_SIZE > tile_y and player_y < tile_y + TILE_SIZE):
                        level_map[row_index][col_index] = 0  # Remove the boots from screen
                        player_speed = player_speed * 1.25 # Up the player speed

        if player_x + TILE_SIZE >= level_width * TILE_SIZE:  # If player reaches the end of the level
            running = False

        if player_x <= 0: # Ensure player is within the bounds of the level and does not go to the left
            player_x = 0

        # Camera follows player
        camera_x = max(0, min(player_x - WIDTH // 2, (level_width * TILE_SIZE) - WIDTH))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()  # Update display

if __name__ == "__main__":
    tutorial_level()
    pygame.quit()