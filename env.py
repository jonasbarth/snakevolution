# The game environment for Snake game


import turtle
import random
from snake import Snake
from food import Food
import numpy as np
import scipy.spatial.distance as distance
import math



class SnakeEnv:

    def __init__(self, screen_width, screen_height):
        self.wn = turtle.Screen() 
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.current_food = None
        self.snake = Snake()
        self.actions = {0: "up", 1: "right", 2: "down", 3: "left"}
        self.points = 0
        self.theta = 45
        
        

    def reset(self):
        """
        Resets the Snake environment
        """
        self.wn.title("Snake Game")
        self.wn.bgcolor("white")
        self.wn.setup(width=self.screen_width, height=self.screen_height)
        self.__generate_food()
        self.snake.reset()
        

      
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

        ## The variables to be returned. Reward will remain 0 if the snake doesn't touch anything.
        reward = 0
        done = False
        state = np.zeros(6, dtype=np.float32)

        ## Move the snake in the desired direction and check whether it touches food
        self.snake.move(direction)
        
        ## If the snake touches a wall or itself, the episode is over
        if self.__touch_wall() or self.__touch_snake():
            reward = -1
            done = True

        ## If the snake touches food, add to the tail
        elif self.__touch_food():
            self.points += 1
            reward = 1
            self.snake.add_tail()
            self.__generate_food()

        ## Update the visuals
        self.wn.update()

        return (state, reward, done)

    
    def __delete_current_food(self):
        """
        Deletes the current piece of food from the screen.

        Parameters:
            None

        Returns:
            None
        """
        self.current_food.he

    def __generate_food(self):
        """
        Generates a piece of food at a random x,y coordinate in the environment.

        Parameters:
            None

        Returns:
            None
        """

        ## Get the min and max x-value in the environment
        x_start = (-1) * self.screen_width / 2
        x_end = self.screen_width / 2

        ## Get the min and max y-value in the environment
        y_start = (-1) * self.screen_height / 2
        y_end = self.screen_height / 2

        ## Get pseudorandom x,y coordinates for the food
        x_rand = random.randrange(x_start, x_end)
        y_rand = random.randrange(y_start, y_end)

        # if a food object has been previously created, just move it to a new random location
        if (self.current_food):
            self.current_food.head.goto(x_rand, y_rand)
        else:
            self.current_food = Food(x_rand, y_rand)


    def __touch_food(self):
        """
        Checks if the snake is currently touching the piece of food in the environment. Touching
        means to be within 20 pixels of the food.

        Parameters:
            None

        Returns:
            True - if the snake touches the food.
            False - if the snake does not touch the food.
        """
        if self.snake.food_distance(self.current_food) < 20.0:
            return True
        return False


    def __food_distance(self, dist_metric=distance.cityblock):
        """
        Measures the distance between the snake and the food according to the given distance metric.
        Default distance metric is the Manhattan distance.

        Parameters:
            dist_metric - The distance metric function taking two 1D numpy arrays as input

        Returns:
            float - The distance between the snake and the food
        """
        snake_x, snake_y = self.snake.head.pos()
        food_x, food_y = self.current_food.head.pos()
        return dist_metric(np.array([snake_x, snake_y]), np.array([food_x, food_y]))

    
    def __touch_wall(self):
        """
        Checks if the snake head is currently touching a wall.

        Parameters:
            None

        Returns:
            True - if the snake head is outside the environment boundaries, i.e. has touched a wall.
            False - if the snake head is inside the environment boundaries, i.e. has not touched a wall
        """
        x, y = self.snake.head.xcor(), self.snake.head.ycor()

        ## Get the min and max x,y coordinates the snake can be at
        x_start = (-1) * self.screen_width / 2
        x_end = self.screen_width / 2
        y_start = (-1) * self.screen_height / 2
        y_end = self.screen_height / 2

        if x <= x_start or x >= x_end:
            return True

        if y <= y_start or y >= y_end:
            return True

        return False

    def __touch_snake(self):
        """
        Checks if the snake is currently touching itself.

        Parameters:
            None

        Returns:
            True - if the snake head is currently within 20 pixels range of a tail section
            False - if the snake head is currently outside of 20 pixels range of a tail section
        """

        head_x = self.snake.head.xcor()
        head_y = self.snake.head.ycor()

        ## Look through the tail section to see if the head touches any of them
        for tail in self.snake.tail[1:]:
            tail_x = tail.head.xcor()
            tail_y = tail.head.ycor()

            if distance.euclidean(np.array([head_x, head_y]), np.array([tail_x, tail_y])) < 20:
                return True

        return False

    
    def __wall_dist_up(self, dist_metric=distance.cityblock):
        """
        Measure the distance to the Northern environment boundary.

        Parameters:
            dist_metric - The distance metric function, taking two 1D numpy arrays

        Returns:
            float - The distance between the snake head and the Northern wall.
        """
        snake_x, snake_y, = self.snake.head.pos()

        wall_x = snake_x
        wall_y = self.screen_height / 2
            
        return dist_metric(np.array([snake_x, snake_y]), np.array([wall_x, wall_y]))


    def __wall_dist_down(self, dist_metric=distance.cityblock):
        """
        Measure the distance to the Southern environment boundary.

        Parameters:
            dist_metric - The distance metric function, taking two 1D numpy arrays

        Returns:
            float - The distance between the snake head and the Southern wall.
        """
        snake_x, snake_y, = self.snake.head.pos()
        wall_x = snake_x
        wall_y = (-1) * self.screen_height / 2

        return dist_metric(np.array([snake_x, snake_y]), np.array([wall_x, wall_y]))

    def __wall_dist_left(self, dist_metric=distance.cityblock):
        """
        Measure the distance to the Western environment boundary.

        Parameters:
            dist_metric - The distance metric function, taking two 1D numpy arrays

        Returns:
            float - The distance between the snake head and the Western wall.
        """
        snake_x, snake_y, = self.snake.head.pos()
        wall_y = snake_y
        wall_x = (-1) * self.screen_width / 2

        return dist_metric(np.array([snake_x, snake_y]), np.array([wall_x, wall_y]))

    def __wall_dist_right(self, dist_metric=distance.cityblock):
        """
        Measure the distance to the Eastern environment boundary.

        Parameters:
            dist_metric - The distance metric function, taking two 1D numpy arrays

        Returns:
            float - The distance between the snake head and the Eastern wall.
        """
        snake_x, snake_y, = self.snake.head.pos()
        wall_y = snake_y
        wall_x = self.screen_width / 2

        return dist_metric(np.array([snake_x, snake_y]), np.array([wall_x, wall_y]))

    def __wall_dist_up_right(self, dist_metric=distance.cityblock):
        """
        Measure the 45° diagonal distance to the boundary in the North-East direction.

        Parameters:
            dist_metric - The distance metric function, taking two 1D numpy arrays

        Returns:
            float - The distance between the snake head and the closest wall in the North-East direction.
        """
        snake_x, snake_y = self.snake.head.pos()
        adjacent_x = snake_x
        adjacent_y = self.screen_height / 2

        # Length of the opposite side of the triangle
        adjacent = distance.euclidean(np.array([snake_x, snake_y]), np.array([adjacent_x, adjacent_y]))
        opposite = adjacent

        opposite_x = adjacent_x + opposite
        opposite_y = self.screen_height / 2

        # If the opposite is outside of the screen, turn the head 90 degrees and recompute the distance
        if opposite_x > self.screen_width / 2:
            return self.__wall_dist_right_up()

            
        return dist_metric(np.array([snake_x, snake_y]), np.array([opposite_x, opposite_y]))


    def __wall_dist_down_right(self, dist_metric=distance.cityblock):
        """
        Measure the 45° diagonal distance to the boundary in the South-East direction.

        Parameters:
            dist_metric - The distance metric function, taking two 1D numpy arrays

        Returns:
            float - The distance between the snake head and the closest wall in the South-East direction.
        """
        snake_x, snake_y = self.snake.head.pos()
        adjacent_x = snake_x
        adjacent_y = (-1) * self.screen_height / 2

        # Length of the opposite side of the triangle
        adjacent = distance.euclidean(np.array([snake_x, snake_y]), np.array([adjacent_x, adjacent_y]))
        opposite = adjacent

        opposite_x = adjacent_x + opposite
        opposite_y = (-1) * self.screen_height / 2

        if opposite_x > self.screen_width / 2:
            return self.__wall_dist_right_down()

        return dist_metric(np.array([snake_x, snake_y]), np.array([opposite_x, opposite_y]))
        

    def __wall_dist_up_left(self, dist_metric=distance.cityblock):
        """
        Measure the 45° diagonal distance to the boundary in the North-West direction.

        Parameters:
            dist_metric - The distance metric function, taking two 1D numpy arrays

        Returns:
            float - The distance between the snake head and the closest wall in the North-West direction.
        """
        snake_x, snake_y = self.snake.head.pos()
        adjacent_x = snake_x
        adjacent_y = self.screen_height / 2

        # Length of the opposite side of the triangle
        adjacent = distance.euclidean(np.array([snake_x, snake_y]), np.array([adjacent_x, adjacent_y]))
        opposite = adjacent

        opposite_x = adjacent_x - opposite
        opposite_y = self.screen_height / 2

        if opposite_x < self.screen_width / 2:
            return self.__wall_dist_left_up()

        return dist_metric(np.array([snake_x, snake_y]), np.array([opposite_x, opposite_y]))
        

    def __wall_dist_down_left(self, dist_metric=distance.cityblock):
        """
        Measure the 45° diagonal distance to the boundary in the South-West direction.

        Parameters:
            dist_metric - The distance metric function, taking two 1D numpy arrays

        Returns:
            float - The distance between the snake head and the closest wall in the South-West direction.
        """
        snake_x, snake_y = self.snake.head.pos()
        adjacent_x = snake_x
        adjacent_y = (-1) * self.screen_height / 2

        # Length of the opposite side of the triangle
        adjacent = distance.euclidean(np.array([snake_x, snake_y]), np.array([adjacent_x, adjacent_y]))
        opposite = adjacent

        opposite_x = adjacent_x - opposite
        opposite_y = (-1) * self.screen_height / 2

        if opposite_x < self.screen_width / 2:
            return self.__wall_dist_left_down()

        return dist_metric(np.array([snake_x, snake_y]), np.array([opposite_x, opposite_y]))


    def __wall_dist_right_up(self, dist_metric=distance.cityblock):
        """
        Measure the 45° diagonal distance to the boundary in the East-North direction.

        Parameters:
            dist_metric - The distance metric function, taking two 1D numpy arrays

        Returns:
            float - The distance between the snake head and the closest wall in the East-North direction.
        """
        snake_x, snake_y = self.snake.head.pos()
        adjacent_x = self.screen_width / 2
        adjacent_y = snake_y

        adjacent = distance.euclidean(np.array([snake_x, snake_y]), np.array([adjacent_x, adjacent_y]))
        opposite = adjacent

        opposite_x = self.screen_width / 2
        opposite_y = adjacent_y + opposite

        return dist_metric(np.array([snake_x, snake_y]), np.array([opposite_x, opposite_y]))


    def __wall_dist_right_down(self, dist_metric=distance.cityblock):
        """
        Measure the 45° diagonal distance to the boundary in the East-South direction.

        Parameters:
            dist_metric - The distance metric function, taking two 1D numpy arrays

        Returns:
            float - The distance between the snake head and the closest wall in the East-North direction.
        """
        snake_x, snake_y = self.snake.head.pos()
        adjacent_x = self.screen_width / 2
        adjacent_y = snake_y

        adjacent = distance.euclidean(np.array([snake_x, snake_y]), np.array([adjacent_x, adjacent_y]))
        opposite = adjacent

        opposite_x = self.screen_width / 2
        opposite_y = adjacent_y - opposite

        return dist_metric(np.array([snake_x, snake_y]), np.array([opposite_x, opposite_y]))


    def __wall_dist_left_up(self, dist_metric=distance.cityblock):
        """
        Measure the 45° diagonal distance to the boundary in the West-North direction.

        Parameters:
            dist_metric - The distance metric function, taking two 1D numpy arrays

        Returns:
            float - The distance between the snake head and the closest wall in the West-North direction.
        """
        snake_x, snake_y = self.snake.head.pos()
        adjacent_x = (-1) * self.screen_width / 2
        adjacent_y = snake_y

        adjacent = distance.euclidean(np.array([snake_x, snake_y]), np.array([adjacent_x, adjacent_y]))
        opposite = adjacent

        opposite_x = (-1) * self.screen_width / 2
        opposite_y = adjacent_y + opposite

        return dist_metric(np.array([snake_x, snake_y]), np.array([opposite_x, opposite_y]))


    def __wall_dist_left_down(self, dist_metric=distance.cityblock):
        """
        Measure the 45° diagonal distance to the boundary in the West-South direction.

        Parameters:
            dist_metric - The distance metric function, taking two 1D numpy arrays

        Returns:
            float - The distance between the snake head and the closest wall in the West-South direction.
        """
        snake_x, snake_y = self.snake.head.pos()
        adjacent_x = (-1) * self.screen_width / 2
        adjacent_y = snake_y

        adjacent = distance.euclidean(np.array([snake_x, snake_y]), np.array([adjacent_x, adjacent_y]))
        opposite = adjacent

        opposite_x = (-1) * self.screen_width / 2
        opposite_y = adjacent_y - opposite

        return dist_metric(np.array([snake_x, snake_y]), np.array([opposite_x, opposite_y]))


    def __up_lidar(self):
        """ 
        Gets the Snake's 5 point lidar distances when it is facing up.

        Parameters:
            None

        Returns:
            lidar - A 1D numpy array with 5 entries, one for each lidar distance.
        """
        lidar = np.zeros((5))

        lidar[0] = self.__wall_dist_up()
        lidar[1] = self.__wall_dist_left()
        lidar[2] = self.__wall_dist_right()
        lidar[3] = self.__wall_dist_up_left()
        lidar[4] = self.__wall_dist_up_right()

        return lidar


    def __right_lidar(self):
        """ 
        Gets the Snake's 5 point lidar distances when it is facing right.

        Parameters:
            None

        Returns:
            lidar - A 1D numpy array with 5 entries, one for each lidar distance.
        """
        lidar = np.zeros((5))

        lidar[0] = self.__wall_dist_up()
        lidar[1] = self.__wall_dist_down()
        lidar[2] = self.__wall_dist_right()
        lidar[3] = self.__wall_dist_up_right()
        lidar[4] = self.__wall_dist_down_right()

        return lidar


    def __down_lidar(self):
        """ 
        Gets the Snake's 5 point lidar distances when it is facing down.

        Parameters:
            None

        Returns:
            lidar - A 1D numpy array with 5 entries, one for each lidar distance.
        """
        lidar = np.zeros((5))

        lidar[0] = self.__wall_dist_left()
        lidar[1] = self.__wall_dist_down()
        lidar[2] = self.__wall_dist_right()
        lidar[3] = self.__wall_dist_down_left()
        lidar[4] = self.__wall_dist_down_right()

        return lidar


    def __left_lidar(self):
        """ 
        Gets the Snake's 5 point lidar distances when it is facing left.

        Parameters:
            None

        Returns:
            lidar - A 1D numpy array with 5 entries, one for each lidar distance.
        """
        lidar = np.zeros((5))

        lidar[0] = self.__wall_dist_left()
        lidar[1] = self.__wall_dist_down()
        lidar[2] = self.__wall_dist_up()
        lidar[3] = self.__wall_dist_down_left()
        lidar[4] = self.__wall_dist_up_left()

        return lidar


    def __get_lidar(self, direction):
        """
        Gets the lidar of the Snake.

        Parameters
            direction - A string indicating the direction the Snake is currently facing.

        Returns:
            numpy.array - Returns a 1D numpy array with 5 entries, one for each lidar distance.
        """
        

        if direction == "up":
            return self.__up_lidar()

        elif direction == "right":
            return self.__right_lidar()

        elif direction == "down":
            return self.__down_lidar()

        elif direction == "left":
            return self.__left_lidar()


    def print_lidar(self):
        print("Up", self.__wall_dist_up(), "Down", self.__wall_dist_down(), "Left",self.__wall_dist_left(), "Right",self.__wall_dist_right())
        print("Up-Right",self.__wall_dist_up_right(), "Up-Left", self.__wall_dist_up_left(), "Down-Right",self.__wall_dist_down_right(), "Down-Left", self.__wall_dist_down_left())

