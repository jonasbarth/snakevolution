from environment.env import Env
from game.snake import SnakeGame


def maximise_moves(env: SnakeGame) -> float:
    return env.n_steps()


def maximise_food_eaten(env: Env) -> float:
    return env.total_points()





