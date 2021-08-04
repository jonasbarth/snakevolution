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

        north_wall = Point(snake_head.x, 0)
        west_wall = Point(0, snake_head.y)
        south_wall = Point(snake_head.x, self.game.dimensions()[1] / self.game.snake_size - 1)
        east_wall = Point(self.game.dimensions()[0] / self.game.snake_size - 1, snake_head.y)

        max_x = east_wall.x
        min_x = west_wall.x
        max_y = south_wall.y
        min_y = north_wall.y

        danger_straight = 0
        danger_left = 0
        danger_right = 0
        # get the snake head
        # check the 4 squares around the snake head
        # if the square contains a 1 or is outside the grid, make it danger

        # use the max and min values for x,y positions and compare them to the snake's head for the walls
        # if snake.x == max(x), then danger right if direction up, danger straight if direction right, danger left if direction down
        if snake_head.x == max_x:
            if direction == Direction.UP:
                danger_right = 1

            if direction == Direction.RIGHT:
                danger_straight = 1

            if direction == Direction.DOWN:
                danger_left = 1


            # if direction up -> danger right
            # if direction right -> danger straight
            # if direction down -> danger left

        # if snake.x == min(x), then danger left if direction up, danger straight if direction left, danger right if direction down
        if snake_head.x == min_x:
            if direction == Direction.UP:
                danger_left = 1

            if direction == Direction.LEFT:
                danger_straight = 1

            if direction == Direction.DOWN:
                danger_right = 1
            # if direction up -> danger left
            # if direction left -> danger straight
            # if direction down -> danger right

        if snake_head.y == max_y:
            if direction == Direction.DOWN:
                danger_straight = 1

            if direction == Direction.LEFT:
                danger_right = 1

            if direction == Direction.RIGHT:
                danger_left = 1
            # if direction down -> danger straight
            # if direction right -> danger right
            # if direction left -> danger left

        if snake_head.y == min_y:
            if direction == Direction.UP:
                danger_straight = 1

            if direction == Direction.LEFT:
                danger_right = 1

            if direction == Direction.RIGHT:
                danger_left = 1
            # if direction up -> danger straight
            # if direction left -> danger right
            # if direction right -> danger left

        straight = []
        left = []
        right = []
        # is there a danger because of the snake's body
        # get the three squares around the snakes head (left, right, straight) and check if they're in the snake's body
        if direction == Direction.UP:
            straight = [snake_head.x, snake_head.y - 1]
            left = [snake_head.x - 1, snake_head.y]
            right = [snake_head.x + 1, snake_head.y]

            # get squares snake_head.y - 1, snake_head.x -1, snake_x + 1

        if direction == Direction.LEFT:
            straight = [snake_head.x - 1, snake_head.y]
            left = [snake_head.x, snake_head.y + 1]
            right = [snake_head.x, snake_head.y - 1]
            # get squares snake_head.x - 1, snake_head.y - 1, snake_head.y + 1

        if direction == Direction.RIGHT:
            straight = [snake_head.x + 1, snake_head.y]
            left = [snake_head.x, snake_head.y - 1]
            right = [snake_head.x, snake_head.y + 1]
            # get squares snake_head.x + 1, snake_head.y - 1, snake_head.y + 1

        if direction == Direction.DOWN:
            straight = [snake_head.x, snake_head.y + 1]
            left = [snake_head.x + 1, snake_head.y]
            right = [snake_head.x - 1, snake_head.y]
            # get squares snake_head.y + 1, snake_head.x - 1, snake_head.x + 1

        if straight in snake_body:
            danger_straight = 1

        if left in snake_body:
            danger_left = 1

        if right in snake_body:
            danger_right = 1

        # if snake.y == min(y), then danger straight if direction up, danger right if direction left, danger left if direction right
        # if snake.y == max(y), then danger straight if direction down, danger left if direction left, danger right if direction right

        # if snake.y == max(y),

        # get the food position
        # if x > snake x, food is right, else left
        # if y > snake y, food is below, else above

        return 0

    def dims(self) -> (int, int):
        return (8, 1)

    def is_danger(self, distance: float) -> int:
        if distance <= 1:
            return 1
        return 0
