import pygame


def main():
    # Initialize Pygame
    pygame.init()

    # Set the size of the window
    size = width, height = 1280, 480

    # Set the speed of the ball (can be different for X and Y axis)
    speed = [1, 1]

    # Set the background color (RGB)
    # https://en.wikipedia.org/wiki/RGB_color_model
    background_color = (50, 200, 50)  # 2^8 - 1 = 255

    # Create the window
    screen = pygame.display.set_mode(size)

    # Load the ball image
    ball = pygame.image.load("ball.png")
    ball_rect = ball.get_rect()

    # Main event loop
    while True:
        # Check for events, close the window if the user clicks the close button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Move the ball
        ball_rect = ball_rect.move(speed)

        # Bounce the ball off the walls
        if ball_rect.left < 0 or ball_rect.right > width:
            speed[0] = -speed[0]
        if ball_rect.top < 0 or ball_rect.bottom > height:
            speed[1] = -speed[1]

        # Try carefully
        # background_color = int(random() * 255), int(random() * 255), int(random() * 255)

        # Redraw the screen (order matters)
        screen.fill(background_color)
        screen.blit(ball, ball_rect)

        # Update the display ("double buffering")
        pygame.display.flip()


if __name__ == "__main__":
    main()
