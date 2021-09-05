import numpy as np
import torch as T

from rl.deep_q_network import DeepQNetwork
from rl.ffnn import FFNN
from rl.mpd import MDP


class GeneticAgent(object):
    fitness = 0
    rewards = 0
    eps_moves = 0
    food_eaten = 0
    time_alive = 0
    generation_fitness = []

    def __init__(self, mdp: MDP, learning_rate: float, input_dims, n_actions: int, mutation_rate: float):
        self.mdp = mdp
        self.neural_network = DeepQNetwork(learning_rate, input_dims, 256,
                                           128, n_actions)
        self.neural_network = FFNN([(input_dims[0], 128), (128, 3)])
        self.mutation_rate = mutation_rate
        self.n_weights = len(self.get_genome())

    def get_genome(self):
        """
        Gets the genome of this agent as a list of layers of the agent's neural network.
        :return: a list of flattened tensors where each tensor is a layer of the network, starting with the input layer,
        then hidden layers, and ending with the output layer
        """
        return [layer.weight.data.flatten() for layer in self.neural_network.layers()]

    def set_genome(self, genome):
        layer_sizes = self.neural_network.layer_sizes()
        reshaped_genome = []
        for gene, size in zip(genome, layer_sizes):
            reshaped_genome.append(gene.reshape(size))

        self.neural_network.set_layer_data(reshaped_genome)

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
        self.fitness = fitness(self.mdp)
        self.generation_fitness.append(self.fitness)

    def simulate(self):
        state, reward, done = self.mdp.reset()

        while not done:
            action = self.choose_action(state)
            state_, reward, done = self.mdp.step(action=action)
            self.time_alive += 1
            state = state_

        self.food_eaten = self.mdp.env_score()
        return self

    def reset(self):
        self.fitness = 0
        self.rewards = 0
        self.eps_moves = 0
        self.food_eaten = 0
        self.time_alive = 0
        self.mdp.reset()
