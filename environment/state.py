# Class for different state representations
import numpy as np

from environment.point import Point


class State:

    def __init__(self, snakeEnv):
        self.snakeEnv = snakeEnv

    def get_state(self):
        pass

    def get_dims(self):
        return 24 + 4 + 4 + 1


class LidarAndOneHot2(State):

    def __init__(self, snakeEnv):
        super(LidarAndOneHot, self).__init__(snakeEnv)


    def get_dims(self):
        return 15 + 4 + 4 + 1


    def get_state(self):
        """
        Gets the current state of the the MDP.
        :return: A numpy array of dimension (1, 6) where the first 5 entries are the lidar and the final entry is the distance to the food
        """
        lidar = self.__get_lidar(self.snakeEnv.snake.head.direction)
        head_direction = np.array(self.snakeEnv.snake.get_current_one_hot_direction())
        tail_direction = np.array(self.snakeEnv.snake.get_tail_one_hot_direction())
        food_dist = np.array([self.snakeEnv.food_distance()])
        state = np.concatenate((lidar, head_direction, tail_direction, food_dist))
        return state

    def __up_lidar(self):
        """
        Gets the Snake's 5 point lidar distances when it is facing up.

        Parameters:
            None

        Returns:
            lidar - A 1D numpy array with 5 entries, one for each lidar distance.
        """
        lidar_pulses = [self.lidar_west_pulse(), self.lidar_north_west_pulse(), self.lidar_north_pulse(), self.lidar_north_east_pulse(), self.lidar_east_pulse()]

        lidar = np.zeros((len(lidar_pulses) * 3), dtype=np.float32)
        snake_x, snake_y = self.snakeEnv.snake.head.pos()[0], self.snakeEnv.snake.head.pos()[1]
        snake_pos = Point(snake_x, snake_y)


        for i in range(len(lidar_pulses)):
            lidar_pulse = lidar_pulses[i]

            index = i * 3
            lidar[index] = snake_pos.distance(lidar_pulse[0])
            lidar[index+1] = lidar_pulse[1]
            lidar[index+2] = lidar_pulse[2]


        self.lidar_end_points = [lidar_pulses[0][0], lidar_pulses[1][0], lidar_pulses[2][0], lidar_pulses[3][0], lidar_pulses[4][0]]

        return lidar


    def __right_lidar(self):
        """
        Gets the Snake's 5 point lidar distances when it is facing right.

        Parameters:
            None

        Returns:
            lidar - A 1D numpy array with 5 entries, one for each lidar distance.
        """
        lidar_pulses = [self.lidar_north_pulse(), self.lidar_north_east_pulse(), self.lidar_east_pulse(), self.lidar_south_east_pulse(), self.lidar_south_pulse()]
        lidar = np.zeros((len(lidar_pulses) * 3), dtype=np.float32)
        snake_x, snake_y = self.snakeEnv.snake.head.pos()[0], self.snakeEnv.snake.head.pos()[1]
        snake_pos = Point(snake_x, snake_y)


        for i in range(len(lidar_pulses)):
            lidar_pulse = lidar_pulses[i]

            index = i * 3
            lidar[index] = snake_pos.distance(lidar_pulse[0])
            lidar[index+1] = lidar_pulse[1]
            lidar[index+2] = lidar_pulse[2]

        self.lidar_end_points = [lidar_pulses[0][0], lidar_pulses[1][0], lidar_pulses[2][0], lidar_pulses[3][0], lidar_pulses[4][0]]

        return lidar


    def __down_lidar(self):
        """
        Gets the Snake's 5 point lidar distances when it is facing down.

        Parameters:
            None

        Returns:
            lidar - A 1D numpy array with 5 entries, one for each lidar distance.
        """
        lidar_pulses = [self.lidar_east_pulse(), self.lidar_south_east_pulse(), self.lidar_south_pulse(), self.lidar_south_west_pulse(), self.lidar_west_pulse()]
        lidar = np.zeros((len(lidar_pulses)*3), dtype=np.float32)
        snake_x, snake_y = self.snakeEnv.snake.head.pos()[0], self.snakeEnv.snake.head.pos()[1]
        snake_pos = Point(snake_x, snake_y)

        for i in range(len(lidar_pulses)):
            lidar_pulse = lidar_pulses[i]

            index = i * 3
            lidar[index] = snake_pos.distance(lidar_pulse[0])
            lidar[index+1] = lidar_pulse[1]
            lidar[index+2] = lidar_pulse[2]

        self.lidar_end_points = [lidar_pulses[0][0], lidar_pulses[1][0], lidar_pulses[2][0], lidar_pulses[3][0], lidar_pulses[4][0]]

        return lidar


    def __left_lidar(self):
        """
        Gets the Snake's 5 point lidar distances when it is facing left.

        Parameters:
            None

        Returns:
            lidar - A 1D numpy array with 5 entries, one for each lidar distance.
        """
        lidar_pulses = [self.lidar_south_pulse(), self.lidar_south_west_pulse(), self.lidar_west_pulse(), self.lidar_north_west_pulse(), self.lidar_north_pulse()]
        lidar = np.zeros((len(lidar_pulses)*3), dtype=np.float32)
        snake_x, snake_y = self.snakeEnv.snake.head.pos()[0], self.snakeEnv.snake.head.pos()[1]
        snake_pos = Point(snake_x, snake_y)

        for i in range(len(lidar_pulses)):
            lidar_pulse = lidar_pulses[i]
            index = i * 3
            lidar[index] = snake_pos.distance(lidar_pulse[0])
            lidar[index+1] = lidar_pulse[1]
            lidar[index+2] = lidar_pulse[2]

        self.lidar_end_points = [lidar_pulses[0][0], lidar_pulses[1][0], lidar_pulses[2][0], lidar_pulses[3][0], lidar_pulses[4][0]]

        return lidar

    def __stop_lidar(self):
        """
        Gets the snakes 8 point lidar in it's starting position.
        :return:
        """
        lidar_pulses = [self.lidar_north_pulse(), self.lidar_north_east_pulse(), self.lidar_east_pulse(), self.lidar_south_east_pulse(), self.lidar_south_pulse(), self.lidar_south_west_pulse(), self.lidar_west_pulse(), self.lidar_north_west_pulse()]
        lidar = np.zeros((len(lidar_pulses)*3), dtype=np.float32)
        snake_x, snake_y = self.snakeEnv.snake.head.pos()[0], self.snakeEnv.snake.head.pos()[1]
        snake_pos = Point(snake_x, snake_y)

        for i in range(len(lidar_pulses)):
            lidar_pulse = lidar_pulses[i]
            index = i * 3
            lidar[index] = snake_pos.distance(lidar_pulse[0])
            lidar[index+1] = lidar_pulse[1]
            lidar[index+2] = lidar_pulse[2]

        self.lidar_end_points = [lidar_pulse[0] for lidar_pulse in lidar_pulses]

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

        elif direction == "stop":
            return self.__stop_lidar()




    def lidar_east_pulse(self):
        """
        The lidar beam that travels east within the game.
        :return: a point of where the beam either hit a wall or a part of the environment.
        """
        pulse_x, pulse_y = self.snakeEnv.snake.head.pos()
        east_pulse = Point(pulse_x, pulse_y)
        east_wall = Point(self.snakeEnv.screen_width / 2, pulse_y)

        hit_obstacle = False
        hit_apple = False

        while True:

            if east_pulse.x >= east_wall.x:
                hit_obstacle = True
                break

            if self.snakeEnv.snake.point_is_in_tail(east_pulse)[0]:
                hit_obstacle = True
                break

            if self.snakeEnv.current_food.point_is_in_food(east_pulse)[0]:
                hit_apple = True
                break

            east_pulse.offset(1, 0)

        return (east_pulse, hit_obstacle, hit_apple)
        """
        while (east_pulse.x < east_wall.x and not self.snakeEnv.snake.point_is_in_tail(east_pulse)[0]):
           # print(self.snakeEnvironment.point_is_in_tail(east_pulse))
            east_pulse.offset(+1, 0)

        #print("Returning east")
        return east_pulse"""


    def lidar_south_pulse(self):
        """
        The lidar beam that travels south within the game.
        :return: a point of where the beam either hit a wall or a part of the environment.
        """
        pulse_x, pulse_y = self.snakeEnv.snake.head.pos()
        south_pulse = Point(pulse_x, pulse_y)
        south_wall = Point(pulse_x, (-1) * (self.snakeEnv.screen_height / 2))

        hit_obstacle = False
        hit_apple = False

        while True:

            if south_pulse.y <= south_wall.y:
                hit_obstacle = True
                break

            if self.snakeEnv.snake.point_is_in_tail(south_pulse)[0]:
                hit_obstacle = True
                break

            if self.snakeEnv.current_food.point_is_in_food(south_pulse)[0]:
                hit_apple = True
                break

            south_pulse.offset(0, -1)

        return (south_pulse, hit_obstacle, hit_apple)
        """
        while (south_pulse.y > south_wall.y and not self.snakeEnv.snake.point_is_in_tail(south_pulse)[0]):
            #print(self.snakeEnvironment.point_is_in_tail(south_pulse))
            south_pulse.offset(0, -1)

        #print("Returning south")
        return south_pulse"""

    def lidar_west_pulse(self):
        """
        The lidar beam that travels west within the game.
        :return: a point of where the beam either hit a wall or a part of the environment.
        """
        pulse_x, pulse_y = self.snakeEnv.snake.head.pos()
        west_pulse = Point(pulse_x, pulse_y)
        west_wall = Point((-1) * (self.snakeEnv.screen_width / 2), pulse_y)

        hit_obstacle = False
        hit_apple = False

        while True:

            if west_pulse.x <= west_wall.x:
                hit_obstacle = True
                break

            if self.snakeEnv.snake.point_is_in_tail(west_pulse)[0]:
                hit_obstacle = True
                break

            if self.snakeEnv.current_food.point_is_in_food(west_pulse)[0]:
                hit_apple = True
                break

            west_pulse.offset(-1, 0)

        return (west_pulse, hit_obstacle, hit_apple)
        """
        while (west_pulse.x > west_wall.x and not self.snakeEnv.snake.point_is_in_tail(west_pulse)[0]):
            #print("West pulse", self.snakeEnvironment.point_is_in_tail(west_pulse))
            west_pulse.offset(-1, 0)

        #print("Returning west")
        return west_pulse"""

    def lidar_north_pulse(self):
        """
        The lidar beam that travels north within the game.
        :return: a point of where the beam either hit a wall or a part of the environment.
        """
        pulse_x, pulse_y = self.snakeEnv.snake.head.pos()
        north_pulse = Point(pulse_x, pulse_y)
        north_wall = Point(pulse_x, self.snakeEnv.screen_height / 2)

        hit_obstacle = False
        hit_apple = False

        while True:

            if north_pulse.y >= north_wall.y:
                hit_obstacle = True
                break

            if self.snakeEnv.snake.point_is_in_tail(north_pulse)[0]:
                hit_obstacle = True
                break

            if self.snakeEnv.current_food.point_is_in_food(north_pulse)[0]:
                hit_apple = True
                break

            north_pulse.offset(0, 1)


        return (north_pulse, hit_obstacle, hit_apple)

    """
        while (north_pulse.y < north_wall.y and not self.snakeEnv.snake.point_is_in_tail(north_pulse)[0]):
            #print(self.snakeEnvironment.point_is_in_tail(north_pulse))
            north_pulse.offset(0, 1)
       #print("Returning north")
        return north_pulse"""

    def lidar_north_east_pulse(self):
        """
        The lidar beam that travels north east within the game.
        :return: a point of where the beam either hit a wall or a part of the environment.
        """
        pulse_x, pulse_y = self.snakeEnv.snake.head.pos()
        north_east_pulse = Point(pulse_x, pulse_y)
        north_wall = Point(pulse_x, self.snakeEnv.screen_height / 2)
        east_wall = Point(self.snakeEnv.screen_width / 2, pulse_y)

        hit_obstacle = False
        hit_apple = False

        while True:

            if north_east_pulse.y >= north_wall.y or north_east_pulse.x >= east_wall.x:
                hit_obstacle = True
                break

            if self.snakeEnv.snake.point_is_in_tail(north_east_pulse)[0]:
                hit_obstacle = True
                break

            if self.snakeEnv.current_food.point_is_in_food(north_east_pulse)[0]:
                hit_apple = True
                break

            north_east_pulse.offset(1, 1)

        return (north_east_pulse, hit_obstacle, hit_apple)

    """
        while (north_east_pulse.y < north_wall.y and north_east_pulse.x < east_wall.x and not self.snakeEnv.snake.point_is_in_tail(north_east_pulse)[0]):
            #print("Is in tail", self.snakeEnvironment.point_is_in_tail(north_east_pulse))
            #print("Bool", north_east_pulse.y < north_wall.y, north_east_pulse.x < east_wall.x)
            north_east_pulse.offset(1, 1)

       # print("Returning north east")
        return north_east_pulse"""

    def lidar_north_west_pulse(self):
        """
        The lidar beam that travels north west within the game.
        :return: a point of where the beam either hit a wall or a part of the environment.
        """
        pulse_x, pulse_y = self.snakeEnv.snake.head.pos()
        north_west_pulse = Point(pulse_x, pulse_y)
        north_wall = Point(pulse_x, self.snakeEnv.screen_height / 2)
        west_wall = Point(((-1) * self.snakeEnv.screen_width) / 2, pulse_y)

        hit_obstacle = False
        hit_apple = False

        while True:

            if north_west_pulse.y >= north_wall.y or north_west_pulse.x <= west_wall.x:
                hit_obstacle = True
                break

            if self.snakeEnv.snake.point_is_in_tail(north_west_pulse)[0]:
                hit_obstacle = True
                break

            if self.snakeEnv.current_food.point_is_in_food(north_west_pulse)[0]:
                hit_apple = True
                break

            north_west_pulse.offset(-1, 1)

        return (north_west_pulse, hit_obstacle, hit_apple)
        """
        while (north_west_pulse.y < north_wall.y and north_west_pulse.x > west_wall.x and not self.snakeEnv.snake.point_is_in_tail(north_west_pulse)[0]):
            #print("Is in tail", self.snakeEnvironment.point_is_in_tail(north_east_pulse))
            #print("Bool", north_east_pulse.y < north_wall.y, north_east_pulse.x < east_wall.x)
            north_west_pulse.offset(-1, 1)

        #print("Returning north west")
        return north_west_pulse"""

    def lidar_south_east_pulse(self):
        """
        The lidar beam that travels south east within the game.
        :return: a point of where the beam either hit a wall or a part of the environment.
        """
        pulse_x, pulse_y = self.snakeEnv.snake.head.pos()
        south_east_pulse = Point(pulse_x, pulse_y)
        south_wall = Point(pulse_x, (-1) * (self.snakeEnv.screen_height / 2))
        east_wall = Point(self.snakeEnv.screen_width / 2, pulse_y)

        hit_obstacle = False
        hit_apple = False

        while True:

            if south_east_pulse.y <= south_wall.y or south_east_pulse.x >= east_wall.x:
                hit_obstacle = True
                break

            if self.snakeEnv.snake.point_is_in_tail(south_east_pulse)[0]:
                hit_obstacle = True
                break

            if self.snakeEnv.current_food.point_is_in_food(south_east_pulse)[0]:
                hit_apple = True
                break

            south_east_pulse.offset(1, -1)

        return (south_east_pulse, hit_obstacle, hit_apple)

        """
        while (south_east_pulse.y > south_wall.y and south_east_pulse.x < east_wall.x and not self.snakeEnv.snake.point_is_in_tail(south_east_pulse)[0]):
            south_east_pulse.offset(1, -1)

        #print("Returning south east")
        return south_east_pulse"""

    def lidar_south_west_pulse(self):
        """
        The lidar beam that travels south west within the game.
        :return: a point of where the beam either hit a wall or a part of the environment.
        """
        pulse_x, pulse_y = self.snakeEnv.snake.head.pos()
        south_west_pulse = Point(pulse_x, pulse_y)
        south_wall = Point(pulse_x, (-1) * (self.snakeEnv.screen_height / 2))
        west_wall = Point((-1) * (self.snakeEnv.screen_width / 2), pulse_y)

        hit_obstacle = False
        hit_apple = False

        while True:

            if south_west_pulse.y <= south_wall.y or south_west_pulse.x <= west_wall.x:
                hit_obstacle = True
                break

            if self.snakeEnv.snake.point_is_in_tail(south_west_pulse)[0]:
                hit_obstacle = True
                break

            if self.snakeEnv.current_food.point_is_in_food(south_west_pulse)[0]:
                hit_apple = True
                break

            south_west_pulse.offset(-1, -1)

        return (south_west_pulse, hit_obstacle, hit_apple)
        """
        while (south_west_pulse.y > south_wall.y and south_west_pulse.x > west_wall.x and not self.snakeEnv.snake.point_is_in_tail(south_west_pulse)[0]):
            south_west_pulse.offset(-1, -1)

        #print("Returning south west")
        return south_west_pulse"""



class LidarAndOneHot(State):

    def __init__(self, snakeEnv):
        super(LidarAndOneHot, self).__init__(snakeEnv)

    def get_state(self):
        """
        Gets the current state of the the MDP.
        :return: A numpy array of dimension (1, 6) where the first 5 entries are the lidar and the final entry is the distance to the food
        """
        lidar = self.__get_lidar(self.snakeEnv.snake.head.direction)
        head_direction = np.array(self.snakeEnv.snake.get_current_one_hot_direction())
        tail_direction = np.array(self.snakeEnv.snake.get_tail_one_hot_direction())
        food_dist = np.array([self.snakeEnv.food_distance()])
        state = np.concatenate((lidar, head_direction, tail_direction, food_dist))
        return state

    def __up_lidar(self):
        """
        Gets the Snake's 5 point lidar distances when it is facing up.

        Parameters:
            None

        Returns:
            lidar - A 1D numpy array with 5 entries, one for each lidar distance.
        """
        lidar_pulses = [self.lidar_north_pulse(), self.lidar_north_east_pulse(), self.lidar_east_pulse(),
                        None, None, None,
                        self.lidar_west_pulse(), self.lidar_north_west_pulse()]

        lidar = np.zeros((len(lidar_pulses) * 3), dtype=np.float32)
        snake_x, snake_y = self.snakeEnv.snake.head.pos()[0], self.snakeEnv.snake.head.pos()[1]
        snake_pos = Point(snake_x, snake_y)


        for i in range(len(lidar_pulses)):
            lidar_pulse = lidar_pulses[i]
            if (lidar_pulse):
                index = i * 3
                lidar[index] = snake_pos.distance(lidar_pulse[0])
                lidar[index+1] = lidar_pulse[1]
                lidar[index+2] = lidar_pulse[2]


        self.lidar_end_points = [lidar_pulses[0][0], lidar_pulses[1][0], lidar_pulses[2][0],None, None, None, lidar_pulses[6][0], lidar_pulses[7][0]]

        return lidar


    def __right_lidar(self):
        """
        Gets the Snake's 5 point lidar distances when it is facing right.

        Parameters:
            None

        Returns:
            lidar - A 1D numpy array with 5 entries, one for each lidar distance.
        """
        lidar_pulses = [self.lidar_north_pulse(), self.lidar_north_east_pulse(), self.lidar_east_pulse(), self.lidar_south_east_pulse(), self.lidar_south_pulse(), None, None, None]
        lidar = np.zeros((len(lidar_pulses) * 3), dtype=np.float32)
        snake_x, snake_y = self.snakeEnv.snake.head.pos()[0], self.snakeEnv.snake.head.pos()[1]
        snake_pos = Point(snake_x, snake_y)


        for i in range(len(lidar_pulses)):
            lidar_pulse = lidar_pulses[i]
            if (lidar_pulse):
                index = i * 3
                lidar[index] = snake_pos.distance(lidar_pulse[0])
                lidar[index+1] = lidar_pulse[1]
                lidar[index+2] = lidar_pulse[2]

        self.lidar_end_points = [lidar_pulses[0][0], lidar_pulses[1][0], lidar_pulses[2][0], lidar_pulses[3][0], lidar_pulses[4][0], None, None, None]


        return lidar


    def __down_lidar(self):
        """
        Gets the Snake's 5 point lidar distances when it is facing down.

        Parameters:
            None

        Returns:
            lidar - A 1D numpy array with 5 entries, one for each lidar distance.
        """
        lidar_pulses = [None, None, self.lidar_east_pulse(), self.lidar_south_east_pulse(), self.lidar_south_pulse(), self.lidar_south_west_pulse(), self.lidar_west_pulse(), None]
        lidar = np.zeros((len(lidar_pulses)*3), dtype=np.float32)
        snake_x, snake_y = self.snakeEnv.snake.head.pos()[0], self.snakeEnv.snake.head.pos()[1]
        snake_pos = Point(snake_x, snake_y)

        for i in range(len(lidar_pulses)):
            lidar_pulse = lidar_pulses[i]
            if (lidar_pulse):
                index = i * 3
                lidar[index] = snake_pos.distance(lidar_pulse[0])
                lidar[index+1] = lidar_pulse[1]
                lidar[index+2] = lidar_pulse[2]

        self.lidar_end_points = [None, None, lidar_pulses[2][0], lidar_pulses[3][0], lidar_pulses[4][0], lidar_pulses[5][0], lidar_pulses[6][0], None]

        return lidar


    def __left_lidar(self):
        """
        Gets the Snake's 5 point lidar distances when it is facing left.

        Parameters:
            None

        Returns:
            lidar - A 1D numpy array with 5 entries, one for each lidar distance.
        """
        lidar_pulses = [self.lidar_north_pulse(), None, None, None, self.lidar_south_pulse(), self.lidar_south_west_pulse(), self.lidar_west_pulse(), self.lidar_north_west_pulse()]
        lidar = np.zeros((len(lidar_pulses)*3), dtype=np.float32)
        snake_x, snake_y = self.snakeEnv.snake.head.pos()[0], self.snakeEnv.snake.head.pos()[1]
        snake_pos = Point(snake_x, snake_y)

        for i in range(len(lidar_pulses)):
            lidar_pulse = lidar_pulses[i]
            if (lidar_pulse):
                index = i * 3
                lidar[index] = snake_pos.distance(lidar_pulse[0])
                lidar[index+1] = lidar_pulse[1]
                lidar[index+2] = lidar_pulse[2]

        self.lidar_end_points = [lidar_pulses[0][0], None, None, None, lidar_pulses[4][0], lidar_pulses[5][0], lidar_pulses[6][0], lidar_pulses[7][0]]


        return lidar

    def __stop_lidar(self):
        """
        Gets the snakes 8 point lidar in it's starting position.
        :return:
        """
        lidar_pulses = [self.lidar_north_pulse(), self.lidar_north_east_pulse(), self.lidar_east_pulse(), self.lidar_south_east_pulse(), self.lidar_south_pulse(), self.lidar_south_west_pulse(), self.lidar_west_pulse(), self.lidar_north_west_pulse()]
        lidar = np.zeros((len(lidar_pulses)*3), dtype=np.float32)
        snake_x, snake_y = self.snakeEnv.snake.head.pos()[0], self.snakeEnv.snake.head.pos()[1]
        snake_pos = Point(snake_x, snake_y)

        for i in range(len(lidar_pulses)):
            lidar_pulse = lidar_pulses[i]
            index = i * 3
            lidar[index] = snake_pos.distance(lidar_pulse[0])
            lidar[index+1] = lidar_pulse[1]
            lidar[index+2] = lidar_pulse[2]

        self.lidar_end_points = [lidar_pulse[0] for lidar_pulse in lidar_pulses]

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

        elif direction == "stop":
            return self.__stop_lidar()




    def lidar_east_pulse(self):
        """
        The lidar beam that travels east within the game.
        :return: a point of where the beam either hit a wall or a part of the environment.
        """
        pulse_x, pulse_y = self.snakeEnv.snake.head.pos()
        east_pulse = Point(pulse_x, pulse_y)
        east_wall = Point(self.snakeEnv.screen_width / 2, pulse_y)

        hit_obstacle = False
        hit_apple = False

        while True:

            if east_pulse.x >= east_wall.x:
                hit_obstacle = True
                break

            if self.snakeEnv.snake.point_is_in_tail(east_pulse)[0]:
                hit_obstacle = True
                break

            if self.snakeEnv.current_food.point_is_in_food(east_pulse)[0]:
                hit_apple = True
                break

            east_pulse.offset(1, 0)

        return (east_pulse, hit_obstacle, hit_apple)
        """
        while (east_pulse.x < east_wall.x and not self.snakeEnv.snake.point_is_in_tail(east_pulse)[0]):
           # print(self.snakeEnvironment.point_is_in_tail(east_pulse))
            east_pulse.offset(+1, 0)

        #print("Returning east")
        return east_pulse"""


    def lidar_south_pulse(self):
        """
        The lidar beam that travels south within the game.
        :return: a point of where the beam either hit a wall or a part of the environment.
        """
        pulse_x, pulse_y = self.snakeEnv.snake.head.pos()
        south_pulse = Point(pulse_x, pulse_y)
        south_wall = Point(pulse_x, (-1) * (self.snakeEnv.screen_height / 2))

        hit_obstacle = False
        hit_apple = False

        while True:

            if south_pulse.y <= south_wall.y:
                hit_obstacle = True
                break

            if self.snakeEnv.snake.point_is_in_tail(south_pulse)[0]:
                hit_obstacle = True
                break

            if self.snakeEnv.current_food.point_is_in_food(south_pulse)[0]:
                hit_apple = True
                break

            south_pulse.offset(0, -1)

        return (south_pulse, hit_obstacle, hit_apple)
        """
        while (south_pulse.y > south_wall.y and not self.snakeEnv.snake.point_is_in_tail(south_pulse)[0]):
            #print(self.snakeEnvironment.point_is_in_tail(south_pulse))
            south_pulse.offset(0, -1)

        #print("Returning south")
        return south_pulse"""

    def lidar_west_pulse(self):
        """
        The lidar beam that travels west within the game.
        :return: a point of where the beam either hit a wall or a part of the environment.
        """
        pulse_x, pulse_y = self.snakeEnv.snake.head.pos()
        west_pulse = Point(pulse_x, pulse_y)
        west_wall = Point((-1) * (self.snakeEnv.screen_width / 2), pulse_y)

        hit_obstacle = False
        hit_apple = False

        while True:

            if west_pulse.x <= west_wall.x:
                hit_obstacle = True
                break

            if self.snakeEnv.snake.point_is_in_tail(west_pulse)[0]:
                hit_obstacle = True
                break

            if self.snakeEnv.current_food.point_is_in_food(west_pulse)[0]:
                hit_apple = True
                break

            west_pulse.offset(-1, 0)

        return (west_pulse, hit_obstacle, hit_apple)
        """
        while (west_pulse.x > west_wall.x and not self.snakeEnv.snake.point_is_in_tail(west_pulse)[0]):
            #print("West pulse", self.snakeEnvironment.point_is_in_tail(west_pulse))
            west_pulse.offset(-1, 0)

        #print("Returning west")
        return west_pulse"""

    def lidar_north_pulse(self):
        """
        The lidar beam that travels north within the game.
        :return: a point of where the beam either hit a wall or a part of the environment.
        """
        pulse_x, pulse_y = self.snakeEnv.snake.head.pos()
        north_pulse = Point(pulse_x, pulse_y)
        north_wall = Point(pulse_x, self.snakeEnv.screen_height / 2)

        hit_obstacle = False
        hit_apple = False

        while True:

            if north_pulse.y >= north_wall.y:
                hit_obstacle = True
                break

            if self.snakeEnv.snake.point_is_in_tail(north_pulse)[0]:
                hit_obstacle = True
                break

            if self.snakeEnv.current_food.point_is_in_food(north_pulse)[0]:
                hit_apple = True
                break

            north_pulse.offset(0, 1)


        return (north_pulse, hit_obstacle, hit_apple)

    """
        while (north_pulse.y < north_wall.y and not self.snakeEnv.snake.point_is_in_tail(north_pulse)[0]):
            #print(self.snakeEnvironment.point_is_in_tail(north_pulse))
            north_pulse.offset(0, 1)
       #print("Returning north")
        return north_pulse"""

    def lidar_north_east_pulse(self):
        """
        The lidar beam that travels north east within the game.
        :return: a point of where the beam either hit a wall or a part of the environment.
        """
        pulse_x, pulse_y = self.snakeEnv.snake.head.pos()
        north_east_pulse = Point(pulse_x, pulse_y)
        north_wall = Point(pulse_x, self.snakeEnv.screen_height / 2)
        east_wall = Point(self.snakeEnv.screen_width / 2, pulse_y)

        hit_obstacle = False
        hit_apple = False

        while True:

            if north_east_pulse.y >= north_wall.y or north_east_pulse.x >= east_wall.x:
                hit_obstacle = True
                break

            if self.snakeEnv.snake.point_is_in_tail(north_east_pulse)[0]:
                hit_obstacle = True
                break

            if self.snakeEnv.current_food.point_is_in_food(north_east_pulse)[0]:
                hit_apple = True
                break

            north_east_pulse.offset(1, 1)

        return (north_east_pulse, hit_obstacle, hit_apple)

    """
        while (north_east_pulse.y < north_wall.y and north_east_pulse.x < east_wall.x and not self.snakeEnv.snake.point_is_in_tail(north_east_pulse)[0]):
            #print("Is in tail", self.snakeEnvironment.point_is_in_tail(north_east_pulse))
            #print("Bool", north_east_pulse.y < north_wall.y, north_east_pulse.x < east_wall.x)
            north_east_pulse.offset(1, 1)

       # print("Returning north east")
        return north_east_pulse"""

    def lidar_north_west_pulse(self):
        """
        The lidar beam that travels north west within the game.
        :return: a point of where the beam either hit a wall or a part of the environment.
        """
        pulse_x, pulse_y = self.snakeEnv.snake.head.pos()
        north_west_pulse = Point(pulse_x, pulse_y)
        north_wall = Point(pulse_x, self.snakeEnv.screen_height / 2)
        west_wall = Point(((-1) * self.snakeEnv.screen_width) / 2, pulse_y)

        hit_obstacle = False
        hit_apple = False

        while True:

            if north_west_pulse.y >= north_wall.y or north_west_pulse.x <= west_wall.x:
                hit_obstacle = True
                break

            if self.snakeEnv.snake.point_is_in_tail(north_west_pulse)[0]:
                hit_obstacle = True
                break

            if self.snakeEnv.current_food.point_is_in_food(north_west_pulse)[0]:
                hit_apple = True
                break

            north_west_pulse.offset(-1, 1)

        return (north_west_pulse, hit_obstacle, hit_apple)
        """
        while (north_west_pulse.y < north_wall.y and north_west_pulse.x > west_wall.x and not self.snakeEnv.snake.point_is_in_tail(north_west_pulse)[0]):
            #print("Is in tail", self.snakeEnvironment.point_is_in_tail(north_east_pulse))
            #print("Bool", north_east_pulse.y < north_wall.y, north_east_pulse.x < east_wall.x)
            north_west_pulse.offset(-1, 1)

        #print("Returning north west")
        return north_west_pulse"""

    def lidar_south_east_pulse(self):
        """
        The lidar beam that travels south east within the game.
        :return: a point of where the beam either hit a wall or a part of the environment.
        """
        pulse_x, pulse_y = self.snakeEnv.snake.head.pos()
        south_east_pulse = Point(pulse_x, pulse_y)
        south_wall = Point(pulse_x, (-1) * (self.snakeEnv.screen_height / 2))
        east_wall = Point(self.snakeEnv.screen_width / 2, pulse_y)

        hit_obstacle = False
        hit_apple = False

        while True:

            if south_east_pulse.y <= south_wall.y or south_east_pulse.x >= east_wall.x:
                hit_obstacle = True
                break

            if self.snakeEnv.snake.point_is_in_tail(south_east_pulse)[0]:
                hit_obstacle = True
                break

            if self.snakeEnv.current_food.point_is_in_food(south_east_pulse)[0]:
                hit_apple = True
                break

            south_east_pulse.offset(1, -1)

        return (south_east_pulse, hit_obstacle, hit_apple)

        """
        while (south_east_pulse.y > south_wall.y and south_east_pulse.x < east_wall.x and not self.snakeEnv.snake.point_is_in_tail(south_east_pulse)[0]):
            south_east_pulse.offset(1, -1)

        #print("Returning south east")
        return south_east_pulse"""

    def lidar_south_west_pulse(self):
        """
        The lidar beam that travels south west within the game.
        :return: a point of where the beam either hit a wall or a part of the environment.
        """
        pulse_x, pulse_y = self.snakeEnv.snake.head.pos()
        south_west_pulse = Point(pulse_x, pulse_y)
        south_wall = Point(pulse_x, (-1) * (self.snakeEnv.screen_height / 2))
        west_wall = Point((-1) * (self.snakeEnv.screen_width / 2), pulse_y)

        hit_obstacle = False
        hit_apple = False

        while True:

            if south_west_pulse.y <= south_wall.y or south_west_pulse.x <= west_wall.x:
                hit_obstacle = True
                break

            if self.snakeEnv.snake.point_is_in_tail(south_west_pulse)[0]:
                hit_obstacle = True
                break

            if self.snakeEnv.current_food.point_is_in_food(south_west_pulse)[0]:
                hit_apple = True
                break

            south_west_pulse.offset(-1, -1)

        return (south_west_pulse, hit_obstacle, hit_apple)
        """
        while (south_west_pulse.y > south_wall.y and south_west_pulse.x > west_wall.x and not self.snakeEnv.snake.point_is_in_tail(south_west_pulse)[0]):
            south_west_pulse.offset(-1, -1)

        #print("Returning south west")
        return south_west_pulse"""