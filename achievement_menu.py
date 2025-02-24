import pygame  # type: ignore

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Achievement Menu")

# Load background image
background_image = pygame.image.load("Assets/Achievement Menu/achievement_background.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Load achievement icons and resize them
icons = [
    pygame.transform.scale(pygame.image.load("Assets/Level Selector/level1_selector_background.png"), (250, 150)) for _ in range(5)
] + [
    pygame.transform.scale(pygame.image.load("Assets/Level Selector/level2_selector_background.png"), (250, 150)) for _ in range(2)
]

# Positions for icons and text
icon_positions = [(80 + i * 330, 100) for i in range(5)] + [(80 + i * 330, 400) for i in range(2)]  # Adjust positions
text_positions = [(pos[0] + 90, pos[1] + 180) for pos in icon_positions]  # Text below icons

# Load and resize yellow circle
yellow_circle = pygame.transform.scale(pygame.image.load("Assets/Achievement Menu/yellow_circle.png"), (140, 140))
yellow_icon_position = (WIDTH // 2 - 825, 700)  # Centered horizontally, adjusted vertically
yellow_text_position = (yellow_icon_position[0] + 40, yellow_icon_position[1] + 160)  # Text below yellow circle

# Font settings
try:
    font = pygame.font.Font("PixelifySans.ttf", 70)  # Large font for numbers and "0x" text
except FileNotFoundError:
    print("Error: Pixelify Sans font file not found. Using default font instead.")
    font = pygame.font.Font(None, 70)  # Fallback to default font with increased size

# Smaller font for the "Back" button
try:
    back_font = pygame.font.Font("PixelifySans.ttf", 36)  # Smaller font size for "Back" text
except FileNotFoundError:
    print("Error: Pixelify Sans font file not found. Using default font instead.")
    back_font = pygame.font.Font(None, 36)  # Fallback to default font with smaller size

# Create a transparent back button
back_button = pygame.Surface((100, 40), pygame.SRCALPHA)  # Use SRCALPHA for transparency
text = back_font.render("Back", True, (255, 255, 255))  # Render text in white using the smaller font
text_rect = text.get_rect(center=(back_button.get_width() // 2, back_button.get_height() // 2))
back_button.blit(text, text_rect)  # Draw text onto the transparent surface

# Button positions (keep centered after cropping)
back_rect = back_button.get_rect(center=(WIDTH // 2, HEIGHT - 50))
achievements_bg = pygame.image.load("Assets/Achievement Menu/achievement_background.png")
achievements_bg = pygame.transform.scale(achievements_bg, (WIDTH, HEIGHT))

# Function to draw text
def draw_text(text, pos, color=(255, 118, 33), outline_color=(0, 0, 0)):
    outline_offset = 1  # Thickness of the border
    for dx in [-outline_offset, outline_offset]:
        for dy in [-outline_offset, outline_offset]:
            text_surface = font.render(text, True, outline_color)
            screen.blit(text_surface, (pos[0] + dx, pos[1] + dy))
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)

def run_achievements_menu():
    """Run the achievements menu."""
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return False  # Exit the program

            # Handle clicks on Back
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    return True  # Go back to Settings page

        # Draw the background
        screen.blit(achievements_bg, (0, 0))

        # Draw achievement icons with numbers
        for i, (icon, pos) in enumerate(zip(icons, icon_positions)):
            screen.blit(icon, pos)
            draw_text(str(i + 1), (pos[0] + 109, pos[1] + 30))  # Center the number on the icon

        # Draw yellow circle
        screen.blit(yellow_circle, yellow_icon_position)

        # Draw counters below icons (white text)
        for pos in text_positions:
            draw_text("0x", pos, color=(255, 255, 255))  # White text for "0x"

        # Draw counter below yellow circle (white text)
        draw_text("0x", yellow_text_position, color=(255, 255, 255))  # White text for "0x"

        # Draw back button
        screen.blit(back_button, back_rect)

        # Update display
        pygame.display.flip()

    return False  # Exit the program