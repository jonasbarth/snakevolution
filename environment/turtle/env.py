import random

import numpy as np
from scipy.spatial import distance

from environment.env import Env, Food, Snake
import turtle

from environment.point import Point


class SnakeEnv(Env):

    def __init__(self, screen_width, screen_height, state_representation):
        self.wn = turtle.Screen()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.max_distance = distance.cityblock(np.array([0, 0]), np.array([screen_width, screen_height]))
        self.current_food = None
        self.snake = None
        self.actions = {0: "up", 1: "right", 2: "down", 3: "left"}
        self.points = 0
        self.n_moves = 0
        self.max_moves_without_food = 1000
        self.theta = 45
        self.state_representation = state_representation(self)

    def reset(self):
        """
        Resets the Snake environment
        """
        self.wn.clear()
        self.current_food = None
        self.wn.title("Snake Game")
        self.wn.bgcolor("white")
        self.wn.setup(width=self.screen_width, height=self.screen_height)
        self.__generate_food()
        self.snake = Snake()
        self.points = 0
        self.n_moves = 0
        state = self.state_representation.get_state()
        done = False
        reward = 0

        return (state, reward, done)

    def step(self, action):
        """
        Take a step in the Snake environment and return the next state, reward and whether the game is over.

        Parameters:
            action - An integer between 0 and 3 denoting the action to be taken.

        Returns:
            state - an ND numpy array
            reward - an integer denoting the reward
            done - a boolean indicating whether the episode is over
        """
        direction = self.actions[action]
        previous_location = self.snake.get_current_location()

        ## Move the environment in the desired direction and check whether it touches food
        self.snake.move(direction)
        self.n_moves += 1
        current_location = self.snake.get_current_location()

        ## The variables to be returned. Reward will remain 0 if the environment doesn't touch anything.
        reward = self.__get_food_distance_reward(previous_location, current_location)
        done = False
        state = None

        state = self.state_representation.get_state()

        ## If the environment touches a wall or itself, the episode is over
        if self.touch_wall() or self.touch_snake() or self.n_moves >= self.max_moves_without_food:
            reward = -100
            done = True

        ## If the environment touches food, add to the tail
        elif self.touch_food():
            self.points += 1
            reward = 10
            self.snake.add_tail()
            self.__generate_food()

        ## Update the visuals
        self.wn.update()

        return (state, reward, done)

    def __generate_food(self):
        """
        Generates a piece of food at a random x,y coordinate in the environment.

        Parameters:
            None

        Returns:
            None
        """

        ## Get the min and max x-value in the environment
        x_start = ((-1) * self.screen_width / 2) / 20 + 1
        x_end = (self.screen_width / 2) / 20 - 1

        ## Get the min and max y-value in the environment
        y_start = ((-1) * self.screen_height / 2) / 20 + 1
        y_end = (self.screen_height / 2) / 20 - 1

        ## Get pseudorandom x,y coordinates for the food
        x_rand = random.randrange(x_start, x_end) * 20
        y_rand = random.randrange(y_start, y_end) * 20

        # if a food object has been previously created, just move it to a new random location
        if (self.current_food):
            self.current_food.head.goto(x_rand, y_rand)
        else:
            self.current_food = Food(x_rand, y_rand)

    def touch_food(self):
        """
        Checks if the environment is currently touching the piece of food in the environment. Touching
        means to be within 20 pixels of the food.

        Parameters:
            None

        Returns:
            True - if the environment touches the food.
            False - if the environment does not touch the food.
        """
        if self.snake.food_distance(self.current_food) < 20.0:
            return True
        return False

    def food_distance(self, dist_metric=distance.cityblock):
        """
        Measures the distance between the environment and the food according to the given distance metric.
        Default distance metric is the Manhattan distance.

        Parameters:
            dist_metric - The distance metric function taking two 1D numpy arrays as input

        Returns:
            float - The distance between the environment and the food. Returns -1 if the either the environment or food does not exist.
        """
        if (self.snake and self.current_food):
            snake_x, snake_y = self.snake.head.pos()
            food_x, food_y = self.current_food.head.pos()
            return dist_metric(np.array([snake_x, snake_y]), np.array([food_x, food_y]))

        return -1

    def touch_wall(self):
        """
        Checks if the environment head is currently touching a wall.

        Parameters:
            None

        Returns:
            True - if the environment head is outside the environment boundaries, i.e. has touched a wall.
            False - if the environment head is inside the environment boundaries, i.e. has not touched a wall
        """
        x, y = self.snake.head.xcor(), self.snake.head.ycor()

        ## Get the min and max x,y coordinates the environment can be at
        x_start = (-1) * self.screen_width / 2
        x_end = self.screen_width / 2
        y_start = (-1) * self.screen_height / 2
        y_end = self.screen_height / 2

        if x <= x_start or x >= x_end:
            return True

        if y <= y_start or y >= y_end:
            return True

        return False

    def touch_snake(self, dist_metric=distance.cityblock):
        """
        Checks if the environment is currently touching itself.

        Parameters:
            None

        Returns:
            True - if the environment head is currently within 20 pixels range of a tail section
            False - if the environment head is currently outside of 20 pixels range of a tail section
        """

        head_x = self.snake.head.xcor()
        head_y = self.snake.head.ycor()

        ## Look through the tail section to see if the head touches any of them
        for tail in self.snake.segments[1:]:
            tail_x = tail.head.xcor()
            tail_y = tail.head.ycor()

            if dist_metric(np.array([head_x, head_y]), np.array([tail_x, tail_y])) < 20:
                return True

        return False

    def get_episode_statistic(self):
        """
        Gets statistics about the current episode.
        :return:
        """
        return (self.points, self.n_moves, self.snake.get_tail_length())

    def __get_food_distance_reward(self, previous_location: Point, current_location: Point):
        """

        :param previous_location: A type point that specifies previous location of the environment
        :param current_location: A type point that specifies the current location of the environment
        :return: 1 if the environment moved towards the food, 0 if the environment moved away from the food
        """
        """
        food_x = self.current_food.head.xcor()
        food_y = self.current_food.head.ycor()
        food_point = Point(food_x, food_y)
        if (previous_location.distance(food_point) > current_location.distance(food_point)):
            return 1

        return 
        """

        def normalise(x):
            return 1 - (x / self.max_distance)

        food_x = self.current_food.head.xcor()
        food_y = self.current_food.head.ycor()
        food_point = Point(food_x, food_y)
        multiplier = len(self.snake.segments) if len(self.snake.segments) > 2 else 1
        return normalise(current_location.distance(food_point)) * multiplier

    def get_lidar_origin_points(self):
        return None

    def draw_lidar(self):
        for end_point in self.state_representation.lidar_end_points:
            if end_point:
                t = turtle.Turtle()
                t.penup()
                t.goto(self.snake.head.xcor(), self.snake.head.ycor())
                t.pendown()
                t.goto(end_point.x, end_point.y)

    def grid_positions(self):
        rows = (self.screen_width / 20) - 1
        columns = (self.screen_height / 20) - 1
        self.grid = np.zeros((rows, columns))

    def update_grid(self):
        for segment in self.snake.segments:
            segment_row = segment.head.xcor() / 20
            segment_column = segment.head.ycor() / 20
            self.grid[segment_row][segment_column] = 1

    def available_points(self):
        return None

    def total_points(self) -> int:
        return self.points

    def total_steps(self) -> int:
        return self.n_moves


class TurtleSnake(Snake):

    def __init__(self, colour="black", x=0, y=0):
        """
        Constructor for the Snake.

        Parameters:
            colour - a string for the colour of the head of the Snake. Default value is Black.
            x - an integer for the x position of the Snake
            y - an integer for the y position of the Snake
        """
        super().__init__(colour, x, y)
        self.head = turtle.Turtle()
        self.head.speed(10)
        turtle.delay(0)
        self.head.shape("square")
        self.head.color(colour)
        self.head.penup()
        self.head.goto(x, y)
        self.head.direction = "stop"
        self.previous_direction = "stop"
        self.final_tail_section = "stop"
        self.moves = {"up": self.__up, "right": self.__right, "down": self.__down, "left": self.__left}
        self.one_hot = {"up": [1, 0, 0, 0], "right": [0, 1, 0, 0], "down": [0, 0, 1, 0], "left": [0, 0, 0, 1],
                        "stop": [0, 0, 0, 0]}
        self.legal_direction = {"up": ["up", "left", "right"], "right": ["right", "up", "down"],
                                "down": ["down", "right", "left"], "left": ["left", "up", "down"],
                                "stop": ["left", "right", "up", "down"]}
        self.tail = [self]

    def set_direction(self, direction):
        """
        Sets the direction that the Snake head is facing.

        Parameters:
            direction - A string specifying the direction the head needs to be facing. Must be in ["stop", "up", "down", "left", "right"]

        Returns:
            None
        """

        ## ensure that the direction is legal
        if direction in ["stop", "up", "down", "left", "right"]:
            self.previous_direction = self.head.direction
            self.head.direction = direction

    def move(self, direction):
        """
        Moves the Snake in the given direction.

        Parameters:
            direction - A string specifying the direction the head needs to be facing. Must be in ["stop", "up", "down", "left", "right"]

        Returns:
            None
        """
        if (self.__direction_is_legal(direction)):
            self.set_direction(direction)
            self.moves[direction]()

    def __down(self):
        """
        Move the Snake downwards if the head is facing down.

        Parameters:
            None

        Returns:
            None
        """

        if self.head.direction == "down":

            ## Move the head
            for i in range(len(self.tail) - 1, 0, -1):
                x = self.tail[i - 1].head.xcor()
                y = self.tail[i - 1].head.ycor()
                self.tail[i].head.direction = self.tail[i - 1].previous_direction
                self.tail[i].head.goto(x, y)

            self.head.sety(self.head.ycor() - 20)

    def __up(self):
        """
        Move the Snake upwards if the head is facing up.

        Parameters:
            None

        Returns:
            None
        """

        if self.head.direction == "up":
            for i in range(len(self.tail) - 1, 0, -1):
                x = self.tail[i - 1].head.xcor()
                y = self.tail[i - 1].head.ycor()
                self.tail[i].head.direction = self.tail[i - 1].previous_direction
                self.tail[i].head.goto(x, y)

            self.head.sety(self.head.ycor() + 20)

    def __left(self):
        """
        Move the Snake left if the head is facing left.

        Parameters:
            None

        Returns:
            None
        """
        if self.head.direction == "left":
            ## Move the head
            for i in range(len(self.tail) - 1, 0, -1):
                x = self.tail[i - 1].head.xcor()
                y = self.tail[i - 1].head.ycor()
                self.tail[i].head.direction = self.tail[i - 1].previous_direction
                self.tail[i].head.goto(x, y)

            self.head.setx(self.head.xcor() - 20)

    def __right(self):
        """
        Move the Snake right if the head is facing right.

        Parameters:
            None

        Returns:
            None
        """
        # TODO set the direction of each element to the direction of t
        if self.head.direction == "right":
            ## Move the head

            for i in range(len(self.tail) - 1, 0, -1):
                x = self.tail[i - 1].head.xcor()
                y = self.tail[i - 1].head.ycor()
                self.tail[i].head.direction = self.tail[i - 1].previous_direction
                self.tail[i].head.goto(x, y)

            self.head.setx(self.head.xcor() + 20)

    def food_distance(self, food, metric=distance.cityblock):
        """
        Measures the distance between the food and the environment head with the given distance metric.

        Parameters:
            food - An instance of the Food class
            metric - A distance function taking two 1D numpy arrays as input

        Returns:
            float - The distance between the food and the environment head
        """

        snake_cor = np.array([self.head.pos()[0], self.head.pos()[1]], dtype=np.float32)
        food_cor = np.array([food.head.pos()[0], food.head.pos()[1]], dtype=np.float32)

        return metric(snake_cor, food_cor)

    def add_tail(self):
        """
        Adds a section to the tail of the environment.

        Parameters:
            None

        Returns:
            None
        """
        x = int(self.tail[-1].head.pos()[0])
        y = int(self.tail[-1].head.pos()[1])
        new_part = TurtleSnake(colour="gray", x=x, y=y)
        new_part.set_direction(self.tail[-1].previous_direction)
        self.tail.append(new_part)

    def point_is_in_tail(self, point):
        """
        Checks whether the provided point is somewhere in the tail of the environment.
        :param point: an object of type Point
        :return: a triples (False, (0, 0)) if the point does not exist in the tail. A triples (True, (cx, cy)) where
        cx and cy are the coordinates of the point.
        """
        for section in self.tail[1:]:
            cx, cy = section.head.pos()
            x_1 = cx - 10
            y_1 = cy - 10
            x_2 = cx + 10
            y_2 = cy + 10

            if (x_1 < point.x < x_2) and (y_1 < point.y < y_2):
                return (True, (cx, cy))

        return (False, (0, 0))

    def reset(self):
        """
        Resets the environment to the starting position (0, 0), sets the direction to stop and remove all the tail elements.
        :return:
        """
        # remove all the tail drawings
        for section in self.tail[1:]:
            section.reset()

        self.tail = [self]
        self.head.goto(0, 0)
        self.head.direction = "stop"
        self.previous_direction = "stop"

    def __direction_is_legal(self, direction):
        """
        Checks whether the direction is legal. A environment can not move in the opposite direction on the same axis but needs
        to move on a different axis. E.g. if the environment is moving left, it cannot move right but needs to move either
        up or down.
        :param direction: a string that specifies the direction to be checked.
        :return: False if the direction is not permitted. True if the direction is permitted.
        """
        try:

            return direction in self.legal_direction[self.head.direction]

        except KeyError:
            return False

    def get_current_one_hot_direction(self):
        return self.one_hot[self.head.direction]

    def get_tail_one_hot_direction(self):
        return self.one_hot[self.tail[-1].head.direction]

    def get_tail_length(self):
        return len(self.tail)

    def get_current_location(self):
        return Point(self.head.xcor(), self.head.ycor())


class SnakeEnv(Env):

    def __init__(self, screen_width, screen_height, state_representation):
        self.wn = turtle.Screen()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.max_distance = distance.cityblock(np.array([0, 0]), np.array([screen_width, screen_height]))
        self.current_food = None
        self.snake = None
        self.actions = {0: "up", 1: "right", 2: "down", 3: "left"}
        self.points = 0
        self.n_moves = 0
        self.max_moves_without_food = 1000
        self.theta = 45
        self.state_representation = state_representation(self)

    def reset(self):
        """
        Resets the Snake environment
        """
        self.wn.clear()
        self.current_food = None
        self.wn.title("Snake Game")
        self.wn.bgcolor("white")
        self.wn.setup(width=self.screen_width, height=self.screen_height)
        self.__generate_food()
        self.snake = TurtleSnake()
        self.points = 0
        self.n_moves = 0
        state = self.state_representation.get_state()
        done = False
        reward = 0

        return (state, reward, done)

    def step(self, action):
        """
        Take a step in the Snake environment and return the next state, reward and whether the game is over.

        Parameters:
            action - An integer between 0 and 3 denoting the action to be taken.

        Returns:
            state - an ND numpy array
            reward - an integer denoting the reward
            done - a boolean indicating whether the episode is over
        """
        direction = self.actions[action]
        previous_location = self.snake.get_current_location()

        ## Move the environment in the desired direction and check whether it touches food
        self.snake.move(direction)
        self.n_moves += 1
        current_location = self.snake.get_current_location()

        ## The variables to be returned. Reward will remain 0 if the environment doesn't touch anything.
        reward = self.__get_food_distance_reward(previous_location, current_location)
        done = False
        state = None

        state = self.state_representation.get_state()

        ## If the environment touches a wall or itself, the episode is over
        if self.touch_wall() or self.touch_snake() or self.n_moves >= self.max_moves_without_food:
            reward = -100
            done = True

        ## If the environment touches food, add to the tail
        elif self.touch_food():
            self.points += 1
            reward = 10
            self.snake.add_tail()
            self.__generate_food()

        ## Update the visuals
        self.wn.update()

        return (state, reward, done)

    def __generate_food(self):
        """
        Generates a piece of food at a random x,y coordinate in the environment.

        Parameters:
            None

        Returns:
            None
        """

        ## Get the min and max x-value in the environment
        x_start = ((-1) * self.screen_width / 2) / 20 + 1
        x_end = (self.screen_width / 2) / 20 - 1

        ## Get the min and max y-value in the environment
        y_start = ((-1) * self.screen_height / 2) / 20 + 1
        y_end = (self.screen_height / 2) / 20 - 1

        ## Get pseudorandom x,y coordinates for the food
        x_rand = random.randrange(x_start, x_end) * 20
        y_rand = random.randrange(y_start, y_end) * 20

        # if a food object has been previously created, just move it to a new random location
        if (self.current_food):
            self.current_food.head.goto(x_rand, y_rand)
        else:
            self.current_food = TurtleFood(x_rand, y_rand)

    def touch_food(self):
        """
        Checks if the environment is currently touching the piece of food in the environment. Touching
        means to be within 20 pixels of the food.

        Parameters:
            None

        Returns:
            True - if the environment touches the food.
            False - if the environment does not touch the food.
        """
        if self.snake.food_distance(self.current_food) < 20.0:
            return True
        return False

    def food_distance(self, dist_metric=distance.cityblock):
        """
        Measures the distance between the environment and the food according to the given distance metric.
        Default distance metric is the Manhattan distance.

        Parameters:
            dist_metric - The distance metric function taking two 1D numpy arrays as input

        Returns:
            float - The distance between the environment and the food. Returns -1 if the either the environment or food does not exist.
        """
        if (self.snake and self.current_food):
            snake_x, snake_y = self.snake.head.pos()
            food_x, food_y = self.current_food.head.pos()
            return dist_metric(np.array([snake_x, snake_y]), np.array([food_x, food_y]))

        return -1

    def touch_wall(self):
        """
        Checks if the environment head is currently touching a wall.

        Parameters:
            None

        Returns:
            True - if the environment head is outside the environment boundaries, i.e. has touched a wall.
            False - if the environment head is inside the environment boundaries, i.e. has not touched a wall
        """
        x, y = self.snake.head.xcor(), self.snake.head.ycor()

        ## Get the min and max x,y coordinates the environment can be at
        x_start = (-1) * self.screen_width / 2
        x_end = self.screen_width / 2
        y_start = (-1) * self.screen_height / 2
        y_end = self.screen_height / 2

        if x <= x_start or x >= x_end:
            return True

        if y <= y_start or y >= y_end:
            return True

        return False

    def touch_snake(self, dist_metric=distance.cityblock):
        """
        Checks if the environment is currently touching itself.

        Parameters:
            None

        Returns:
            True - if the environment head is currently within 20 pixels range of a tail section
            False - if the environment head is currently outside of 20 pixels range of a tail section
        """

        head_x = self.snake.head.xcor()
        head_y = self.snake.head.ycor()

        ## Look through the tail section to see if the head touches any of them
        for tail in self.snake.segments[1:]:
            tail_x = tail.head.xcor()
            tail_y = tail.head.ycor()

            if dist_metric(np.array([head_x, head_y]), np.array([tail_x, tail_y])) < 20:
                return True

        return False

    def get_episode_statistic(self):
        """
        Gets statistics about the current episode.
        :return:
        """
        return (self.points, self.n_moves, self.snake.get_tail_length())

    def __get_food_distance_reward(self, previous_location: Point, current_location: Point):
        """

        :param previous_location: A type point that specifies previous location of the environment
        :param current_location: A type point that specifies the current location of the environment
        :return: 1 if the environment moved towards the food, 0 if the environment moved away from the food
        """
        """
        food_x = self.current_food.head.xcor()
        food_y = self.current_food.head.ycor()
        food_point = Point(food_x, food_y)
        if (previous_location.distance(food_point) > current_location.distance(food_point)):
            return 1

        return 
        """

        def normalise(x):
            return 1 - (x / self.max_distance)

        food_x = self.current_food.head.xcor()
        food_y = self.current_food.head.ycor()
        food_point = Point(food_x, food_y)
        multiplier = len(self.snake.segments) if len(self.snake.segments) > 2 else 1
        return normalise(current_location.distance(food_point)) * multiplier

    def get_lidar_origin_points(self):
        return None

    def draw_lidar(self):
        for end_point in self.state_representation.lidar_end_points:
            if end_point:
                t = turtle.Turtle()
                t.penup()
                t.goto(self.snake.head.xcor(), self.snake.head.ycor())
                t.pendown()
                t.goto(end_point.x, end_point.y)

    def grid_positions(self):
        rows = (self.screen_width / 20) - 1
        columns = (self.screen_height / 20) - 1
        self.grid = np.zeros((rows, columns))

    def update_grid(self):
        for segment in self.snake.segments:
            segment_row = segment.head.xcor() / 20
            segment_column = segment.head.ycor() / 20
            self.grid[segment_row][segment_column] = 1

    def available_points(self):
        return None

    def total_points(self) -> int:
        return self.points

    def total_steps(self) -> int:
        return self.n_moves


class TurtleFood(Food):

    def __init__(self, x, y, colour="green"):
        """
        Constructor for the Food.

        Parameters:
            colour - a string for the colour of the Food. Default value is Red.
            x - an integer for the x position of the Food
            y - an integer for the y position of the Food
        """
        self.head = turtle.Turtle()
        self.head.speed(0)
        self.head.shape("square")
        self.head.color(colour)
        self.head.penup()
        self.head.goto(x, y)
        self.head.direction = "stop"

    def point_is_in_food(self, point: Point):
        cx, cy = self.head.pos()
        x_1 = cx - 10
        y_1 = cy - 10
        x_2 = cx + 10
        y_2 = cy + 10

        if (x_1 < point.x < x_2) and (y_1 < point.y < y_2):
            return True, (cx, cy)

        return False, (0, 0)
