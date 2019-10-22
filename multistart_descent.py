from hill_climbing import *
from simple_descent import *
from deepest_descent import *

TIPOS = [ (1,3), (4,6), (5,7) ]

def multistart_descent(types, max_size, max_iter):
    aux = 1
    state = [0 for i in types]
    best_state = [0 for i in types]
    while aux <= max_iter:
        neighbor = getNeighbor(best_state, types, max_size)
        
        coin = random.randint(0,1)
        if coin == 0:
            state = simple_descent(types, max_size, neighbor)
        else:
            state = deepest_descent(types, max_size, neighbor)
        
        if stateValue(state, types) > stateValue(best_state, types):
            best_state = state
        
        aux += 1
    return best_state

if __name__ == "__main__":
    result = multistart_descent(TIPOS, 19, 10)
    print(result)
    print("Custo da solução: "+str(stateSize(result, TIPOS))+", Valor da solução: "+str(stateValue(result, TIPOS)))