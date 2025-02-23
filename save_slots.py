import pygame

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
        """ Update text surface and rect based on the current font """
        self.text_surface = render_text_with_outline(self.text, self.current_font, (255, 255, 255), (0, 0, 0), 2)
        self.rect = self.text_surface.get_rect(center=(self.x, self.y))

    def draw(self, surface):
        surface.blit(self.text_surface, self.rect.topleft)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def check_hover(self, mouse_pos):
        """ Change font size when hovered """
        if self.rect.collidepoint(mouse_pos):
            if self.current_font != self.hover_font:
                self.current_font = self.hover_font
                self.update_surface()
        else:
            if self.current_font != self.normal_font:
                self.current_font = self.normal_font
                self.update_surface()
    

def Screen_SaveSlot():
    # When running only this screen for testing, it should initialize basic screen and pygame
    if __name__ == "__main__":
        pygame.init()
        WIDTH, HEIGHT = 1920, 1080
        screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Display the screen title
    pygame.display.set_caption("Save Slot Screen")
    
    # Set custom values
    background_path = 'background.png'
    font_path = 'PixelifySans.ttf'
    
    # Try setting the custom font & background
    try:
        font = pygame.font.Font(font_path, 64)
        background = pygame.image.load(background_path)
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    except pygame.error or FileNotFoundError:
        print('Custom font or background not found! Please try again...')
    
    buttons = [
        TransparentButton("Save 1", font_path, WIDTH//2, HEIGHT//2 - 200),
        TransparentButton("Save 2", font_path, WIDTH//2, HEIGHT//2 - 50),
        TransparentButton("Save 3", font_path, WIDTH//2, HEIGHT//2 + 100),
        TransparentButton("Back", font_path, WIDTH//2, HEIGHT - 100),
    ]

    # Main loop
    running = True
    while running:
        screen.fill((255, 255, 255))
        
        if background:
            screen.blit(background, (0, 0))

        mouse_position = pygame.mouse.get_pos()
        for button in buttons:
            button.check_hover(mouse_position)
            button.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, button in enumerate(buttons):
                    if button.is_clicked(event.pos):
                        if i == 3:
                            print("Back button clicked")
                            running = False 
                        else:
                            print(f"Save {i+1} clicked")

    pygame.quit()
            

            
Screen_SaveSlot()