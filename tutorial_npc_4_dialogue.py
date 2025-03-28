import pygame #type: ignore

# Initialize font for dialogue
pygame.font.init()
font = pygame.font.Font(None, 36)  # Font for dialogue

# List of dialogue lines
dialogue_lines = [
    "",  # Empty line to avoid skipping the first dialogue
    "This place is not as beautiful as I thought it would be.",
    "It usually looks better in the spring.",
    "Oh, the terrain got you confused?",
    "Don't worry, everybody tends to forget.",
    "Move around by using 'A' and 'D' keys.",
    "'A' is to move left and 'D' is to move right.",
    "If you wanna take a leap of faith, use the 'SPACEBAR' key.",
    "If you see any obstacle that might end your life, just jump over it",
    "Of course, keep moving right though.",
    "You'll meet more people and more places to explore.",
    "This place is definitely not recommended to stay for long, but hey,",
    "The world is open am I right?"
]

# Variables to track dialogue state
current_dialogue_index = 0
show_dialogue = False

# Cooldown variables
cooldown_time = 400  # Cooldown between key presses in milliseconds
last_key_press_time = 0  # Tracks the last time "E" was pressed

def draw_thought_bubble(screen, npc_rect):
    """
    Draws a thought bubble (cloud-like shape) slightly to the right above the NPC's head.
    """

    # Shifted to the right
    offset_x = 20  # Shift amount
    bubble_x = npc_rect.x + npc_rect.width // 2 + offset_x
    bubble_y = npc_rect.y - 40  # Positioned higher

    # Main cloud bubble
    pygame.draw.ellipse(screen, (255, 255, 255), (bubble_x - 25, bubble_y - 20, 50, 30))  # Main bubble
    pygame.draw.ellipse(screen, (0, 0, 0), (bubble_x - 25, bubble_y - 20, 50, 30), 2)  # Outline

    # Thought trail (smaller bubbles leading down to the NPC)
    pygame.draw.circle(screen, (255, 255, 255), (bubble_x - 5, bubble_y + 10), 6)  # Medium circle
    pygame.draw.circle(screen, (0, 0, 0), (bubble_x - 5, bubble_y + 10), 6, 2)  # Outline

    pygame.draw.circle(screen, (255, 255, 255), (bubble_x - 10, bubble_y + 25), 4)  # Small circle
    pygame.draw.circle(screen, (0, 0, 0), (bubble_x - 10, bubble_y + 25), 4, 2)  # Outline

    # Add 'E' inside the main bubble
    font = pygame.font.Font(None, 28)
    text_surface = font.render('E', True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(bubble_x, bubble_y - 5))
    screen.blit(text_surface, text_rect)


# Function to draw the dialogue box
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

def handle_npc_4_dialogue(screen, player_rect, npc_rect, keys, current_time):
    """
    Handles NPC dialogue logic, including showing prompts, advancing dialogue, and drawing the dialogue box.
    """
    global current_dialogue_index, show_dialogue, last_key_press_time

    if player_rect.colliderect(npc_rect):
    # Show thought bubble when the player is near the NPC but not in dialogue
        if not show_dialogue:
            draw_thought_bubble(screen, npc_rect)

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