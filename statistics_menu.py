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
    # Calculate proportional positions based on screen height
    slot_height = HEIGHT // 3  # Each slot takes 1/3 of the screen
    title_y = start_y + (slot_height * 0.15)  # Title at 15% of slot height
    stats_start_y = start_y + (slot_height * 0.3)  # Stats start at 30% of slot height
    line_spacing = slot_height * 0.15  # Spacing between stat lines

    # Draw save slot title (centered horizontally)
    title = render_text_with_outline(f"Save Slot {slot_number}", title_font, (255, 255, 255), (0, 0, 0), 2)
    title_rect = title.get_rect(center=(WIDTH // 2, title_y))
    screen.blit(title, title_rect)

    # Calculate statistics (unchanged)
    total_deaths = sum(
        int(value) for key, value in save_data.items() 
        if key.startswith("Level ") and key.endswith(" Deaths") and not key.startswith("Level 0 ")
    )
    
    completed_levels = 0
    for key in save_data:
        if key.endswith("_unlocks") and isinstance(save_data[key], list):
            completed_levels += sum(1 for level in save_data[key][1:] if level)
    
    stats = [
        ("Total Deaths:", total_deaths),
        ("Yellow Eclipses:", save_data.get("Eclipse", 0)),
        ("Levels Completed:", max(0, completed_levels))  # Simplified negative check
    ]

    # Calculate dynamic horizontal positions
    label_x = WIDTH // 3
    value_x = WIDTH * 2 // 3

    for i, (label, value) in enumerate(stats):
        current_y = stats_start_y + i * line_spacing
        
        # Draw label (right-aligned to label_x)
        label_text = render_text_with_outline(label, stat_font, (255, 255, 255), (0, 0, 0), 2)
        label_rect = label_text.get_rect(midright=(label_x, current_y))
        screen.blit(label_text, label_rect)
        
        # Draw value (left-aligned to value_x)
        value_text = render_text_with_outline(str(value), stat_font, (255, 118, 33), (0, 0, 0), 2)
        value_rect = value_text.get_rect(midleft=(value_x, current_y))
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