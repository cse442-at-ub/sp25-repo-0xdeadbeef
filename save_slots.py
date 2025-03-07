import pygame
import main_menu
import settings_menu
import achievement_menu
import sys

import character_customization
import world_select
from saves_handler import check_save, create_new_save

import pygame_widgets 
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox 

pygame.init()   # Initialize Pygame

info = pygame.display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Save Slot Screen")

def render_text_with_outline(text, font, text_color, outline_color, outline_thickness):
    text_surface = font.render(text, True, text_color)
    outline_surface = pygame.Surface(
        (text_surface.get_width() + outline_thickness * 2, text_surface.get_height() + outline_thickness * 2),
        pygame.SRCALPHA
    )

    # Render multiple copies of the text slightly offset to create an outline effect
    offsets = [(dx, dy) for dx in (-outline_thickness, outline_thickness) for dy in (-outline_thickness, outline_thickness)]
    for dx, dy in offsets:
        outline_surface.blit(font.render(text, True, outline_color), (dx + outline_thickness, dy + outline_thickness))

    # Draw the actual text in the center
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
    

def Screen_SaveSlot():
    # Display the screen title
    pygame.display.set_caption("Save Slot Screen")
    
    # Set custom values
    background_path = 'Assets/Save Slot Menu/background.png'
    font_path = 'Assets/Save Slot Menu/PixelifySans.ttf'
    
    # Try setting the custom font & background
    try:
        font = pygame.font.Font(font_path, 64)
        background = pygame.image.load(background_path)
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    except pygame.error or FileNotFoundError:
        print('Custom font or background not found! Please try again...')

    buttonNames = []
    
    for i in range(0, 3):
        if check_save(i+1):
            buttonNames.append("Save " + f"{i+1}")
        else:
            buttonNames.append("Save " + f"{i+1}" + " {New}")
    
    buttons = [
        TransparentButton(buttonNames[0], font_path, WIDTH//2, HEIGHT//2 - 200),
        TransparentButton(buttonNames[1], font_path, WIDTH//2, HEIGHT//2 - 50),
        TransparentButton(buttonNames[2], font_path, WIDTH//2, HEIGHT//2 + 100),
        TransparentButton("Back", font_path, WIDTH//2, HEIGHT - 100),
    ]

    
    # Main loop
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0].is_clicked(event.pos):  # Use buttons[0] for the Save Slot 1 button (New instance)
                    print("Save Slot 1 Clicked. Going to character customization...")
                    running = False
                    if not check_save(1): 
                        create_new_save(1)
                        character_customization.customization_screen(1)
                    else:
                        world_select.World_Selector(1)
                    sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[1].is_clicked(event.pos):  # Use buttons[1] for the Save Slot 2 button (New instance) 
                    print("Save Slot 2 Clicked. Going to character customization...")
                    running = False
                    if not check_save(2): 
                        create_new_save(2)
                        character_customization.customization_screen(2)
                    else:
                        world_select.World_Selector(2)
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[2].is_clicked(event.pos):  # Use buttons[2] for the Save Slot 3 button (Forwards to level/map selector - TO DO: saved state functionality)
                    print("Save Slot 3 Clicked. Going to map/level selector...")
                    running = False
                    if not check_save(3): 
                        create_new_save(3)
                        character_customization.customization_screen(3)
                    else:
                        world_select.World_Selector(3)
                    sys.exit()

            # Handle clicks on Back button using the fourth button in the array (index 3)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[3].is_clicked(event.pos):  # Use buttons[3] for the Back button
                    print("Back clicked. Going to main menu...")
                    running = False
                    main_menu.run_main_menu()  # Go back to main menu
                    sys.exit()

        mouse_position = pygame.mouse.get_pos()
        for button in buttons:
            button.check_hover(mouse_position)
            button.draw(screen)

        screen.fill((255, 255, 255))
        
        if background:
            screen.blit(background, (0, 0))

        for button in buttons:
            button.draw(screen)

        pygame.display.flip()

    
            

if __name__ == "__main__":        
    Screen_SaveSlot()
    pygame.quit()