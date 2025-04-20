import pygame  # type: ignore
import main_menu  
import settings_menu  
import os
import json

# Initialize pygame
pygame.init()
pygame.mixer.init() # Initialize Pygame Audio Mixer

# Screen settings
info = pygame.display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Statistics Menu")

# Load background image
background_image = pygame.image.load("Assets/Achievement Menu/achievement_background.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Font settings
try:
    title_font = pygame.font.Font("Assets/Save Slot Menu/PixelifySans.ttf", 55)
    stat_font = pygame.font.Font("Assets/Save Slot Menu/PixelifySans.ttf", 45)
except FileNotFoundError:
    print("Error: Pixelify Sans font file not found. Using default font instead.")
    title_font = pygame.font.Font(None, 80)
    stat_font = pygame.font.Font(None, 70)

# Define TransparentButton and its helper function
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
        self.hover_size = 72
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

# Create Back button
back_button = TransparentButton("Back", "Assets/Save Slot Menu/PixelifySans.ttf", WIDTH // 2, HEIGHT - 100)

def draw_save_slot_stats(save_data, slot_number, start_y):
    # Draw save slot title
    title = render_text_with_outline(f"Save Slot {slot_number}", title_font, (255, 255, 255), (0, 0, 0), 2)
    title_rect = title.get_rect(center=(WIDTH // 2, start_y + 50))  # Keep title position the same
    screen.blit(title, title_rect)

    # Draw statistics
    stats = [
        ("Deaths:", save_data.get("total_deaths", 0)),
        ("Yellow Eclipses:", save_data.get("Eclipse", 0)),
        ("Levels Completed:", len(save_data.get("map1_unlocks", [])))
    ]

    for i, (label, value) in enumerate(stats):
        # Draw label
        label_text = render_text_with_outline(label, stat_font, (255, 255, 255), (0, 0, 0), 2)
        label_rect = label_text.get_rect(center=(WIDTH // 2 - 200, start_y + 150 + i * 80))  # Reduced spacing from 120 to 80
        screen.blit(label_text, label_rect)
        
        # Draw value
        value_text = render_text_with_outline(str(value), stat_font, (255, 118, 33), (0, 0, 0), 2)
        value_rect = value_text.get_rect(center=(WIDTH // 2 + 200, start_y + 150 + i * 80))  # Reduced spacing from 120 to 80
        screen.blit(value_text, value_rect)

def run_statistics_menu():
    # Check if any music is currently playing
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load("Audio/Background.mp3")
        pygame.mixer.music.play(-1)

    # Load save data
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

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_clicked(event.pos):
                    print("Back clicked. Going to settings menu...")
                    running = False
                    settings_menu.run_settings_menu()

        # Draw the background
        screen.blit(background_image, (0, 0))

        # Draw statistics for each save slot with more vertical spacing
        draw_save_slot_stats(save_data_one, 1, 50)    # Start first slot higher
        draw_save_slot_stats(save_data_two, 2, 450)   # More space between slots
        draw_save_slot_stats(save_data_three, 3, 850) # More space between slots

        # Update and draw back button
        mouse_pos = pygame.mouse.get_pos()
        back_button.check_hover(mouse_pos)
        back_button.draw(screen)

        pygame.display.flip()

    return False

if __name__ == "__main__":        
    run_statistics_menu()
    pygame.quit()