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
        self.snake = PyGameSnake(start_position=self.start_position(), snake_size=snake_size)

    def start(self) -> None:
        pass

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
        start_x = self.screen_width / 2 - self.snake_size / 2
        start_y = self.screen_height / 2 - self.snake_size / 2
        return Point(start_x, start_y)


class PyGameSnakeGame(SnakeGame):

    def __init__(self, screen_width: int, screen_height: int, snake_size: int):
        super().__init__(screen_width, screen_height, snake_size)

    def start(self) -> None:
        self.window = pygame.display.set_mode((self.screen_width, self.screen_height))
        # 0,0 is in the top left corner
        #
        center_x = self.screen_width / 2 - self.snake_size / 2
        center_y = self.screen_height / 2 - self.snake_size / 2
        self.snake = pygame.Rect(center_x, center_y, self.snake_size, self.snake_size)
        pygame.draw.rect(self.window, super.red, self.snake)
        pygame.display.flip()
        running = True
        direction = 'RIGHT'
        change_to = direction

    def move(self, direction: Direction) -> Point:

        self.__set_direction(direction=direction)

        if direction == Direction.UP:
            self.snake.move_ip(0, -self.snake_size)
        elif direction == Direction.DOWN:
            self.snake.move_ip(0, self.snake_size)
        elif direction == Direction.LEFT:
            self.snake.move_ip(-self.snake_size, 0)
        elif direction == Direction.RIGHT:
            self.snake.move_ip(self.snake_size, 0)

        return Point(self.snake.x, self.snake.y)

    def game_over(self) -> None:
        pass

    def is_game_over(self) -> bool:
        pass

    def snake_position(self) -> Point:
        return Point(self.snake.x, self.snake.y)

    def food_position(self) -> Point:
        pass

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

    def __random_food(self):
        pass

    def __available_food_positions(self):
        pass


class Snake(object):

    def __init__(self, start_position: Point, direction: Direction, snake_size: int, grid_slots: int):
        self.snake_size = snake_size
        self.segments = np.zeros((grid_slots, 2))
        self.segments[0] = start_position.as_numpy()
        self.tail_index = 1
        self.direction = direction

    def get_head_position(self) -> Point:
        pass

    def move(self, direction: Direction, add_tail: bool = False) -> Point:
        self.__set_direction(direction=direction)

        # remove last value, shift all values down by one, insert new value at top
        # copy the segments matrix
        new_segments = np.copy(self.segments)

        # remove last value of tail if we don't add a new segment
        if not add_tail:
            new_segments[self.tail_index - 1] = np.array([0, 0])
        else:
            self.tail_index += 1

        # shift values down by one
        np.roll(new_segments, 1)

        # insert new value at top
        if direction == Direction.UP:
            new_segments[0][1] -= self.snake_size
            #self.snake.move_ip(0, -self.snake_size)
        elif direction == Direction.DOWN:
            new_segments[0][1] += self.snake_size
            #self.snake.move_ip(0, self.snake_size)
        elif direction == Direction.LEFT:
            new_segments[0][0] -= self.snake_size
            #self.snake.move_ip(-self.snake_size, 0)
        elif direction == Direction.RIGHT:
            new_segments[0][0] += self.snake_size
            #self.snake.move_ip(self.snake_size, 0)

        self.segments = new_segments

        return Point.from_numpy(self.segments)

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
