from hill_climbing import *
from time import time

TIPOS = [ (1,3), (4,6), (5,7) ]

def beam_search(types, max_size, param):
    (m, ) = param
    f = []
    state = [0 for i in types]
    newStates = expandState(state)

    validStates = list(
        filter(
            lambda state: stateIsValid(state, types, max_size),
            newStates,
        )
    )

    validStates.sort(key=lambda x: stateValue(x, types))
    #print(validStates)

    for i in range(0,m):
        f.append(validStates.pop())
        if len(validStates) == 0:
            break
    
    #print(f)
    start = time()
    best = [0 for x in range(len(types))]
    while (time() - start < 120):
        aux = []
        
        for i in range(0, len(f)):
            validStates = []
            newStates = expandState(f[i])

            validStates = list(
                filter(
                    lambda state: stateIsValid(state, types, max_size),
                    newStates,
                )
            )
            aux += validStates

        if not aux:
            break  

        aux.sort(key=lambda x: stateValue(x, types))
        #print(aux)

        f = []
        for i in range(0,m):
            f.append(aux.pop())
            if len(aux) == 0:
                break
        if stateValue(best,types) < stateValue(f[0],types):
            best = f[0]

        #print(f)
    return best

def beam_search_test(types, max_size, param):
    (m, ) = param
    f = []
    state = [0 for i in types]
    newStates = expandState(state)

    validStates = list(
        filter(
            lambda state: stateIsValid(state, types, max_size),
            newStates,
        )
    )

    validStates.sort(key=lambda x: stateValue(x, types))
    #print(validStates)

    for i in range(0,m):
        f.append(validStates.pop())
        if len(validStates) == 0:
            break
    
    #print(f)
    start = time()
    best = [0 for x in range(len(types))]
    while (time() - start < 300):
        aux = []
        
        for i in range(0, len(f)):
            validStates = []
            newStates = expandState(f[i])

            validStates = list(
                filter(
                    lambda state: stateIsValid(state, types, max_size),
                    newStates,
                )
            )
            aux += validStates

        if not aux:
            break  

        aux.sort(key=lambda x: stateValue(x, types))
        #print(aux)

        f = []
        for i in range(0,m):
            f.append(aux.pop())
            if len(aux) == 0:
                break
        if stateValue(best,types) < stateValue(f[0],types):
            best = f[0]

        #print(f)
    return best

# if __name__ == "__main__":
#     result = beam_search(TIPOS, 19, (2,))
#     print(result)
#     print("Custo da solução: "+str(stateSize(result, TIPOS))+", Valor da solução: "+str(stateValue(result, TIPOS)))
    


    
