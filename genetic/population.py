import random
import torch as T

from agents.genetic_agent import GeneticAgent
from environment.env import SnakeEnv, Env
from environment.snake import Snake
from environment.state import LidarAndOneHot2
from genetic.selection import roulette_wheel, rank_based_selection


class Population:

    def __init__(self, pop_size: int, mutation_rate: float, crossover_rate: float, fitness_func, selection_func):
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.fitness_func = fitness_func
        self.selection_func = selection_func
        self.population = []
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


class SnakePopulation(Population):

    def __init__(self, pop_size, mutation_rate, crossover_rate, fitness_func, selection_func):
        Population.__init__(self, pop_size=pop_size, mutation_rate=mutation_rate, crossover_rate=crossover_rate, fitness_func=fitness_func, selection_func=selection_func)

    def initialise_population(self):
        self.selected_population = []
        self.children_genomes = []
        for n in range(self.pop_size):
            env: Env = SnakeEnv(400, 400, LidarAndOneHot2)
            self.population.append(GeneticAgent(env=env, learning_rate=0, input_dims=[24], n_actions=4, mutation_rate=0.001))
            print("initialising...")

    def simulate(self):
        for solution in self.population:
            solution.simulate()
            print("simulating...")

    def calculate_fitness(self):
        for solution in self.population:
            solution.calculate_fitness(self.fitness_func)

        self.population = sorted(self.population, key=lambda solution: solution.fitness)
        print("Calculated fitness")

    def candidate_selection(self):
        self.selected_population = self.selection_func(self.population, len(self.population)) #rank_based_selection(population=self.population, n_parents=len(self.population))
        print("")
        pass

    def crossover(self, n_crossover_points=1):
        """

        :param n_crossover_points:
        :return:
        """
        # TODO refactor this method
        parents = []
        for selected_individual in self.selected_population:
            # do crossover for two parents at a time
            parents.append(selected_individual)

            if len(parents) == 2:
                # do a crossover with the probability of the crossover rate
                if random.random() <= self.crossover_rate:
                    # get genomes
                    parent_1_genome = parents[0].get_genome()
                    parent_2_genome = parents[1].get_genome()

                    child_1_genome, child_2_genome = self._make_children(parent_1_genome, parent_2_genome,
                                                                         n_crossover_points)

                    self.children_genomes.append(child_1_genome)
                    self.children_genomes.append(child_2_genome)

                parents = []


    def _make_children(self, parent_1_genome, parent_2_genome, n_crossover_points):
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

        for child_genome in self.children_genomes:
            child_genome.apply_(lambda x: mutate(x))

    def replace(self):
        """
        Replacement strategy?
        :return:
        """
        # loop over the genomes of children
        # create a new Genetic Agent for each genome
        # replace agent in population
        for solution, child in zip(self.population, self.children_genomes):
            solution.set_genome(child)

    def reset(self):
        for solution in self.population:
            solution.reset()