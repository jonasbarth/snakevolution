## Class for a food item in the environment
import turtle

class Food:

    def __init__(self, x, y, colour="green"):
        """
        Constructor for the Food.

        Parameters:
            colour - a string for the colour of the Food. Default value is Red.
            x - an integer for the x position of the Food
            y - an integer for the y position of the Food
        """
        self.head = turtle.Turtle()
        self.head.speed(0)
        self.head.shape("square")
        self.head.color(colour)
        self.head.penup()
        self.head.goto(x, y)
        self.head.direction = "stop"


    def point_is_in_food(self, point):
        cx, cy = self.head.pos()
        x_1 = cx - 10
        y_1 = cy - 10
        x_2 = cx + 10
        y_2 = cy + 10

        if (x_1 < point.x < x_2) and (y_1 < point.y < y_2):
            return (True, (cx, cy))

        return (False, (0, 0))

