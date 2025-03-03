import pygame
import sys
from pygame.locals import *

import save_slots
import world_select
from saves_handler import *

pygame.init()  # Initialize Pygame

# Get full screen dimensions
info = pygame.display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Character Customization Screen")

print(f"Width: {WIDTH}")
print(f"Height: {HEIGHT}")

FPS = pygame.time.Clock()
FONT = pygame.font.SysFont("comicsans", 60)

# Creates a simple Button class (for arrow buttons, etc.)
class Button():
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        DISPLAY.blit(self.image, self.rect)

    def input_check(self, coordinates):
        return self.rect.collidepoint(coordinates)

# Renders text with an outline
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

# TransparentButton class with hover effect for text-based buttons (e.g. Back)
class TransparentButton:
    def __init__(self, text, font_path, x, y):
        self.text = text
        self.font_path = font_path
        self.base_size = 64
        self.hover_size = 72
        self.x, self.y = x, y
        try:
            self.normal_font = pygame.font.Font(font_path, self.base_size)
        except FileNotFoundError:
            print(f"Warning: {font_path} not found. Using default font.")
            self.normal_font = pygame.font.SysFont(None, self.base_size)
        try:
            self.hover_font = pygame.font.Font(font_path, self.hover_size)
        except FileNotFoundError:
            print(f"Warning: {font_path} not found for hover. Using default font.")
            self.hover_font = pygame.font.SysFont(None, self.hover_size)
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

def create_screen(display, bg):
    display.blit(bg, (0, 0))

def customization_screen(slot: int): 
    pygame.display.set_caption("Character Customization Screen")


    # Load confirm button as an image only once
    confirm_button_img = pygame.image.load("Assets/character_customization/confirm-button.png")
    confirm_button_img = pygame.transform.scale(confirm_button_img, (150, 30))
    confirm_button_rect = confirm_button_img.get_rect(center=(WIDTH-130, HEIGHT-75))


    hair_left_img = pygame.image.load("Assets/character_customization/left-arrow.png")
    hair_left_img = pygame.transform.scale(hair_left_img, (80, 80))
    hair_left_button_class = Button(hair_left_img, WIDTH - (WIDTH*.41), (HEIGHT*.125))

    hair_right_img = pygame.image.load("Assets/character_customization/right-arrow.png")
    hair_right_img = pygame.transform.scale(hair_right_img, (80, 80))
    hair_right_button_class = Button(hair_right_img, WIDTH - (WIDTH*.1875), (HEIGHT*.13194))

    shirt_left_img = pygame.image.load("Assets/character_customization/left-arrow.png")
    shirt_left_img = pygame.transform.scale(shirt_left_img, (80,80))
    shirt_left_button_class = Button(shirt_left_img, (WIDTH*.59375), (HEIGHT*.27083))

    shirt_right_img = pygame.image.load("Assets/character_customization/right-arrow.png")
    shirt_right_img = pygame.transform.scale(shirt_right_img, (80,80))
    shirt_right_button_class = Button(shirt_right_img, (WIDTH*.8125), (HEIGHT*.27))

    pants_left_img = pygame.image.load("Assets/character_customization/left-arrow.png")
    pants_left_img = pygame.transform.scale(pants_left_img, (80,80))
    pants_left_button_class = Button(pants_left_img, (WIDTH*.59375), (HEIGHT*.39583))

    pants_right_img = pygame.image.load("Assets/character_customization/right-arrow.png")
    pants_right_img = pygame.transform.scale(pants_right_img, (80,80))
    pants_right_button_class = Button(pants_right_img, (WIDTH*.8125), (HEIGHT*.40277))

    skin_left_img = pygame.image.load("Assets/character_customization/left-arrow.png")
    skin_left_img = pygame.transform.scale(skin_left_img, (80,80))
    skin_left_button_class = Button(skin_left_img, (WIDTH*.59375), (HEIGHT*.52083))

    skin_right_img = pygame.image.load("Assets/character_customization/right-arrow.png")
    skin_right_img = pygame.transform.scale(skin_right_img, (80,80))
    skin_right_button_class = Button(skin_right_img, (WIDTH*.8125), (HEIGHT*.52777))

    # Transparent "Back" button using our TransparentButton class
    back_button = TransparentButton("Back", "Assets/Save Slot Menu/PixelifySans.ttf", 600, 550)
    back_button = TransparentButton("Back", "Assets/Save Slot Menu/PixelifySans.ttf", WIDTH // 3, HEIGHT // 1.7)


    # Place labels
    hair_text = pygame.image.load("Assets/character_customization/hair-color-text.png")
    hair_text = pygame.transform.scale(hair_text, (200,100))
    
    shirt_text = pygame.image.load("Assets/character_customization/shirt-color-text.png")
    shirt_text = pygame.transform.scale(shirt_text, (200,100))
    
    pants_text = pygame.image.load("Assets/character_customization/pants-color-text.png")
    pants_text = pygame.transform.scale(pants_text, (180, 80))
    
    skin_text = pygame.image.load("Assets/character_customization/skin-color-text.png")
    skin_text = pygame.transform.scale(skin_text, (190, 90))

    shoe_image = pygame.image.load("Assets/character_customization/shoes.png")
    shoe_image = pygame.transform.scale(shoe_image, (250,250))

    # Load color variants
    shirt_images = [pygame.image.load(f"Assets/character_customization/shirt_color/shirt_{i}.png") for i in range(3)]
    hair_images = [pygame.image.load(f"Assets/character_customization/hair_color/hair_{i}.png") for i in range(3)]
    pants_images = [pygame.image.load(f"Assets/character_customization/pants_color/pants_{i}.png") for i in range(3)]
    skin_images = [pygame.image.load(f"Assets/character_customization/skin_color/skin_{i}.png") for i in range(2)]

    # Indices for customization
    shirt_index = 0
    hair_index = 0
    pants_index = 0
    skin_index = 0

    running = True
    while running:
        # Draw background each frame
        DISPLAY.fill("blue")

        # Blit text labels
        DISPLAY.blit(hair_text, (WIDTH*.625, HEIGHT*.0694))
        DISPLAY.blit(shirt_text, (WIDTH*.625, HEIGHT*.2083))
        DISPLAY.blit(pants_text, (WIDTH*.6328125, HEIGHT*.3472))
        DISPLAY.blit(skin_text, (WIDTH*.625, HEIGHT*.4583))

        # Blit shoe
        DISPLAY.blit(shoe_image, (WIDTH*.234375, HEIGHT*.3472))

        # Update arrow buttons
        hair_left_button_class.update()
        hair_right_button_class.update()
        shirt_left_button_class.update()
        shirt_right_button_class.update()
        pants_left_button_class.update()
        pants_right_button_class.update()
        skin_left_button_class.update()
        skin_right_button_class.update()

        # Hover & draw back button (TransparentButton)
        mouse_pos = pygame.mouse.get_pos()
        back_button.check_hover(mouse_pos)
        back_button.draw(DISPLAY)
        
        # Hover effect for the confirm button (image-based scaling)
        # Use the preloaded confirm_button_img and its rect
        if confirm_button_rect.collidepoint(mouse_pos):
            scaled_confirm = pygame.transform.scale(confirm_button_img, (int(150 * 1.1), int(30 * 1.1)))
            scaled_confirm_rect = scaled_confirm.get_rect(center=confirm_button_rect.center)
            DISPLAY.blit(scaled_confirm, scaled_confirm_rect)
        else:
            DISPLAY.blit(confirm_button_img, confirm_button_rect)

        # Check events
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            elif event.type == MOUSEBUTTONDOWN:
                # Back button -> go to save slots
                if back_button.is_clicked(mouse_pos):
                    print("Back button clicked. Going to save slot menu...")
                    running = False
                    save_slots.Screen_SaveSlot()
                    sys.exit()

                # Confirm button -> go to world selector
                if confirm_button_rect.collidepoint(mouse_pos):
                    print("Confirm button clicked. Going to map/level selector...")
                    update_save(slot, {"shirt": f"Assets\character_customization\shirt_color\shirt_{shirt_index}.png", "hair": f"Assets\character_customization\hair_color\hair_{hair_index}.png", "pants": f"Assets\character_customization\pants_color\pants_{pants_index}.png", "skin": f"Assets\character_customization\skin_color\skin_{skin_index}.png"})
                    running = False
                    world_select.World_Selector()
                    sys.exit()

                # Hair arrows
                if hair_left_button_class.input_check(mouse_pos):
                    hair_index = (hair_index - 1) % len(hair_images)
                if hair_right_button_class.input_check(mouse_pos):
                    hair_index = (hair_index + 1) % len(hair_images)

                # Skin arrows
                if skin_left_button_class.input_check(mouse_pos):
                    skin_index = (skin_index - 1) % len(skin_images)
                if skin_right_button_class.input_check(mouse_pos):
                    skin_index = (skin_index + 1) % len(skin_images)

                # Shirt arrows
                if shirt_left_button_class.input_check(mouse_pos):
                    shirt_index = (shirt_index - 1) % len(shirt_images)
                if shirt_right_button_class.input_check(mouse_pos):
                    shirt_index = (shirt_index + 1) % len(shirt_images)

                # Pants arrows
                if pants_left_button_class.input_check(mouse_pos):
                    pants_index = (pants_index - 1) % len(pants_images)
                if pants_right_button_class.input_check(mouse_pos):
                    pants_index = (pants_index + 1) % len(pants_images)

        # Blit color variants
        shirt_size = pygame.transform.scale(shirt_images[shirt_index], (250,250))
        hair_size = pygame.transform.scale(hair_images[hair_index], (250,250))
        pants_size = pygame.transform.scale(pants_images[pants_index], (250,250))
        skin_size = pygame.transform.scale(skin_images[skin_index], (250,250))

        # Draw them in correct layering order
        DISPLAY.blit(hair_size, (WIDTH*.234375, HEIGHT*.3694))
        DISPLAY.blit(skin_size, (WIDTH*.234375, HEIGHT*.361))
        DISPLAY.blit(shirt_size, (WIDTH*.234375, HEIGHT*.3472))
        DISPLAY.blit(pants_size, (WIDTH*.234375, HEIGHT*.3472))

        pygame.display.flip()
        FPS.tick(60)

    return

if __name__ == "__main__":
    customization_screen()
    pygame.quit()
