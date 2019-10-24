from hill_climbing import * 
import random
import math

TIPOS = [ (1,3), (4,6), (5,7) ]

def getTypeValue(t):
    return t[0]

def getTypeSize(t):
    return t[1]

def randomState(types, maxSize):
    state = [0]*len(types)
    randNum = random.randint(0,len(types)-1)
    maxItem = math.floor(maxSize/getTypeSize(types[randNum]))
    state[randNum] += random.randint(1,maxItem)
    return state

def bestStates(statesList, types, k):
    statesList.sort(key=lambda x: stateValue(x, types), reverse = True)
    #print(statesList)
    bestStates = statesList[:k]
    return bestStates

def genetic(types, maxSize, params): #maxGen, populationSize):
    (populationSize, crossRate, mutationRate) = params
    population = [randomState(types, maxSize) for x in range(populationSize)]
    inert = 0
    while inert < 5:
        elit = 1
        best_States = bestStates(population.copy(), types, elit)

        #Parent Selection
        parentStates = bestStates(population.copy(), types, (len(population)))
        parentValues = [stateValue(x, types) for x in parentStates]
        total = sum(parentValues)
        ratio = [(x/total) for x in parentValues]
        for i in range(len(ratio)-1):
            ratio[i] = sum(ratio[i:])
        population = []
        ratio.reverse()
        parentStates.reverse()
        for _ in range(populationSize - elit):
            prob = random.random()
            for i in range(len(ratio)-1):
                if(prob <= ratio[i]):
                    population.append(parentStates[i].copy())
                    break
        
        #Crossover
        for i in range(len(population)-1):
            prob = random.random()
            if prob < crossRate:
                auxState = random.randint(0, len(population)-1)
                itemIndex = random.randint(0, len(types)-1)
                aux = population[auxState][itemIndex]
                population[auxState][itemIndex] = population[i][itemIndex]
                population[i][itemIndex] = aux
        
        #Mutation
        for i in range(len(population)-1):
            prob = random.random()
            if prob < mutationRate:
                item = random.randint(0, len(types)-1)
                radioactivity = math.floor(maxSize/getTypeSize(types[item]))
                population[i][item] = random.randint(1, radioactivity)

        #Filtrando a nova população, adicionando a elite e substituindo os inviáveis
        population = list(
            filter(
                lambda state: stateIsValid(state, types, maxSize),
                population,
            )
        )
        population += best_States
        left_space = populationSize - len(population)
        for i in range(left_space):
            population.append(randomState(types, maxSize)) 
        parentStates.reverse()

        values = [stateValue(x, types) for x in population]
        if max(values) >= max(parentValues):
            inert = 0
        else:
            inert += 1

    best_States = bestStates(population, types, 1)
    #print("Best States:", best_States)
    return best_States[0]
        

#nha = genetic(TIPOS, 19, 10, 20, 0.95, 0.1)
# if __name__ == "__main__":
#     result = genetic(TIPOS, 19, 10, 20, 0.95, 0.1)
#     print(result)
#     print("Custo da solução: "+str(stateSize(result, TIPOS))+", Valor da solução: "+str(stateValue(result, TIPOS)))
