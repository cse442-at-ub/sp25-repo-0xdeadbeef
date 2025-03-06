import pygame #type: ignore
import sys
import world_select  # Assuming world_select is a module you have for level selection

WIDTH = 800
HEIGHT = 600 

def show_level_completed_screen(screen, background):
    # Display the background image
    screen.blit(background, (0, 0))

    # Set fonts for the text
    title_font = pygame.font.Font('PixelifySans.ttf', 100)
    menu_font = pygame.font.Font('PixelifySans.ttf', 60)

    # Render the "Level Completed" text
    level_completed_text = title_font.render("Level Completed", True, (255, 255, 255))
    select_level_text = menu_font.render("Back to Select Level", True, (255, 255, 255))

    # Position the texts
    level_completed_rect = level_completed_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    select_level_rect = select_level_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 120))

    # Create box around the text
    box_padding = 20
    level_end_screen_box = pygame.Rect(level_completed_rect.left - box_padding, level_completed_rect.top - box_padding, level_completed_rect.width + box_padding*2, level_completed_rect.height + (box_padding*2) + 80)
    pygame.draw.rect(screen, (255, 0, 0), level_end_screen_box, 10)
    
    # Draw the texts
    screen.blit(level_completed_text, level_completed_rect)
    screen.blit(select_level_text, select_level_rect)

    pygame.display.flip()

    # Wait for player to either press a key or click the button
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    waiting = False  # You could also go back to level select here

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if select_level_rect.collidepoint(mouse_x, mouse_y):
                    # pygame.quit()
                    world_select.World_Selector()
                    sys.exit()  # Go back to level select