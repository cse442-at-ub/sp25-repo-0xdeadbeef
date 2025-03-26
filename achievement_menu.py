import pygame  # type: ignore
import main_menu  
import settings_menu  
import save_slots  
import os
import json

# Initialize pygame
pygame.init()

# Screen settings
info = pygame.display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Achievement Menu")

# Load background image
background_image = pygame.image.load("Assets/Achievement Menu/achievement_background.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Load achievement icons and resize them
icons = [
    pygame.transform.scale(pygame.image.load("Assets/Level Selector/level1_selector_background.png"), (250, 150))
    for _ in range(5)
] + [
    pygame.transform.scale(pygame.image.load("Assets/Level Selector/level2_selector_background.png"), (250, 150))
    for _ in range(2)
]

# Positions for icons and text
icon_positions = [(80 + i * 330, 100) for i in range(5)] + [(80 + i * 330, 400) for i in range(2)]
# text_positions = [(pos[0] + 90, pos[1] + 180) for pos in icon_positions]
text_positions = [
    [(pos[0] + 20, pos[1] + 195), (pos[0] + 120, pos[1] + 195), (pos[0] + 220, pos[1] + 195)]
    for pos in icon_positions]


# Load and resize yellow circle
yellow_circle = pygame.transform.scale(pygame.image.load("Assets/Achievement Menu/yellow_circle.png"), (140, 140))
yellow_icon_position = (WIDTH // 2 - 825, 700)
yellow_text_position = (yellow_icon_position[0] + 40, yellow_icon_position[1] + 160)

# Font settings
try:
    font = pygame.font.Font("Assets/Save Slot Menu/PixelifySans.ttf", 45)
except FileNotFoundError:
    print("Error: Pixelify Sans font file not found. Using default font instead.")
    font = pygame.font.Font(None, 70)


# --------------------------------------------- MODIFIED CODE FROM THE SAVE_SLOTS.PY FILE ------------------------------------------------------- #

# Define TransparentButton and its helper function in this file
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

# Create Back button using TransparentButton
back_button = TransparentButton("Back", "Assets/Save Slot Menu/PixelifySans.ttf", WIDTH // 2, HEIGHT - 50)

# Load achievements background (reuse background_image if desired)
achievements_bg = pygame.image.load("Assets/Achievement Menu/achievement_background.png")
achievements_bg = pygame.transform.scale(achievements_bg, (WIDTH, HEIGHT))

# Function to draw text (for numbers and "0x" labels)
def draw_text(text_str, pos, color=(255, 118, 33), outline_color=(0, 0, 0)):
    outline_offset = 1
    for dx in [-outline_offset, outline_offset]:
        for dy in [-outline_offset, outline_offset]:
            text_surface = font.render(text_str, True, outline_color)
            screen.blit(text_surface, (pos[0] + dx, pos[1] + dy))
    text_surface = font.render(text_str, True, color)
    screen.blit(text_surface, pos)

def run_achievements_menu():
    """Run the achievements menu."""
    saveslotone = "User Saves/save1.json"
    saveslottwo = "User Saves/save2.json"
    saveslotthree = "User Saves/save3.json"

    save_data_one = {}
    save_data_two = {}
    save_data_three = {}

    if os.path.exists(saveslotone):
        with open(saveslotone, "r") as file:
            save_data_one = json.load(file)

    if os.path.exists(saveslottwo):
        with open(saveslottwo, "r") as file:
            save_data_two = json.load(file)

    if os.path.exists(saveslotthree):
        with open(saveslotthree, "r") as file:
            save_data_three = json.load(file)

    level_names = ["Tutorial", "Level One", "Level Two", "Level Four", "Level Five"]
    level_clears = {level: [0,0,0,] for level in level_names}

    for level in level_names:
        level_clears[level][0] = save_data_one.get(level, 0)
        level_clears[level][1] = save_data_two.get(level, 0)
        level_clears[level][2] = save_data_three.get(level, 0)


    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return False  # Exit the program

            # Handle Back button click on mouse button down
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_clicked(event.pos):
                    print("Back clicked. Going to settings menu...")
                    running = False
                    settings_menu.run_settings_menu()  # Go back to settings menu

        # Draw the background
        screen.blit(achievements_bg, (0, 0))

        # Draw achievement icons with numbers
        for i, (icon, pos) in enumerate(zip(icons, icon_positions)):
            screen.blit(icon, pos)
            draw_text(str(i + 1), (pos[0] + 109, pos[1] + 30))

        # Draw yellow circle and its counter
        screen.blit(yellow_circle, yellow_icon_position)
        draw_text("0x", yellow_text_position, color=(255, 255, 255))

        # Draw counters below icons
        for i, level_name in enumerate(level_names):
            for o, clears in enumerate(level_clears[level_name]): 
                text_position = text_positions[i][o]
                draw_text(f"{clears}x", text_position)

                
        # for pos in text_positions:
        #     for po in pos:
        #         draw_text("0x", po, color=(255, 255, 255))



        # Use correct variable name for mouse position and update back_button hover effect
        mouse_pos = pygame.mouse.get_pos()  # FIXED: was incorrectly written as mouse.pos
        back_button.check_hover(mouse_pos)
        back_button.draw(screen)

        pygame.display.flip()

    return False  # Exit the program

if __name__ == "__main__":        
    run_achievements_menu()
    pygame.quit()