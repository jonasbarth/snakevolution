# The game environment for Snake game


from enum import Enum

import numpy as np

from environment.point import Point
import scipy.spatial.distance as distance



class Env:

    def reset(self) -> (np.array, int, bool):
        pass

    def step(self, action: int) -> (np.array, int, bool):
        pass

    def total_points(self) -> int:
        pass

    def total_steps(self) -> int:
        pass


class Food:

    def point_is_in_food(self, point: Point):
        pass


class Snake:

    def __init__(self, colour="black", x=0, y=0):
        self.colour = colour
        self.position = Point(x, y)
        pass

    def set_direction(self, direction):
        pass

    def move(self, direction):
        pass

    def food_distance(self, food, metric=distance.cityblock):
        pass

    def add_tail(self):
        pass


class Direction(Enum):
    UP = "up"
    RIGHT = "right"
    DOWN = "down"
    LEFT = "left"
