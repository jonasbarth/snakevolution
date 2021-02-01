# Class for the Snake 

import turtle
import scipy.spatial.distance as distance
import numpy as np

from snake.point import Point


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
        self.legal_direction = {"up": self.__get_legal_directions_x, "right": self.__get_legal_directions_y, "down": self.__get_legal_directions_x, "left": self.__get_legal_directions_y}
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
            self.head.sety(y + 20)

            ## Move all tail sections to the coordinates of the section that is in front of them
            for section in self.tail[1:]:
                old_x = section.head.xcor()
                old_y = section.head.ycor()
                section.head.sety(y)
                section.head.setx(x)
                x = old_x
                y = old_y



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


    def point_is_in_tail(self, point):
        """
        Checks whether the provided point is somewhere in the tail of the snake.
        :param point: an object of type Point
        :return: a triples (False, (0, 0)) if the point does not exist in the tail. A triples (True, (cx, cy)) where
        cx and cy are the coordinates of the point.
        """
        for section in self.tail[1:]:
            cx, cy = section.head.pos()
            x_1 = cx - 10
            y_1 = cy - 10
            x_2 = cx + 10
            y_2 = cy + 10

            if (x_1 < point.x < x_2) and (y_1 < point.y < y_2):
                return (True, (cx, cy))

            return (False, (0, 0))

        return (False, (0, 0))


    def reset(self):
        """
        Resets the snake to the starting position (0, 0), sets the direction to stop and remove all the tail elements.
        :return:
        """
        # remove all the tail drawings
        for section in self.tail[1:]:
            section.reset()

        self.tail = [self]
        self.head.goto(0, 0)
        self.head.direction = "stop"


    def __direction_is_legal(self, direction):
        """
        Checks whether the direction is legal. A snake can not move in the opposite direction on the same axis but needs
        to move on a different axis. E.g. if the snake is moving left, it cannot move right but needs to move either
        up or down.
        :param direction: a string that specifies the direction to be checked.
        :return: False if the direction is not permitted. True if the direction is permitted.
        """
        try:
            return direction in self.legal_direction[self.head.direction]

        except KeyError:
            return False

    def __get_legal_directions_x(self):
        """
        Gets a list of legal directions that the snake can move to when its current direction is on the x axis.
        :return: a list of strings with legal directions.
        """
        return ["up", 'down']

    def __get_legal_directions_y(self):
        """
        Gets a list of legal directions that the snake can move to when its current direction is on the y axis.
        :return: a list of strings with legal directions.
        """
        return ["left", "right"]

    def __get_legal_directions_stop(self):
        """
        Gets a list of legal directions that the snake can move to when its current direction is stop.
        :return: a list of strings with legal directions.
        """
        return self.__get_legal_directions_x() + self.__get_legal_directions_y()

    def get_tail_length(self):
        return len(self.tail)

    def get_current_location(self):
        return Point(self.head.xcor(), self.head.ycor())
        

    
 