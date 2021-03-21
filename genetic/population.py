import random
import torch as T

from agents.genetic_agent import GeneticAgent
from environment.env import SnakeEnv
from environment.snake import Snake
from environment.state import LidarAndOneHot2
from genetic.selection import roulette_wheel, rank_based_selection


class Population:

    def __init__(self, pop_size, mutation_rate, crossover_rate):
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
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


class SnakePopulation(Population):

    def __init__(self, pop_size, mutation_rate, crossover_rate):
        Population.__init__(self, pop_size=pop_size, mutation_rate=mutation_rate, crossover_rate=crossover_rate)

    def initialise_population(self):
        self.selected_population = []
        self.children_genomes = []
        self.population = []
        for n in range(self.pop_size):
            self.population.append(GeneticAgent(learning_rate=0, input_dims=[24], n_actions=4, mutation_rate=0.001))
            print("initialising...")

    def simulate(self):
        env = SnakeEnv(400, 400, LidarAndOneHot2)
        for solution in self.population:
            solution.simulate(env)
            print("simulating...")

    def calculate_fitness(self):
        for solution in self.population:
            solution.calculate_fitness(None)

        self.population = sorted(self.population, key=lambda solution: solution.fitness)
        print("Calculated fitness")


    def candidate_selection(self):
        self.selected_population = rank_based_selection(population=self.population, n_parents=len(self.population))
        print("")
        pass

    def crossover(self, n_crossover_points=1):
        """

        :param n_crossover_points:
        :return:
        """
        #TODO refactor this method
        parents = []
        for selected_individual in self.selected_population:
            # do crossover for two parents at a time
            if len(parents) == 2:
                # get genomes
                parent_1_genome = parents[0].get_genome()
                parent_2_genome = parents[1].get_genome()

                # get the crossover indexes
                crossover_indexes = [random.randint(0, len(parent_1_genome)) for i in range(n_crossover_points)]
                crossover_indexes.append(len(parent_1_genome)) # append final index of list so that we can get the final slice

                # prepare the child genomes
                child_1_genome = T.tensor([])
                child_2_genome = T.tensor([])

                start_index = 0
                for i in range(len(crossover_indexes)):
                    index = crossover_indexes[i]

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

                self.children_genomes.append([child_1_genome, child_2_genome])
                    # assign the new genome
                # create genetic agent
                    # add slice to children.
                parents = []


            parents.append(selected_individual)
        # take two parents
        # get their genome
        # choose k (number of crossovers)
        # pick k random indeces
        # make k crossovers at the specified indeces


    def mutate(self):
        """

        :return:
        """
        pass

    def replace(self):
        """
        Replacement strategy?
        :return:
        """
        # loop over the genomes of children
            # create a new Genetic Agent for each genome
            # replace agent in population

        pass