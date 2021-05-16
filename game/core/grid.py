import numpy as np

from environment.env import Direction
from environment.point import Point


class Food(object):

    def __init__(self, screen_width: int, screen_height: int, position: np.array):
        self._position = position
        self.screen_width = screen_width
        self.screen_height = screen_height

    def move(self, position: np.array) -> None:
        self._position = position

    def position(self) -> np.array:
        return self._position


class Snake(object):

    def __init__(self, start_position: np.array, direction: Direction, snake_size: int, grid_slots: int):
        self.snake_size = snake_size
        self.segments = np.zeros((grid_slots, 2))
        self.segments[0] = start_position
        self.tail_index = 1
        self.direction = direction

    def head(self) -> np.array:
        return self.segments[0]

    def move(self, direction: Direction, add_tail: bool = False) -> np.array:
        self.__set_direction(direction=direction)

        # remove last value, shift all values down by one, insert new value at top
        # copy the segments matrix
        new_segments = np.copy(self.segments)


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

        if add_tail:
            self.tail_index += 1
        else:
            new_segments[self.tail_index] = np.array([0, 0])

        self.segments = new_segments

        return self.segments[0]

    def length(self) -> int:
        return self.tail_index

    def position(self) -> np.array:
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

    def touches_tail(self) -> bool:
        # how do I know if the snake touches its own tail?
        # if I have duplicates in the matrix
        # unique is the sorted unique segments
        # counts is the number of times each of the unique values comes up in the segments matrix
        unique, counts = np.unique(self.segments[:self.tail_index], return_counts=True, axis=0)

        # if the count is greater than 1, it means we have duplicates and the snake touches its tail
        return len(unique[counts > 1]) > 0


class Grid(object):

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = np.zeros((width, height))
        self._snake = Snake(start_position=self.start_position(), direction=Direction.UP, snake_size=1, grid_slots=self.grid.size)
        self.set_snake_in_grid()
        self._food = Food(screen_width=width, screen_height=height, position=self.random_food())
        self.set_food_in_grid()
        self._touched_wall = False

    def reset(self):
        self._food = Food(screen_width=self.width, screen_height=self.height, position=self.random_food())
        self._snake = Snake(start_position=self.start_position(), direction=Direction.UP, snake_size=1,
                            grid_slots=self.grid.size)

        self.update_grid()
        self._touched_wall = False

    def random_food(self) -> np.array:
        available_slots = self.available_slots()
        index = np.random.randint(available_slots.shape[0], size=1)
        new_food = available_slots[index]
        return new_food[0]

    def move_snake(self, direction: Direction, ate_food: bool) -> np.array:
        self._snake.move(direction, ate_food)
        self.update_grid()
        return self._snake.head()

    def update_grid(self):
        self.grid = np.zeros((self.width, self.height))

        self.set_food_in_grid()
        self.set_snake_in_grid()


    def set_snake_in_grid(self):
        for segment in self._snake.position():
            new_x = int(segment[0])
            new_y = int(segment[1])

            if new_x < 0 or new_x >= self.width or new_y < 0 or new_y >= self.height:
                self._touched_wall = True
            else:
                self.grid[new_x][new_y] = 1
                self._touched_wall = False

    def set_food_in_grid(self):
        food_x = int(self._food.position()[0])
        food_y = int(self._food.position()[1])
        self.grid[food_x][food_y] = 1

    def food(self) -> Food:
        return self._food

    def snake(self) -> Snake:
        return self._snake

    def available_slots(self) -> np.array:
        indeces = np.where(self.grid == 0)
        a = indeces[0].reshape((indeces[0].size, 1))
        b = indeces[1].reshape((indeces[1].size, 1))

        return np.concatenate((a, b), axis=1)

    def snake_is_touching_food(self) -> bool:
        return (self._snake.head() == self._food.position()).all()

    def snake_is_touching_wall(self) -> bool:
        return self._touched_wall

    def snake_is_touching_tail(self) -> bool:
        return self._snake.touches_tail()

    def start_position(self) -> np.array:
        start_x = self.width / 2
        start_y = self.height / 2
        return np.array([start_x, start_y])

    @staticmethod
    def scale(coordinates: np.array, slot_size: int) -> np.array:
        return coordinates * slot_size

    @staticmethod
    def scale_to_grid(coordinates: np.array, slot_size: int) -> np.array:
        return coordinates / slot_size