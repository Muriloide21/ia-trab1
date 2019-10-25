from hill_climbing import * 
import random
import math
from time import time

TIPOS = [ (1,3), (4,6), (5,7) ]


def probability(state, neighbor, types, t):
    exponent = (-(stateValue(state, types) - stateValue(neighbor, types))) / t
    #print(exponent)
    probability = math.exp(exponent)
    return probability

def simulated_annealing(types, maxsize, param):
    (t, alpha, numiter) = param
    best = hillClimb(TIPOS, maxsize)
    state = [0 for i in types]
    t_min = t/20
    start = time()
    while t > t_min and ((time() - start) < 120): 
        for _ in range(0, numiter):
            neighbor = getNeighbor(state, types, maxsize)
            if stateValue(neighbor, types) > stateValue(state, types):
                state = neighbor
                if stateValue(state, types) > stateValue(best, types):
                    best = state
            else:
                prob = probability(state, neighbor, types, t)
                aux = prob*100
                if random.randint(0,100) < aux:
                    state = neighbor
        t = alpha*t
    return best

def simulated_annealing_2(types, maxsize, numiter, t, nmax, initial):
    trivial = hillClimb(TIPOS, maxsize)
    alpha = random.random()
    state = initial
    for j in range(0, nmax):
        for i in range(0, numiter):
            neighbor = getNeighbor(state, types, maxsize)
            if stateValue(neighbor, types) > stateValue(state, types):
                state = neighbor
                if stateValue(state, types) > stateValue(trivial, types):
                    trivial = state
            else:
                prob = probability(state, neighbor, types, t)
                aux = prob*100
                if random.randint(0,100) < aux:
                    state = neighbor
        t = alpha*t
    return state

# if __name__ == "__main__":
#     result = simulated_annealing(TIPOS, 5000, 100, 100, 100)
#     print(str(result))
#     print("Custo da solução: "+str(stateSize(result, TIPOS))+", Valor da solução: "+str(stateValue(result, TIPOS)))
