import pygame  # type: ignore
import random  # For random snow positions and speeds
import achievement_menu  # Import the achievements menu

import pygame_widgets
from pygame_widgets.slider import Slider

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Settings Menu")

# BLIZZARD SETUP (same as before, but we preserve it here)
num_snowflakes = random.randint(0, 25)  # random between 50 and 200
snowflakes = []

def create_blizzard():
    """Create snowflakes with random positions and speeds."""
    for _ in range(num_snowflakes):
        x = random.randint(0, WIDTH)
        y = random.randint(-HEIGHT, 0)
        speed_x = random.uniform(-1, 0.5)
        speed_y = random.uniform(1, 2.5)
        size = random.randint(4, 7)
        snowflakes.append([x, y, speed_x, speed_y, size])

def update_and_draw_blizzard():
    """Update snowflake positions and draw them on the screen."""
    for flake in snowflakes:
        flake[0] += flake[2]  # Horizontal wind
        flake[1] += flake[3]  # Vertical fall
        # Reset snowflake if it goes below the screen
        if flake[1] > HEIGHT:
            flake[0] = random.randint(0, WIDTH)
            flake[1] = random.randint(-50, -10)
            flake[2] = random.uniform(-1, 1)
            flake[3] = random.uniform(1, 2.5)
            flake[4] = random.randint(4, 7)
        pygame.draw.circle(screen, (255, 255, 255), (flake[0], flake[1]), flake[4])

# Load and scale the Settings background
settings_bg = pygame.image.load("Assets/Settings Menu/SettingsMenuBackground.png").convert_alpha()
settings_bg = pygame.transform.scale(settings_bg, (WIDTH, HEIGHT))

# Load and scale "text only" images
movement_img = pygame.image.load("Assets/Settings Menu/MovementSettings.png").convert_alpha()
movement_img = pygame.transform.scale(movement_img, (600, 200))  # Scale to desired size

audio_img = pygame.image.load("Assets/Settings Menu/AudioSettings.png").convert_alpha()
audio_img = pygame.transform.scale(audio_img, (400, 150))  # Scale to desired size

# Define rects for the images
movement_rect = movement_img.get_rect(center=(WIDTH // 2, 200))  # Near top center
audio_rect = audio_img.get_rect(center=(WIDTH // 2.25, 400))     # A bit lower

# Achievements button (hoverable)
achievements_normal = pygame.image.load("Assets/Settings Menu/AchievementsButton.png").convert_alpha()
achievements_hover = pygame.transform.scale(achievements_normal, (int(achievements_normal.get_width() * 1.1),
                                                                  int(achievements_normal.get_height() * 1.1)))
achievements_rect = achievements_normal.get_rect(center=(WIDTH // 2, 600))

# Back button (hoverable)
back_normal = pygame.image.load("Assets/Settings Menu/BackButton.png").convert_alpha()
back_hover = pygame.transform.scale(back_normal, (int(back_normal.get_width() * 1.1),
                                                 int(back_normal.get_height() * 1.1)))
back_rect = back_normal.get_rect(center=(WIDTH // 2.05, 800))  # Near bottom center

# Volume slider
slider = None

def run_settings_menu():
    """Run the settings menu."""
    global slider
    create_blizzard()

    # Set up the volume slider
    slider = Slider(
        screen,
        x=(WIDTH // 2) - 200,  # Center position of the slider
        y=500,                 # Near the bottom of the screen
        width=400, height=10,
        min=0, max=99, step=1,
        colour=(200, 195, 218),       # Track color (light purple)
        handleColour=(255, 255, 255),   # Handle color (light blue)
        initial=50
    )

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return False  # Exit the program

            # Handle clicks on Achievements and Back
            if event.type == pygame.MOUSEBUTTONDOWN:
                if achievements_rect.collidepoint(event.pos):
                    # Switch to Achievements page
                    if not achievement_menu.run_achievements_menu():
                        return False  # Exit the program
                elif back_rect.collidepoint(event.pos):
                    running = False  # Go back to main menu

        # Draw the background
        screen.blit(settings_bg, (0, 0))

        # Draw the blizzard behind everything
        update_and_draw_blizzard()

        # Draw the “MovementSettings” and “AudioSettings” images (not buttons)
        screen.blit(movement_img, movement_rect)
        screen.blit(audio_img, audio_rect)

        # Check if mouse is over Achievements
        mouse_pos = pygame.mouse.get_pos()
        if achievements_rect.collidepoint(mouse_pos):
            hover_rect = achievements_hover.get_rect(center=achievements_rect.center)
            screen.blit(achievements_hover, hover_rect)
        else:
            screen.blit(achievements_normal, achievements_rect)

        # Check if mouse is over Back
        if back_rect.collidepoint(mouse_pos):
            hover_rect = back_hover.get_rect(center=back_rect.center)
            screen.blit(back_hover, hover_rect)
        else:
            screen.blit(back_normal, back_rect)

        # Update the slider and draw it
        pygame_widgets.update(events)

        # Update the display
        pygame.display.flip()

    return True  # Go back to main menu

# Main loop
if __name__ == "__main__":
    if run_settings_menu():
        print("Returned to main menu.")
    pygame.quit()  # Close Pygame