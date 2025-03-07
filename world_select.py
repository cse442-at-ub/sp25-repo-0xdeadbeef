import pygame  # type: ignore
import sys
from pygame.locals import *

# import tutorial
# import save_slots
# import world_select
# import main_menu  

pygame.init()  # Initialize Pygame

# Get full screen resolution
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("World Selector")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Load background images
background_images = [
    pygame.image.load("Accessories/menu_level1_selector_background.jpg"),
    pygame.image.load("Accessories/menu_level2_selector_background.png"),
    # Add more background images for additional levels here
]
background_images = [pygame.transform.scale(img, (WIDTH, HEIGHT)) for img in background_images]

# Load and crop level preview images
def crop_image(image):
    """Crops the transparent/white parts of the image automatically."""
    mask = pygame.mask.from_surface(image)
    rect = mask.get_bounding_rects()[0]
    return image.subsurface(rect)

level_previews = [
    pygame.image.load("Accessories/level1_selector_background.png"),  # Level 1
    pygame.image.load("Accessories/level2_selector_background.png"),  # Level 2
    # Add more level preview images for additional levels here
]
level_previews = [crop_image(img) for img in level_previews]
level_previews = [pygame.transform.scale(img, (700, 450)) for img in level_previews]

# Load arrow images
left_arrow_image = pygame.image.load("Accessories/left_arrow.png")
right_arrow_image = pygame.image.load("Accessories/right_arrow.png")
arrow_width, arrow_height = 80, 60
left_arrow_image = pygame.transform.scale(left_arrow_image, (arrow_width, arrow_height))
right_arrow_image = pygame.transform.scale(right_arrow_image, (arrow_width, arrow_height))

# Load Pixelify Sans font
try:
    font = pygame.font.Font("Accessories/PixelifySans-VariableFont_wght.ttf", 36)
except FileNotFoundError:
    print("Error: Pixelify Sans font file not found. Using default font instead.")
    font = pygame.font.Font(None, 36)

# ---------------------------------------------- MODIFIED CODE FROM SAVE_SLOTS.PY FILE ------------------------------------------------------- #

def render_text_with_outline(text, font, text_color, outline_color, outline_thickness):
    text_surface = font.render(text, True, text_color)
    outline_surface = pygame.Surface(
        (text_surface.get_width() + outline_thickness * 2, text_surface.get_height() + outline_thickness * 2),
        pygame.SRCALPHA
    )
    offsets = [(dx, dy) for dx in (-outline_thickness, outline_thickness) for dy in (-outline_thickness, outline_thickness)]
    for dx, dy in offsets:
        outline_surface.blit(font.render(text, True, outline_color), (dx + outline_thickness, dy + outline_thickness))
    outline_surface.blit(text_surface, (outline_thickness, outline_thickness))
    return outline_surface

class TransparentButton:
    def __init__(self, text, font_path, x, y):
        self.text = text
        self.font_path = font_path
        self.base_size = 64
        self.hover_size = 72  # Slightly larger font for hover
        self.x, self.y = x, y
        self.normal_font = pygame.font.Font(font_path, self.base_size)
        self.hover_font = pygame.font.Font(font_path, self.hover_size)
        self.current_font = self.normal_font
        self.update_surface()
    
    def update_surface(self):
        self.text_surface = render_text_with_outline(self.text, self.current_font, (255, 255, 255), (0, 0, 0), 2)
        self.rect = self.text_surface.get_rect(center=(self.x, self.y))
    
    def draw(self, surface):
        surface.blit(self.text_surface, self.rect.topleft)
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
    def check_hover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            if self.current_font != self.hover_font:
                self.current_font = self.hover_font
                self.update_surface()
        else:
            if self.current_font != self.normal_font:
                self.current_font = self.normal_font
                self.update_surface()

# ---------------------------------------------- End TransparentButton --------------------------------------------------------------

# Create Back button using TransparentButton (for consistent UI)
back_button = TransparentButton("Back", "Assets/Save Slot Menu/PixelifySans.ttf", WIDTH // 2, HEIGHT - 50)
back_rect = back_button.rect  # Use its rect for collision

# Define arrow button positions
left_rect = left_arrow_image.get_rect(center=(WIDTH // 4 - 20, HEIGHT // 2))
right_rect = right_arrow_image.get_rect(center=(3 * WIDTH // 4 + 20, HEIGHT // 2))

# Load mini square images
unlocked_level_image = pygame.image.load("Accessories/unlocked_level_button.png")
current_level_images = [
    pygame.image.load("Accessories/current_snow_level_button.png"),
    pygame.image.load("Accessories/current_desert_level_button.png"),
    # Add more as needed
]
locked_level_image = pygame.image.load("Accessories/locked_level_button.png")
unlocked_level_image = pygame.transform.scale(unlocked_level_image, (40, 40))
current_level_images = [pygame.transform.scale(img, (40, 40)) for img in current_level_images]
locked_level_image = pygame.transform.scale(locked_level_image, (40, 40))

mini_squares = [
    [  # Level 1
        {"pos": (WIDTH // 2 - 150, HEIGHT // 2 - 80), "image": unlocked_level_image},
        {"pos": (WIDTH // 2 + 10, HEIGHT // 2 - 20), "image": current_level_images[0]},  # current_snow_level_button.png
        {"pos": (WIDTH // 2 - 140, HEIGHT // 2 + 70), "image": unlocked_level_image},
        {"pos": (WIDTH // 2 + 157, HEIGHT // 2 - 35), "image": unlocked_level_image},
        {"pos": (WIDTH // 2 + 110, HEIGHT // 2 + 150), "image": locked_level_image},
    ],
    [  # Level 2
        {"pos": (WIDTH // 2 - 200, HEIGHT // 2 - 180), "image": unlocked_level_image},
        {"pos": (WIDTH // 2 - 250, HEIGHT // 2 - 20), "image": current_level_images[1]},
        {"pos": (WIDTH // 2 - 30, HEIGHT // 2 - 40), "image": unlocked_level_image},
        {"pos": (WIDTH // 2 + 110, HEIGHT // 2 + 40), "image": unlocked_level_image},
        {"pos": (WIDTH // 2 - 20, HEIGHT // 2 + 140), "image": locked_level_image},
    ],
    # Add more mini square configurations for additional levels here
]

def World_Selector(slot: int):
    current_level = 0
    num_levels = len(background_images)
    running = True
    while running:
        # Draw background
        screen.blit(background_images[current_level], (0, 0))
        # Center level preview image
        level_rect = level_previews[current_level].get_rect(center=(WIDTH // 2, HEIGHT // 2))
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_clicked(event.pos):  # TransparentButton for back button
                    print("Back clicked. Going to save slot menu...")
                    running = False
                    # save_slots.Screen_SaveSlot()
                    sys.exit()
                elif event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if left_rect.collidepoint(mouse_pos):
                        current_level = (current_level - 1) % num_levels
                    elif right_rect.collidepoint(mouse_pos):
                        current_level = (current_level + 1) % num_levels
                    # Check mini squares click
                    for idx, square in enumerate(mini_squares[current_level]):
                        rect = square["image"].get_rect(topleft=square["pos"])
                        if rect.collidepoint(event.pos):
                            if current_level == 0 and idx == 1:
                                print("Current snow level button clicked. Going to tutorial snow level...")
                                running = False
                                # tutorial.tutorial_level()
                                tutorial.tutorial_level(slot)
                                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_level = (current_level - 1) % num_levels
                elif event.key == pygame.K_RIGHT:
                    current_level = (current_level + 1) % num_levels

        # Draw level preview image
        screen.blit(level_previews[current_level], level_rect)
        
        # Draw left/right arrow images with hover effect by scaling if hovered
        mouse_pos = pygame.mouse.get_pos()
        if left_rect.collidepoint(mouse_pos):
            scaled_left = pygame.transform.scale(left_arrow_image, (int(arrow_width * 1.1), int(arrow_height * 1.1)))
            left_rect_hover = scaled_left.get_rect(center=left_rect.center)
            screen.blit(scaled_left, left_rect_hover)
        else:
            screen.blit(left_arrow_image, left_rect)
            
        if right_rect.collidepoint(mouse_pos):
            scaled_right = pygame.transform.scale(right_arrow_image, (int(arrow_width * 1.1), int(arrow_height * 1.1)))
            right_rect_hover = scaled_right.get_rect(center=right_rect.center)
            screen.blit(scaled_right, right_rect_hover)
        else:
            screen.blit(right_arrow_image, right_rect)
        
        # Draw back button using TransparentButton's draw method
        back_button.check_hover(mouse_pos)
        back_button.draw(screen)
        
        # Draw mini squares with hover effect
        for idx, square in enumerate(mini_squares[current_level]):
            rect = square["image"].get_rect(topleft=square["pos"])
            if rect.collidepoint(mouse_pos):
                scaled_img = pygame.transform.scale(square["image"], (int(rect.width * 1.1), int(rect.height * 1.1)))
                scaled_rect = scaled_img.get_rect(center=rect.center)
                screen.blit(scaled_img, scaled_rect)
            else:
                screen.blit(square["image"], square["pos"])
        
        pygame.display.flip()

if __name__ == "__main__":
    World_Selector()
    pygame.quit()