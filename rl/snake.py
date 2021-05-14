from game.snake import PyGameSnakeGame
from rl.mpd import MDP, MDPAction
import numpy as np

from rl.state import SnakeState1


class SnakeMDP(MDP):

    def __init__(self):
        super().__init__()
        self.environment = PyGameSnakeGame(screen_width=400, screen_height=400, snake_size=20)
        self.state_representation = SnakeState1(self.environment)

    def reset(self) -> (np.array, float, bool):
        self.environment.start()
        return self.state_representation.get_state(), 0, False

    def step(self, action: MDPAction) -> (np.array, float, bool):
        snake_action = action
        reward = 0

        _, ate_food, is_game_over = self.environment.move(snake_action)

        if ate_food:
            reward = 10

        if is_game_over:
            reward = -10

        self._reward_sum += reward
        self._n_steps += 1

        return self.state_representation.get_state(), reward, is_game_over
