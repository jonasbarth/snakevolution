import pygame

from game.snake import PyGameSnakeGame
from rl.snake import SnakeMDP


class HumanAgent:

    def __init__(self, env: SnakeMDP):
        self.env = env


    def play(self):
        self.env.reset()
        game = PyGameSnakeGame(200, 200, 20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                current_direction = game.direction()
                if event.key == pygame.K_LEFT:
                    self.direction = ""
                elif event.key == pygame.K_RIGHT:
                    self.direction = ""
                elif event.key == pygame.K_UP:
                    self.direction = ""
                elif event.key == pygame.K_DOWN:
                    self.direction = ""


    def w(self):
        self.env.step(0)

    def d(self):
        self.env.step(1)

    def s(self):
        self.env.step(2)

    def a(self):
        self.env.step(3)

