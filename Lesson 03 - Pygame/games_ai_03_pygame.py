import pygame
from pygame import Surface
from pygame.font import Font
from pygame.key import ScancodeWrapper


def main():
    # Initialize Pygame
    pygame.init()

    # Screen dimensions
    screen_width: int = 900
    screen_height: int = 500
    screen: Surface = pygame.display.set_mode(size=(screen_width, screen_height))

    # Colors
    background_color: tuple[int, int, int] = (40, 40, 40)  # dark grey
    items_color: tuple[int, int, int] = (255, 220, 50)  # orange

    # Ball settings
    ball_size: int = 20
    ball_x_speed: int = 5
    ball_y_speed: int = 5

    # Ball position
    ball_x_origin: int = (screen_width // 2) - (ball_size // 2)
    ball_y_origin: int = (screen_height // 2) - (ball_size // 2)
    ball_x: int = ball_x_origin
    ball_y: int = ball_y_origin

    # Paddles settings
    paddle_width: int = 10
    paddle_height: int = 100
    paddle_speed: int = 10

    # Paddles positions
    left_paddle_y: int = (screen_height // 2) - (paddle_height // 2)
    right_paddle_y: int = (screen_height // 2) - (paddle_height // 2)

    font: Font = pygame.font.Font(None, 36)

    # Game loop
    running: bool = True
    while running:
        # First we need to see if the user has requested to exit from the application (i.e. the game)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Manage pressed keys
        keys: ScancodeWrapper = pygame.key.get_pressed()
        if keys[pygame.K_w] and left_paddle_y > 0:
            left_paddle_y -= paddle_speed
        if keys[pygame.K_s] and left_paddle_y < screen_height - paddle_height:
            left_paddle_y += paddle_speed
        if keys[pygame.K_UP] and right_paddle_y > 0:
            right_paddle_y -= paddle_speed
        if keys[pygame.K_DOWN] and right_paddle_y < screen_height - paddle_height:
            right_paddle_y += paddle_speed

        # Move the ball
        ball_x += ball_x_speed
        ball_y += ball_y_speed

        # Ball collisions with top and bottom
        if ball_y <= 0 or ball_y >= screen_height - ball_size:
            ball_y_speed *= -1

        # Ball collisions with paddles
        left_paddle_collision: bool = (ball_x <= paddle_width) and \
                                      (left_paddle_y < ball_y < left_paddle_y + paddle_height)
        right_paddle_collision: bool = (ball_x >= screen_width - paddle_width - ball_size) and \
                                       (right_paddle_y < ball_y < right_paddle_y + paddle_height)
        if left_paddle_collision or right_paddle_collision:
            ball_x_speed *= -1

        # Scoring
        if ball_x < 0 or ball_x > screen_width:
            # Reset the ball
            ball_x, ball_y = ball_x_origin, ball_y_origin

        # Drawing
        screen.fill(color=background_color)
        # Left paddle
        pygame.draw.rect(
            surface=screen,
            color=items_color,
            rect=(0, left_paddle_y, paddle_width, paddle_height),
        )
        # Right paddle
        pygame.draw.rect(
            surface=screen,
            color=items_color,
            rect=(screen_width - paddle_width, right_paddle_y, paddle_width, paddle_height),
        )
        # Ball
        pygame.draw.ellipse(
            surface=screen,
            color=items_color,
            rect=(ball_x, ball_y, ball_size, ball_size),
        )

        pygame.display.flip()
        pygame.time.Clock().tick(60)  # Forcing fixed FPS. If you don't you have to handle that manually.

    # Clean up when running is False
    pygame.quit()


if __name__ == "__main__":
    main()

# Ctrl+Alt+O / Control+Option+O = Organize imports
# Ctrl+Alt+L / Option+Command+L = Format code according to the settings
