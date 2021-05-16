import numpy as np

class MDPAction(object):

    def __init__(self, action: int):
        self.action = action

    def get_action(self):
        pass


class MDP(object):

    def __init__(self):
        self.environment = None
        self._reward_sum = 0
        self._n_steps = 0

    def reset(self) -> (np.array, float, bool):
        pass

    def step(self, action: int) -> (np.array, float, bool):
        pass

    def reward_sum(self) -> float:
        return self._reward_sum

    def n_steps(self) -> int:
        return self._n_steps

    def env_score(self) -> float:
        return self.environment.score()

    def state_dims(self) -> (int, int):
        pass

