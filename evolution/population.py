import copy
import random

import numpy as np
import torch as T
from pysnakegym.game.core import Direction
from pysnakegym.mdp import SnakeMDP
from pysnakegym.model import FFNN
from tqdm import tqdm, trange

from agents import GeneticAgent
from evolution.selection import Selection
from util.io.export import GeneticPopulationData


class Population:

    def __init__(self, pop_size: int, hidden_layers, mutation_rate: float, crossover_rate: float, elitism: float,
                 fitness_func, selection: Selection, show_game: bool, screen_width: int, screen_height: int,
                 snake_size: int):
        self.pop_size = pop_size
        self.hidden_layers = hidden_layers
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism = elitism
        self.fitness_func = fitness_func
        self.selection = selection
        self.individuals = []
        self.best_individual = None
        self.population_data = None
        self.selected_individuals = []
        self.elites = []
        self.show_game = show_game
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.snake_size = snake_size
        pass

    def initialise_population(self):
        pass

    def simulate(self):
        pass

    def calculate_fitness(self):
        pass

    def candidate_selection(self):
        pass

    def crossover(self):
        pass

    def mutate(self):
        pass

    def replace(self):
        pass

    def mutate_children(self):
        pass

    def reset(self):
        pass

    def is_finished(self):
        pass


class SnakePopulation(Population):

    def __init__(self, pop_size, hidden_layers, mutation_rate, crossover_rate, elitism, fitness_func, selection,
                 show_game, screen_width, screen_height, snake_size):
        Population.__init__(self,
                            pop_size=pop_size,
                            hidden_layers=hidden_layers,
                            mutation_rate=mutation_rate,
                            elitism=elitism,
                            crossover_rate=crossover_rate,
                            fitness_func=fitness_func,
                            selection=selection,
                            show_game=show_game,
                            screen_width=screen_width,
                            screen_height=screen_height,
                            snake_size=snake_size)
        self.population_data = GeneticPopulationData()

    def initialise_population(self):
        self.selected_individuals = []
        self.children_genomes = []

        for _ in trange(self.pop_size, desc='Initialising population'):
            mdp = SnakeMDP(screen_width=self.screen_width, screen_height=self.screen_height, snake_size=self.snake_size,
                           show_game=self.show_game)
            layers = self.hidden_layers.copy()
            layers.insert(0, mdp.state_dims()[0])
            layers.append(Direction.n_actions())
            neural_network = FFNN(layers)
            self.individuals.append(
                GeneticAgent(mdp=mdp, neural_network=neural_network, mutation_rate=self.mutation_rate))

        self.best_individual = copy.deepcopy(self.individuals[0])

    def simulate(self):
        for solution in tqdm(self.individuals, desc='Simulating'):
            solution.simulate()


    def calculate_fitness(self):
        for solution in tqdm(self.individuals, desc='Calculating fitness'):
            solution.calculate_fitness(self.fitness_func)

            # keeping track of the best performing individual across all generations
            if solution.fitness > self.best_individual.fitness:
                self.best_individual = copy.deepcopy(solution)

        print(f'best fitness: {self.best_individual.fitness}')

        self.individuals = sorted(self.individuals, key=lambda solution: solution.fitness)
        self.population_data.add_generational_fitness(np.array([[solution.fitness for solution in self.individuals]]))

    def candidate_selection(self):
        # self.elitism of len of self.individuals
        elite_index = len(self.individuals) - int(self.elitism * len(self.individuals))
        elites = self.individuals[elite_index:]
        for elite in tqdm(elites, desc='Copying elites into the next generation'):
            self.elites.append(elite.get_genome())

        print(f'Elite fitness:{[individual.fitness for individual in self.individuals[elite_index:]]}')
        print(f'Selecting {elite_index} individuals from the population')
        selected = self.selection.select(self.individuals, len(self.individuals[:elite_index]))
        self.selected_individuals.extend(selected)

    def crossover(self, n_crossover_points=1):
        """

        :param n_crossover_points:
        :return:
        """

        middle = int(len(self.selected_individuals) / 2)

        for parent_1, parent_2 in zip(self.selected_individuals[:middle], self.selected_individuals[middle:]):
            if random.random() <= self.crossover_rate:
                # get genomes
                parent_1_genomes = parent_1.get_genome()
                parent_2_genomes = parent_2.get_genome()

                child_1_genomes = []
                child_2_genomes = []

                for parent_1_genome, parent_2_genome in zip(parent_1_genomes, parent_2_genomes):
                    child_1_genome, child_2_genome = self._make_children(parent_1_genome, parent_2_genome,
                                                                         n_crossover_points)

                    child_1_genomes.append(child_1_genome)
                    child_2_genomes.append(child_2_genome)

                self.children_genomes.append(child_1_genomes)
                self.children_genomes.append(child_2_genomes)

    def _make_children(self, parent_1_genome, parent_2_genome, n_crossover_points: int):
        crossover_indexes = self._get_crossover_indeces(n_crossover_points, parent_1_genome)
        crossover_indexes.append(len(parent_1_genome))  # append final index of list so that we can get the final slice

        # prepare the child genomes
        child_1_genome = T.tensor([])
        child_2_genome = T.tensor([])

        start_index = 0
        for i in range(len(crossover_indexes)):
            index: int = crossover_indexes[i]

            # slice parents
            parent_1_partition = parent_1_genome[start_index:index]
            parent_2_partition = parent_2_genome[start_index:index]

            # this is to ensure that only ever other index is actually swapped
            if i % 2 == 0:
                child_1_genome = T.cat([child_1_genome, parent_2_partition])
                child_2_genome = T.cat([child_2_genome, parent_1_partition])
            else:
                child_1_genome = T.cat([child_1_genome, parent_1_partition])
                child_2_genome = T.cat([child_2_genome, parent_2_partition])

            start_index = index

        return child_1_genome, child_2_genome

    def _get_crossover_indeces(self, n_crossover_points, parent_genome):
        return [random.randint(0, len(parent_genome)) for i in range(n_crossover_points)]

    def mutate_children(self):
        """

        :return:
        """

        def mutate(value):
            if self.mutation_rate > random.random():
                return random.random() * 2 - 1
            return value

        def mutate_gauss(value, mean, sd):
            if self.mutation_rate > random.random():
                return np.random.normal(loc=mean, scale=sd, size=1)
            return value

        for child_genome in self.children_genomes:
            for layer_genome in child_genome:
                # mean = np.mean(layer_genome.numpy())
                # sd = np.std(layer_genome.numpy())
                # layer_genome.apply_(lambda x: mutate_gauss(x, mean, sd))
                layer_genome.apply_(lambda x: mutate(x))

    def replace(self):
        """
        Replacement strategy?
        :return:
        """
        # loop over the genomes of children
        # create a new Genetic Agent for each genome
        # replace agent in population
        self.children_genomes.extend(self.elites)
        for solution, child in zip(self.individuals, self.children_genomes):
            solution.set_genome(child)

    def reset(self):
        for solution in self.individuals:
            solution.reset()

        self.selected_individuals = []
        self.children_genomes = []
        self.elites = []

    def is_finished(self):
        # here return the max value that we expect
        pass
