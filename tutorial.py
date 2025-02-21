import pygame # type: ignore

# Initialize PyGame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1200, 600
TILE_SIZE = 40  # Adjusted for better layout
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tutorial Level")

# Load tile images (ensure they are the same size)
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

# Set up the level with a width of 125 and an initial height of 11 rows
level_width = 200
level_height = 20  # Adjust height as needed

level_map = [[0] * level_width for _ in range(level_height)]  # Start with air

# Add ground with an **endless pit** at columns 20-25
for row_index in range(11, level_height):  # Only draw ground from row 11 down
    row = [1] * level_width  # Default to full ground row
    if row_index >= 10:  # At row 10 and below, create a pit
        for col_index in range(20, 25):  # Remove ground in columns 20-25
            row[col_index] = 0  # Set to air (pit)
        for col_index in range(70, 85):
            row[col_index] = 0  # Set to air (pit)
    level_map[row_index] = row  # Add row to level map

# Add solid ground at the very bottom
level_map.append([1] * level_width)  # Only if you want a final boundary

level_map[6][35:40] = [1] * 5
level_map[5][55:60] = [2] * 5
level_map[9][74:76] = [2] * 2

# Find the ground level for each column
ground_levels = [len(level_map)] * len(level_map[0])
for row_index, row in enumerate(level_map):
    for col_index, tile in enumerate(row):
        if tile == 1 and ground_levels[col_index] == len(level_map):
            ground_levels[col_index] = row_index

level_map[10][28] = 6 #Boots
level_map[10][60] = 7
level_map[8][62] = 8

level_map[4][57] = 6 #Boots

# Camera position
camera_x = 0
player_x = 100  # Start position
player_y = 400
player_speed = 3

# npc_x = 1000
# npc_y = 400

# Main loop
running = True
while running:
    screen.blit(background, (0, 0))

    # Draw level using tile images
    for row_index, row in enumerate(level_map):
        for col_index, tile in enumerate(row):
            x, y = col_index * TILE_SIZE - camera_x, row_index * TILE_SIZE
            if tile == 1:
                screen.blit(ground_tile, (x, y))  # Draw ground
            elif tile == 2:
                screen.blit(platform_tile, (x, y))  # Draw platform
            elif tile == 6:
                screen.blit(boots, (x, y)) #Draw boots
            elif tile == 7:
                screen.blit(flipped_npc, (x, y)) #Draw NPC
            elif tile == 8:
                screen.blit(house, (x, y)) #Draw house

    # Draw dirt below ground
    for col_index, ground_y in enumerate(ground_levels):
        for row_index in range(ground_y + 1, len(level_map) + 10):  # Extra depth
            x, y = col_index * TILE_SIZE - camera_x, row_index * TILE_SIZE
            screen.blit(dirt_tile, (x, y))  # Draw dirt using image

    for i in range(10, 100, 20):  # Adding trees at columns 10 to 15
        x = i * TILE_SIZE - camera_x
        y = (ground_levels[i] - 3) * TILE_SIZE  # Place tree 2 tiles above the ground
        screen.blit(tree, (x, y))

    # Draw player
    pygame.draw.rect(screen, (255, 0, 0), (player_x - camera_x, player_y, TILE_SIZE, TILE_SIZE))

    # Handle events
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_LEFT]:
        player_x -= player_speed

    # Camera follows player
    camera_x = max(0, min(player_x - WIDTH // 2, (level_width * TILE_SIZE) - WIDTH))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()  # Update display

pygame.quit()
