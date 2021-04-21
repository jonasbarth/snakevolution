from environment.env import Env


def maximise_moves(env: Env) -> float:
    return env.total_steps()


def maximise_food_eaten(env: Env) -> float:
    return env.total_points()


fitness_func_mapping = dict()
fitness_func_mapping["MAXIMISE_MOVES"] = maximise_moves
fitness_func_mapping["MAXIMISE_FOOD_EATEN"] = maximise_food_eaten
