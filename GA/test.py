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
ROUND_CUTOFF = 2

#probability of a mutation occuring on a given trait.
MUTATION_RATE = 0.1
MUTATION_AMOUNT = 0.01
def evaluate(individual1, individual2):
    #have fight, return winner.
    return individual1

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
    endround = powerof(numWinners, 2)
    numrounds = totalrounds - endround

    chosen = population
    for i in xrange(numrounds):
        chosen = map(evaluate, chosen[0::2], chosen[1::2])
        #print chosen
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

#does not support combining breeds with a different number of appendages
def mutate(next):
    nextapp = next['appendages']
    for j in xrange(len(nextapp)):
        for i in nextapp[j].__dict__:
            dictval = exec("next." + i)
            if (isinstance(dictval, float) or isinstance(dictval, int)):
                rand = r.random()
                if rand < MUTATION_RATE:
                    if rand < (MUTATION_RATE / 2):
                        exec("nextapp[j]." + i + " -= MUTATION_AMOUNT")
                    else:
                        exec("nextapp[j]." + i + " += MUTATION_AMOUNT")
            if (isinstance(dictval, collections.Iterable)):
                rand = randrange(0,len(dictval)) 
                if rand < (MUTATION_RATE):
                    
    for i in next.__dict__:
        if (isinstance(exec("next." + i), float) or isinstance(exec("next." + i) is int)):
    
def combine(ind1, ind2):
    assert(ind1.nAppendages == ind2.nAppendages)

    next = Caveman(ind1.nAppendages)
    dict1 = ind1.__dict__
    dict2 = ind2.__dict__
    app1 = dict1['appendages']
    app2 = dict2['appendages']
    nextapp = next['appendages']
    
            
            
def mate(generation):
    return map(combine, generation[0::2], generation[1::2])

for g in xrange(NGEN):
    nextGen = fightTournament(population, ROUND_CUTOFF)
    nextGen = mate(nextGen)
    #mate pairs.
    
