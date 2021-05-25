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
        #if self._dims == None:
            #self._dims = self.get_state().shape

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
