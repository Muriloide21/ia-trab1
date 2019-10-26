from hill_climbing import * 
from simulated_annealing import *
from genetic import *
import random
import math
from time import time
from deepest_descent import deepest_descent_2

TIPOS = [ (1,3), (4,6), (5,7) ]

def greedyRandomConstruct(types, maxSize, numBest, tempo):
    start = tempo
    state = [0 for x in range(len(types))] # [0 0 0]
    while True:
        if (time() - start) > 120:
            return state
        validStates = []
        expandedStates = expandState(state)
        validStates = list(
            filter(
                lambda state: stateIsValid(state, types, maxSize),
                expandedStates,
            )
        )
        
        if not validStates:
            return state
        
        kbestStates = bestStates(validStates, types, numBest) #Tá dando erro aqui pq numBest pode ser maior que o tamanho da lista de melhores
        choice = random.randint(0, len(kbestStates)-1)
        state = kbestStates[choice]

def grasp(types, maxSize, param):
    (numIter, numBest) = param
    best_state = [0 for x in range(len(types))]
    start = time()
    for _ in range(numIter):
        if (time() - start) > 120:
            return best_state
        state = greedyRandomConstruct(types, maxSize, numBest, start)
        if (time() - start) > 120:
            return best_state
        state = deepest_descent_2(types, maxSize, state)

        if stateValue(state, types) > stateValue(best_state, types):
            best_state = state
    return best_state

def greedyRandomConstruct_test(types, maxSize, numBest, tempo):
    start = tempo
    state = [0 for x in range(len(types))] # [0 0 0]
    while True:
        if (time() - start) > 300:
            return state
        validStates = []
        expandedStates = expandState(state)
        validStates = list(
            filter(
                lambda state: stateIsValid(state, types, maxSize),
                expandedStates,
            )
        )
        
        if not validStates:
            return state
        
        kbestStates = bestStates(validStates, types, numBest) #Tá dando erro aqui pq numBest pode ser maior que o tamanho da lista de melhores
        choice = random.randint(0, len(kbestStates)-1)
        state = kbestStates[choice]

def grasp_test(types, maxSize, param):
    (numIter, numBest) = param
    best_state = [0 for x in range(len(types))]
    start = time()
    for _ in range(numIter):
        if (time() - start) > 300:
            return best_state
        state = greedyRandomConstruct_test(types, maxSize, numBest, start)
        if (time() - start) > 300:
            return best_state
        state = deepest_descent_2(types, maxSize, state)

        if stateValue(state, types) > stateValue(best_state, types):
            best_state = state
    return best_state

# if __name__ == "__main__":
#     result = grasp(TIPOS, 19, 10, 2)
#     print(result)
#     print("Custo da solução: "+str(stateSize(result, TIPOS))+", Valor da solução: "+str(stateValue(result, TIPOS)))