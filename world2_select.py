import pygame #type: ignore

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Level Selector")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Load background image
background_image = pygame.image.load("Accessories/menu_level2_selector_background.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Resize to fit screen

# Load and crop level preview image
def crop_image(image):
    """Crops the transparent/white parts of the image automatically."""
    mask = pygame.mask.from_surface(image)  # Create a mask from non-transparent pixels
    rect = mask.get_bounding_rects()[0]  # Get the bounding box of non-transparent pixels
    return image.subsurface(rect)  # Crop the image to that area

level_preview = pygame.image.load("Accessories/level2_selector_background.png")  # Load image
level_preview = crop_image(level_preview)  # Auto-crop
level_preview = pygame.transform.scale(level_preview, (700, 450))  # Resize if needed

# Load arrow images
left_arrow_image = pygame.image.load("Accessories/left_arrow.png")  # Replace with your left arrow image file
right_arrow_image = pygame.image.load("Accessories/right_arrow.png")  # Replace with your right arrow image file

# Resize arrow images if needed
arrow_width, arrow_height = 80, 50  # Adjust size as needed
left_arrow_image = pygame.transform.scale(left_arrow_image, (arrow_width, arrow_height))
right_arrow_image = pygame.transform.scale(right_arrow_image, (arrow_width, arrow_height))

# Load Pixelify Sans font
try:
    font = pygame.font.Font("Accessories/PixelifySans-VariableFont_wght.ttf", 36)  # Replace with the path to your Pixelify Sans font file
except FileNotFoundError:
    print("Error: Pixelify Sans font file not found. Using default font instead.")
    font = pygame.font.Font(None, 36)  # Fallback to default font

# Create a transparent back button
back_button = pygame.Surface((100, 40), pygame.SRCALPHA)  # Use SRCALPHA for transparency
text = font.render("Back", True, WHITE)  # Render text in white
text_rect = text.get_rect(center=(back_button.get_width() // 2, back_button.get_height() // 2))
back_button.blit(text, text_rect)  # Draw text onto the transparent surface

# Button positions (keep centered after cropping)
level_rect = level_preview.get_rect(center=(WIDTH // 2, HEIGHT // 2))
left_rect = left_arrow_image.get_rect(center=(WIDTH // 4 - 20, HEIGHT // 2))  # Shift left arrow slightly
right_rect = right_arrow_image.get_rect(center=(3 * WIDTH // 4 + 20, HEIGHT // 2))  # Shift right arrow slightly
back_rect = back_button.get_rect(center=(WIDTH // 2, HEIGHT - 50))

# Define mini square properties
mini_square_size = 40  # Size of the mini square

# Load mini square images
unlocked_level_image = pygame.image.load("Accessories/unlocked_level_button.png")  # Replace with your image file
current_level_image = pygame.image.load("Accessories/current_desert_level_button.png")  # Replace with your image file
locked_level_image = pygame.image.load("Accessories/locked_level_button.png")  # Replace with your image file

# Resize mini square images to match the desired size
unlocked_level_image = pygame.transform.scale(unlocked_level_image, (mini_square_size, mini_square_size))
current_level_image = pygame.transform.scale(current_level_image, (mini_square_size, mini_square_size))
locked_level_image = pygame.transform.scale(locked_level_image, (mini_square_size, mini_square_size))

# Define mini square positions and their corresponding images
mini_squares = [
    {"pos": (level_rect.centerx - 200, level_rect.centery - 180), "image": unlocked_level_image},  # Top left position
    {"pos": (level_rect.centerx - 250, level_rect.centery - 20), "image": current_level_image},    # Current position
    {"pos": (level_rect.centerx - 30, level_rect.centery - 40), "image": unlocked_level_image},  # Middle position
    {"pos": (level_rect.centerx + 110, level_rect.centery + 40), "image": unlocked_level_image},  # Middle right position
    {"pos": (level_rect.centerx - 20, level_rect.centery + 140), "image": locked_level_image},   # Bottom right position
]

# Main loop
running = True
while running:
    # Draw background
    screen.blit(background_image, (0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw elements
    screen.blit(level_preview, level_rect)  # Draw level preview image
    screen.blit(left_arrow_image, left_rect)  # Draw left arrow image
    screen.blit(right_arrow_image, right_rect)  # Draw right arrow image
    screen.blit(back_button, back_rect)  # Draw transparent back button with text "← Back"

    # Draw mini squares (images) on top of the level preview image
    for square in mini_squares:
        screen.blit(square["image"], square["pos"])

    # Update display
    pygame.display.flip()

pygame.quit()