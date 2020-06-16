## Class for a food item in the environment

import turtle

class Food:

    def __init__(self, x, y, colour="red"):
        self.head = turtle.Turtle()
        self.head.speed(0)
        self.head.shape("circle")
        self.head.color(colour)
        self.head.penup()
        self.head.goto(x, y)
        self.head.direction = "stop"

