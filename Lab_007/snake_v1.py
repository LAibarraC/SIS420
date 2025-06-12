import pygame
import numpy as np
import random

# Tamaño de celdas y pantalla
BLOCK_SIZE = 20
WIDTH = 400
HEIGHT = 400
ROWS = HEIGHT // BLOCK_SIZE
COLS = WIDTH // BLOCK_SIZE

class SnakeEnv:
    def __init__(self, width=COLS, height=ROWS):
        pygame.init()
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.width = width
        self.height = height
        self.actions = [0, 1, 2, 3]  # 0: up, 1: down, 2: left, 3: right
        self.reset()

    def reset(self):
        self.snake = [[self.width // 2, self.height // 2]]
        self.direction = 3  # start moving right
        self._place_food()
        self.score = 0
        self.done = False
        return self._get_state()

    def _place_food(self):
        while True:
            self.food = [random.randint(0, self.width-1), random.randint(0, self.height-1)]
            if self.food not in self.snake:
                break

    def _get_state(self):
        head = self.snake[0]
        food_dir = [np.sign(self.food[0] - head[0]), np.sign(self.food[1] - head[1])]
        danger = [
            self._is_collision([head[0], head[1]-1]),
            self._is_collision([head[0], head[1]+1]),
            self._is_collision([head[0]-1, head[1]]),
            self._is_collision([head[0]+1, head[1]]),
        ]
        return tuple(food_dir + danger)

    def _is_collision(self, pos):
        return (
            pos[0] < 0 or pos[0] >= self.width or
            pos[1] < 0 or pos[1] >= self.height or
            pos in self.snake
        )

    def step(self, action):
        if self.done:
            return self._get_state(), 0, self.done

        # Prevent direct reversal
        if (action == 0 and self.direction == 1) or \
           (action == 1 and self.direction == 0) or \
           (action == 2 and self.direction == 3) or \
           (action == 3 and self.direction == 2):
            action = self.direction

        self.direction = action
        head = self.snake[0][:]

        if action == 0:
            head[1] -= 1
        elif action == 1:
            head[1] += 1
        elif action == 2:
            head[0] -= 1
        elif action == 3:
            head[0] += 1

        reward = -0.1

        if self._is_collision(head):
            self.done = True
            reward = -10
            return self._get_state(), reward, self.done

        self.snake.insert(0, head)

        if head == self.food:
            reward = 10
            self._place_food()
            self.score += 1
        else:
            self.snake.pop()

        return self._get_state(), reward, self.done

    def render(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self.display.fill((0, 0, 0))
        for x, y in self.snake:
            pygame.draw.rect(self.display, (0, 255, 0), pygame.Rect(x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        fx, fy = self.food
        pygame.draw.rect(self.display, (255, 0, 0), pygame.Rect(fx*BLOCK_SIZE, fy*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        font = pygame.font.SysFont("arial", 25)
        score_text = font.render(f"Puntuación: {self.score}", True, (255, 255, 255))
        self.display.blit(score_text, [10, 10])
        if self.done:
            over_text = font.render("GAME OVER", True, (255, 0, 0))
            self.display.blit(over_text, [WIDTH//3, HEIGHT//2])
        pygame.display.flip()
        self.clock.tick(10)
