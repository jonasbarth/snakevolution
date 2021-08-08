from environment.env import Direction
from game.snake import PyGameSnakeGame, SnakeGame
from rl.mpd import MDP, MDPAction
import numpy as np

from rl.state import SnakeState1, SnakeState3


class SnakeMDP(MDP):

    def __init__(self):
        super().__init__()
        self.environment = PyGameSnakeGame(screen_width=400, screen_height=400, snake_size=20)
        self.state_representation = SnakeState3(self.environment)

    def reset(self) -> (np.array, float, bool):
        self.environment.start()
        self._reward_sum = 0
        self._n_steps = 0
        return self.state_representation.get_state(), 0, False

    def step(self, action: int) -> (np.array, float, bool):
        snake_action = list(Direction)[action]
        reward = 0

        _, ate_food, is_game_over = self.environment.move(snake_action)

        if ate_food:
            reward = 10

        if is_game_over:
            reward = -10

        self._reward_sum += reward
        self._n_steps += 1

        return self.state_representation.get_state(), reward, is_game_over

    def state_dims(self) -> (int, int):
        return self.state_representation.dims()



class SnakeAction(MDPAction):

    def __init__(self, action: int):
        super().__init__(action)

    def get_action(self):
        return list(Direction)[self.action]
