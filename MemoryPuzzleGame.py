import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 30
CARD_SIZE = 100
PADDING = 10
BACKGROUND_COLOR = (255, 255, 255)
CARD_COLOR = (0, 0, 255)
FONT_COLOR = (255, 255, 255)
FONT_SIZE = 36

# Initialize the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Memory Puzzle')

# Load font
font = pygame.font.Font(None, FONT_SIZE)

# Helper function to create the board
def create_board(rows, cols):
    icons = list(range(1, (rows * cols) // 2 + 1)) * 2
    random.shuffle(icons)
    board = [icons[i * cols:(i + 1) * cols] for i in range(rows)]
    return board

# Helper function to draw the board
def draw_board(board, revealed):
    rows = len(board)
    cols = len(board[0])
    total_width = cols * CARD_SIZE + (cols - 1) * PADDING
    total_height = rows * CARD_SIZE + (rows - 1) * PADDING
    start_x = (WIDTH - total_width) // 2
    start_y = (HEIGHT - total_height) // 2

    for row in range(rows):
        for col in range(cols):
            x = start_x + col * (CARD_SIZE + PADDING)
            y = start_y + row * (CARD_SIZE + PADDING)
            if revealed[row][col]:
                pygame.draw.rect(screen, CARD_COLOR, (x, y, CARD_SIZE, CARD_SIZE))
                text = font.render(str(board[row][col]), True, FONT_COLOR)
                screen.blit(text, (x + (CARD_SIZE - text.get_width()) // 2, y + (CARD_SIZE - text.get_height()) // 2))
            else:
                pygame.draw.rect(screen, CARD_COLOR, (x, y, CARD_SIZE, CARD_SIZE))
                pygame.draw.rect(screen, BACKGROUND_COLOR, (x + 5, y + 5, CARD_SIZE - 10, CARD_SIZE - 10))

# Main game loop
def game_loop():
    rows, cols = 4, 4
    board = create_board(rows, cols)
    revealed = [[False] * cols for _ in range(rows)]
    first_selection = None
    matches_found = 0
    total_matches = (rows * cols) // 2

    running = True
    game_over = False

    while running:
        screen.fill(BACKGROUND_COLOR)
        draw_board(board, revealed)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                # Calculate offsets to detect clicks on centered grid
                total_width = cols * CARD_SIZE + (cols - 1) * PADDING
                total_height = rows * CARD_SIZE + (rows - 1) * PADDING
                start_x = (WIDTH - total_width) // 2
                start_y = (HEIGHT - total_height) // 2

                x, y = event.pos
                grid_x = x - start_x
                grid_y = y - start_y

                if 0 <= grid_x < total_width and 0 <= grid_y < total_height:
                    col = grid_x // (CARD_SIZE + PADDING)
                    row = grid_y // (CARD_SIZE + PADDING)
                    if row < rows and col < cols and not revealed[row][col]:
                        revealed[row][col] = True
                        if first_selection is None:
                            first_selection = (row, col)
                        else:
                            r1, c1 = first_selection
                            if board[row][col] != board[r1][c1]:
                                pygame.time.wait(1000)
                                revealed[row][col] = False
                                revealed[r1][c1] = False
                            else:
                                matches_found += 1
                                # Show the last matched card before game over
                                if matches_found == total_matches:
                                    draw_board(board, revealed)
                                    pygame.display.flip()
                                    pygame.time.wait(1000)  # Pause 1 second to show last card
                                    game_over = True
                            first_selection = None

        if game_over:
            # Display "Game is over"
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            text = font.render("Game is over!", True, (255, 0, 0))
            screen.blit(text, ((WIDTH - text.get_width()) // 2, (HEIGHT - text.get_height()) // 2))
            pygame.display.flip()
            # Wait for 3 seconds then exit
            pygame.time.wait(3000)
            running = False

        pygame.time.Clock().tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()
