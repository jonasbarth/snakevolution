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
        self.wn.title("Snake Game")
        self.wn.bgcolor("white")
        self.wn.setup(width=self.screen_width, height=self.screen_height)
        self.__generate_food()
        

      
    def step(self, action):
        
        direction = self.actions[action]

        reward = 0
        done = False
        state = np.zeros(6, dtype=np.float32)
        ## Move the snake in the desired direction and check whether it touches food
        self.snake.move(direction)

        if self.__touch_wall() or self.__touch_snake():
            reward = -1
            done = True
       
        elif self.__touch_food():
            self.points += 1
            reward = 1
            self.snake.add_tail()
            self.__generate_food()

        self.wn.update()

        return (state, reward, done)

    

    def __generate_food(self):
        x_start = (-1) * self.screen_width / 2
        x_end = self.screen_width / 2
        x_rand = random.randrange(x_start, x_end)

        y_start = (-1) * self.screen_height / 2
        y_end = self.screen_height / 2
        y_rand = random.randrange(y_start, y_end)

        self.current_food = Food(x_rand, y_rand)


    def __touch_food(self):
        if self.snake.food_distance(self.current_food) < 20.0:
            return True
        return False

    
    def __touch_wall(self):
        x, y = self.snake.head.xcor(), self.snake.head.ycor()

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

        head_x = self.snake.head.xcor()
        head_y = self.snake.head.ycor()

        for tail in self.snake.tail[1:]:
            tail_x = tail.head.xcor()
            tail_y = tail.head.ycor()

            if distance.euclidean(np.array([head_x, head_y]), np.array([tail_x, tail_y])) < 20:
                return True


        return False

    
    def __wall_dist_up(self):
        snake_x, snake_y, = self.snake.head.pos()

        wall_x = snake_x
        wall_y = self.screen_height / 2
            
        return distance.cityblock(np.array([snake_x, snake_y]), np.array([wall_x, wall_y]))


    def __wall_dist_down(self):
        snake_x, snake_y, = self.snake.head.pos()
        wall_x = snake_x
        wall_y = (-1) * self.screen_height / 2

        return distance.cityblock(np.array([snake_x, snake_y]), np.array([wall_x, wall_y]))

    def __wall_dist_left(self):
        snake_x, snake_y, = self.snake.head.pos()
        wall_y = snake_y
        wall_x = (-1) * self.screen_width / 2

        return distance.cityblock(np.array([snake_x, snake_y]), np.array([wall_x, wall_y]))

    def __wall_dist_right(self):
        snake_x, snake_y, = self.snake.head.pos()
        wall_y = snake_y
        wall_x = self.screen_width / 2

        return distance.cityblock(np.array([snake_x, snake_y]), np.array([wall_x, wall_y]))

    def __wall_dist_up_right(self):
        snake_x, snake_y = self.snake.head.pos()
        adjacent_x = snake_x
        adjacent_y = self.screen_height / 2

        # Length of the opposite side of the triangle
        adjacent = distance.euclidean(np.array([snake_x, snake_y]), np.array([adjacent_x, adjacent_y]))
        opposite = adjacent

        opposite_x = adjacent_x + opposite
        opposite_y = self.screen_height / 2

        return distance.cityblock(np.array([snake_x, snake_y]), np.array([opposite_x, opposite_y]))


    def __wall_dist_down_right(self):
        snake_x, snake_y = self.snake.head.pos()
        adjacent_x = snake_x
        adjacent_y = (-1) * self.screen_height / 2

        # Length of the opposite side of the triangle
        adjacent = distance.euclidean(np.array([snake_x, snake_y]), np.array([adjacent_x, adjacent_y]))
        opposite = adjacent

        opposite_x = adjacent_x + opposite
        opposite_y = (-1) * self.screen_height / 2

        return distance.cityblock(np.array([snake_x, snake_y]), np.array([opposite_x, opposite_y]))
        

    def __wall_dist_up_left(self):
        snake_x, snake_y = self.snake.head.pos()
        adjacent_x = snake_x
        adjacent_y = self.screen_height / 2

        # Length of the opposite side of the triangle
        adjacent = distance.euclidean(np.array([snake_x, snake_y]), np.array([adjacent_x, adjacent_y]))
        opposite = adjacent

        opposite_x = adjacent_x - opposite
        opposite_y = self.screen_height / 2

        return distance.cityblock(np.array([snake_x, snake_y]), np.array([opposite_x, opposite_y]))
        

    def __wall_dist_down_left(self):
        snake_x, snake_y = self.snake.head.pos()
        adjacent_x = snake_x
        adjacent_y = (-1) * self.screen_height / 2

        # Length of the opposite side of the triangle
        adjacent = distance.euclidean(np.array([snake_x, snake_y]), np.array([adjacent_x, adjacent_y]))
        opposite = adjacent

        opposite_x = adjacent_x - opposite
        opposite_y = (-1) * self.screen_height / 2

        return distance.cityblock(np.array([snake_x, snake_y]), np.array([opposite_x, opposite_y]))

    
    def __up_lidar(self):
        lidar = np.zeros((5))

        lidar[0] = self.__wall_dist_up()
        lidar[1] = self.__wall_dist_left()
        lidar[2] = self.__wall_dist_right()
        lidar[3] = self.__wall_dist_up_left()
        lidar[4] = self.__wall_dist_up_right()

        return lidar


    def __right_lidar(self):
        lidar = np.zeros((5))

        lidar[0] = self.__wall_dist_up()
        lidar[1] = self.__wall_dist_down()
        lidar[2] = self.__wall_dist_right()
        lidar[3] = self.__wall_dist_up_right()
        lidar[4] = self.__wall_dist_down_right()

        return lidar


    def __down_lidar(self):
        lidar = np.zeros((5))

        lidar[0] = self.__wall_dist_left()
        lidar[1] = self.__wall_dist_down()
        lidar[2] = self.__wall_dist_right()
        lidar[3] = self.__wall_dist_down_left()
        lidar[4] = self.__wall_dist_down_right()

        return lidar

    def __left_lidar(self):
        lidar = np.zeros((5))

        lidar[0] = self.__wall_dist_left()
        lidar[1] = self.__wall_dist_down()
        lidar[2] = self.__wall_dist_up()
        lidar[3] = self.__wall_dist_down_left()
        lidar[4] = self.__wall_dist_up_left()

        return lidar


    def __get_lidar(self, direction):
        lidar = np.zeros((5))

        if direction == "up":
            return self.__up_lidar()

        elif direction == "right":
            return self.__right_lidar()

        elif direction == "down":
            return self.__down_lidar()

        elif direction == "left":
            return self.__left_lidar()


    def print_lidar(self):
        print(self.__wall_dist_up(),self.__wall_dist_down(), self.__wall_dist_left(), self.__wall_dist_right())
        print(self.__wall_dist_up_right(), self.__wall_dist_up_left(), self.__wall_dist_down_right(), self.__wall_dist_down_left())

