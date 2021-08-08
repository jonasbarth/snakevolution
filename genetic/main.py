import argparse
import distutils

from torch.utils.tensorboard import SummaryWriter

from environment.argument_validator import GeneticArgumentValidator
from genetic.generational import Generational
from genetic.population import SnakePopulation

parser = argparse.ArgumentParser()



parser.add_argument("-g", "--generations", nargs='?', type=int, default=1, help="number of generations to run the genetic algorithm for")
parser.add_argument("-p", "--population_size", nargs='?', type=int, default=10, help="size of the population")
parser.add_argument("-m", "--mutation_rate", nargs='?', type=float, default=0.0001, help="the mutation rate")
parser.add_argument("-c", "--crossover_rate", nargs='?', type=float, default=0.9, help="the percentage of offspring that will be created by crossover")
parser.add_argument("-f", "--fitness_function", nargs='?', type=str, help="the fitness function")
parser.add_argument("-cp", "--crossover_points", nargs='?', type=int, default=2, help="number of crossover points")
parser.add_argument("-s", "--selection_function", nargs='?', type=str, default="", help="the selection function")
parser.add_argument("-t", "--type", nargs='?', type=str, const="GENERATIONAL", help="the type of genetic algorithm, either generational or steady state. Generational replaces the entire population after each generation, Steady state keeps evolving the same population.")
parser.add_argument("-r", "--replacement_function", nargs='?', type=str, help="the type of replacement function. Only necessary for steady state algorithms")
parser.add_argument("-e", "--elitism", nargs='?', type=float, default=0.0, help="percentage of parents that will be copied to the next generation unchanged")
parser.add_argument("--graphics", dest='graphics', action='store_true', help="use this option if you want show the game on the screen")
parser.add_argument("--no-graphics", dest='graphics', action='store_false', help="use this option if you do not want show the game on the screen")


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
graphics = args.graphics

pop = SnakePopulation(pop_size=pop_size, mutation_rate=mutation_rate, crossover_rate=crossover_rate, elitism=elitism, fitness_func=fitness_func, selection_func=selection_func, show_game=graphics)

print(f'Generations: {n_generations}; Population Size: {pop_size}; Mutation Rate: {mutation_rate}; Crossover Rate: {crossover_rate}; Crossover Points: {crossover_points}; Elitism: {elitism};')

if algorithm_type == "GENERATIONAL":
    algorithm = Generational(pop)
    algorithm.run(n_generations=n_generations)


