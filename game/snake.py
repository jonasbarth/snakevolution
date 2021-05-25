import math
import random
from typing import List

import pygame

from environment.env import Direction
from environment.point import Point

import numpy as np

from game import colour
from game.core.grid import Snake, Grid, Food


class SnakeGame(object):

    def __init__(self, screen_width: int, screen_height: int, snake_size: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.snake_size = snake_size
        self._direction = Direction.UP
        self._game_over = False
        self.running = False
        self.ate_food = False

        self._n_steps = 0
        self._n_food_eaten = 0
        self._n_steps_without_food = 0
        self.grid_slots = int((screen_width / snake_size) * (screen_height / snake_size))

        self.grid = Grid(int(screen_width / snake_size), int(screen_height / snake_size))

    def start(self) -> None:
        self._game_over = False
        self.running = True
        self._n_steps = 0
        self._n_food_eaten = 0
        self._n_steps_without_food = 0
        #self.grid.reset()
        self.grid = Grid(int(self.screen_width / self.snake_size), int(self.screen_height / self.snake_size))

    def move(self, direction: Direction) -> (Point, bool, bool):
        snake_head = self.grid.move_snake(direction, self.ate_food)
        self._n_steps += 1

        if self.grid.snake().touches_tail() or self.grid.snake_is_touching_wall():
            self.game_over()
            return Point.from_numpy(snake_head), self.ate_food, self.is_game_over()

        # check if the snake touches food
        if self.grid.snake_is_touching_food():
            self.ate_food = True
            self._n_food_eaten += 1
            self._n_steps_without_food = 0
            self.grid.random_food()
        else:
            self.ate_food = False
            self._n_steps_without_food += 1

        if self._n_steps_without_food > 1000:
            self.game_over()

        return Point.from_numpy(snake_head), self.ate_food, self.is_game_over()

    def game_over(self) -> None:
        self._game_over = True

    def is_game_over(self) -> bool:
        return self._game_over

    def snake_head(self) -> Point:
        return Point.from_numpy(self.grid.snake().head())

    def snake_position(self) -> np.array:
        return self.grid.snake().segments

    def direction(self) -> Direction:
        return self._direction

    def food_position(self) -> Point:
        return Point.from_numpy(self.grid.food().position())

    def dimensions(self) -> (int, int):
        return self.screen_width, self.screen_height

    def start_position(self) -> Point:
        start_x = self.screen_width / 2
        start_y = self.screen_height / 2
        return Point(start_x, start_y)

    def n_steps(self):
        return self._n_steps

    def n_food_eaten(self):
        return self._n_food_eaten

    def score(self):
        return self.n_food_eaten()

    def n_steps_without_food(self):
        return self._n_steps_without_food


class PyGameSnakeGame(SnakeGame):

    def __init__(self, screen_width: int, screen_height: int, snake_size: int):
        super().__init__(screen_width, screen_height, snake_size)

    def start(self) -> None:
        super().start()
        self.snake = Snake(start_position=self.start_position(), direction=Direction.UP, snake_size=self.snake_size,
                           grid_slots=self.grid_slots)
        self.window = pygame.display.set_mode((self.screen_width, self.screen_height))
        # 0,0 is in the top left corner

        self.__random_food()

        self.__draw_snake()
        self.__draw_food()

    def move(self, direction: Direction) -> (Point, bool, bool):

        # move the snake in a new direction
        snake_head = self.snake.move(direction, self.ate_food)

        self._n_steps += 1

        if self.snake.touches_tail() or self.__is_touching_wall():
            self.game_over()
            return Point.from_numpy(snake_head), self.ate_food, self.is_game_over()

        # check if the snake touches food
        if self.__is_touching_food():
            self.ate_food = True
            self._n_food_eaten += 1
            self._n_steps_without_food = 0
            print("Ate food")
            self.__random_food()
        else:
            self.ate_food = False
            self._n_steps_without_food += 1

        if self._n_steps_without_food > 1000:
            self.game_over()
            return Point.from_numpy(snake_head), self.ate_food, self.is_game_over()

        self.__draw_snake()
        self.__draw_food()

        return Point.from_numpy(snake_head), self.ate_food, self.is_game_over()

    def __random_food(self) -> Point:
        available_slots = self.__available_food_positions()

        grid_slot = random.choice(tuple(available_slots))
        n_columns = self.screen_width / self.snake_size
        n_rows = self.screen_height / self.snake_size
        slot_x = grid_slot % n_columns
        slot_y = math.floor(grid_slot / n_rows)

        food_x = slot_x * self.snake_size
        food_y = slot_y * self.snake_size
       # self.food = pygame.Rect(food_x, food_y, self.snake_size, self.snake_size)
        return Point(food_x, food_y)

    def __available_food_positions(self) -> set:
        # get the snake positions
        snake_segments = self.snake.position()

        snake_grid_slots = set()
        all_slots = set(x for x in range(self.grid_slots))

        # convert snake positions into grid slots
        for segment in snake_segments:
            column = segment[0] / self.snake_size  # the column
            row = segment[1] / self.snake_size  # the row
            slot = column * (row + 1)

            snake_grid_slots.add(slot)

        # get all available slots
        return all_slots - snake_grid_slots

    def __is_touching_food(self) -> bool:
        return Point.from_numpy(self.snake.head()) == self.food_position()

    def __is_touching_wall(self) -> bool:
        # get the head of the snake. If x >= screen_width or x <= 0. If y >= screen_height or y <= 0
        head_x, head_y = self.snake.head()[0], self.snake.head()[1]

        return head_x < 0 or head_x >= self.screen_width or head_y < 0 or head_y >= self.screen_height

    def __draw_food(self):
        pygame.draw.rect(self.window, colour.green, self.food)
        pygame.display.flip()

    def __draw_snake(self):
        self.window.fill(colour.black)
        snake_segments = self.snake.position()
        index = 0
        for segment in snake_segments:
            segment_colour = colour.blue
            # the head of the snake is a different colour than the rest
            if index == 0:
                segment_colour = colour.red
            index += 1

            rect = pygame.Rect(segment[0], segment[1], self.snake_size, self.snake_size)
            pygame.draw.rect(self.window, segment_colour, rect)
            pygame.display.flip()




