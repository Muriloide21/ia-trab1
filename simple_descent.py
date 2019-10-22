from hill_climbing import *
import random

TIPOS = [ (1,3), (4,6), (5,7) ]

def simple_descent(types, max_size, state):
    best_state = state
    while True:
        expandedStates = expandState(best_state)
        validStates = list(
            filter(
                lambda state: stateIsValid(state, types, max_size),
                expandedStates,
            )
        )

        if not validStates:
            return best_state

        #Seleciona aleatoriamente um vizinho
        aux = random.randint(0,len(validStates)-1)
        neighbor = validStates.pop(aux)
        best_state = neighbor
        
        
if __name__ == "__main__":
    result = simple_descent(TIPOS, 19, [0,0,0])
    print(str(result)+" - Simple Descent")
    print("Custo da solução: "+str(stateSize(result, TIPOS))+", Valor da solução: "+str(stateValue(result, TIPOS)))
