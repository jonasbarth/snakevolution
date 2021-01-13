# Class for the Snake 

import turtle
import scipy.spatial.distance as distance
import numpy as np

class Snake:

    def __init__(self, colour="black", x=0, y=0):
        """
        Constructor for the Snake.

        Parameters:
            colour - a string for the colour of the head of the Snake. Default value is Black.
            x - an integer for the x position of the Snake
            y - an integer for the y position of the Snake
        """
        self.head = turtle.Turtle()
        self.head.speed(0)
        self.head.shape("square")
        self.head.color(colour)
        self.head.penup()
        self.head.goto(x,y)
        self.head.direction = "stop"
        self.moves = {"up": self.__up, "right": self.__right, "down": self.__down, "left": self.__left}
        self.tail = [self]


    def __set_direction(self, direction):
        """ 
        Sets the direction that the Snake head is facing.

        Parameters:
            direction - A string specifying the direction the head needs to be facing. Must be in ["stop", "up", "down", "left", "right"]

        Returns:
            None
        """

        ## ensure that the direction is legal
        if direction in ["stop", "up", "down", "left", "right"]:
            self.head.direction = direction



    def move(self, direction):
        """
        Moves the Snake in the given direction.

        Parameters:
            direction - A string specifying the direction the head needs to be facing. Must be in ["stop", "up", "down", "left", "right"]

        Returns:
            None
        """
        self.__set_direction(direction)

        self.moves[direction]()


    def __down(self):
        """
        Move the Snake downwards if the head is facing down.

        Parameters:
            None

        Returns:
            None
        """

        if self.head.direction == "down":

            ## Move the head
            y = self.head.ycor()
            x = self.head.xcor()
            self.head.sety(y - 20)


            ## Move all tail sections to the coordinates of the section that is in front of them
            for section in self.tail[1:]:
                old_x = section.head.xcor()
                old_y = section.head.ycor()
                section.head.sety(y)
                section.head.setx(x)
                x = old_x
                y = old_y

        
    def __up(self):
        """
        Move the Snake upwards if the head is facing up.

        Parameters:
            None

        Returns:
            None
        """

        if self.head.direction == "up":
            
            ## Move the head
            y = self.head.ycor()
            x = self.head.xcor()
            print("Currently at", x,y)
            self.head.sety(y + 20)

            print("Moving up to", x, self.head.ycor())
            ## Move all tail sections to the coordinates of the section that is in front of them
            for section in self.tail[1:]:
                old_x = section.head.xcor()
                old_y = section.head.ycor()
                section.head.sety(y)
                section.head.setx(x)
                x = old_x
                y = old_y

            print(self.tail[0].head.ycor())


    def __left(self):
        """
        Move the Snake left if the head is facing left.

        Parameters:
            None

        Returns:
            None
        """
        if self.head.direction == "left":
            ## Move the head
            y = self.head.ycor()
            x = self.head.xcor()
            self.head.setx(x - 20)

            for section in self.tail[1:]:
                ## Move all tail sections to the coordinates of the section that is in front of them
                old_x = section.head.xcor()
                old_y = section.head.ycor()
                section.head.sety(y)
                section.head.setx(x)
                x = old_x
                y = old_y

    def __right(self):
        """
        Move the Snake right if the head is facing right.

        Parameters:
            None

        Returns:
            None
        """
        if self.head.direction == "right":
            ## Move the head
            y = self.head.ycor()
            x = self.head.xcor()
            self.head.setx(x + 20)

            for section in self.tail[1:]:
                ## Move all tail sections to the coordinates of the section that is in front of them
                old_x = section.head.xcor()
                old_y = section.head.ycor()
                section.head.sety(y)
                section.head.setx(x)
                x = old_x
                y = old_y


    def food_distance(self, food, metric=distance.cityblock):
        """
        Measures the distance between the food and the snake head with the given distance metric.

        Parameters:
            food - An instance of the Food class
            metric - A distance function taking two 1D numpy arrays as input

        Returns:
            float - The distance between the food and the snake head
        """
       
        snake_cor = np.array([self.head.pos()[0], self.head.pos()[1]], dtype=np.float32)
        food_cor = np.array([food.head.pos()[0], food.head.pos()[1]], dtype=np.float32)
       
        return metric(snake_cor, food_cor)

    def tail_distance(self):

        head_cor = np.array([self.head.xcor(), self.head.ycor()], dtype=np.float32)
        

    def add_tail(self):
        """
        Adds a section to the tail of the snake.

        Parameters:
            None

        Returns:
            None
        """ 
        x = self.tail[-1].head.pos()[0] 
        y = self.tail[-1].head.pos()[1]
        new_part = Snake(colour="gray", x=x, y=y)
        self.tail.append(new_part)

    def tail_pos(self):
        tail_xy = []

        for t in zip(self.tail[1:]):
            tail_xy.append(t.pos())


    def point_is_in_tail(self, point):
        for section in self.tail[1:]:
            cx, cy = section.head.pos()
            x_1 = cx - 10
            y_1 = cy - 10
            x_2 = cx + 10
            y_2 = cy + 10

            print(cx, cy, x_1, y_1, x_2, y_2, point.x, point.y)

            if (x_1 < point.x < x_2) and (y_1 < point.y < y_2):
                print(point.x, point.y, "are in the tail");
                return (True, (cx, cy))

            print(point.x, point.y, "are not in the tail");
            return (False, (cx, cy))


    def reset(self):
        # remove all the tail drawings
        for section in self.tail[1:]:
            section.clear()

        self.tail = [self]
        self.head.goto(0, 0)
        self.head.direction = "stop"


    
        

    
 