from hill_climbing import *

TIPOS = [ (1,3), (4,6), (5,7) ]

def beam_search(types, max_size, m):
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

    while True:
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
            return f.pop(0)

        aux.sort(key=lambda x: stateValue(x, types))
        #print(aux)

        f = []
        for i in range(0,m):
            f.append(aux.pop())
            if len(aux) == 0:
                break

        #print(f)

if __name__ == "__main__":
    result = beam_search(TIPOS, 19, 2)
    print(result)
    print("Custo da solução: "+str(stateSize(result, TIPOS))+", Valor da solução: "+str(stateValue(result, TIPOS)))
    


    
