import pygame
from pygame.font import Font
from pygame.key import ScancodeWrapper


def main():
    # Initialize Pygame
    pygame.init()

    # Screen dimensions
    screen_width: int = 900
    screen_height: int = 500
    screen = pygame.display.set_mode(size=(screen_width, screen_height))

    # Colors
    background_color: tuple[int, int, int] = (40, 40, 40)  # dark gey
    items_color: tuple[int, int, int] = (255, 220, 50)  # orange

    # Ball settings
    ball_size: int = 16
    ball_x_speed: int = 5
    ball_y_speed: int = 5

    # Ball position
    ball_x: int = (screen_width // 2) - (ball_size // 2)
    ball_y: int = (screen_height // 2) - (ball_size // 2)

    # Paddles settings
    paddle_width: int = 10
    paddle_height: int = 60
    paddle_speed: int = 10

    # Paddles positions
    left_paddle_y: int = (screen_height // 2) - (paddle_height // 2)
    right_paddle_y: int = (screen_height // 2) - (paddle_height // 2)

    font: Font = pygame.font.Font(None, 36)

    # Game loop
    running: bool = True
    while running:
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
        left_paddle_collision = (ball_x <= paddle_width) and (left_paddle_y < ball_y < left_paddle_y + paddle_height)
        right_paddle_collision = (ball_x >= screen_width - paddle_width - ball_size) and \
                                 (right_paddle_y < ball_y < right_paddle_y + paddle_height)
        if left_paddle_collision or right_paddle_collision:
            ball_x_speed *= -1

        # Scoring
        if ball_x < 0 or ball_x > screen_width:
            ball_x, ball_y = (screen_width // 2) - (ball_size // 2), (screen_height // 2) - (ball_size // 2)

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
        pygame.time.Clock().tick(60)  # FPS

    pygame.quit()


if __name__ == "__main__":
    main()

# Ctrl+Alt+O / Control+Option+O = Organize imports
# Ctrl+Alt+L / Option+Command+L = Format code according to the settings
