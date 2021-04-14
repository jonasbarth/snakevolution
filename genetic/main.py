import functools
from torch.utils.tensorboard import SummaryWriter
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
parser.add_argument("-t", "--type", nargs='?', type=str, help="the type of genetic algorithm, either generational or steady state")
parser.add_argument("-r", "--replacement_function", nargs='?', type=str, help="the type of replacement function")

args = parser.parse_args()


print(args)

writer = SummaryWriter()
n_generations = args.generations
pop_size = 10
pop = SnakePopulation(pop_size=pop_size, mutation_rate=0.001, crossover_rate=0.5)
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
    #population.calculate_fitness(population)
    #selection = select_candidates(population)




