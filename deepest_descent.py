from hill_climbing import *

TIPOS = [ (1,3), (4,6), (5,7) ]

def deepest_descent(types, max_size, state):
    best_state = state
    #print(best_state)
    while True:
        validStates = []
        expandedStates = expandState(best_state)
        validStates = list(
            filter(
                lambda state: stateIsValid(state, types, max_size),
                expandedStates,
            )
        )

        if not validStates:
            return best_state

        validStates.sort(key=lambda x: stateValue(x, types))

        best_state = validStates.pop()

def deepest_descent_2(types, max_size, state):
    best_state = state
    #print(best_state)
    while True:
        validStates = []
        expandedStates = neighborhood(best_state)
        validStates = list(
            filter(
                lambda state: stateIsValid(state, types, max_size),
                expandedStates,
            )
        )

        # if not validStates:
        #     return best_state

        validStates.sort(key=lambda x: stateValue(x, types))

        aux = validStates.pop()
        if(stateValue(best_state,types) >= stateValue(aux,types)):
            return best_state
        
        best_state = aux
        
        
# if __name__ == "__main__":
#     result = deepest_descent(TIPOS, 19, [0,0,0])
#     print(str(result)+" - Deepest Descent")
#     print("Custo da solução: "+str(stateSize(result, TIPOS))+", Valor da solução: "+str(stateValue(result, TIPOS)))