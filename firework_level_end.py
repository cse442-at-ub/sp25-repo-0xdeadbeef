import pygame
import random
import math
import sys

# Our files
import world_select
from saves_handler import eclipse_increment, achievement_counter

# Initialize Pygame and mixer for sound
pygame.init()
pygame.mixer.init()

# Load the level complete sound 
level_complete_sound = pygame.mixer.Sound("Audio/LevelComplete.mp3")

# Screen settings
BASE_WIDTH = 1920
BASE_HEIGHT = 1080

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h # Will only work with resolutions 1920 x 1080 or better

scale_factor = HEIGHT / BASE_HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Level 3")

background = pygame.image.load("./images/background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Scale to screen size

# Firework class
class Firework:
    def __init__(self):
        self.x = random.randint(100, WIDTH - 100)
        self.y = HEIGHT
        self.color = random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)])
        self.speed_y = random.uniform(6, 9)  # Launch speed
        self.exploded = False
        self.timer = random.randint(40, 70)  # Time before explosion
        self.particles = []

    def explode(self):
        for _ in range(40):  # More particles for a better explosion
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            self.particles.append([self.x, self.y, dx, dy, 255])  # (x, y, dx, dy, alpha)

    def update(self):
        if not self.exploded:
            self.y -= self.speed_y  # Move upwards
            self.timer -= 1
            if self.timer <= 0 or self.y < HEIGHT // 3:
                self.exploded = True
                self.explode()
        else:
            for p in self.particles:
                p[0] += p[2]  # Move x
                p[1] += p[3]  # Move y
                p[4] -= 3  # Slower fade-out

    def draw(self, screen):
        if not self.exploded:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 5)
        else:
            for p in self.particles:
                if p[4] > 0:  # Only draw if visible
                    faded_color = (self.color[0], self.color[1], self.color[2], p[4])
                    pygame.draw.circle(screen, self.color, (int(p[0]), int(p[1])), 3)

# Firework list
fireworks = []
clock = pygame.time.Clock()
running = True
LIGHT_BLUE = (173, 216, 230)  # Light blue color
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

def show_level_complete(slot: int, coin: int):
    global fireworks
    # Stop tutorial music
    pygame.mixer.music.stop()

    # Play the level complete sound once when this function runs
    level_complete_sound.play()

    title_font = pygame.font.Font('PixelifySans.ttf', 100)
    menu_font = pygame.font.Font('PixelifySans.ttf', 60)
    level_completed_text = title_font.render("Level Completed", True, (255, 255, 255))
    select_level_text = menu_font.render("Back to Select Level", True, (255, 255, 255))

    level_completed_rect = level_completed_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    select_level_rect = select_level_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 120))
    box_padding = 20
    level_end_screen_box = pygame.Rect(level_completed_rect.left - box_padding, level_completed_rect.top - box_padding, level_completed_rect.width + box_padding*2, level_completed_rect.height + (box_padding*2) + 80)
    pygame.draw.rect(screen, (0, 0, 255), level_end_screen_box, 10)
    
    screen.blit(level_completed_text, level_completed_rect)
    screen.blit(select_level_text, select_level_rect)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        # Create a screen with blue background
        screen.blit(background, (0, 0))

        # Firework Effect: Add new fireworks at intervals
        if random.randint(0, 20) == 0:
            fireworks.append(Firework())
        for firework in fireworks:
            firework.update()
            firework.draw(screen)
        # Remove fully faded fireworks
        fireworks = [f for f in fireworks if any(p[4] > 0 for p in f.particles) or not f.exploded]
        clock.tick(30)

        # Draw boxes necessary for user input like returning to level
        screen.blit(level_completed_text, level_completed_rect)
        screen.blit(select_level_text, select_level_rect)
        pygame.draw.rect(screen, (0, 0, 255), level_end_screen_box, 10)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    waiting = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if select_level_rect.collidepoint(mouse_x, mouse_y):
                    level_name = "Level One"
                    achievement_counter(slot, level_name)
                    eclipse_increment(slot, coin)
                    world_select.World_Selector(slot)
                    sys.exit()

def show_level_complete_deaths(slot: int, coin: int, death_counter: int):
    global fireworks
    # Stop tutorial music
    pygame.mixer.music.stop()

    # Play the level complete sound once when this function runs
    level_complete_sound.play()
    
    waiting = True
    while waiting:
        # Set fonts for the text
        title_font = pygame.font.Font('PixelifySans.ttf', 100)
        menu_font = pygame.font.Font('PixelifySans.ttf', 60)
        menu_font_hover = pygame.font.Font('PixelifySans.ttf', 65)  # Larger for hover

        # Render hover effect dynamically
        select_level_hover = False

        # Render the "Level Completed" text
        level_completed_text = title_font.render("Level Completed", True, WHITE)
        death_count_text = title_font.render(f"Deaths: {death_counter}", True, WHITE)
        select_level_text = menu_font.render("Back to Select Level", True, WHITE)

        # Position the texts
        level_completed_rect = level_completed_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        death_count_rect = death_count_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 120))
        select_level_rect = select_level_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 240))

        # Check if mouse is hovering
        if select_level_rect.collidepoint(pygame.mouse.get_pos()):
            select_level_hover = True

        # If hovering, change text size dynamically
        if select_level_hover:
            select_level_text = menu_font_hover.render("Back to Select Level", True, BLUE)
            select_level_rect = select_level_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 240))  # Recalculate position

        # Create box around the text
        box_padding = 20
        level_end_screen_box = pygame.Rect(level_completed_rect.left - box_padding, level_completed_rect.top - box_padding, level_completed_rect.width + box_padding*2, level_completed_rect.height + (box_padding*2) + 200)


        # Create a screen with blue background
        screen.blit(background, (0, 0))

        # Firework Effect: Add new fireworks at intervals
        if random.randint(0, 20) == 0:
            fireworks.append(Firework())
        for firework in fireworks:
            firework.update()
            firework.draw(screen)
        # Remove fully faded fireworks
        fireworks = [f for f in fireworks if any(p[4] > 0 for p in f.particles) or not f.exploded]
        clock.tick(30)

        # Draw boxes necessary for user input like returning to level
        pygame.draw.rect(screen, BLUE, level_end_screen_box, 10)
        screen.blit(level_completed_text, level_completed_rect)
        screen.blit(death_count_text, death_count_rect)
        screen.blit(select_level_text, select_level_rect)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    waiting = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if select_level_rect.collidepoint(mouse_x, mouse_y):
                    level_name = "Level One"
                    achievement_counter(slot, level_name)
                    eclipse_increment(slot, coin)
                    world_select.World_Selector(slot)
                    sys.exit()

if __name__ == "__main__":
    show_level_complete_deaths(1, 2, 1)