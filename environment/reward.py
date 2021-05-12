# class for different rewards

from environment.env import SnakeEnv
from environment.point import Point


def zero_reward(env: SnakeEnv):
    return 0

def minus_one_reward(env: SnakeEnv):
    return -1

def one_towards_apple_zero_away_from_apple_reward(env: SnakeEnv):
    # get current environment location
    return 0

def distance_to_apple_percentage(env: SnakeEnv):
    def normalise(x):
        return 1 - (x / env.max_distance)

    food_x = env.current_food.head.xcor()
    food_y = env.current_food.head.ycor()
    food_point = Point(food_x, food_y)
    current_location = Point(env.snake.head.xcor(), env.snake.head.ycor())
    #multiplier = len(env.environment.tail) if len(env.environment.tail) > 2 else 1
    return normalise(current_location.distance(food_point))


def distance_to_apple_percentage_tail_length_multiplier(env: SnakeEnv):
    def normalise(x):
        return 1 - (x / env.max_distance)

    food_x = env.current_food.head.xcor()
    food_y = env.current_food.head.ycor()
    food_point = Point(food_x, food_y)
    current_location = Point(env.snake.head.xcor(), env.snake.head.ycor())
    multiplier = len(env.snake.segments) if len(env.snake.segments) > 2 else 1
    return normalise(current_location.distance(food_point)) * multiplier

