from environment.env import Env
from game.snake import SnakeGame
from rl.mpd import MDP


def maximise_moves(env: SnakeGame) -> float:
    return env.n_steps()


def maximise_food_eaten(env: MDP) -> float:
    return env.env_score()

def maximise_reward(env: MDP) -> float:
    return env.reward_sum()




