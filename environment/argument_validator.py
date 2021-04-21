import genetic.fitness as fitness
import genetic.selection as selection


class ArgumentValidator:

    def validate(self, arg) -> bool:
        pass

    def get(self, arg):
        pass


class GeneticArgumentValidator:

    def __init__(self):
        self.fitness_validator = FitnessFunctionValidator()
        self.selection_validator = SelectionFunctionValidator()

    def validate_fitness_func(self, arg):
        return self.fitness_validator.validate(arg)

    def get_fitness_func(self, arg):
        return self.fitness_validator.get(arg)

    def validate_selection_func(self, arg):
        return self.selection_validator.validate(arg)

    def get_selection_func(self, arg):
        return self.selection_validator.get(arg)

    def validate_n_generations(self, arg: int):
        if arg >= 0:
            return arg

        raise Exception("%s is not recognised as a correct argument for %s. It must be >= 0." % (arg, "Number of Generations"))

    def validate_population_size(self, arg: int):
        if arg >= 0:
            return arg

        raise Exception("%s is not recognised as a correct argument for %s. It must be >= 0." % (arg, "Population Size"))

    def validate_mutation_rate(self, arg: int):
        if 0 <= arg <= 1:
            return arg

        raise Exception("%s is not recognised as a correct argument for %s. It must be >= 0." % (arg, "Mutation Rate"))

    def validate_crossover_rate(self, arg: int):
        if 0 <= arg <= 1:
            return arg

        raise Exception("%s is not recognised as a correct argument for %s. It must be >= 0." % (arg, "Crossover Rate"))

    def validate_n_crossover_points(self, arg: int):
        if arg >= 0:
            return arg

        raise Exception("%s is not recognised as a correct argument for %s. It must be >= 0." % (arg, "Crossover Points"))




class FitnessFunctionValidator(ArgumentValidator):

    def __init__(self):
        self.fitness_func_mapping = dict()
        self.fitness_func_mapping["MAXIMISE_MOVES"] = fitness.maximise_moves
        self.fitness_func_mapping["MAXIMISE_FOOD_EATEN"] = fitness.maximise_food_eaten

    def validate(self, arg: str) -> bool:
        return arg in self.fitness_func_mapping.keys()

    def get(self, arg):
        if (self.validate(arg)):
            return self.fitness_func_mapping[arg]

        raise Exception("%s is not recognised as a correct argument for %s" % (arg, "Fitness Function"))


class SelectionFunctionValidator(ArgumentValidator):

    def __init__(self):
        self.selection_func_mapping = dict()
        self.selection_func_mapping["ROULETTE"] = selection.roulette_wheel
        self.selection_func_mapping["RANK"] = selection.rank_based_selection

    def validate(self, arg: str) -> bool:
        return arg in self.selection_func_mapping.keys()

    def get(self, arg):
        if (self.validate(arg)):
            return self.selection_func_mapping[arg]

        raise Exception("%s is not recognised as a correct argument for %s" % (arg, "Selection Function"))



