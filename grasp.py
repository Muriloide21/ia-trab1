from hill_climbing import * 
from simulated_annealing import *
from genetic import *
import random
import math

TIPOS = [ (1,3), (4,6), (5,7) ]

def greedyRandomConstruct(types, maxSize, numBest):
    state = [0 for x in range(len(types))] # [0 0 0]
    while True:
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

def grasp(types, maxSize, numIter, numBest):
    best_state = [0 for x in range(len(types))]
    for _ in range(numIter):
        state = greedyRandomConstruct(types, maxSize, numBest)
        state = simulated_annealing_2(types, maxSize, 10, 20, 30, state)
        if stateValue(state, types) > stateValue(best_state, types):
            best_state = state
    return best_state

if __name__ == "__main__":
    result = grasp(TIPOS, 19, 10, 2)
    print(result)
    print("Custo da solução: "+str(stateSize(result, TIPOS))+", Valor da solução: "+str(stateValue(result, TIPOS)))