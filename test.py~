import random as r
from Caveman import Caveman
import numpy as np
import pdb

"""
#from deap import base
#from deap import creator
#from deap import tools
"""
#number of appendages
NUM_APP = 2

#size of the population
POPULATION_SIZE = 64

#number of generations
NGEN = 10

#number of rounds from the end the tournament cuts off.
ROUND_CUTOFF = 2

#probability of a mutation occuring on a given trait.
MUTATION_RATE = 0.15
MUTATION_AMOUNT = 0.1
def evaluate(individual1, individual2):
    #have fight, return winner.
    return individual1

def ispower(n, bs):
    assert(n > 0)
    assert(bs > 0)

    if n == bs:
        return True
    if bs == 1:
        return False
    temp = bs
    while (temp <= n):
        if temp == n:
            return True
        temp *= bs
    return False

def powerof(n, bs):
    counter = 1
    if n == bs:
        return counter
    if bs == 1:
        return n
    temp = bs
    while(temp <= n):
        if temp == n:
            return counter
        temp *= bs
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

"""
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
"""

def generatePopulation():
    return [Caveman(NUM_APP) for i in xrange(POPULATION_SIZE)]

population = generatePopulation()

#does not support combining breeds with a different number of appendages
#this is nasty code but I'm not going to change it right now. Should just use dict.keys() and dict.items() instead of this eval shit
def mutate(nxt):
    #the list of appendages in next
    nextapp = nxt.appendages
    for j in xrange(len(nextapp)):
        for i in nextapp[j].__dict__:
            dictval = eval("nextapp[j]." + i)
            #if the value in the dictionary is an int or a float, attempt mutation
            if (isinstance(dictval, float) or isinstance(dictval, int)):
                rand = r.random()
                if rand < MUTATION_RATE:
                    if r.random() < 0.5:
                        exec "nextapp[j]." + i + " += MUTATION_AMOUNT"
                    else:
                        exec "nextapp[j]." + i + " -=  MUTATION_AMOUNT"

            #if the value in the dictionary is a polynomial, go through the coefficients and mutate them
            if (isinstance(dictval, np.poly1d)):
                #len(np.poly1d) returns the mathematical degree, so we add one to make all coefficients available
                for k in xrange(len(dictval) + 1):
                    rand = r.random()
                    if rand < MUTATION_RATE:
                        if r.random() < 0.5:
                            dictval[k] -= MUTATION_AMOUNT
                        else:
                            dictval[k] += MUTATION_AMOUNT
    
    #going through the fields in nxt.
    nextdict = nxt.__dict__
    for i in nextdict.keys():
        if not i == 'appendages':
            #pdb.set_trace()
            dictval = eval("nextdict['" + i + "']")
            if (isinstance(dictval, float) or isinstance(dictval, int)):
                rand = r.random()
                if rand < MUTATION_RATE:
                    if r.random() < 0.5:
                        exec "nxt." + i + " -= MUTATION_AMOUNT" 
                    else:
                        exec "nxt." + i + " += MUTATION_AMOUNT"
            if (isinstance(dictval, np.poly1d)):
                for k in xrange(len(dictval) + 1):
                    rand = r.random()
                    if rand < MUTATION_RATE:
                        if r.random() < 0.5:
                            dictval[k] -= MUTATION_AMOUNT
                        else:
                            dictval[k] += MUTATION_AMOUNT
    return nxt
                    
    
def combine(ind1, ind2):
    assert(ind1.nAppendages == ind2.nAppendages)
    
    nxt = Caveman(ind1.nAppendages)
    dict1 = ind1.__dict__
    dict2 = ind2.__dict__
    app1 = dict1['appendages']
    app2 = dict2['appendages']
    nxtdict = nxt.__dict__
    for key in nxtdict.keys():
        if key != 'appendages':
            if r.random() < 0.5:
                exec "nxt." + str(key) + " = dict1['" + str(key) + "']"
            else:
                exec "nxt." + str(key) + " = dict2['" + str(key) + "']"

    for i in xrange(len(nxtdict['appendages'])):
        arm = nxtdict['appendages'][i]
        for key in arm.__dict__.keys():
            if r.random() < 0.5:
                exec "arm." + str(key) + " = app1[" + str(i) + "]." + key
            else:
                exec "arm." + str(key) + " = app2[" + str(i) + "]." + key
        
    return nxt
            
            
def mate(generation):
    return map(combine, generation[0::2], generation[1::2])

nxtGen = fightTournament(population, ROUND_CUTOFF)
derp = mate(nxtGen)

herp = mutate(derp[0])

def runtrial(numtrials):
    for i in numtrials:
        fightTournament(population, ROUND_CUTOFF
