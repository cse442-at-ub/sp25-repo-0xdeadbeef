# npc_dialogue.py

import pygame

# Initialize font for dialogue
pygame.font.init()
font = pygame.font.Font(None, 36)  # Font for dialogue

# List of dialogue lines
dialogue_lines = [
    "",  # Empty line to avoid skipping the first dialogue
    "Ah! A visitor!",
    "It's a strange thing that you seek a place to stay here.",
    "Us folks around here have been living in these snowy mountains for years and everyone is just dying to find a lush green place to live.",
    "But hey,",
    "Beggers can't be chooser, right?",
    "My apoloigies, I haven't told you my name have I?",
    "The name's Kris.",
    "If you want to know more about the locals, you need to get familiaried with the customs here.",
    "Every folks around here talk by pressing 'E'",
    "It's a bit unconventional, but you'll get used to it.",
    "If you want to stay here, go talk to Sharon.",
    "She and her husband have been staying here the longest",
    "They know this land more than the speck of dust on my worn hair.",
    "You can find her at the next area.",
    "Just keep going right and you'll find her.",
    "Although, nature can be very cruel sometimes.",
    "There's spikes and ravines laying around this mountain so watch your step when you go around here.",
    "But hey, you're a young lad!",
    "I can tell you'll make it through.",
    "Good luck on your journey!"
]

# Variables to track dialogue state
current_dialogue_index = 0
show_dialogue = False

# Cooldown variables
cooldown_time = 400  # Cooldown between key presses in milliseconds
last_key_press_time = 0  # Tracks the last time "E" was pressed

# Function to draw the dialogue box
def draw_dialogue_box(screen, text, font, x, y):
    """
    Draws a dialogue box with the given text at the specified position.
    """
    # Calculate the size of the text
    text_surface = font.render(text, True, (0, 0, 0))
    text_width, text_height = text_surface.get_size()

    # Define padding for the dialogue box
    padding = 20

    # Calculate the size of the dialogue box
    box_width = text_width + padding * 2
    box_height = text_height + padding * 2

    # Position the box above the NPC
    box_x = x - box_width // 2
    box_y = y - box_height - 20  # Position above the NPC

    # Draw the box
    pygame.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_width, box_height))
    pygame.draw.rect(screen, (0, 0, 0), (box_x, box_y, box_width, box_height), 2)

    # Render the text
    text_rect = text_surface.get_rect(center=(x, box_y + box_height // 2))
    screen.blit(text_surface, text_rect)

def handle_npc_dialogue(screen, player_rect, npc_rect, keys, current_time):
    """
    Handles NPC dialogue logic, including showing prompts, advancing dialogue, and drawing the dialogue box.
    """
    global current_dialogue_index, show_dialogue, last_key_press_time

    if player_rect.colliderect(npc_rect):
        # # Show prompt to press 'E'
        # prompt_text = font.render("Press 'E' to talk", True, (255, 255, 255))
        # screen.blit(prompt_text, (player_rect.x - 70, player_rect.y - 50))

        # Check if 'E' is pressed with cooldown
        if keys[pygame.K_e] and current_time - last_key_press_time > cooldown_time:
            # Only proceed if there are more dialogue lines to show
            if current_dialogue_index < len(dialogue_lines) - 1:
                show_dialogue = True
                current_dialogue_index += 1  # Move to the next dialogue line
            last_key_press_time = current_time  # Update the last key press time

        # Draw dialogue box if active
        if show_dialogue:
            draw_dialogue_box(screen, dialogue_lines[current_dialogue_index], font, npc_rect.x + npc_rect.width // 2, npc_rect.y)
    else:
        # Hide dialogue box and reset dialogue when player moves out of range
        show_dialogue = False
        current_dialogue_index = 0  # Reset dialogue to the first line