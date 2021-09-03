import math

import torch as T
import numpy as np
from rl.deep_q_network import DeepQNetwork
from rl.mpd import MDP
from rl.simple_deep_q_network import Linear_QNet


class GeneticAgent(object):
    fitness = 0
    rewards = 0
    eps_moves = 0
    food_eaten = 0
    time_alive = 0

    def __init__(self, mdp: MDP, learning_rate: float, input_dims, n_actions: int, mutation_rate: float):
        self.mdp = mdp
        self.neural_network = DeepQNetwork(learning_rate, input_dims, 256,
                                           128, n_actions)

        #self.neural_network = Linear_QNet(11, 256, 3)
        self.mutation_rate = mutation_rate
        self.n_weights = len(self.get_genome())

    def get_genome(self):
        fc1_weights = self.neural_network.fc1.weight.data.flatten()  # gets a 2D array of the data (16, 33)
        fc2_weights = self.neural_network.fc2.weight.data.flatten()
        fc3_weights = self.neural_network.fc3.weight.data.flatten()

        return [fc1_weights, fc2_weights, fc3_weights]

    def set_genome(self, genome):
        fc1_size = self.neural_network.fc1.weight.data.size()
        fc1 = genome[0].reshape(fc1_size)

        fc2_size = self.neural_network.fc2.weight.data.size()
        fc2 = genome[1].reshape(fc2_size)

        fc3_size = self.neural_network.fc3.weight.data.size()
        fc3 = genome[2].reshape(fc3_size)

        self.neural_network.fc1.weight.data = fc1
        self.neural_network.fc2.weight.data = fc2
        self.neural_network.fc3.weight.data = fc3

    def set_model(self, state_dict):
        self.neural_network.load_state_dict(state_dict)

    def _calc_genome_index(self, size):
        w, h = size
        return w * h

    def choose_action(self, observation):
        action = np.array([0, 0, 0])
        state = T.tensor([observation]).to(self.neural_network.device)
        actions = self.neural_network.forward(state.float())
        action[T.argmax(actions).item()] = 1
        return action

    def mutate(self):
        pass

    def calculate_fitness(self, fitness):
        """
        Calculates the fitness based on the length of the snake and the number of moves per episode
        :param fitness: a function that calculates the fitness of this snake
        :return:
        """
        # self.fitness = ((self.food_eaten*2)**2) * (self.time_alive**1.5)
        # self.fitness = self.time_alive
        self.fitness = fitness(self.mdp)
        #print("Food eaten: %d - Time alive: %d - Fitness: %d" % (self.food_eaten, self.time_alive, self.fitness))

    def simulate(self):
        state, reward, done = self.mdp.reset()

        while not done:
            action = self.choose_action(state)
            state_, reward, done = self.mdp.step(action=action)
            self.time_alive += 1
            state = state_

        self.food_eaten += self.mdp.env_score()
        return self

    def reset(self):
        self.fitness = 0
        self.rewards = 0
        self.eps_moves = 0
        self.food_eaten = 0
        self.time_alive = 0
        self.mdp.reset()
