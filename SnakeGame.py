import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
DARK_GREEN = (0, 150, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return  # Cannot turn directly opposite
        else:
            self.direction = point

    def move(self):
        head = self.get_head_position()
        x, y = self.direction
        new_x = (head[0] + (x * GRID_SIZE)) % WIDTH
        new_y = (head[1] + (y * GRID_SIZE)) % HEIGHT
        new_position = (new_x, new_y)

        if new_position in self.positions[1:]:
            return False  # Game over - snake collided with itself
        else:
            self.positions.insert(0, new_position)
            if len(self.positions) > self.length:
                self.positions.pop()
            return True

    def reset(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0

    def draw(self, surface):
        for i, p in enumerate(self.positions):
            # Draw snake body
            pygame.draw.rect(surface, self.color, pygame.Rect(p[0], p[1], GRID_SIZE, GRID_SIZE))

            # Draw a darker rectangle inside for a segmented look
            inner_rect = pygame.Rect(p[0] + 4, p[1] + 4, GRID_SIZE - 8, GRID_SIZE - 8)
            pygame.draw.rect(surface, DARK_GREEN, inner_rect)

            # Draw eyes on the head
            if i == 0:  # Head of the snake
                # Determine eye positions based on direction
                if self.direction == UP:
                    left_eye = (p[0] + GRID_SIZE // 4, p[1] + GRID_SIZE // 4)
                    right_eye = (p[0] + 3 * GRID_SIZE // 4, p[1] + GRID_SIZE // 4)
                elif self.direction == DOWN:
                    left_eye = (p[0] + GRID_SIZE // 4, p[1] + 3 * GRID_SIZE // 4)
                    right_eye = (p[0] + 3 * GRID_SIZE // 4, p[1] + 3 * GRID_SIZE // 4)
                elif self.direction == LEFT:
                    left_eye = (p[0] + GRID_SIZE // 4, p[1] + GRID_SIZE // 4)
                    right_eye = (p[0] + GRID_SIZE // 4, p[1] + 3 * GRID_SIZE // 4)
                else:  # RIGHT
                    left_eye = (p[0] + 3 * GRID_SIZE // 4, p[1] + GRID_SIZE // 4)
                    right_eye = (p[0] + 3 * GRID_SIZE // 4, p[1] + 3 * GRID_SIZE // 4)

                # Draw eyes
                pygame.draw.circle(surface, BLACK, left_eye, 2)
                pygame.draw.circle(surface, BLACK, right_eye, 2)


class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self, snake_positions=None):
        if snake_positions is None:
            snake_positions = []
        while True:
            x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            if (x, y) not in snake_positions:
                self.position = (x, y)
                break

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))


def draw_grid(surface):
    for y in range(0, HEIGHT, GRID_SIZE):
        for x in range(0, WIDTH, GRID_SIZE):
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, (40, 40, 40), rect, 1)


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Snake Game')

    font = pygame.font.SysFont('Arial', 25)
    game_over_font = pygame.font.SysFont('Arial', 50)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    snake = Snake()
    food = Food()

    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_SPACE:
                        snake.reset()
                        food.randomize_position(snake.positions)
                        game_over = False
                else:
                    if event.key == pygame.K_UP:
                        snake.turn(UP)
                    elif event.key == pygame.K_DOWN:
                        snake.turn(DOWN)
                    elif event.key == pygame.K_LEFT:
                        snake.turn(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        snake.turn(RIGHT)

        if not game_over:
            # Move snake and check for collision
            if not snake.move():
                game_over = True

            # Check if snake ate food
            if snake.get_head_position() == food.position:
                snake.length += 1
                snake.score += 10
                food.randomize_position(snake.positions)

        # Clear screen
        surface.fill(BLACK)

        # Draw grid, snake, and food
        draw_grid(surface)
        snake.draw(surface)
        food.draw(surface)

        # Display score
        score_text = font.render(f'Score: {snake.score}', True, WHITE)
        surface.blit(score_text, (5, 5))

        # Display game over message
        if game_over:
            game_over_text = game_over_font.render('GAME OVER', True, WHITE)
            restart_text = font.render('Press SPACE to restart', True, WHITE)
            surface.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
            surface.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))

        # Update screen
        screen.blit(surface, (0, 0))
        pygame.display.update()

        # Control game speed
        clock.tick(FPS)


if __name__ == '__main__':
    main()