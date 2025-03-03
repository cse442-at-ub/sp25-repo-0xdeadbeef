# import pygame  # type: ignore

# # Initialize pygame
# pygame.init()

# # Screen settings
# WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h  # Get the screen width and height
# screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
# pygame.display.set_caption("World Selector")

# # Colors
# WHITE = (255, 255, 255)
# BLUE = (0, 0, 255)

# # Load background images
# background_images = [
#     pygame.image.load("Accessories/menu_level1_selector_background.jpg"),
#     pygame.image.load("Accessories/menu_level2_selector_background.png"),
#     # Add more background images for additional levels here
# ]
# background_images = [pygame.transform.scale(img, (WIDTH, HEIGHT)) for img in background_images]  # Resize to fit screen

# # Load and crop level preview images
# def crop_image(image):
#     """Crops the transparent/white parts of the image automatically."""
#     mask = pygame.mask.from_surface(image)  # Create a mask from non-transparent pixels
#     rect = mask.get_bounding_rects()[0]  # Get the bounding box of non-transparent pixels
#     return image.subsurface(rect)  # Crop the image to that area

# level_previews = [
#     pygame.image.load("Accessories/level1_selector_background.png"),  # Level 1
#     pygame.image.load("Accessories/level2_selector_background.png"),  # Level 2
#     # Add more level preview images for additional levels here
# ]
# level_previews = [crop_image(img) for img in level_previews]  # Auto-crop
# level_previews = [pygame.transform.scale(img, (700, 450)) for img in level_previews]  # Resize if needed

# # Load arrow images
# left_arrow_image = pygame.image.load("Accessories/left_arrow.png")  # Replace with your left arrow image file
# right_arrow_image = pygame.image.load("Accessories/right_arrow.png")  # Replace with your right arrow image file

# # Resize arrow images if needed
# arrow_width, arrow_height = 80, 60  # Adjust size as needed
# left_arrow_image = pygame.transform.scale(left_arrow_image, (arrow_width, arrow_height))
# right_arrow_image = pygame.transform.scale(right_arrow_image, (arrow_width, arrow_height))

# # Load Pixelify Sans font
# try:
#     font = pygame.font.Font("Accessories/PixelifySans-VariableFont_wght.ttf", 36)  # Replace with the path to your Pixelify Sans font file
# except FileNotFoundError:
#     print("Error: Pixelify Sans font file not found. Using default font instead.")
#     font = pygame.font.Font(None, 36)  # Fallback to default font

# # Create a transparent back button
# back_button = pygame.Surface((100, 40), pygame.SRCALPHA)  # Use SRCALPHA for transparency
# text = font.render("Back", True, WHITE)  # Render text in white
# text_rect = text.get_rect(center=(back_button.get_width() // 2, back_button.get_height() // 2))
# back_button.blit(text, text_rect)  # Draw text onto the transparent surface

# # Button positions (keep centered after cropping)
# left_rect = left_arrow_image.get_rect(center=(WIDTH // 4 - 20, HEIGHT // 2))  # Shift left arrow slightly
# right_rect = right_arrow_image.get_rect(center=(3 * WIDTH // 4 + 20, HEIGHT // 2))  # Shift right arrow slightly
# back_rect = back_button.get_rect(center=(WIDTH // 2, HEIGHT - 50))

# # Define mini square properties
# mini_square_size = 40  # Size of the mini square

# # Load mini square images
# unlocked_level_image = pygame.image.load("Accessories/unlocked_level_button.png")  # Replace with your image file
# current_level_images = [
#     pygame.image.load("Accessories/current_snow_level_button.png"),  # Level 1
#     pygame.image.load("Accessories/current_desert_level_button.png"),  # Level 2
#     # Add more current level images for additional levels here
# ]
# locked_level_image = pygame.image.load("Accessories/locked_level_button.png")  # Replace with your image file

# # Resize mini square images to match the desired size
# unlocked_level_image = pygame.transform.scale(unlocked_level_image, (mini_square_size, mini_square_size))
# current_level_images = [pygame.transform.scale(img, (mini_square_size, mini_square_size)) for img in current_level_images]
# locked_level_image = pygame.transform.scale(locked_level_image, (mini_square_size, mini_square_size))

# # Define mini square positions and their corresponding images for all levels
# mini_squares = [
#     [  # Level 1
#         {"pos": (WIDTH // 2 - 150, HEIGHT // 2 - 80), "image": unlocked_level_image},  # Top left position
#         {"pos": (WIDTH // 2 + 10, HEIGHT // 2 - 20), "image": current_level_images[0]},  # Middle position
#         {"pos": (WIDTH // 2 - 140, HEIGHT // 2 + 70), "image": unlocked_level_image},  # Current position
#         {"pos": (WIDTH // 2 + 157, HEIGHT // 2 - 35), "image": unlocked_level_image},  # Middle right position
#         {"pos": (WIDTH // 2 + 110, HEIGHT // 2 + 150), "image": locked_level_image},  # Bottom right position
#     ],
#     [  # Level 2
#         {"pos": (WIDTH // 2 - 200, HEIGHT // 2 - 180), "image": unlocked_level_image},  # Top left position
#         {"pos": (WIDTH // 2 - 250, HEIGHT // 2 - 20), "image": current_level_images[1]},  # Current position
#         {"pos": (WIDTH // 2 - 30, HEIGHT // 2 - 40), "image": unlocked_level_image},  # Middle position
#         {"pos": (WIDTH // 2 + 110, HEIGHT // 2 + 40), "image": unlocked_level_image},  # Middle right position
#         {"pos": (WIDTH // 2 - 20, HEIGHT // 2 + 140), "image": locked_level_image},  # Bottom right position
#     ],
#     # Add more mini square configurations for additional levels here
# ]

# # Track the current level
# current_level = 0  # Start with Level 1 (index 0)
# num_levels = len(background_images)  # Total number of levels

# # Main loop
# running = True
# while running:
#     # Draw background based on current level
#     screen.blit(background_images[current_level], (0, 0))

#     # Center the level preview image
#     level_rect = level_previews[current_level].get_rect(center=(WIDTH // 2, HEIGHT // 2))

#     # Event handling
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             if event.button == 1:  # Left mouse button
#                 mouse_pos = pygame.mouse.get_pos()
#                 # Check if left arrow is clicked
#                 if left_rect.collidepoint(mouse_pos):
#                     current_level = (current_level - 1) % num_levels  # Circular navigation to the previous level
#                 # Check if right arrow is clicked
#                 elif right_rect.collidepoint(mouse_pos):
#                     current_level = (current_level + 1) % num_levels  # Circular navigation to the next level
#         elif event.type == pygame.KEYDOWN:  # Handle keyboard input
#             if event.key == pygame.K_LEFT:  # Left arrow key
#                 current_level = (current_level - 1) % num_levels  # Circular navigation to the previous level
#             elif event.key == pygame.K_RIGHT:  # Right arrow key
#                 current_level = (current_level + 1) % num_levels  # Circular navigation to the next level

#     # Draw elements
#     screen.blit(level_previews[current_level], level_rect)  # Draw level preview image (centered)
#     screen.blit(left_arrow_image, left_rect)  # Draw left arrow image
#     screen.blit(right_arrow_image, right_rect)  # Draw right arrow image
#     screen.blit(back_button, back_rect)  # Draw transparent back button with text "← Back"

#     # Draw mini squares (images) on top of the level preview image
#     for square in mini_squares[current_level]:
#         screen.blit(square["image"], square["pos"])

#     # Update display
#     pygame.display.flip()

# pygame.quit()