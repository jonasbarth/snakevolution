# The game environment for Snake game


import turtle


class SnakeEnv:

    def __init__(self, screen_width, screen_height):
        self.wn = turtle.Screen()
        self.wn.title("Snake Game")
        self.wn.bgcolor("white")
        self.wn.setup(width=screen_width, height=screen_height)
        self.wn.tracer(0)
        self.screen_width = screen_width
        self.screen_height = screen_height
        print("Hello")
        


    def reset(self):
        print(self.wn)
        self.wn.mainloop()