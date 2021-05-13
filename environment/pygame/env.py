import numpy as np
import pygame
from scipy.spatial import distance

from environment.env import Env, Food, Snake, Direction
from environment.point import Point


class PyGameSnake(Snake):

    def __init__(self, colour="black", x=0, y=0):
        super().__init__(colour=colour, x=x, y=y)

    def set_direction(self, direction: Direction):
        pass

    def move(self, direction: Direction):
        pass

    def food_distance(self, food, metric=distance.cityblock):
        pass

    def add_tail(self):
        pass


class PyGameEnv(Env):

    def __init__(self, screen_width: int, screen_height: int):
        super().__init__(screen_width, screen_height)
        pygame.init()
        self.window = pygame.display.set_mode((screen_width, screen_height))

    def reset(self) -> (np.array, int, bool):
        self.current_food = None
        self.__generate_food()
        self.snake = PyGameSnake()
        self.points = 0
        self.n_moves = 0
        state = np.zeros((24, 12))#self.state_representation.get_state()
        done = False
        reward = 0

        return (state, reward, done)

    def step(self, action: int) -> (np.array, int, bool):
        state = np.zeros((10, 10))  # self.state_representation.get_state()
        done = False
        reward = 0

        return (state, reward, done)

    def total_points(self) -> int:
        return 0

    def total_steps(self) -> int:
        return 0


class PyGameFood(Food):
    def point_is_in_food(self, point: Point):
        pass

