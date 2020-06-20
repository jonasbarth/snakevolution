## Class for a food item in the environment

import turtle

class Food:

    def __init__(self, x, y, colour="red"):
         """
        Constructor for the Food.

        Parameters:
            colour - a string for the colour of the Food. Default value is Red.
            x - an integer for the x position of the Food
            y - an integer for the y position of the Food
        """
        self.head = turtle.Turtle()
        self.head.speed(0)
        self.head.shape("circle")
        self.head.color(colour)
        self.head.penup()
        self.head.goto(x, y)
        self.head.direction = "stop"

