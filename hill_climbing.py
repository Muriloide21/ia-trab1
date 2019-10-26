#!/bin/env python3

import random
from time import time

# (valor, tamanho)

TIPOS = [ (1,3), (4,6), (5,7) ]

def stateValue(state, types):
    return sum((e * tp[0]) for (e, tp) in zip(state, types))

def stateSize(state, types):
    return sum((e * tp[1]) for (e, tp) in zip(state, types))

def stateIsValid(state, types, max_size):
    return stateSize(state, types) <= max_size

def newListWithValueAt(lst, pos, value):
    newList = lst.copy()
    newList[pos] = value
    return newList

def expandState(state):
    return [ newListWithValueAt(state, i, state[i]+1) for i in range(len(state)) ]

def isPositiveState(state):
    for i in range(len(state)):
        if state[i] < 0:
            return False
    return True

def regressState(state):
    regression = [ newListWithValueAt(state, i, state[i]-1) for i in range(len(state)) ]
    regression = list(filter(isPositiveState, regression))
    return regression

def neighborhood(state):
    expandedStates = expandState(state)
    regressionStates = regressState(state)
    newStates = expandedStates + regressionStates
    return newStates

def getNeighbor(state, types, maxsize):
    newStates = neighborhood(state)
    newStates = list(filter(lambda x: stateIsValid(x, types, maxsize), newStates))
    aux = random.randint(0,len(newStates)-1)
    neighbor = newStates[aux]

    return neighbor

def hillClimb(types, max_size, param):
    _ = param
    state = [0 for i in types]
    start = time()
    while (time() - start) < 300:

        newStates = expandState(state)
        validStates = list(
            filter(
                lambda state: stateIsValid(state, types, max_size),
                newStates,
            )
        )

        if not validStates:
            return bestState

        statesWithValues = []
        for st in validStates:
            statesWithValues.append( (st, stateValue(st, types)) )

        (bestState, _) = max( statesWithValues, key=lambda st: st[1] )
        #print(bestState)

        state = bestState
    return bestState


# if __name__ == "__main__":
#     result = hillClimb(TIPOS, 19)
#     print(result)
#     print("Custo da solução: "+str(stateSize(result, TIPOS))+", Valor da solução: "+str(stateValue(result, TIPOS)))