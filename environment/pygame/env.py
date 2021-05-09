import numpy as np
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

    def __init__(self):
        pass

    def reset(self) -> (np.array, int, bool):
        pass

    def step(self, action: int) -> (np.array, int, bool):
        pass

    def total_points(self) -> int:
        pass

    def total_steps(self) -> int:
        pass


class PyGameFood(Food):
    def point_is_in_food(self, point: Point):
        pass

