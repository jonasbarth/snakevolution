from environment.env import Env


def maximise_moves(env: Env) -> float:
    return env.total_steps()


def maximise_food_eaten(env: Env) -> float:
    return env.total_points()





