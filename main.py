from env import SnakeEnv
import time
from human_agent import HumanAgent
import scipy.spatial.distance as distance
import numpy as np
import turtle
import math


env = SnakeEnv(600, 600)
env.reset()
env.step(1)

wall_x = 0
wall_y = 600 / 2

snake_x, snake_y = 0, 0
opposite_x = snake_x
opposite_y = 600 / 2

opposite = distance.euclidean(np.array([snake_x, snake_y]), np.array([opposite_x, opposite_y]))

adjacent = opposite * math.tan(45)
adjacent = 600 / 2

hypotenuse = math.sqrt(opposite**2 + adjacent**2)


t = turtle.Turtle()
t.color("red")
t.goto(wall_x, wall_y)
t.goto(wall_x + adjacent, wall_y)
t.goto(wall_x - adjacent, wall_y)
t.goto(wall_x - adjacent, (-1) * wall_y)
t.goto(wall_x + adjacent, (-1) * wall_y)


env.wn.mainloop()
