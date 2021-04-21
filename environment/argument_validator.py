import genetic.fitness as fitness


class ArgumentValidator:

    def validate(self, arg) -> bool:
        pass

    def get(self, arg):
        pass


class GeneticArgumentValidator:

    def __init__(self):
        self.fitness_validator = FitnessFunctionValidator()

    def validate_fitness_func(self, arg):
        return self.fitness_validator.validate(arg)

    def get_fitness_func(self, arg):
        return self.fitness_validator.get(arg)


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
