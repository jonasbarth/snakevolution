# The game environment for Snake game


import turtle
import random
from snake import Snake
from food import Food
import numpy as np


class SnakeEnv:

    def __init__(self, screen_width, screen_height):
        self.wn = turtle.Screen() 
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.current_food = None
        self.snake = Snake()
        self.actions = {0: "up", 1: "right", 2: "down", 3: "left"}
        self.points = 0
        
        

    def reset(self):
        self.wn.title("Snake Game")
        self.wn.bgcolor("white")
        self.wn.setup(width=self.screen_width, height=self.screen_height)
        self.__generate_food()
        #self.wn.tracer(0)

      
    def step(self, action):
        
        direction = self.actions[action]

        reward = 0
        done = False
        state = np.zeros(6, dtype=np.float32)

        ## Move the snake in the desired direction and check whether it touches food
        self.snake.move(direction)

        print(self.__touch_wall())

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
        return False

