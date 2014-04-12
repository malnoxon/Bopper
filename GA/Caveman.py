from __future__ import division
import random as r
from scipy import interpolate
import numpy as np

MAXIMUM_WEIGHT_CAVEMAN = 5
HEIGHT = 10
BODY_WEIGHT_PROPORTION = 0.75
NUM_POINTS = 3

MINIMUM_LENGTH_FOREARM = 2
MAXIMUM_LENGTH_FOREARM = 5


MINIMUM_LENGTH_BICEP = 2
MAXIMUM_LENGTH_BICEP = 4

MINIMUM_LENGTH_STRING = 0
MAXIMUM_LENGTH_STRING = 0

MINIMUM_RADIUS_BOPPER = 1
MAXIMUM_RADIUS_BOPPER = 1

MINIMUM_HEIGHT_ARMS = HEIGHT * (3/4)
MAXIMUM_HEIGHT_ARMS = HEIGHT * (3/4)

class Appendage:
    def __init__(self, wFor, wBic, wBop):
        #weight meant to be set
        self.lForearm = r.uniform(MAXIMUM_LENGTH_FOREARM, MINIMUM_LENGTH_FOREARM)
        self.lBicep = r.uniform(MAXIMUM_LENGTH_BICEP, MINIMUM_LENGTH_BICEP)
        self.rBopper = r.uniform(MAXIMUM_RADIUS_BOPPER, MINIMUM_RADIUS_BOPPER)
        self.lString = r.uniform(MAXIMUM_LENGTH_STRING, MINIMUM_LENGTH_STRING)
        self.wForearm = wFor
        self.wBicep = wBic
        self.wBopper = wBop

        x = np.linspace(0, 1.0, num = NUM_POINTS)
        y = np.array([r.uniform(-1, 1) for _ in xrange(NUM_POINTS - 1)])
        y = np.append(y, y[0])
        self.iElbow = np.poly1d(np.polyfit(x, y, NUM_POINTS))
        x = np.linspace(0, 1.0, num = NUM_POINTS)
        y = np.array([r.uniform(-1, 1) for _ in xrange(NUM_POINTS - 1)])
        y = np.append(y, y[0])
        self.iShoulder = np.poly1d(np.polyfit(x, y, NUM_POINTS))

        #set elasticiy
        self.elasticity = r.random()

class Caveman:    
    def __init__(self, numApp):
        self.nAppendages = numApp
        self.hBody = HEIGHT

        self.arm_height = r.uniform(MINIMUM_HEIGHT_ARMS, MAXIMUM_HEIGHT_ARMS)
        print "satr"
        print self.arm_height
        
        #sample the body weight between 0 and MAXIMUM_WEIGHT_CAVEMAN * BODY_WEIGHT_PROPORTION
        actProp = r.uniform(BODY_WEIGHT_PROPORTION, 0)
        self.wBody = MAXIMUM_WEIGHT_CAVEMAN * actProp

        #setting the weights, and then normalizing them.
        #remainingWeight holds the weight that is to be divided up into the arms and bopper.
        remainingWeight = (1 - actProp) * MAXIMUM_WEIGHT_CAVEMAN

        weg = [r.random() for _ in xrange(3 * numApp)]
        sumw = sum(weg)
        weg = [remainingWeight * (i / sumw) for i in weg]
        
        #setting the appendages
        self.appendages = []
        for j in xrange(numApp):
            self.appendages.append( Appendage(weg[int(j)], weg[int(j) + 1], weg[int(j) + 2]) )
        

