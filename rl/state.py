from environment.env import Direction
from environment.point import Point
from game.snake import SnakeGame
import numpy as np


class State(object):

    def get_state(self) -> np.array:
        pass

    def dims(self) -> (int, int):
        pass


class SnakeState(State):

    def __init__(self, game: SnakeGame):
        self.game = game

    def get_state(self) -> np.array:
        pass

    def dims(self) -> (int, int):
        pass


class SnakeState1(SnakeState):

    def __init__(self, game: SnakeGame):
        super().__init__(game)
        self.game = game
        self._dims = None

    def get_state(self) -> np.array:
        food = self.game.food_position()
        snake_head = self.game.snake_head()
        direction = self.game.direction()

        # distance from snakehead to all 4 walls
        # TODO add diagonal distances as well
        # TODO compute distance as being the closest obstacle, which is either the wall or the snake
        # how can I compute the distance to the wall diagonally?
        wall_distances = self.__wall_distances(snake_head=snake_head, direction=direction)
        food_distance = np.array([snake_head.distance(food)])

        state = np.concatenate((Direction.one_hot(direction), wall_distances, food_distance))
        return state

    def dims(self) -> (int, int):
        # if self._dims == None:
        # self._dims = self.get_state().shape

        return (8, 1)

    def __wall_distances(self, snake_head: Point, direction: Direction) -> np.array:
        north_wall = Point(snake_head.x, 0)
        west_wall = Point(0, snake_head.y)
        south_wall = Point(snake_head.x, self.game.dimensions()[1])
        east_wall = Point(self.game.dimensions()[0], snake_head.y)

        snake_north_wall_dist = snake_head.distance(north_wall)
        snake_west_wall_dist = snake_head.distance(west_wall)
        snake_south_wall_dist = snake_head.distance(south_wall)
        snake_east_wall_dist = snake_head.distance(east_wall)

        if direction == Direction.UP:
            return np.array([snake_west_wall_dist, snake_north_wall_dist, snake_east_wall_dist])

        if direction == Direction.RIGHT:
            return np.array([snake_north_wall_dist, snake_east_wall_dist, snake_south_wall_dist])

        if direction == Direction.DOWN:
            return np.array([snake_east_wall_dist, snake_south_wall_dist, snake_west_wall_dist])

        if direction == Direction.LEFT:
            return np.array([snake_south_wall_dist, snake_west_wall_dist, snake_north_wall_dist])


class SnakeState2(SnakeState):
    """
    A class where the state is the entire grid as a matrix
    """
    pass


class SnakeState3(SnakeState):
    """
    Use a model that does not use distances but boolean values to say whether there is a danger (left, right, up, down),
    which direction we are going in (left, right, up, down), and which direction the food is in (left, right, up, down)
    https://www.youtube.com/watch?v=PJl4iabBEz0
    """

    def __init__(self, game: SnakeGame):
        super().__init__(game)
        self.game = game
        self._dims = None

    def get_state(self) -> np.array:
        direction = self.game.direction()
        snake_head = self.game.snake_head()
        snake_body = self.game.snake_position()[1:, :]

        danger_straight = 0
        danger_left = 0
        danger_right = 0

        straight = []
        left = []
        right = []
        # is there a danger because of the snake's body
        # get the three squares around the snakes head (left, right, straight) and check if they're in the snake's body
        #
        vicinity = self.game.snake_head_vicinity()

        if self.game.is_outside(vicinity[0]) or vicinity[0] in snake_body:
            danger_straight = 1
        if self.game.is_outside(vicinity[1]) or vicinity[1] in snake_body:
            danger_left = 1
        if self.game.is_outside(vicinity[2]) or vicinity[2] in snake_body:
            danger_right = 1


        food = self.game.food_position()
        food_left = 0
        food_right = 0
        food_up = 0
        food_down = 0

        if food.x > snake_head.x:
            food_right = 1

        elif food.x < snake_head.x:
            food_left = 1

        elif food.x == snake_head.x:
            food_left = 0
            food_right = 0

        if food.y > snake_head.y:
            food_down = 1

        elif food.y < snake_head.y:
            food_up = 1

        elif food.y == snake_head.y:
            food_up = 0
            food_down = 0

        else:
            food_left = 1
            food_right = 1
            food_up = 1
            food_down = 1
        # get the food position
        # if x > snake x, food is right, else left
        # if y > snake y, food is below, else above
        return np.array([danger_straight, danger_left, danger_right, food_up, food_down, food_left, food_right])

    def dims(self) -> (int, int):
        return (7, 1)

    def is_danger(self, distance: float) -> int:
        if distance <= 1:
            return 1
        return 0
