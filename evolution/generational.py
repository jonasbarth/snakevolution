import functools

from torch.utils.tensorboard import SummaryWriter

from agents import GeneticAgent
from evolution import Population


class Generational:
    """
    Class for a generational evolution algorithm where the entire population is replaced each generation.
    """

    def __init__(self, population: Population):
        self.population = population
        self.writer = SummaryWriter()
        self.best_individuals = []

    def run(self, n_generations: int) -> None:
        """
        Runs the generational evolution algorithm with the population for the number of generations.
        :return:
        """
        self.population.initialise_population()

        for generation in range(n_generations):
            print(f"\n------------- Generation {generation} -------------")
            self.population.simulate()
            self.population.calculate_fitness()
            self.best_individuals.append(self.population.best_individual)
            self.population.candidate_selection()
            self.population.crossover()
            self.population.mutate_children()
            self.population.replace()

            total_fitness = functools.reduce(lambda x, y: x + y,
                                            map(lambda solution: solution.fitness, self.population.individuals))
            avg_fitness = total_fitness / self.population.pop_size
            print(f"Avg Fitness {avg_fitness}\n")
            self.writer.add_scalar("Average Fitness", avg_fitness, global_step=generation)
            #
            self.population.reset()

    def best_individual_of(self, generation: int) -> GeneticAgent:
        """
        Returns the best individual of the specified generation where the first generations is generation 0. The last
        generation is n_generations - 1.
        :param generation: the generation from which the best individual is to be returned
        :return: the best individual of a generation. If the generation doesn't exist, None is returned
        """
        return self.best_individuals[generation]

    def best_individual(self) -> GeneticAgent:
        return self.population.best_individual

    def get_population_data(self):
        return self.population.population_data

