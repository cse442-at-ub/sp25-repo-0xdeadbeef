import pygame # type: ignore
import random

import world_select 

# Initialize PyGame
pygame.init()

# Screen settings

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h # Will only work with resolutions 1920 x 1080 or better
TILE_SIZE = 40  # Adjusted for better layout

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tutorial Level")

# Load all the images into their respective variables
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

npc = pygame.image.load("./images/sprite.png")
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

level_map[SURFACE - 5][53:58] = [2] * 5   # Platform containing speed boots
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
tiles = {1: ground_tile, 2: platform_tile, 3: boots, 4: flipped_npc, 5: house, 6: thorn, 7: flag, 8: super_speed_powerup, 9: dash_powerup, 10: fence, 11: sign, 12: npc} 

level_map[SURFACE][28], level_map[SURFACE-6][55] = 3, 3 # Boots
level_map[SURFACE][60] = 4 # NPC 
level_map[SURFACE-2][62] = 5 # House

level_map[SURFACE][98:104] , level_map[SURFACE][113:115]= [6] * 6, [6] * 2 # Thorns
level_map[SURFACE][87] = 7 # Flag

level_map[SURFACE][95] = 8 # Super speed power up
level_map[SURFACE-2][113] = 9 # Dash power up

level_map[SURFACE-6][122:124] = [10] * 2 # Fence
level_map[SURFACE-7][135:140] = [10] * 5 # Fence

level_map[SURFACE-7][130] = 11 # Sign

rocks = {14, 33, 45, 68, 108, 124} # Column numbers for all the rocks
trees = {10, 30, 50, 90} # Column numbers for all the trees
background_trees = {16, 42, 55, 93, 133} # Column numbers for all the background trees


# Converts the x coordinates to the column on the map
def calculate_column(x): 
    return x // TILE_SIZE

# Converts the column number to the x-coordinate
def calculate_x_coordinate(column):
    return column * TILE_SIZE

def tutorial_level():

    # Camera position
    camera_x = 0
    player_x = 200  # Start position, change this number to spawn in a different place
    player_y = HEIGHT - 200
    player_speed = (WIDTH // 640) * 2 # Adjust player speed according to their resolution

    player_vel_y = 0 # Vertical velocity for jumping
    gravity = 1 # Gravity effect (Greater number means stronger gravity)
    jump_power = -16 # Jump strength (Bigger negative number means higher jump)
    on_ground = False # Track if player is on the ground

    # Main loop
    running = True
    while running:
        screen.blit(background, (0, 0))

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

        # Draw player
        pygame.draw.rect(screen, (255, 0, 0), (player_x - camera_x, player_y, TILE_SIZE, TILE_SIZE))

        # Handle events
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: # If player presses D or right arrow key
            player_x += player_speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: # If player presses A or left arrow key
            player_x -= player_speed
        if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and on_ground: # If player presses Space bar or W key
            player_vel_y = jump_power # Apply jump force
            on_ground = False # Player is now airborne

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
            

        if player_x >= level_width * TILE_SIZE:  # If player reaches the end of the level
            running = False

        # Camera follows player
        camera_x = max(0, min(player_x - WIDTH // 2, (level_width * TILE_SIZE) - WIDTH))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()

        pygame.display.flip()  # Update display


if __name__ == "__main__":
    tutorial_level()
    pygame.quit()