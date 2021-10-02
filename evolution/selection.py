import math
import random
from typing import List, Dict

from agents.genetic_agent import GeneticAgent


def roulette_wheel_select(probabilities):
    """
    selects a single individual from the population
    :return:
    """
    # I have a list of probabilities ordered ascendingly
    # initialise a sum
    # I pick a random number
    # if the probability is greater than the random number
    random_number = random.random()
    probability_sum = next(iter(probabilities.items()))[1]  # start with highest value in the sum
    for item in probabilities.items():
        if probability_sum > random_number:
            return item[0]

        probability_sum += item[1]


class Selection:
    """
    Interface for the evolutionary selection mechanism
    """
    def __init__(self, params: Dict):
        self.params = params

    def select(self, population: List[GeneticAgent], n_parents: int = 1):
        pass

    def set_params(self, params):
        pass


class RouletteWheelSelection(Selection):
    """
    Implementation of a roulette wheel selection algorithm
    """

    def select(self, population: List[GeneticAgent], n_parents: int = 1):
        return RouletteWheelSelection.roulette_wheel(population, n_parents, self.params)

    @staticmethod
    def roulette_wheel(population: List[GeneticAgent], n_parents: int = 1, params: Dict = {}) -> List:
        """
        Performs a roulette wheel selection on the population fitness. For each entry in the fitness array, the probability
        of it being chosen is proportional to its fitness.
        :param params:
        :param population:
        :return: a list of parents that have been chosen
        """

        # sum up the fitness for all individuals
        fitness_sum = sum(solution.fitness for solution in population)

        # calculate the probability of an individual being selected

        # calculate probability of entry: fitness over sum and add to list which is sorted in descending order
        probability_map = dict()
        for solution in population:
            probability = solution.fitness / fitness_sum
            probability_map[solution] = probability

        sorted_probability_map = dict(sorted(probability_map.items(), key=lambda item: item[1], reverse=True))

        parents = []
        for n in range(n_parents):
            parents.append(roulette_wheel_select(sorted_probability_map))

        return parents

        # generate random number n

        # loop over list of sorted probabilities and choose the first that is greater than n


class RankSelection(Selection):
    """
    Implementation of a rank based selection algorithm
    """

    def select(self, population: List[GeneticAgent], n_parents: int = 1):
        return RankSelection.rank_based_selection(population, n_parents, self.params)

    def set_params(self, params):
        if params["bias"]:
            self.params = params
        else:
            raise Exception(f'{params} must contain a value for the key "bias"')

    @staticmethod
    def rank_based_selection(population: List[GeneticAgent], n_parents: int = 1, params: Dict = {}) -> List:
        """
        Performs a rank based selection. Individuals are sorted according to their fitness and assigned a fitness proportionate
        rank, i.e. the individual with the highest fitness is assigned the highest rank raised to a bias. A high bias
        value weighs fitter individuals more than it does weaker individuals, i.e. it increases the selection pressure. A low bias
        means a lower selection pressure, i.e. weaker individuals have a higher change of being included as well.
        :param n_parents: The number of parents to be returned by the rank based selection
        :param population: the population from which the algorithm will choose
        :param bias: the bias value that decides seleciton pressure
        :return: a list of selected Genetic Agents
        """

        # rank population according to fitness
        # calculate probability for each entry
        # select individual
        bias = params["bias"]
        sorted_population = sorted(population, key=lambda entry: entry.fitness, reverse=True)

        rank_sum = sum(i ** bias for i in range(1, len(population) + 1))

        probability_population = dict()

        for i in range(len(sorted_population)):
            rank = i + 1
            solution = sorted_population[i]
            probability = rank ** bias / rank_sum
            probability_population[solution] = probability

        sorted_probability_population = dict(
            sorted(probability_population.items(), key=lambda item: item[1], reverse=True))

        parents = []
        for n in range(n_parents):
            parents.append(roulette_wheel_select(sorted_probability_population))

        return parents


class TournamentSelection(Selection):
    """
    Implementation of a tournament selection algorithm
    """
    def select(self, population: List[GeneticAgent], n_parents: int = 1):
        return TournamentSelection.tournament_selection(population, n_parents, self.params)

    def set_params(self, params):
        if params["tournament_size"]:
            self.params = params
        else:
            raise Exception(f'{params} must contain a value for the key "tournament_size"')

    @staticmethod
    def tournament_selection(population: List[GeneticAgent], n_parents: int, params: Dict = {}) -> List:
        """
        Performs a tournament selection on a list of Genetic Agents for a specified number of iterations. In a tournament
        selection, a random number of individuals is chosen from the population out of which the individual with the best
        fitness is declared winner and added to the parents will be returned.
        :param population: the population from which the tournament selection algorithm will choose from
        :param n_parents: the number of parents that should be returned by the overall tournament selection
        :param tournament_size: the size of each individual tournament round
        :return: a list of GeneticAgent of length n_parents
        """
        tournament_size = math.floor(n_parents * params["tournament_size"])

        parents = []
        for _ in range(n_parents):
            tournament_participants = []
            for _ in range(tournament_size):
                tournament_participants.append(random.choice(population))

            tournament_winner = sorted(tournament_participants, key=lambda participant: participant.fitness)[-1]
            parents.append(tournament_winner)

        return parents
