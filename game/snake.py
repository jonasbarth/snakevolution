import math
import random
from typing import List

import pygame

from environment.env import Direction
from environment.point import Point

import numpy as np

from game import colour


class SnakeGame(object):

    def __init__(self, screen_width: int, screen_height: int, snake_size: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.snake_size = snake_size
        self._direction = Direction.UP
        self._game_over = False
        self.running = False
        self.ate_food = False
        self.food = None
        self._n_steps = 0
        self._n_food_eaten = 0
        self._n_steps_without_food = 0
        self.grid_slots = int((screen_width / snake_size) * (screen_height / snake_size))

    def start(self) -> None:
        self.running = True
        self._n_steps = 0
        self._n_food_eaten = 0
        self._n_steps_without_food = 0

    def move(self, direction: Direction) -> (Point, bool, bool):
        pass

    def game_over(self) -> None:
        self._game_over = True

    def is_game_over(self) -> bool:
        return self._game_over

    def snake_head(self) -> Point:
        pass

    def snake_position(self) -> np.array:
        pass

    def direction(self) -> Direction:
        return self._direction

    def food_position(self) -> Point:
        pass

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

    def snake_head(self) -> Point:
        return Point.from_numpy(self.snake.head())

    def snake_position(self) -> np.array:
        return self.snake.position()

    def food_position(self) -> Point:
        return Point(self.food.x, self.food.y)

    def __random_food(self) -> Point:
        available_slots = self.__available_food_positions()

        grid_slot = random.choice(tuple(available_slots))
        n_columns = self.screen_width / self.snake_size
        n_rows = self.screen_height / self.snake_size
        slot_x = grid_slot % n_columns
        slot_y = math.floor(grid_slot / n_rows)

        food_x = slot_x * self.snake_size
        food_y = slot_y * self.snake_size
        self.food = pygame.Rect(food_x, food_y, self.snake_size, self.snake_size)
        return Point(food_x, food_y)

    def __available_food_positions(self) -> set:
        # get the snake positions
        snake_segments = self.snake.position()

        snake_grid_slots = set()
        all_slots = set(x for x in range(self.grid_slots))

        # convert snake positions into grid slots
        for segment in snake_segments:
            column = segment[0] / self.snake_size # the column
            row = segment[1] / self.snake_size # the row
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



class Snake(object):

    def __init__(self, start_position: Point, direction: Direction, snake_size: int, grid_slots: int):
        self.snake_size = snake_size
        self.segments = np.zeros((grid_slots, 2))
        self.segments[0] = start_position.as_numpy()
        self.tail_index = 1
        self.direction = direction

    def head(self) -> np.array:
        return self.segments[0]

    def move(self, direction: Direction, add_tail: bool = False) -> np.array:
        self.__set_direction(direction=direction)

        # remove last value, shift all values down by one, insert new value at top
        # copy the segments matrix
        new_segments = np.copy(self.segments)

        # remove last value of tail if we don't add a new segment and if the snake is longer than 1
        if not add_tail:
            if self.tail_index != 1:
                new_segments[self.tail_index - 1] = np.array([0, 0])
        else:
            self.tail_index += 1

        # shift values down by one
        new_segments = np.roll(new_segments, 1, axis=0)

        # copy the head back to the first row so that it can be moved
        new_segments[0] = new_segments[1]

        # insert new value at top
        if direction == Direction.UP:
            new_segments[0][1] -= self.snake_size
        elif direction == Direction.DOWN:
            new_segments[0][1] += self.snake_size
        elif direction == Direction.LEFT:
            new_segments[0][0] -= self.snake_size
        elif direction == Direction.RIGHT:
            new_segments[0][0] += self.snake_size

        self.segments = new_segments

        return self.segments[0]

    def length(self) -> int:
        return self.tail_index

    def position(self):
        return self.segments[:self.tail_index]

    def __set_direction(self, direction: Direction):
        if direction == Direction.UP and self.direction != Direction.DOWN:
            self.direction = Direction.UP
        elif direction == Direction.DOWN and direction != Direction.UP:
            self.direction = Direction.DOWN
        elif direction == Direction.LEFT and direction != Direction.RIGHT:
            self.direction = Direction.LEFT
        elif direction == Direction.RIGHT and direction != Direction.LEFT:
            self.direction = Direction.RIGHT
        else:
            self.direction = direction

    def touches_tail(self):
        # how do I know if the snake touches its own tail?
        # if I have duplicates in the matrix
        # unique is the sorted unique segments
        # counts is the number of times each of the unique values comes up in the segments matrix
        unique, counts = np.unique(self.segments[:self.tail_index], return_counts=True, axis=0)

        # if the count is greater than 1, it means we have duplicates and the snake touches its tail
        return len(unique[counts > 1]) > 0

class Food(object):

    def __init__(self):
        self.point = None

    def move(self, point: np.array):
        self.point = point

    def random_move(self, points: np.array):
        index = np.random.randint(points.size, size=1)
        self.point = points[index]
