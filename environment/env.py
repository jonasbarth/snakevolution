# The game environment for Snake game


import turtle
import random
from environment.snake import Snake
from environment.food import Food
import numpy as np
import scipy.spatial.distance as distance
from environment.point import Point
from environment.state import LidarAndOneHot


class SnakeEnv:

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
        if self.touch_wall() or self.touch_snake() or self.n_moves > self.max_moves_without_food:
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
        for tail in self.snake.tail[1:]:
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
        multiplier = len(self.snake.tail) if len(self.snake.tail) > 2 else 1
        return normalise(current_location.distance(food_point)) * multiplier

    def get_lidar_origin_points(self):
        return None

    def draw_lidar(self):
        for end_point in self.state_representation.lidar_end_points:
            if (end_point):
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
        for segment in self.snake.tail:
            segment_row = segment.head.xcor() / 20
            segment_column = segment.head.ycor() / 20
            self.grid[segment_row][segment_column] = 1

    def available_points(self):
        return None