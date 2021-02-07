# The game environment for Snake game


import turtle
import random
from snake.snake import Snake
from snake.food import Food
import numpy as np
import scipy.spatial.distance as distance
from snake.point import Point



class SnakeEnv:

    def __init__(self, screen_width, screen_height):
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
        state = self.__get_current_state()
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

        ## Move the snake in the desired direction and check whether it touches food
        self.snake.move(direction)
        self.n_moves += 1
        current_location = self.snake.get_current_location()

        ## The variables to be returned. Reward will remain 0 if the snake doesn't touch anything.
        reward = self.__get_food_distance_reward(previous_location, current_location)
        done = False
        state = None

        state = self.__get_current_state()


        ## If the snake touches a wall or itself, the episode is over
        if self.__touch_wall() or self.__touch_snake() or self.n_moves > self.max_moves_without_food:
            reward = -100
            done = True

        ## If the snake touches food, add to the tail
        elif self.__touch_food():
            self.points += 1
            reward = 10
            self.snake.add_tail()
            self.__generate_food()

        ## Update the visuals
        self.wn.update()

        return (state, reward, done)


    def __get_current_state(self):
        """
        Gets the current state of the the MDP.
        :return: A numpy array of dimension (1, 6) where the first 5 entries are the lidar and the final entry is the distance to the food
        """
        lidar = self.__get_lidar(self.snake.head.direction)
        food_dist = np.array([self.__food_distance()])
        state = np.concatenate((lidar, food_dist))
        return state


    def __generate_food(self):
        """
        Generates a piece of food at a random x,y coordinate in the environment.

        Parameters:
            None

        Returns:
            None
        """

        ## Get the min and max x-value in the environment
        x_start = ((-1) * self.screen_width / 2) / 20 - 1
        x_end = (self.screen_width / 2) / 20 + 1

        ## Get the min and max y-value in the environment
        y_start = ((-1) * self.screen_height / 2) / 20 - 1
        y_end = (self.screen_height / 2) / 20 + 1

        ## Get pseudorandom x,y coordinates for the food
        x_rand = random.randrange(x_start, x_end) * 20
        y_rand = random.randrange(y_start, y_end) * 20

        # if a food object has been previously created, just move it to a new random location
        if (self.current_food):
            print("Ate food")
            self.current_food.head.goto(x_rand, y_rand)
        else:
            print("generated food")
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
            float - The distance between the snake and the food. Returns -1 if the either the snake or food does not exist.
        """
        if (self.snake and self.current_food):
            snake_x, snake_y = self.snake.head.pos()
            food_x, food_y = self.current_food.head.pos()
            return dist_metric(np.array([snake_x, snake_y]), np.array([food_x, food_y]))

        return -1

    
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

    def __touch_snake(self, dist_metric=distance.cityblock):
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

            if dist_metric(np.array([head_x, head_y]), np.array([tail_x, tail_y])) < 20:
                return True

        return False


    def __up_lidar(self):
        """ 
        Gets the Snake's 5 point lidar distances when it is facing up.

        Parameters:
            None

        Returns:
            lidar - A 1D numpy array with 5 entries, one for each lidar distance.
        """
        lidar = np.zeros((5), dtype=np.float32)
        snake_x, snake_y = self.snake.head.pos()[0], self.snake.head.pos()[1]
        snake_pos = Point(snake_x, snake_y)

        lidar[0] = snake_pos.distance(self.lidar_west_pulse())
        lidar[1] = snake_pos.distance(self.lidar_north_west_pulse())
        lidar[2] = snake_pos.distance(self.lidar_north_pulse())
        lidar[3] = snake_pos.distance(self.lidar_north_east_pulse())
        lidar[4] = snake_pos.distance(self.lidar_east_pulse())

        self.lidar_end_points = [self.lidar_west_pulse(), self.lidar_north_west_pulse(), self.lidar_north_pulse(), self.lidar_north_east_pulse(), self.lidar_east_pulse()]

        return lidar


    def __right_lidar(self):
        """ 
        Gets the Snake's 5 point lidar distances when it is facing right.

        Parameters:
            None

        Returns:
            lidar - A 1D numpy array with 5 entries, one for each lidar distance.
        """
        lidar = np.zeros((5), dtype=np.float32)
        snake_x, snake_y = self.snake.head.pos()[0], self.snake.head.pos()[1]
        snake_pos = Point(snake_x, snake_y)

        lidar[0] = snake_pos.distance(self.lidar_north_pulse())
        lidar[1] = snake_pos.distance(self.lidar_north_east_pulse())
        lidar[2] = snake_pos.distance(self.lidar_east_pulse())
        lidar[3] = snake_pos.distance(self.lidar_south_east_pulse())
        lidar[4] = snake_pos.distance(self.lidar_south_pulse())

        self.lidar_end_points = [self.lidar_north_pulse(), self.lidar_north_east_pulse(), self.lidar_east_pulse(), self.lidar_south_east_pulse(), self.lidar_south_pulse()]


        return lidar


    def __down_lidar(self):
        """ 
        Gets the Snake's 5 point lidar distances when it is facing down.

        Parameters:
            None

        Returns:
            lidar - A 1D numpy array with 5 entries, one for each lidar distance.
        """
        lidar = np.zeros((5), dtype=np.float32)
        snake_x, snake_y = self.snake.head.pos()[0], self.snake.head.pos()[1]
        snake_pos = Point(snake_x, snake_y)

        lidar[0] = snake_pos.distance(self.lidar_east_pulse())
        lidar[1] = snake_pos.distance(self.lidar_south_east_pulse())
        lidar[2] = snake_pos.distance(self.lidar_south_pulse())
        lidar[3] = snake_pos.distance(self.lidar_south_west_pulse())
        lidar[4] = snake_pos.distance(self.lidar_west_pulse())

        self.lidar_end_points = [self.lidar_east_pulse(), self.lidar_south_east_pulse(),self.lidar_south_pulse(),self.lidar_south_west_pulse(),self.lidar_west_pulse() ]


        return lidar


    def __left_lidar(self):
        """ 
        Gets the Snake's 5 point lidar distances when it is facing left.

        Parameters:
            None

        Returns:
            lidar - A 1D numpy array with 5 entries, one for each lidar distance.
        """
        lidar = np.zeros((5), dtype=np.float32)
        snake_x, snake_y = self.snake.head.pos()[0], self.snake.head.pos()[1]
        snake_pos = Point(snake_x, snake_y)

        lidar[0] = snake_pos.distance(self.lidar_south_pulse())
        lidar[1] = snake_pos.distance(self.lidar_south_west_pulse())
        lidar[2] = snake_pos.distance(self.lidar_west_pulse())
        lidar[3] = snake_pos.distance(self.lidar_north_west_pulse())
        lidar[4] = snake_pos.distance(self.lidar_north_pulse())

        self.lidar_end_points = [self.lidar_south_pulse(),self.lidar_south_west_pulse(),self.lidar_west_pulse(),self.lidar_north_west_pulse(),self.lidar_north_pulse()]


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

    #def lidar_pulse(self):





    def lidar_east_pulse(self):
        """
        The lidar beam that travels east within the game.
        :return: a point of where the beam either hit a wall or a part of the snake.
        """
        pulse_x, pulse_y = self.snake.head.pos()
        east_pulse = Point(pulse_x, pulse_y)
        east_wall = Point(self.screen_width / 2, pulse_y)
        while (east_pulse.x < east_wall.x and not self.snake.point_is_in_tail(east_pulse)[0]):
           # print(self.snake.point_is_in_tail(east_pulse))
            east_pulse.offset(+1, 0)

        #print("Returning east")
        return east_pulse


    def lidar_south_pulse(self):
        """
        The lidar beam that travels south within the game.
        :return: a point of where the beam either hit a wall or a part of the snake.
        """
        pulse_x, pulse_y = self.snake.head.pos()
        south_pulse = Point(pulse_x, pulse_y)
        south_wall = Point(pulse_x, (-1) * (self.screen_height / 2))
        while (south_pulse.y > south_wall.y and not self.snake.point_is_in_tail(south_pulse)[0]):
            #print(self.snake.point_is_in_tail(south_pulse))
            south_pulse.offset(0, -1)

        #print("Returning south")
        return south_pulse

    def lidar_west_pulse(self):
        """
        The lidar beam that travels west within the game.
        :return: a point of where the beam either hit a wall or a part of the snake.
        """
        pulse_x, pulse_y = self.snake.head.pos()
        west_pulse = Point(pulse_x, pulse_y)
        west_wall = Point((-1) * (self.screen_width / 2), pulse_y)
        while (west_pulse.x > west_wall.x and not self.snake.point_is_in_tail(west_pulse)[0]):
            #print("West pulse", self.snake.point_is_in_tail(west_pulse))
            west_pulse.offset(-1, 0)

        #print("Returning west")
        return west_pulse

    def lidar_north_pulse(self):
        """
        The lidar beam that travels north within the game.
        :return: a point of where the beam either hit a wall or a part of the snake.
        """
        pulse_x, pulse_y = self.snake.head.pos()
        north_pulse = Point(pulse_x, pulse_y)
        north_wall = Point(pulse_x, self.screen_height / 2)
        while (north_pulse.y < north_wall.y and not self.snake.point_is_in_tail(north_pulse)[0]):
            #print(self.snake.point_is_in_tail(north_pulse))
            north_pulse.offset(0, 1)
       #print("Returning north")
        return north_pulse

    def lidar_north_east_pulse(self):
        """
        The lidar beam that travels north east within the game.
        :return: a point of where the beam either hit a wall or a part of the snake.
        """
        pulse_x, pulse_y = self.snake.head.pos()
        north_east_pulse = Point(pulse_x, pulse_y)
        north_wall = Point(pulse_x, self.screen_height / 2)
        east_wall = Point(self.screen_width / 2, pulse_y)

        while (north_east_pulse.y < north_wall.y and north_east_pulse.x < east_wall.x and not self.snake.point_is_in_tail(north_east_pulse)[0]):
            #print("Is in tail", self.snake.point_is_in_tail(north_east_pulse))
            #print("Bool", north_east_pulse.y < north_wall.y, north_east_pulse.x < east_wall.x)
            north_east_pulse.offset(1, 1)

       # print("Returning north east")
        return north_east_pulse

    def lidar_north_west_pulse(self):
        """
        The lidar beam that travels north west within the game.
        :return: a point of where the beam either hit a wall or a part of the snake.
        """
        pulse_x, pulse_y = self.snake.head.pos()
        north_west_pulse = Point(pulse_x, pulse_y)
        north_wall = Point(pulse_x, self.screen_height / 2)
        west_wall = Point(((-1) * self.screen_width) / 2, pulse_y)

        while (north_west_pulse.y < north_wall.y and north_west_pulse.x > west_wall.x and not self.snake.point_is_in_tail(north_west_pulse)[0]):
            #print("Is in tail", self.snake.point_is_in_tail(north_east_pulse))
            #print("Bool", north_east_pulse.y < north_wall.y, north_east_pulse.x < east_wall.x)
            north_west_pulse.offset(-1, 1)

        #print("Returning north west")
        return north_west_pulse

    def lidar_south_east_pulse(self):
        """
        The lidar beam that travels south east within the game.
        :return: a point of where the beam either hit a wall or a part of the snake.
        """
        pulse_x, pulse_y = self.snake.head.pos()
        south_east_pulse = Point(pulse_x, pulse_y)
        south_wall = Point(pulse_x, (-1) * (self.screen_height / 2))
        east_wall = Point(self.screen_width / 2, pulse_y)

        while (south_east_pulse.y > south_wall.y and south_east_pulse.x < east_wall.x and not self.snake.point_is_in_tail(south_east_pulse)[0]):
            south_east_pulse.offset(1, -1)

        #print("Returning south east")
        return south_east_pulse

    def lidar_south_west_pulse(self):
        """
        The lidar beam that travels south west within the game.
        :return: a point of where the beam either hit a wall or a part of the snake.
        """
        pulse_x, pulse_y = self.snake.head.pos()
        south_west_pulse = Point(pulse_x, pulse_y)
        south_wall = Point(pulse_x, (-1) * (self.screen_height / 2))
        west_wall = Point((-1) * (self.screen_width / 2), pulse_y)

        while (south_west_pulse.y > south_wall.y and south_west_pulse.x > west_wall.x and not self.snake.point_is_in_tail(south_west_pulse)[0]):
            south_west_pulse.offset(-1, -1)

        #print("Returning south west")
        return south_west_pulse

    def get_episode_statistic(self):
        """
        Gets statistics about the current episode.
        :return:
        """
        return (self.points, self.n_moves, self.snake.get_tail_length())

    def __get_food_distance_reward(self, previous_location: Point, current_location: Point):
        """

        :param previous_location: A type point that specifies previous location of the snake
        :param current_location: A type point that specifies the current location of the snake
        :return: 1 if the snake moved towards the food, 0 if the snake moved away from the food
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

    def draw_lidar(self):
        for end_point in self.lidar_end_points:
            t = turtle.Turtle()
            t.penup()
            t.goto(self.snake.head.xcor(), self.snake.head.ycor())
            t.pendown()
            t.goto(end_point.x, end_point.y)


