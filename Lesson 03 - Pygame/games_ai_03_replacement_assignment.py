# Import the Pygame library
import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display variables
screen_width = 640
screen_height = 480
background_color = (0, 0, 0)  # Black

# Create the display surface
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simple Moving Object")

# Set up game variables
object_color = (255, 0, 0)  # Red
object_position = [300, 220]  # Starting position of the object
object_size = [50, 50]  # Size of the object (width, height)
move_distance = 5  # Distance to move the object each frame
# mo...

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update game state
    object_position[0] += move_distance  # Move the object horizontally
    if object_position[0] > screen_width or object_position[0] < 0:
        move_distance = -move_distance  # Change direction
        print("a")

    # Draw everything
    screen.fill(background_color)  # Fill the background color
    pygame.draw.rect(screen, object_color, pygame.Rect(object_position[0], object_position[1], object_size[0], object_size[1]))
    pygame.display.flip()  # Update the display

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()

# Task 1: Change the `object_color` variable to modify the rectangle's color.
# Presentation question: What is the RGB color model and how does it work?

# Task 2: Implement vertical movement. Now the movement is only horizontal.
# Prepare a new variable for the move distance and change `object_position[1]` in each draw loop.
# Check the boundaries the same it is done for the horizontal movement.
# Presentation question: Why does the object goes beyond the screen boundaries on some sides?

# Task 3: Add a counter that increments each time the object changes direction.
# Print the counter into the console using `print()`.
# Presentation question: What kind of data type is the counter variable and why? Are there any limits to the value?

# Each task accounts for 27 points, making the maximum 81 points (%) for this assignment.
# This is on purpose lower than 100% to make it fair to the students who were able to complete the main assignment.
# But with this, those of you who struggled with the main assignment can still get a passing grade at the end.
