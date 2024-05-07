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
BACKGROUND_COLOR = (200, 200, 200)  # White-ish
X_WIN_COLOR = (200, 150, 150)  # Red
O_WIN_COLOR = (150, 150, 200)  # Blue
DRAW_COLOR = (150, 150, 150)  # Gray

LINE_COLOR = (30, 30, 30)  # Black
X_COLOR = (200, 0, 0)  # Red
O_COLOR = (0, 0, 200)  # Blue

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tic Tac Toe with Minimax AI")
screen.fill(BACKGROUND_COLOR)

# Tic Tac Toe board (3x3 matrix)
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
                # Draw O mark
                pygame.draw.circle(screen, O_COLOR, (center_x, center_y), int(min(CELL_WIDTH, CELL_HEIGHT) / 4), 5)
            elif board[row][col] == AI:
                # Draw X mark
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


def minimax(board_variant, depth, is_maximizing):
    """
    Minimax algorithm to determine the best move for the AI
    :param board_variant: The current game state at the given depth
    :param depth: The depth of the game tree
    :param is_maximizing: True if the AI is maximizing, False if the AI is minimizing (playing as the human)
    :return: The best score in context of the AI player
    """
    global iterations
    iterations = iterations + 1
    print(f"depth: {depth}, is_maximizing: {is_maximizing}, board: {board_variant}, iterations: {iterations}")

    if check_win(AI):
        return 1
    if check_win(HUMAN):
        return -1
    if check_draw():
        return 0

    if is_maximizing:
        best_score = -math.inf
        for row in range(3):
            for col in range(3):
                # Check if cell is available
                if board_variant[row][col] == "":
                    board_variant[row][col] = AI
                    score = minimax(board_variant, depth + 1, False)
                    board_variant[row][col] = ""
                    best_score = max(score, best_score)
                    # print(f"best_score max: {best_score}, depth: {depth}")
        # print(f"return best_score max: {best_score}, depth: {depth}")
        return best_score
    else:
        best_score = math.inf
        for row in range(3):
            for col in range(3):
                # Check if cell is available
                if board_variant[row][col] == "":
                    board_variant[row][col] = HUMAN
                    score = minimax(board_variant, depth + 1, True)
                    board_variant[row][col] = ""
                    best_score = min(score, best_score)
                    # print(f"best_score min: {best_score}, depth: {depth}")
        # print(f"return best_score min: {best_score}, depth: {depth}")
        return best_score


def ai_turn():
    """
    Determine the best move for the AI at the current game state
    """
    global iterations
    iterations = 0
    best_score = -math.inf
    move = [-1, -1]
    # Iterate over the board and determine the best move
    for row in range(3):
        for col in range(3):
            # Check if cell is available
            if board[row][col] == "":
                board[row][col] = AI  # Simulate the move
                score = minimax(board, 0, False)
                board[row][col] = ""  # Undo the move
                if score > best_score:
                    best_score = score
                    move = [row, col]

    print(f"number of iterations: {iterations}")
    board[move[0]][move[1]] = AI


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
