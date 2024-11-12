import math
import sys

import pygame
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Screen size
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400

CELL_WIDTH = SCREEN_WIDTH / 3
CELL_HEIGHT = SCREEN_HEIGHT / 3

# Colors
BACKGROUND_COLOR = (200, 200, 200)  # Light grey
X_WIN_COLOR = (200, 150, 150)  # Red
O_WIN_COLOR = (150, 150, 200)  # Blue
DRAW_COLOR = (150, 150, 150)  # Gray

LINE_COLOR = (30, 30, 30)  # Dark grey
X_COLOR = (200, 0, 0)  # Red
O_COLOR = (0, 0, 200)  # Blue

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tic Tac Toe with Heuristics AI")
screen.fill(BACKGROUND_COLOR)

# Tic Tac Toe board (3×3 matrix)
board = [["" for _ in range(3)] for _ in range(3)]

# Define player and AI marks
HUMAN = "O"
AI = "X"

# Game states
game_over = False
winner = None
current_player = HUMAN  # Human starts

iterations = 0


def draw_board():
    """
    Draw the Tic Tac Toe board respectively to the screen size
    """
    # Draw vertical lines
    pygame.draw.line(screen, LINE_COLOR, (CELL_WIDTH, 0), (CELL_WIDTH, SCREEN_HEIGHT), 3)
    pygame.draw.line(screen, LINE_COLOR, (CELL_WIDTH * 2, 0), (CELL_WIDTH * 2, SCREEN_HEIGHT), 3)

    # Draw horizontal lines
    pygame.draw.line(screen, LINE_COLOR, (0, CELL_HEIGHT), (SCREEN_WIDTH, CELL_HEIGHT), 3)
    pygame.draw.line(screen, LINE_COLOR, (0, CELL_HEIGHT * 2), (SCREEN_WIDTH, CELL_HEIGHT * 2), 3)


def draw_marks():
    """
    Draw the marks (X or O) on the Tic Tac Toe board respectively to the current game state
    """
    for row in range(3):
        for col in range(3):
            center_x = int(col * CELL_WIDTH + CELL_WIDTH / 2)
            center_y = int(row * CELL_HEIGHT + CELL_HEIGHT / 2)

            # Fill in already made moves
            if board[row][col] == HUMAN:
                # Draw O mark for human player
                pygame.draw.circle(screen, O_COLOR, (center_x, center_y), int(min(CELL_WIDTH, CELL_HEIGHT) / 4), 5)
            elif board[row][col] == AI:
                # Draw X mark for AI player
                margin = int(min(CELL_WIDTH, CELL_HEIGHT) / 4)  # Margin from the cell borders
                pygame.draw.line(screen, X_COLOR, (center_x - margin, center_y - margin), (center_x + margin, center_y + margin), 5)
                pygame.draw.line(screen, X_COLOR, (center_x + margin, center_y - margin), (center_x - margin, center_y + margin), 5)


def check_win(player):
    """
    Check rows, columns and diagonals for a win
    :param player: The player to check for a win
    :return: True if the player has won, False otherwise
    """
    # Check rows
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] == player:
            return True
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == player:
            return True
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] == player or board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False


def check_draw():
    """
    Check if any board place is still empty, otherwise the game is a draw
    :return: True if the game is a draw, False otherwise
    """
    for row in range(3):
        for col in range(3):
            if board[row][col] == "":
                return False
    return True


def evaluate_move():
    """
    Evaluate the board and return the best move for the AI based on a simple heuristic.
    :return: Tuple (row, col) indicating the best move
    """
    # 1 Prioritize winning moves
    for row in range(3):
        for col in range(3):
            if board[row][col] == "":  # If the cell is empty
                board[row][col] = AI  # Simulate the AI's move
                if check_win(AI):  # Check if this is a winning move for the AI
                    board[row][col] = ""  # Reset the board back
                    return row, col  # Return the coordinates of the cell for the winning move
                board[row][col] = ""  # Reset the board back

    # 2 Block opponent's winning moves
    for row in range(3):
        for col in range(3):
            if board[row][col] == "":  # If the cell is empty
                board[row][col] = HUMAN  # Simulate the human's move
                if check_win(HUMAN):  # Check if this is a winning move for the human player - if so then block it
                    board[row][col] = ""  # Reset the board back
                    return row, col  # Return the coordinates of the cell for the opponent's winning move
                board[row][col] = ""  # Reset the board back

    # 3 Take the center cell if available
    # - because the center cell is the most powerful cell in the game
    # - it gives the largest number (4) of possible winning states (1 row, 1 column, 2 diagonals)
    if board[1][1] == "":
        return 1, 1

    # 4 Take any corner cell if available
    # - because they are the most powerful cells after the center cell
    # - it gives you 3 possible winning states (1 row, 1 column, 1 diagonal)
    for row, col in [(0, 0), (0, 2), (2, 0), (2, 2)]:
        if board[row][col] == "":  # If the cell is empty
            return row, col

    # 5 Take any open space
    # - they are the least powerful cells in the game - it gives you only 2 possible winning states (1 row, 1 column)
    # - but the player always has to make a move
    for row in range(3):
        for col in range(3):
            if board[row][col] == "":  # If the cell is empty
                return row, col


def ai_turn():
    """
    Perform the AI's move using the heuristic evaluation
    """
    global current_player
    row, col = evaluate_move()
    board[row][col] = AI
    current_player = HUMAN


def main_loop():
    global game_over, current_player, winner

    while not game_over:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN and current_player == HUMAN:
                mouse_x = event.pos[0]  # Column
                mouse_y = event.pos[1]  # Row

                clicked_row = int(mouse_y // CELL_HEIGHT)
                clicked_col = int(mouse_x // CELL_WIDTH)

                # Check if this is a valid move - it must be an empty cell
                if board[clicked_row][clicked_col] == "":
                    board[clicked_row][clicked_col] = HUMAN
                    if check_win(HUMAN):
                        game_over = True
                        winner = HUMAN
                    current_player = AI

        if check_draw() and not game_over:
            game_over = True
            winner = "Draw"

        if current_player == AI and not game_over:
            ai_turn()
            if check_win(AI):
                game_over = True
                winner = AI
            current_player = HUMAN

        if winner == HUMAN:
            screen.fill(O_WIN_COLOR)
        elif winner == AI:
            screen.fill(X_WIN_COLOR)
        elif game_over:
            screen.fill(DRAW_COLOR)
        else:
            screen.fill(BACKGROUND_COLOR)

        draw_board()
        draw_marks()

        pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN or event.type == QUIT:
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    # Start the main game loop
    main_loop()
