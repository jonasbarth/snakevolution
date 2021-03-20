import random

def roulette_wheel_select(probabilities):
    """
    selects a single individual from the population
    :return:
    """
    # I have a list of probabilities ordered ascendingly
    # initialise a sum
    # I pick a random number
    # if the probability is greater than the random number
    random_number = random.random()
    probability_sum = next(iter(probabilities.items()))[1] # start with highest value in the sum
    for item in probabilities.items():
        if probability_sum > random_number:
            return item[0]

        probability_sum += item[1]


def roulette_wheel(population, n_parents=1):
    """
    Performs a roulette wheel selection on the population fitness. For each entry in the fitness array, the probability
    of it being chosen is proportional to its fitness.
    :param population:
    :return: a list of parents that have been chosen
    """

    # sum up the fitness for all individuals
    fitness_sum = sum(solution.fitness for solution in population)

    # calculate the probability of an individual being selected


    # calculate probability of entry: fitness over sum and add to list which is sorted in descending order
    probability_map = dict()
    for solution in population:
        probability = solution.fitness/fitness_sum
        probability_map[solution] = probability

    sorted_probability_map = dict(sorted(probability_map.items(), key=lambda item: item[1], reverse=True))


    parents = []
    for n in range(n_parents):
        parents.append(roulette_wheel_select(sorted_probability_map))

    print("Parents", parents)


    return parents

    # generate random number n

    # loop over list of sorted probabilities and choose the first that is greater than n


def rank_based_selection(population, n_parents=1, bias=1):
    """
    Performs a rank based selection
    :param population:
    :param bias:
    :return:
    """

    # rank population according to fitness
    # calculate probability for each entry
    # select individual

    sorted_population = sorted(population, key=lambda entry: entry.fitness, reverse=True)

    rank_sum = sum(i**bias for i in range(1, len(population) + 1))

    probability_population = dict()

    for i in range(len(sorted_population)):
        rank = i + 1
        solution = sorted_population[i]
        probability = rank**bias / rank_sum
        probability_population[solution] = probability

    sorted_probability_population = dict(sorted(probability_population.items(), key=lambda item: item[1]))

    parents = []
    for n in range(n_parents):
        parents.append(roulette_wheel_select(sorted_probability_population))

    print("Parents", parents)

    return parents







