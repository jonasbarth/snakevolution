import random

def roulette_wheel(population, n_parents=2):
    """
    Performs a roulette wheel selection on the population fitness. For each entry in the fitness array, the probability
    of it being chosen is proportional to its fitness.
    :param population:
    :return: a list of parents that have been chosen
    """

    # sum up probabilities for all entries
    fitness_sum = sum(solution.fitness for solution in population)

    # calculate probability of entry: fitness over sum and add to list which is sorted in descending order
    probability_map = dict()
    for solution in population:
        probability = solution.fitness/fitness_sum
        probability_map[solution] = probability

    sorted_probability_map = dict(sorted(probability_map.items(), key=lambda item: item[1]))

    #pick two parents
    parents = []
    for n in range(n_parents):
        random_number = random.random()
        for item in sorted_probability_map.items():
            if item[1] > random_number:
                parents.append(item[0])
                break

    print("Parents", parents)
    return parents

    # generate random number n

    # loop over list of sorted probabilities and choose the first that is greater than n




