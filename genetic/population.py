from agents.genetic_agent import GeneticAgent
from environment.env import SnakeEnv
from environment.snake import Snake
from environment.state import LidarAndOneHot2


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
        self.population = []
        for n in range(self.pop_size):
            self.population.append(GeneticAgent(learning_rate=0, input_dims=[24], n_actions=4, mutation_rate=0.001))
            print("initialising...")

    def simulate(self):
        env = SnakeEnv(400, 400, LidarAndOneHot2)
        for snake in self.population:
            snake.simulate(env)
            print("simulating...")

    def calculate_fitness(self):
        [snake.calculate_fitness(None) for snake in self.population]
        self.population = sorted(self.population, key=lambda solution: solution.fitness)
        print("Calculated fitness")


    def candidate_selection(self):
        pass

    def crossover(self):
        pass

    def mutate(self):
        pass

    def replace(self):
        pass