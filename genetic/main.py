import functools
from torch.utils.tensorboard import SummaryWriter

from environment.argument_validator import FitnessFunctionValidator, GeneticArgumentValidator
from genetic.population import Population, SnakePopulation
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-g", "--generations", nargs='?', type=int, const=1, help="number of generations to run the genetic algorithm for")
parser.add_argument("-p", "--population_size", nargs='?', type=int, const=10, help="size of the population")
parser.add_argument("-m", "--mutation_rate", nargs='?', type=float, const=0.0001, help="the mutation rate")
parser.add_argument("-c", "--crossover_rate", nargs='?', type=float, const=0.9, help="the percentage of offspring that will be created by crossover")
parser.add_argument("-f", "--fitness_function", nargs='?', type=str, help="the fitness function")
parser.add_argument("-cp", "--crossover_points", nargs='?', type=int, const=2, help="number of crossover points")
parser.add_argument("-s", "--selection_function", nargs='?', type=str, help="the selection function")
parser.add_argument("-t", "--type", nargs='?', type=str, const="generational", help="the type of genetic algorithm, either generational or steady state. Generational replaces the entire population after each generation, Steady state keeps evolving the same population.")
parser.add_argument("-r", "--replacement_function", nargs='?', type=str, help="the type of replacement function. Only necessary for steady state algorithms")
parser.add_argument("-e", "--elitism", nargs='?', type=float, const=0.0, help="percentage of parents that will be copied to the next generation unchanged")

args = parser.parse_args()


arg_validator = GeneticArgumentValidator()
n_generations = arg_validator.validate_n_generations(args.generations)
pop_size = arg_validator.validate_population_size(args.population_size)
mutation_rate = arg_validator.validate_mutation_rate(args.mutation_rate)
crossover_rate = arg_validator.validate_crossover_rate(args.crossover_rate)
crossover_points = arg_validator.validate_n_crossover_points(args.crossover_points)
fitness_func = arg_validator.get_fitness_func(args.fitness_function)
selection_func = arg_validator.get_selection_func(args.selection_function)
algorithm_type = arg_validator.validate_algorithm_type(args.type)
elitism = arg_validator.validate_elitism(args.elitism)


writer = SummaryWriter()

pop = SnakePopulation(pop_size=pop_size, mutation_rate=mutation_rate, crossover_rate=crossover_rate, fitness_func=fitness_func, selection_func=selection_func)
pop.initialise_population()

print(n_generations)

for generation in range(n_generations):
    print("Generation", generation)
    pop.simulate()
    pop.calculate_fitness()
    pop.candidate_selection()
    pop.crossover()
    pop.mutate_children()
    pop.replace()

    total_fitness = functools.reduce(lambda x, y: x + y, map(lambda solution: solution.fitness, pop.population))
    avg_fitness = total_fitness / pop_size
    print("Avg Fitness", avg_fitness)
    writer.add_scalar("Average Fitness", avg_fitness, global_step=generation)
