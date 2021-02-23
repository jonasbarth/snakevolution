import torch as T
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from environment.env import SnakeEnv
from rl.deep_q_network import DeepQNetwork
import math


class GeneticAgent(object):

    def __init__(self, learning_rate, input_dims, n_actions, mutation_rate):
        self.neural_network = DeepQNetwork(learning_rate, input_dims, math.floor(input_dims[0]/2), math.floor(input_dims[0]/2), n_actions)
        self.mutation_rate = mutation_rate
        self.rewards = 0
        self.eps_moves = 0
        self.food_eaten = 0


    def get_genome(self):
        fc1_weights = self.neural_network.fc1.weight.data.flatten() #gets a 2D array of the data (16, 33)
        fc2_weights = self.neural_network.fc2.weight.data.flatten()
        fc3_weights = self.neural_network.fc3.weight.data.flatten()

        return T.concat([fc1_weights, fc2_weights, fc3_weights])

    def choose_action(self, observation):
        state = T.tensor([observation]).to(self.neural_network.device)
        actions = self.neural_network.forward(state.float())
        action = T.argmax(actions).item()
        return action


    def mutate(self):
        pass

    def fitness(self, fitness):
        """
        Calculates the fitness based on the length of the snake and the number of moves per episode
        :param fitness: a function that calculates the fitness of this snake
        :return:
        """
        pass

    def simulate(self, env):
        state, reward, done = env.reset()

        while not done:
            action = self.choose_action(state)
            state_, reward, done = env.step(action)
            self.food_eaten += env.points



