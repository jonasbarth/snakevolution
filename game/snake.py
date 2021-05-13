import math
import random
from typing import List

import pygame

from environment.env import Direction
from environment.point import Point

import numpy as np


class SnakeGame(object):

    def __init__(self, screen_width: int, screen_height: int, snake_size: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.snake_size = snake_size
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.blue = pygame.Color(0, 0, 255)
        self.direction = None
        self.running = False
        self.ate_food = False
        self.food = None

        self.grid_slots = int((screen_width / snake_size) * (screen_height / snake_size))
        self.snake = Snake(start_position=self.start_position(), direction=Direction.UP, snake_size=snake_size, grid_slots=self.grid_slots)

    def start(self) -> None:
        self.running = True

    def move(self, direction: Direction) -> Point:
        pass

    def game_over(self) -> None:
        pass

    def is_game_over(self) -> bool:
        pass

    def snake_position(self) -> Point:
        pass

    def food_position(self) -> Point:
        pass

    def start_position(self) -> Point:
        start_x = self.screen_width / 2
        start_y = self.screen_height / 2
        return Point(start_x, start_y)


class PyGameSnakeGame(SnakeGame):

    def __init__(self, screen_width: int, screen_height: int, snake_size: int):
        super().__init__(screen_width, screen_height, snake_size)
        self.snake_rect = pygame.Rect(self.snake.get_head_position()[0], self.snake.get_head_position()[0], snake_size, snake_size)


    def start(self) -> None:
        super().start()
        self.window = pygame.display.set_mode((self.screen_width, self.screen_height))
        # 0,0 is in the top left corner
        #

        pygame.draw.rect(self.window, self.red, self.snake_rect)
        pygame.display.flip()

        self.__random_food()

    def move(self, direction: Direction) -> Point:

        # check if the snake would touch food in the next move

        # move the snake in a new direction
        snake_head = self.snake.move(direction, self.ate_food)

        # check if the snake touches food
        if self.__is_touching_food():
            self.ate_food = True
            self.__random_food()
        else:
            self.ate_food = False

        self.__draw_snake()
        self.__draw_food()


        return Point.from_numpy(snake_head)

    def game_over(self) -> None:
        pass

    def is_game_over(self) -> bool:
        pass

    def snake_position(self) -> Point:
        return Point.from_numpy(self.snake.get_head_position())

    def food_position(self) -> Point:
        return Point(190, 150)

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
        return Point.from_numpy(self.snake.get_head_position()) == self.food_position()

    def __draw_food(self):
        pygame.draw.rect(self.window, self.green, self.food)
        pygame.display.flip()

    def __draw_snake(self):
        self.window.fill(self.black)
        snake_segments = self.snake.position()
        index = 0
        for segment in snake_segments:
            colour = self.blue
            # the head of the snake is a different colour than the rest
            if index == 0:
                colour = self.red
            index += 1

            rect = pygame.Rect(segment[0], segment[1], self.snake_size, self.snake_size)
            pygame.draw.rect(self.window, colour, rect)
            pygame.display.flip()



class Snake(object):

    def __init__(self, start_position: Point, direction: Direction, snake_size: int, grid_slots: int):
        self.snake_size = snake_size
        self.segments = np.zeros((grid_slots, 2))
        self.segments[0] = start_position.as_numpy()
        self.tail_index = 1
        self.direction = direction

    def get_head_position(self) -> np.array:
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


class Food(object):

    def __init__(self):
        self.point = None

    def move(self, point: np.array):
        self.point = point

    def random_move(self, points: np.array):
        index = np.random.randint(points.size, size=1)
        self.point = points[index]


class PyGameSnake(Snake):

    def __init__(self, start_position: Point, snake_size: int):
        super().__init__(start_position, snake_size)
        head = pygame.Rect(start_position.x, start_position.y, snake_size, snake_size)
        super().segments.append(head)

    def move(self, direction: Direction):
        self.__set_direction(direction=direction)

        if direction == Direction.UP:
            self.snake.move_ip(0, -self.snake_size)
        elif direction == Direction.DOWN:
            self.snake.move_ip(0, self.snake_size)
        elif direction == Direction.LEFT:
            self.snake.move_ip(-self.snake_size, 0)
        elif direction == Direction.RIGHT:
            self.snake.move_ip(self.snake_size, 0)

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
