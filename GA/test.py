import random
from Caveman import Caveman

from deap import base
from deap import creator
from deap import tools

#number of appendages
NUM_APP = 2

#size of the population
POPULATION_SIZE = 64

#number of generations
NGEN = 10

#number of rounds from the end the tournament cuts off.
cutoff = 2

def evaluate(individual1, individual2):
    #have fight, return winner.
    return individua11

def ispower(n, base):
    assert(n > 0)
    assert(base > 0)

    if n == base:
        return True
    if base == 1:
        return False
    temp = base
    while (temp <= n):
        if temp == n:
            return True
        temp *= base
    return False

def powerof(n, base):
    counter = 1
    if n == base:
        return counter
    if base == 1:
        return n
    temp = base
    while(temp <= n):
        if temp == n:
            return counter
        temp *= base
        counter += 1
    return counter

#population must be a multiple of 2 and numWinners must be a multiple of 2
def fightTournament(population, numWinners):
    length = len(population)
    assert(ispower(length, 2))
    assert(ispower(numWinners, 2))

    totalrounds = powerof(length , 2)
    endround = powerof(length, 2)
    numrounds = totalrounds - endround

    chosen = np.array(population)
    for i in xrange(numrounds):
        chosen = map(evaluate, chosen[0::2], chosen[1::2])
    return chosen
        
    
toolbox = base.Toolbox()
#creates a function toolbox.individual() that calls Caveman(NUM_APP)
toolbox.register("individual", Caveman, NUM_APP)
#population creates a list of Caveman
toolbox.register("population", tools.initRepeat, list, toolbox.individual, POPULATION_SIZE)
#selects the 4 people from a population
toolbox.register("select4", tools.selTournament, toolbox.population(), 4, POPULATION_SIZE)
#fights two individuals
toolbox.register("fight", evaluate)

population = toolbox.population()

#for g in xrange(NGEN):
     
    
