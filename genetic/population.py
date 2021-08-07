import random
import sys

import torch as T

from agents.genetic_agent import GeneticAgent
from environment.turtle.env import SnakeEnv
from environment.pygame.env import PyGameEnv
from environment.env import Env, Direction
from environment.turtle.env import TurtleSnake
from environment.state import LidarAndOneHot2
from genetic.selection import roulette_wheel, rank_based_selection
from rl.mpd import MDP
from rl.snake import SnakeMDP


class Population:

    def __init__(self, pop_size: int, mutation_rate: float, crossover_rate: float, elitism: float, fitness_func, selection_func):
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism = elitism
        self.fitness_func = fitness_func
        self.selection_func = selection_func
        self.individuals = []
        self.selected_individuals = []
        self.elites = []
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


class SnakePopulation(Population):

    def __init__(self, pop_size, mutation_rate, crossover_rate, elitism, fitness_func, selection_func):
        Population.__init__(self, pop_size=pop_size, mutation_rate=mutation_rate, elitism=elitism, crossover_rate=crossover_rate, fitness_func=fitness_func, selection_func=selection_func)

    def initialise_population(self):
        self.selected_individuals = []
        self.children_genomes = []
        for n in range(self.pop_size):
            sys.stdout.write('\r' + f'Initialising population ({n + 1}/{self.pop_size})')
            sys.stdout.flush()
            mdp = SnakeMDP()
            self.individuals.append(
                GeneticAgent(mdp=mdp, learning_rate=0, input_dims=[mdp.state_dims()[0]], n_actions=Direction.n_actions(), mutation_rate=self.mutation_rate))

    def simulate(self):
        for solution in self.individuals:

            sys.stdout.write('\r' + f'Simulating ({self.individuals.index(solution) + 1}/{len(self.individuals)})')
            sys.stdout.flush()
            solution.simulate()

    def calculate_fitness(self):
        highest_fitness = 0
        for solution in self.individuals:
            sys.stdout.write('\r' + f'Calculating fitness ({self.individuals.index(solution) + 1}/{len(self.individuals)})')
            sys.stdout.flush()
            solution.calculate_fitness(self.fitness_func)
            if solution.fitness >= highest_fitness:
                highest_fitness = solution.fitness


        print(f'Highest fitness: {highest_fitness}')
        self.individuals = sorted(self.individuals, key=lambda solution: solution.fitness)

    def candidate_selection(self):
        # self.elitism of len of self.individuals
        index = len(self.individuals) - int(self.elitism * len(self.individuals))
        elites = self.individuals[index:]
        for elite in elites:
            sys.stdout.write('\r' + f'Copying over ({elites.index(elite) + 1}/{len(elites)}) elites into the next generation')
            sys.stdout.flush()
            self.elites.append(elite.get_genome())

        print(f'\nSelecting {index} individuals from the population')
        selected = self.selection_func(self.individuals[:index], len(self.individuals[:index]))
        self.selected_individuals.extend(selected) #rank_based_selection(population=self.population, n_parents=len(self.population))

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

        for child_genome in self.children_genomes:
            for layer_genome in child_genome:
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