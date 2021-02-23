from agents.deep_q_agent import DeepQAgent
from agents.genetic_agent import GeneticAgent
from agents.human_agent import HumanAgent
from environment.env import SnakeEnv
from random import randint
from agents.random_agent import RandomAgent
import numpy as np
from torch.utils.tensorboard import SummaryWriter
from environment.state import LidarAndOneHot, LidarAndOneHot2
import torch


def initialise_population(pop_size):
    population = []
    for n in range(pop_size):
        population.append(GeneticAgent(learning_rate=0.0001, input_dims=[24], n_actions=4, mutation_rate=0.01))

    return population

def simulate(population):
    for solution in population:
        env = SnakeEnv(400, 400, LidarAndOneHot2)
        solution.simulate(env)

    return population

writer = SummaryWriter()

env = SnakeEnv(400, 400, LidarAndOneHot2)


action_space = np.array([0,1,2,3])
n_games = 1000
score = 0
global_step = 0
eps_dec = 1 / (n_games * 0.8)

n_generations = 100
pop_size = 100
population = initialise_population(pop_size)

for generation in range(n_generations):
    population = simulate(population)
    population = calculate_fitness(population)
    selection = select_candidates(population)




