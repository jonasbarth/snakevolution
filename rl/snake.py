import numpy as np

from environment.env import Direction
from pysnakegame.game.snake import SnakeGame
from pysnakegame.game.snake import PyGameSnakeGame
from rl.mpd import MDP, MDPAction
from rl.state import SnakeState3


class SnakeMDP(MDP):

    def __init__(self, show_game: bool):
        super().__init__()
        if show_game:
            self.environment = PyGameSnakeGame(screen_width=400, screen_height=400, snake_size=20)
        else:
            self.environment = SnakeGame(screen_width=200, screen_height=200, snake_size=20)
        self.state_representation = SnakeState3(self.environment)

    def reset(self) -> (np.array, float, bool):
        self.environment.start()
        self._reward_sum = 0
        self._n_steps = 0
        self._score = 0
        return self.state_representation.get_state(), 0, False

    def step(self, action: np.array) -> (np.array, float, bool):

        _, ate_food, is_game_over = self.environment.move(action)
        reward = 0

        if ate_food:
            self._score += 1
            reward = 10

        if is_game_over:
            reward = -10

        self._reward_sum += reward
        self._n_steps += 1

        return self.state_representation.get_state(), reward, is_game_over

    def state_dims(self) -> (int, int):
        return self.state_representation.dims()

    def n_actions(self):
        return 3




class SnakeAction(MDPAction):

    def __init__(self, action: int):
        super().__init__(action)

    def get_action(self):
        return list(Direction)[self.action]
