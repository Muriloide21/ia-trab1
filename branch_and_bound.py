from hill_climbing import *
import math

TIPOS = [ (1,3), (4,6), (5,7) ]

def estimate(state, types, best_type, max_size):
    available_space = max_size - stateSize(state, types)
    qtd_items = available_space / best_type[1]
    qtd_items = math.ceil(qtd_items)
    aux = qtd_items*best_type[0]
    estimative = stateValue(state, types) + aux
    return estimative

def get_ratio(type):
    ratio = type[0] / type[1]
    return ratio

def branch_and_bound(types, max_size):

    queue = []
    initial = hillClimb(TIPOS, 19)
    queue.append([0 for i in types])
    state = []
    best_type = max(types, key=lambda x: get_ratio(x))
    #print(best_type)

    while len(queue) > 0:
        validStates = []
        state = queue.pop(0)
        expandedStates = expandState(state)
        validStates = list(
            filter(
                lambda state: stateIsValid(state, types, max_size),
                expandedStates,
            )
        )

        if not validStates:
            return queue.pop()

        bestStates = list(
            filter(
                lambda x:(estimate(x,types,best_type, max_size) > stateValue(initial, types)),
                validStates,
            )
        )
        
        # print(bestStates)
        # print(queue)
        queue += bestStates
        queue.sort(key=lambda x: stateValue(x, types))


if __name__ == "__main__":
    result = branch_and_bound(TIPOS, 19)
    print(result)
    print("Custo da solução: "+str(stateSize(result, TIPOS))+", Valor da solução: "+str(stateValue(result, TIPOS)))

