import functools

from torch.utils.tensorboard import SummaryWriter

from genetic.population import Population


class Generational:
    """
    Class for a generational genetic algorithm where the entire population is replaced each generation.
    """

    def __init__(self, population: Population):
        self.population = population
        self.writer = SummaryWriter()

    def run(self, n_generations: int) -> None:
        """
        Runs the generational genetic algorithm with the population for the number of generations.
        :return:
        """
        self.population.initialise_population()

        for generation in range(n_generations):
            print("Generation", generation)
            self.population.simulate()
            # self.population.calculate_fitness()
            # self.population.candidate_selection()
            # self.population.crossover()
            # self.population.mutate_children()
            # self.population.replace()
            #
            # total_fitness = functools.reduce(lambda x, y: x + y,
            #                                  map(lambda solution: solution.fitness, self.population.individuals))
            # avg_fitness = total_fitness / self.population.pop_size
            # print("Avg Fitness", avg_fitness)
            # self.writer.add_scalar("Average Fitness", avg_fitness, global_step=generation)
            #
            # self.population.reset()
