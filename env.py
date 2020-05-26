# The game environment for Snake game


import turtle
import time
from snake import Snake


class SnakeEnv:

    def __init__(self, screen_width, screen_height):
        self.wn = turtle.Screen() 
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        

    def reset(self):
        self.wn.title("Snake Game")
        self.wn.bgcolor("white")
        self.wn.setup(width=self.screen_width, height=self.screen_height)
        #self.wn.tracer(0)

      


    def step(self, action):
        snake = Snake()
        snake.set_direction("up")

        while True:
            self.wn.update()
            time.sleep(0.1)
            #print(snake.head.direction)
            snake.up()

        self.wn.mainloop()