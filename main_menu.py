import pygame   # type: ignore
import random   #For random snow positions and speeds
import settings_menu 


pygame.init()   # Initialize Pygame

WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu with Hover Effect")

# BLIZZARD SETUP
num_snowflakes = random.randint(50, 200) # randomly set the number of snowflakes to something between 50 and 2000
snowflakes = []

def create_blizzard():
    # Create initial snowflakes at random positions, with random speeds."""
    for i in range(num_snowflakes):
        x = random.randint(0, WIDTH)
        y = random.randint(-HEIGHT, 0)  # start above the screen
        speed_x = random.uniform(-1, 1) # wind: flakes drift left/right
        speed_y = random.uniform(1, 0.5)  # fall speed (slow and steady)
        size = random.randint(4, 7)    # flake size for thick snow
        snowflakes.append([x, y, speed_x, speed_y, size])

def update_and_draw_blizzard():
    # Move snowflakes in a slow, windy pattern and draw them.
    for flake in snowflakes:
        # flake: [x, y, speed_x, speed_y, size]
        flake[0] += flake[2]  # move horizontally (wind)
        flake[1] += flake[3]  # move downward
        if flake[1] > HEIGHT - 300:
            # Reset flake to the top once it goes past the bottom
            flake[0] = random.randint(0, WIDTH)
            flake[1] = random.randint(-50, -10)
            flake[2] = random.uniform(-1, 1)
            flake[3] = random.uniform(1, 2.5)
            flake[4] = random.randint(4, 7)
        # Draw the flake as a white circle
        pygame.draw.circle(screen, (255, 255, 255), (flake[0], flake[1]), flake[4])

# Load and scale the background
bg = pygame.image.load("Assets/Main Menu/MainMenuBackground.png").convert_alpha()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

# --- Load button images ---
# Normal images
start_normal = pygame.image.load("Assets/Main Menu/StartGameButton.png").convert_alpha()
settings_normal = pygame.image.load("Assets/Main Menu/SettingsButton.png").convert_alpha()
exit_normal = pygame.image.load("Assets/Main Menu/ExitButton.png").convert_alpha()

# Scale normal size (wider and taller for a more relaxed look)
start_normal = pygame.transform.scale(start_normal, (450, 120))
settings_normal = pygame.transform.scale(settings_normal, (450, 120))
exit_normal = pygame.transform.scale(exit_normal, (250, 120))

# Hover images (slightly bigger for a highlight effect)
start_hover = pygame.transform.scale(start_normal, (550, 130))
settings_hover = pygame.transform.scale(settings_normal, (550, 130))
exit_hover = pygame.transform.scale(exit_normal, (350, 130))

# --- Define button positions ---
# We'll center them and space them vertically
start_rect = start_normal.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
settings_rect = settings_normal.get_rect(center=(WIDTH // 2, HEIGHT // 2))
exit_rect = exit_normal.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))

# Initialize snow before main loop
def run_main_menu():
    create_blizzard() # Initialize snow

    running = True
    while running:
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If a button is clicked, print an action
                if start_rect.collidepoint(event.pos):
                    print("Start Game")
                    # Switch to your game or next screen
                elif settings_rect.collidepoint(event.pos):
                    print("Settings")

                    # Stop main menu loop, call settings menu 
                    running = False
                    settings_menu.run_settings_menu()
                elif exit_rect.collidepoint(event.pos):
                    print("Exit")
                    running = False

        # Clear screen by drawing background
        screen.blit(bg, (0, 0))

        # [ADDED] Update and draw the blizzard behind the buttons
        update_and_draw_blizzard()

        # Get current mouse position
        mouse_pos = pygame.mouse.get_pos()

        # --- Draw Start Button ---
        if start_rect.collidepoint(mouse_pos):
            hover_rect = start_hover.get_rect(center=start_rect.center)
            screen.blit(start_hover, hover_rect)
        else:
            screen.blit(start_normal, start_rect)
        
        # --- Draw Settings Button ---
        if settings_rect.collidepoint(mouse_pos):
            hover_rect = settings_hover.get_rect(center=settings_rect.center)
            screen.blit(settings_hover, hover_rect)
        else:
            screen.blit(settings_normal, settings_rect)
        
        # --- Draw Exit Button ---
        if exit_rect.collidepoint(mouse_pos):
            hover_rect = exit_hover.get_rect(center=exit_rect.center)
            screen.blit(exit_hover, hover_rect)
        else:
            screen.blit(exit_normal, exit_rect)

        # Update the window
        pygame.display.flip()

        
# Start the main menu
if __name__ == "__main__":
    run_main_menu()
    pygame.quit()  # Quit Pygame   
