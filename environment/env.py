# The game environment for Snake game


from enum import Enum

import numpy as np

from environment.point import Point
import scipy.spatial.distance as distance



class Env:

    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.current_food = None
        self.snake = None
        self.actions = {0: "up", 1: "right", 2: "down", 3: "left"}
        self.points = 0
        self.n_moves = 0
        self.max_moves_without_food = 1000
        self.theta = 45

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


class Direction():
    STRAIGHT = np.array([0, 1, 0])
    RIGHT = np.array([0, 0, 1])
    LEFT = np.array([1, 0, 0])

    @staticmethod
    def one_hot(direction) -> np.array:
        as_list = list(Direction)
        one_hot = np.zeros(3)
        index = as_list.index(direction)
        one_hot[index] = 1
        return one_hot

    @staticmethod
    def n_actions():
        return 3#len(list(Direction))

    @staticmethod
    def is_straight(direction: np.array) -> bool:
        return (direction == np.array([0, 1, 0])).all()

    @staticmethod
    def is_left(direction: np.array) -> bool:
        return (direction == np.array([1, 0, 0])).all()

    @staticmethod
    def is_right(direction: np.array) -> bool:
        return (direction == np.array([0, 0, 1])).all()

