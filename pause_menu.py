import pygame
import world_select
import sys

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font('PixelifySans.ttf', 60)
        self.font_hover = pygame.font.Font('PixelifySans.ttf', 65)  # Larger for hover
        self.WHITE = (255, 255, 255)
        self.BLUE = (0, 0, 255)
        self.paused = False
        # Button rectangles
        self.resume_rect = None
        self.exit_rect = None

    def toggle_pause(self):
        self.paused = not self.paused

    def handle_event(self, event, slot: int):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.paused = True if not self.paused else False
        elif self.paused:
                
            resume_hover = False
            exit_hover = False

            resume_text = self.font.render("Resume", True, self.WHITE)
            exit_text = self.font.render("Save and Quit", True, self.WHITE)

            # Position the texts
            self.resume_rect = resume_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
            self.exit_rect = exit_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 120))
            box = self.resume_rect
            # Check if mouse is hovering
            if self.resume_rect.collidepoint(pygame.mouse.get_pos()):
                resume_hover = True
            if self.exit_rect.collidepoint(pygame.mouse.get_pos()):
                exit_hover = True

            # If hovering, change text size dynamically
            if resume_hover:
                resume_text = self.font_hover.render("Resume", True, self.BLUE)
                self.resume_rect = resume_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))  # Recalculate position
            if exit_hover:
                exit_text = self.font_hover.render("Save and Quit", True, self.BLUE)
                self.exit_rect = exit_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 120))  # Recalculate position

            box_padding = 150
            game_over_screen_box = pygame.Rect(box.left - box_padding, box.top, box.width + (box_padding*2), box.height + (box_padding))
            pygame.draw.rect(self.screen, self.BLUE, game_over_screen_box, 10)
            
            # Draw the texts
            self.screen.blit(resume_text, self.resume_rect)
            self.screen.blit(exit_text, self.exit_rect)

            pygame.display.flip()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.resume_rect.collidepoint(pygame.mouse.get_pos()):
                    self.paused = False
                elif self.exit_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.mixer.music.stop()                               # stop level music
                    pygame.mixer.music.load("Audio/Background2.mp3")        # map/world selector background music 2
                    pygame.mixer.music.play(-1)                             # loop forever
                    self.paused = False
                    world_select.World_Selector(slot)
                    sys.exit()  # Go back to level select
            if event.type == pygame.K_ESCAPE:
                self.paused = False