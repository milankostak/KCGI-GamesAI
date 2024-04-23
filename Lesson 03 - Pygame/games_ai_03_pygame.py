import pygame


def main():
    # Initialize Pygame
    pygame.init()

    # Screen dimensions
    screen_width, screen_height = 900, 500
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Colors
    background_color = (40, 40, 40)
    items_color = (255, 221, 51)

    # Ball settings
    ball_size = 16
    ball_x_speed = 5
    ball_y_speed = 5

    # Ball position
    ball_x = screen_width // 2
    ball_y = screen_height // 2

    # Paddles settings
    paddle_width, paddle_height = 10, 60
    paddle_speed = 10

    # Paddles positions
    left_paddle_y = (screen_height // 2) - (paddle_height // 2)
    right_paddle_y = (screen_height // 2) - (paddle_height // 2)

    font = pygame.font.Font(None, 36)

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Manage pressed keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and left_paddle_y > 0:
            left_paddle_y -= paddle_speed
        if keys[pygame.K_s] and left_paddle_y < screen_height - paddle_height:
            left_paddle_y += paddle_speed
        if keys[pygame.K_UP] and right_paddle_y > 0:
            right_paddle_y -= paddle_speed
        if keys[pygame.K_DOWN] and right_paddle_y < screen_height - paddle_height:
            right_paddle_y += paddle_speed

        # Move ball
        ball_x += ball_x_speed
        ball_y += ball_y_speed

        # Ball collisions with top and bottom
        if ball_y <= 0 or ball_y >= screen_height - ball_size:
            ball_y_speed *= -1

        # Ball collision with paddles
        left_paddle_collision = ball_x <= paddle_width and left_paddle_y < ball_y < left_paddle_y + paddle_height
        right_paddle_collision = (ball_x >= screen_width - paddle_width - ball_size) and \
                                 (right_paddle_y < ball_y < right_paddle_y + paddle_height)
        if left_paddle_collision or right_paddle_collision:
            ball_x_speed *= -1

        # Scoring
        if ball_x < 0 or ball_x > screen_width:
            ball_x, ball_y = screen_width // 2, screen_height // 2

        # Drawing
        screen.fill(background_color)
        pygame.draw.rect(screen, items_color, (0, left_paddle_y, paddle_width, paddle_height))
        pygame.draw.rect(screen, items_color, (screen_width - paddle_width, right_paddle_y, paddle_width, paddle_height))
        pygame.draw.ellipse(screen, items_color, (ball_x, ball_y, ball_size, ball_size))

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()

# Ctrl+Alt+O - Organize imports
# Ctrl+Alt+L - Format code according to the settings
