import numpy as np

class MDPAction(object):

    def get_action(self):
        pass


class MDP(object):

    def __init__(self):
        self.environment = None
        self._reward_sum = 0
        self._n_steps = 0

    def reset(self) -> (np.array, float, bool):
        pass

    def step(self, action: MDPAction) -> (np.array, float, bool):
        pass

    def reward_sum(self):
        return self._reward_sum

    def n_steps(self):
        return self._n_steps

