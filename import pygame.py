import pygame
import random

# Initialize pygame
pygame.init()
pygame.display.set_caption("TETRIS")
# Get full-screen resolution
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
BLOCK_SIZE = 30

# Define the size of the central square (50% of screen dimensions)
SQUARE_WIDTH, SQUARE_HEIGHT = SCREEN_WIDTH // 3, (SCREEN_HEIGHT // 2)-10

# Calculate the position of the central square
SQUARE_X = (SCREEN_WIDTH - SQUARE_WIDTH) // 2
SQUARE_Y = (SCREEN_HEIGHT - SQUARE_HEIGHT) // 2

WHITE, BLACK, GRAY, RED, GREEN, BLUE, YELLOW, CYAN = (
    (255, 255, 255), (0, 0, 0), (128, 128, 128),
    (255, 0, 0), (0, 255, 0), (0, 0, 255),
    (255, 255, 0), (0, 255, 255)
)

# SHAPES and corresponding colors
SHAPES = [
    ([[1, 1, 1], [0, 1, 0]], CYAN),     # T-shape
    ([[1, 1, 0], [0, 1, 1]], RED),      # Z-shape
    ([[0, 1, 1], [1, 1, 0]], GREEN),    # S-shape
    ([[1, 1, 1, 1]], YELLOW),           # I-shape
    ([[1, 1], [1, 1]], BLUE),           # O-shape
    ([[1, 1, 1], [1, 0, 0]], WHITE),    # L-shape
    ([[1, 1, 1], [0, 0, 1]], GRAY)      # J-shape
]

class Tetrimino:
    def __init__(self):
        self.shape, self.color = random.choice(SHAPES)
        # Ensure tetrimino spawns within bounds
        self.x = (SQUARE_WIDTH // BLOCK_SIZE) // 2 - len(self.shape[0]) // 2
        self.y = 0  # Start at the top of the grid

    def rotate(self):
        # Rotating the shape
        new_shape = [list(row) for row in zip(*self.shape[::-1])]
        # Check if rotation is within valid bounds
        if self.is_valid_shape(new_shape):
            self.shape = new_shape

    def is_valid_shape(self, shape, offset_x=0, offset_y=0):
        """Check if rotating or placing the shape is valid"""
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x, new_y = self.x + x + offset_x, self.y + y + offset_y
                    # Ensure position is within grid bounds
                    if new_x < 0 or new_x >= SQUARE_WIDTH // BLOCK_SIZE or new_y >= SQUARE_HEIGHT // BLOCK_SIZE:
                        return False
                    # Ensure we are not overlapping an existing block
                    if new_y >= 0 and tetris.grid[new_y][new_x] != BLACK:
                        return False
        return True

class Tetris:
    def __init__(self, background_image):
        self.grid = [[BLACK for _ in range(SQUARE_WIDTH // BLOCK_SIZE)] for _ in range(SQUARE_HEIGHT // BLOCK_SIZE)]
        self.tetrimino = Tetrimino()
        self.game_over = False
        self.font = pygame.font.SysFont('Arial', 24)
        self.score = 0
        self.countdown = 120  # Countdown timer (120 seconds)
        self.last_time = pygame.time.get_ticks()
        self.background = background_image
        self.clear_animation_time = 0  # Time for "Great!" or "COMBO!" animation
        self.combo_message = ""  # Store the combo message

    def is_valid(self, offset_x=0, offset_y=0):
        for y, row in enumerate(self.tetrimino.shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x, new_y = self.tetrimino.x + x + offset_x, self.tetrimino.y + y + offset_y
                    # Ensure we are within the bounds of the grid
                    if new_x < 0 or new_x >= SQUARE_WIDTH // BLOCK_SIZE or new_y >= SQUARE_HEIGHT // BLOCK_SIZE:
                        return False
                    if new_y >= 0 and self.grid[new_y][new_x] != BLACK:
                        return False
        return True

    def place_tetrimino(self):
        """Places the current Tetrimino on the grid"""
        for y, row in enumerate(self.tetrimino.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.tetrimino.y + y][self.tetrimino.x + x] = self.tetrimino.color
        self.clear_lines()
        self.tetrimino = Tetrimino()
        if not self.is_valid():
            self.game_over = True

    def clear_lines(self):
        """Check for full lines and clear them"""
        lines = [i for i, row in enumerate(self.grid) if all(cell != BLACK for cell in row)]
        if len(lines) > 0:
            self.clear_animation_time = pygame.time.get_ticks()  # Start animation time
        # Calculate score based on number of lines cleared
        if len(lines) == 1:
            self.score += 50
            self.combo_message = "Great!"
        elif len(lines) == 2:
            self.score += 150
            self.combo_message = "Great! Double!"
        elif len(lines) >= 3:
            self.score += 250
            self.combo_message = "COMBO!"

        for i in lines:
            del self.grid[i]
            self.grid.insert(0, [BLACK for _ in range(SQUARE_WIDTH // BLOCK_SIZE)])

    def move_down(self):
        """Move Tetrimino down if valid, otherwise place it"""
        if self.is_valid(offset_y=1):
            self.tetrimino.y += 1
        else:
            self.place_tetrimino()

    def move(self, direction):
        """Move Tetrimino left or right"""
        offset_x = 1 if direction == 'right' else -1
        if self.is_valid(offset_x=offset_x):
            self.tetrimino.x += offset_x

    def draw(self, screen):
        # Draw the background image
        screen.blit(self.background, (0, 0))

        # Draw the central square area
        pygame.draw.rect(screen, GRAY, (SQUARE_X, SQUARE_Y, SQUARE_WIDTH, SQUARE_HEIGHT), 2)

        # Draw the Tetris grid and pieces inside the central square
        for y, row in enumerate(self.grid):
            for x, color in enumerate(row):
                if color != BLACK:
                    pygame.draw.rect(screen, color, pygame.Rect(SQUARE_X + x * BLOCK_SIZE, SQUARE_Y + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        for y, row in enumerate(self.tetrimino.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.tetrimino.color,
                                     pygame.Rect(SQUARE_X + (self.tetrimino.x + x) * BLOCK_SIZE,
                                                 SQUARE_Y + (self.tetrimino.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        self.draw_countdown(screen)
        self.draw_score(screen)
        self.draw_combo_message(screen)
        pygame.display.flip()

    def draw_score(self, screen):
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH - 150, 10))

    def update_countdown(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_time > 1000:  # Update countdown every second
            self.countdown -= 1
            self.last_time = current_time
        if self.countdown <= 0:
            self.game_over = True

    def draw_countdown(self, screen):
        countdown_text = self.font.render(f"Time Left: {self.countdown}", True, WHITE)
        screen.blit(countdown_text, (10, 10))

    def draw_combo_message(self, screen):
        if self.combo_message and pygame.time.get_ticks() - self.clear_animation_time < 2000:
            combo_text = self.font.render(self.combo_message, True, GREEN)
            screen.blit(combo_text, (SCREEN_WIDTH // 2 - combo_text.get_width() // 2, SCREEN_HEIGHT // 4))
        else:
            self.combo_message = ""  # Clear the message after 2 seconds

def main():
    try:
        # Load background image and scale to full-screen size
        background_image = pygame.image.load('MainBackround.jpg')  # Replace with your image path
        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except pygame.error as e:
        print(f"Error loading background image: {e}")
        return

    # Set the game window to full-screen mode
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)

    clock = pygame.time.Clock()
    tetris = Tetris(background_image)
    move_delay = 500
    last_move_time = pygame.time.get_ticks()

    while not tetris.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Exit full-screen on pressing ESC
                    pygame.quit()
                    return
                if event.key == pygame.K_LEFT:
                    tetris.move('left')
                elif event.key == pygame.K_RIGHT:
                    tetris.move('right')
                elif event.key == pygame.K_DOWN:
                    tetris.move_down()
                elif event.key == pygame.K_UP:  # Rotate the Tetrimino
                    tetris.tetrimino.rotate()

        current_time = pygame.time.get_ticks()
        if current_time - last_move_time > move_delay:
            tetris.move_down()
            last_move_time = current_time

        tetris.update_countdown()
        tetris.draw(screen)
        if tetris.score >= 1000:
            tetris.game_over = True
        clock.tick(60)  # Set FPS to 60

    # Game over handling
    screen.fill(BLACK)
    if tetris.game_over and tetris.score >= 1000:
        game_over_text = tetris.font.render("You Won!", True, WHITE)
    else:
        game_over_text = tetris.font.render("Game Over!", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)  # Wait for 2 seconds before closing
    pygame.quit()

if __name__ == "__main__":
    main()