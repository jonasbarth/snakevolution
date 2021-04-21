from environment.env import Env


def maximise_moves(env: Env) -> float:
    return env.total_steps()


fitness_func_mapping = dict()
fitness_func_mapping["MAXIMISE_MOVES"] = maximise_moves
