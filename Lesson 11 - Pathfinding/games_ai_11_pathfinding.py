import random
from queue import PriorityQueue

import pygame

# Window setup
ROWS = 50
WIDTH = 800
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Pathfinding Algorithms")

# Colors
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

GRID = []

DIJKSTRA = "Dijkstra"
A_STAR = "A*"


# Node class to represent each cell in the grid
class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == BLUE

    def is_end(self):
        return self.color == YELLOW

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = BLUE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = YELLOW

    def make_path(self):
        self.color = GREY

    def draw(self):
        pygame.draw.rect(WINDOW, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not GRID[self.row + 1][self.col].is_barrier():  # Down
            self.neighbors.append(GRID[self.row + 1][self.col])
        if self.row > 0 and not GRID[self.row - 1][self.col].is_barrier():  # Up
            self.neighbors.append(GRID[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not GRID[self.row][self.col + 1].is_barrier():  # Right
            self.neighbors.append(GRID[self.row][self.col + 1])
        if self.col > 0 and not GRID[self.row][self.col - 1].is_barrier():  # Left
            self.neighbors.append(GRID[self.row][self.col - 1])

    def __lt__(self, other):
        return False


START = Node(0, 0, 0, 0)
END = Node(0, 0, 0, 0)


# Heuristic function for A* (Manhattan distance)
def heuristic(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


# Reconstruct path after algorithm finishes
def reconstruct_path(came_from, current):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


# Algorithm implementations
def algorithm(start: Node, end: Node, algorithm_type=A_STAR):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in GRID for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in GRID for node in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos()) if algorithm_type == "A*" else 0

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                if algorithm_type == "A*":
                    f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos())
                else:  # For Dijkstra, we don't use a heuristic.
                    f_score[neighbor] = temp_g_score

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()


def make_grid():
    global GRID, START, END
    GRID = []
    gap = WIDTH // ROWS  # Divide the total width by the number of rows to get the width of each cell
    for i in range(ROWS):
        GRID.append([])
        for j in range(ROWS):
            node = Node(i, j, gap, ROWS)
            GRID[i].append(node)

    START = GRID[0][0]
    START.make_start()

    END = GRID[ROWS - 1][ROWS - 1]
    END.make_end()

    return GRID


def draw_grid():
    gap = WIDTH // ROWS
    for i in range(ROWS):
        pygame.draw.line(WINDOW, GREY, (0, i * gap), (WIDTH, i * gap))  # Draw horizontal lines
        for j in range(ROWS):
            pygame.draw.line(WINDOW, GREY, (j * gap, 0), (j * gap, WIDTH))  # Draw vertical lines


def draw():
    WINDOW.fill(WHITE)

    for row in GRID:
        for node in row:
            node.draw()

    draw_grid()
    pygame.display.update()


def get_clicked_pos(pos):
    gap = WIDTH // ROWS
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def generate_random_obstacles(obstacle_probability=0.1):
    """
    Fills the grid with random obstacles.

    Parameters:
    - grid: The grid of nodes.
    - start: The start node, which should not be turned into an obstacle.
    - end: The end node, which should not be turned into an obstacle.
    - obstacle_probability: The probability of a node becoming an obstacle (between 0 and 1).
    """
    for row in GRID:
        for node in row:
            if node != START and node != END and random.random() < obstacle_probability:
                node.make_barrier()


def reset_grid():
    for row in GRID:
        for node in row:
            if node.is_barrier():
                continue
            elif node == START:
                node.make_start()
            elif node == END:
                node.make_end()
            else:
                node.reset()


def main():
    make_grid()

    run = True
    algorithm_type = A_STAR

    while run:
        draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:  # Left or right mouse button
                pos = pygame.mouse.get_pos()
                if pos[0] < 0 or pos[0] >= WIDTH or pos[1] < 0 or pos[1] >= WIDTH:
                    continue
                row, col = get_clicked_pos(pos)
                node = GRID[row][col]
                if node != END and node != START:
                    if pygame.mouse.get_pressed()[0]:
                        node.make_barrier()
                    else:
                        node.reset()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    make_grid()

                elif event.key == pygame.K_SPACE:
                    for row in GRID:
                        for node in row:
                            node.update_neighbors()

                    algorithm(START, END, algorithm_type)

                elif event.key == pygame.K_a:  # Press 'A' to select A* algorithm
                    algorithm_type = A_STAR
                    reset_grid()

                elif event.key == pygame.K_d:  # Press 'D' to select Dijkstra's algorithm
                    algorithm_type = DIJKSTRA
                    reset_grid()

                elif event.key == pygame.K_r:  # Press 'R' to generate random obstacles
                    generate_random_obstacles()

    pygame.quit()


if __name__ == "__main__":
    main()
