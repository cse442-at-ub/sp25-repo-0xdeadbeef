import pygame   # type: ignore
import random   # For random snow positions and speeds
import main_menu 
import achievement_menu
import save_slots
import statistics_menu  # Add this import at the top

import pygame_widgets  # type: ignore
from pygame_widgets.slider import Slider # type: ignore
from pygame_widgets.textbox import TextBox  # type: ignore

pygame.init()   # Initialize Pygame
pygame.mixer.init() # Initialize Pygame Audio Mixer
current_volume_value = 20

info = pygame.display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Settings Menu")

# BLIZZARD SETUP (same as before, but we preserve it here)
num_snowflakes = random.randint(25, 50)  # random between 25 and 50
snowflakes = []

for i in range(num_snowflakes):
    x = random.randint(0, WIDTH)
    y = random.randint(-HEIGHT, 0)
    speed_x = random.uniform(-1, 0.5)
    speed_y = random.uniform(1, 0.5)
    size = random.randint(4, 7)
    snowflakes.append([x, y, speed_x, speed_y, size])

def update_and_draw_blizzard():
    for flake in snowflakes:
        flake[0] += flake[2]  # horizontal wind
        flake[1] += flake[3]  # vertical fall
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

# Images that are "text only" (not buttons)
movement_img = pygame.image.load("Assets/Settings Menu/MovementSettings.png").convert_alpha()
audio_img = pygame.image.load("Assets/Settings Menu/AudioSettings.png").convert_alpha()

# Scale them to match your design if desired
movement_img = pygame.transform.scale(movement_img, (600, 300)) 
audio_img = pygame.transform.scale(audio_img, (400, 150))       

# Define rects for those images
movement_rect = movement_img.get_rect(center=(WIDTH // 2, 200))  # near top center
audio_rect = audio_img.get_rect(center=(WIDTH // 2.25, 400))     # a bit lower

# Achievements button (hoverable)
achievements_normal = pygame.image.load("Assets/Settings Menu/AchievementsButton.png").convert_alpha()
achievements_hover = pygame.transform.scale(achievements_normal, (int(achievements_normal.get_width()*1.1),
                                                                  int(achievements_normal.get_height()*1.1)))
achievements_rect = achievements_normal.get_rect(center=(WIDTH // 2 - 200, 600))  # Moved left to make room for Statistics

# Statistics button (hoverable)
statistics_normal = pygame.image.load("Assets/Settings Menu/StatisticsButton.png").convert_alpha()
statistics_hover = pygame.transform.scale(statistics_normal, (int(statistics_normal.get_width()*1.1),
                                                             int(statistics_normal.get_height()*1.1)))
statistics_rect = statistics_normal.get_rect(center=(WIDTH // 2 + 200, 600))  # Positioned to the right of Achievements

# Back button (hoverable)
back_normal = pygame.image.load("Assets/Settings Menu/BackButton.png").convert_alpha()
back_hover = pygame.transform.scale(back_normal, (int(back_normal.get_width()*1.1),
                                                 int(back_normal.get_height()*1.1)))
back_rect = back_normal.get_rect(center=(WIDTH // 2.05, 800))  # near bottom center

slider = None

def run_settings_menu():
    # Check if any music is currently playing
    if not pygame.mixer.music.get_busy():
        # If not, load the "Background.mp3" again
        pygame.mixer.music.load("Audio/Background.mp3")
        pygame.mixer.music.play(-1)  # loop forever

    # create_blizzard()

    # Set up the volume slider 
    global slider, current_volume_value

    slider = Slider(
        screen, 
        x=(WIDTH // 2) - 200,  # center position of the slider 
        y=500,                 # near the bottom of the screen
        width=400, height=10,
        min=0, max=99, step=1,
        colour=(200, 195, 218),       # track color (light purple)
        handleColour=(255, 255, 255),   # handle color (light blue)
        initial=current_volume_value
    )

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            
            # Handle clicks on Achievements and Back
            if event.type == pygame.MOUSEBUTTONDOWN:
                if achievements_rect.collidepoint(event.pos):
                    print("Achievements clicked. Going to achievements...")
                    running = False
                    achievement_menu.run_achievements_menu() # Go to achievements menu
                elif statistics_rect.collidepoint(event.pos):
                    print("Statistics clicked. Going to statistics...")
                    running = False
                    statistics_menu.run_statistics_menu() # Go to statistics menu
                elif back_rect.collidepoint(event.pos):
                    print("Back clicked. Going to main menu...")
                    running = False
                    main_menu.run_main_menu() # Go back to main menu

        # Draw the background
        screen.blit(settings_bg, (0, 0))

        # Draw the blizzard behind everything
        update_and_draw_blizzard()

        # Draw the "MovementSettings" and "AudioSettings" images (not buttons)
        screen.blit(movement_img, movement_rect)
        screen.blit(audio_img, audio_rect)

        # Check if mouse is over Achievements
        mouse_pos = pygame.mouse.get_pos()
        if achievements_rect.collidepoint(mouse_pos):
            hover_rect = achievements_hover.get_rect(center=achievements_rect.center)
            screen.blit(achievements_hover, hover_rect)
        else:
            screen.blit(achievements_normal, achievements_rect)

        # Check if mouse is over Statistics
        if statistics_rect.collidepoint(mouse_pos):
            hover_rect = statistics_hover.get_rect(center=statistics_rect.center)
            screen.blit(statistics_hover, hover_rect)
        else:
            screen.blit(statistics_normal, statistics_rect)

        # Check if mouse is over Back
        if back_rect.collidepoint(mouse_pos):
            hover_rect = back_hover.get_rect(center=back_rect.center)
            screen.blit(back_hover, hover_rect)
        else:
            screen.blit(back_normal, back_rect)
  

        pygame_widgets.update(events) # Update the slider and draw it

        # Get slider value (0 to 100) and convert to 0.0-1/0 for set_volume()
        current_value = slider.getValue()
        pygame.mixer.music.set_volume(current_value / 100.0) # Set volume based on slider
        current_volume_value = current_value

        pygame.display.flip()

# Settings menu
if __name__ == "__main__":
    run_settings_menu()
    pygame.quit()  # Close Pygame