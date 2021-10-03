import argparse
from datetime import datetime

from util.analysis.json_loader import JsonLoader
from util.argument_validator import GeneticArgumentValidator
from util.io.export.genetic_exporter import GeneticExporter, GeneticPopulationDataExporter
from util.io.export.hyper_parameter_exporter import HyperParameterExporter
from evolution.generational import Generational
from evolution.population import SnakePopulation

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-hp", "--hyper_params", nargs='?', type=str, help="the path to a hyper parameters json file that will be loaded")
    parser.add_argument("-ex", "--executions", nargs='?', type=int, default=1, help="the number of times the entire algorithm should be run")

    args = parser.parse_args()
    hyper_params_path = args.hyper_params
    loader = JsonLoader(hyper_params_path)
    if not loader.load():
        exit(1)

    params = loader.get_data()

    arg_validator = GeneticArgumentValidator()
    n_executions = arg_validator.validate_n_executions(args.executions)
    n_generations = arg_validator.validate_n_generations(params["generations"])
    pop_size = arg_validator.validate_population_size(params["population_size"])
    mutation_rate = arg_validator.validate_mutation_rate(params["mutation_rate"])
    crossover_rate = arg_validator.validate_crossover_rate(params["crossover_rate"])
    crossover_points = arg_validator.validate_n_crossover_points(params["crossover_points"])
    fitness_func = arg_validator.get_fitness_func(params["fitness_function"])
    selection = arg_validator.get_selection(params["selection_type"])
    selection.set_params(params["selection_params"])
    algorithm_type = arg_validator.validate_algorithm_type(params["type"])
    elitism = arg_validator.validate_elitism(params["elitism"])
    screen_width, screen_height, snake_size = arg_validator.validate_screen_size(params["screen_width"], params["screen_height"], params["snake_size"])
    graphics = params["graphics"]

    for execution in range(n_executions):
        print(f'Execution: {execution + 1}')
        pop = SnakePopulation(pop_size=pop_size, mutation_rate=mutation_rate, crossover_rate=crossover_rate, elitism=elitism, fitness_func=fitness_func, selection=selection, show_game=graphics, screen_width=screen_width, screen_height=screen_height, snake_size=snake_size)

        print(f'Generations: {n_generations}; Population Size: {pop_size}; Mutation Rate: {mutation_rate}; Crossover Rate: {crossover_rate}; Crossover Points: {crossover_points}; Elitism: {elitism};')

        if algorithm_type == "GENERATIONAL":

            algorithm = Generational(pop)
            algorithm.run(n_generations=n_generations)

            now = datetime.now()
            date_time = now.strftime("%m_%d_%Y__%H_%M_%S")
            path = '../models/evolution/' + date_time
            genetic_exporter = GeneticExporter(path)
            genetic_exporter.export(algorithm.best_individual(n_generations - 1))

            genetic_population_data_exporter = GeneticPopulationDataExporter(path)
            genetic_population_data_exporter.export(algorithm.get_population_data())

            hp_exporter = HyperParameterExporter(path)
            hp_exporter.export(params)




