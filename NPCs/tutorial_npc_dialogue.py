import pygame #type: ignore

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
    "My apologies, I haven't told you my name have I?",
    "The name's Kris.",
    "If you want to know more about the locals, you need to get familiaried with the customs here.",
    "Every folks around here talk by pressing 'E'.",
    "It's a bit unconventional, but you'll get used to it.",
    "If you want to stay here, go talk to Sharon.",
    "She and her husband have been staying here the longest.",
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
def draw_dialogue_box(screen, text, font, x, y, max_width=400):
    """
    Draws a dialogue box with the given text at the specified position.
    Automatically wraps text to fit within the specified max_width.
    Ensures no extra empty space below the text.
    """
    # Split the text into words
    words = text.split(' ')
    lines = []
    current_line = ''

    for word in words:
        # Check if adding the next word exceeds the max width
        test_line = current_line + ' ' + word if current_line else word
        test_width, _ = font.size(test_line)

        if test_width <= max_width:
            current_line = test_line
        else:
            # If the line exceeds max width, finalize the current line and start a new one
            lines.append(current_line)
            current_line = word

    # Add the last line
    if current_line:
        lines.append(current_line)

    # Calculate the total height of the dialogue box
    line_height = font.get_linesize()
    total_height = len(lines) * line_height

    # Define padding for the dialogue box
    padding = 20

    # Calculate the size of the dialogue box
    box_width = max_width + padding * 2
    box_height = total_height + padding * 2

    # Position the box above the NPC
    box_x = x - box_width // 2
    box_y = y - box_height - 20  # Position above the NPC

    # Draw the box
    pygame.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_width, box_height))
    pygame.draw.rect(screen, (0, 0, 0), (box_x, box_y, box_width, box_height), 2)

    # Render each line of text
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, (0, 0, 0))
        # Adjust the vertical position to remove extra space
        text_y = box_y + padding + i * line_height
        text_rect = text_surface.get_rect(midtop=(x, text_y))
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
            draw_dialogue_box(screen, dialogue_lines[current_dialogue_index], font, npc_rect.x + npc_rect.width // 2, npc_rect.y, max_width=400)
    else:
        # Hide dialogue box and reset dialogue when player moves out of range
        show_dialogue = False
        current_dialogue_index = 0  # Reset dialogue to the first line