import functools
from copy import copy

from genetic.population import Population


def total_fitness(population: Population) -> float:
    """
    Calculates the total fitness of the population
    :param population:
    :return:
    """
    individuals = copy(population.individuals)
    return functools.reduce(lambda x, y: x + y,
                            map(lambda solution: solution.fitness, individuals))


def avg_fitness(population: Population) -> float:
    """
    Calculates the average fitness of the population
    :param population:
    :return:
    """
    return population.pop_size / total_fitness(population)
