# The game environment for Snake game


import turtle
import random
from snake import Snake
from food import Food


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

        self.snake.move(direction)
       
        self.wn.update()

        if self.__touch_food():
            self.points += 1
            self.__generate_food()

    

    def __generate_food(self):
        x_start = (-1) * self.screen_width / 2
        x_end = self.screen_width / 2
        x_rand = random.randrange(x_start, x_end)

        y_start = (-1) * self.screen_height / 2
        y_end = self.screen_height / 2
        y_rand = random.randrange(y_start, y_end)

        self.current_food = Food(x_rand, y_rand)


    def __touch_food(self):
        if self.snake.food_distance(self.current_food) < 20:
            return True
        return False

