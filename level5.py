import pygame # type: ignore
import sys
import world_select
from saves_handler import *
from pause_menu import PauseMenu  # Import the PauseMenu class

# Initialize PyGame
pygame.init()

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

background = pygame.image.load("./desert_images/background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Set up the level with a width of 300 and a height of 30 rows
level_width = 300
level_height = HEIGHT // TILE_SIZE  # Adjust level height according to user's resolution

level_map = [[0] * level_width for _ in range(level_height)]  # Start with air

GROUND = level_height - 4 #Constant for the ground level
SURFACE = GROUND - 1 #Constant for the surface level

WHITE = (255, 255, 255)
RED = (255, 0, 0) # For timer
BLUE = (0, 0, 255) # For hover

# Initialize the PauseMenu
pause_menu = PauseMenu(screen)

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
    pass

def show_game_over_screen(slot: int):
    
    update_save(slot, {"Level 5 Checkpoint": 0}) # Set checkpoint to 0
    update_save(slot, {"Level 5 Time": 150})

def respawn_terrain():
    pass

def respawn_gadgets():
    pass

def respawn_powerups():
    pass

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

    start_time = load_save(slot).get("Level 5 Time") # Timer resumes from last time they saved
    if not start_time:
        start_time = 150  # Timer starts at 150 seconds
    timer = start_time
    clock = pygame.time.Clock()

    running = True
    while running:
        
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

        level_name_font = pygame.font.Font('PixelifySans.ttf', 48)  # Larger font for level name
        level_name_text = level_name_font.render("Level 4", True, WHITE)  # White text

        screen.blit(level_name_text, (20, 20))  # Position at (20, 20)

        dt = clock.tick(60) / 1000  # Time elapsed per frame in seconds
        timer -= dt  # Decrease timer
        timer_text = level_name_font.render(f"Time: {int(timer)}", True, RED if timer <= 30 else WHITE)
        screen.blit(timer_text, (WIDTH // 2 - 50, 20))
    
        pygame.display.flip()  # Update display

if __name__ == "__main__":
    level_5(1)
    pygame.quit()