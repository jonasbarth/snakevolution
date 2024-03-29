import numpy as np
import torch as T
import torch.nn as nn
from pysnakegym.game import SnakeGameSequencePlayer, GameSequence
from pysnakegym.mdp import MDP


class GeneticAgent(object):
    fitness = 0
    rewards = 0
    eps_moves = 0
    food_eaten = 0
    time_alive = 0
    generation_fitness = []
    game_sequences = []

    def __init__(self, mdp: MDP, neural_network: nn.Module, mutation_rate: float):
        self.mdp = mdp
        self.neural_network = neural_network
        self.mutation_rate = mutation_rate
        self.n_weights = len(self.get_genome())

    def get_genome(self):
        """
        Gets the genome of this agent as a list of layers of the agent's neural network.
        :return: a list of flattened tensors where each tensor is a layer of the network, starting with the input layer,
        then hidden layers, and ending with the output layer
        """
        return [layer.weight.data.flatten() for layer in self.neural_network.layers()].copy()

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
        self.game_sequences = []
        self.game_sequences.append(self.mdp.environment.get_sequence())

        while not done:
            action = self.choose_action(state)
            state_, reward, done = self.mdp.step(action=action)
            self.game_sequences.append(self.mdp.environment.get_sequence())
            self.time_alive += 1
            state = state_

        self.food_eaten = self.mdp.env_score()
        return self

    def replay(self):
        player = SnakeGameSequencePlayer(20)
        for sequence in self.game_sequences:
            player.add(sequence)

        player.play()

    def get_replay(self) -> [GameSequence]:
        return self.game_sequences

    def reset(self):
        self.fitness = 0
        self.rewards = 0
        self.eps_moves = 0
        self.food_eaten = 0
        self.time_alive = 0
        self.mdp.reset()
