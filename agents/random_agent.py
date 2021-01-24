from agents.agent import Agent
from random import randint

class RandomAgent(Agent):

    def get_action(self, state):
        index = randint(0, len(self.action_space) - 1)
        return self.action_space[index]