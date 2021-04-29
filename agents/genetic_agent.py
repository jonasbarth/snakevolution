import torch as T

from environment.env import SnakeEnv, Env
from rl.deep_q_network import DeepQNetwork
import math


class GeneticAgent(object):
    fitness = 0
    rewards = 0
    eps_moves = 0
    food_eaten = 0
    time_alive = 0

    def __init__(self, env: Env, learning_rate: float, input_dims, n_actions: int, mutation_rate: float):
        self.env = env
        self.neural_network = DeepQNetwork(learning_rate, input_dims, math.floor(input_dims[0] / 2),
                                           math.floor(input_dims[0] / 2), n_actions)
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

    def _calc_genome_index(self, size):
        w, h = size
        return w * h

    def choose_action(self, observation):
        state = T.tensor([observation]).to(self.neural_network.device)
        actions = self.neural_network.forward(state.float())
        action = T.argmax(actions).item()
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
        self.fitness = fitness(self.env)
        print("Food eaten: %d - Time alive: %d - Fitness: %d" % (self.food_eaten, self.time_alive, self.fitness))

    def simulate(self):
        state, reward, done = self.env.reset()

        while not done:
            action = self.choose_action(state)
            state_, reward, done = self.env.step(action)
            self.time_alive += 1
            state = state_

        self.food_eaten += self.env.total_points()

    def reset(self):
        self.fitness = 0
        self.rewards = 0
        self.eps_moves = 0
        self.food_eaten = 0
        self.time_alive = 0
