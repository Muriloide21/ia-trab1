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
    statesList.sort(key=lambda x: stateValue(x, types))
    #print(statesList)
    bestStates = []
    while(k > 0):
        bestStates.append(statesList.pop())
        k -= 1
    return bestStates

def genetic(types, maxSize, populationSize, maxGen, crossRate, mutationRate): #maxGen, populationSize):
    population = [randomState(types, maxSize) for x in range(populationSize)]
    #print(population)
    #populationValues = [stateValue(x, types) for x in population]
    #print(parentStates)
    #inert = 0
    while(maxGen > 0): #and inert < 5):
        # elitismo de 10%
        #best_States = []
        elit = 1
        best_States = bestStates(population.copy(), types, elit)

        #Parent Selection
        parentStates = bestStates(population.copy(), types, (len(population)))
        #print(parentStates)
        parentValues = [stateValue(x, types) for x in parentStates]
        #print(parentValues)
        total = sum(parentValues)
        #print(total)
        ratio = [(x/total) for x in parentValues]
        #print(ratio)
        for i in range(len(ratio)-1):
            ratio[i] = sum(ratio[i:])
        population = []
        ratio.reverse()
        parentStates.reverse()
        #print(ratio)
        for _ in range(populationSize - elit):
            prob = random.random()
            for i in range(len(ratio)-1):
                if(prob <= ratio[i]):
                    #print("Cheguei aqui")
                    population.append(parentStates[i].copy())
                    break
        print(population)
        
        #Crossover
        for i in range(len(population)-1):
            prob = random.random()
            #print(prob)
            if prob < crossRate:
                print("Fazendo crossover")
                auxState = random.randint(0, len(population)-1)
                itemIndex = random.randint(0, len(types)-1)
                aux = population[auxState][itemIndex]
                # print(population[auxState])
                # print(population[i])
                # print(itemIndex)
                population[auxState][itemIndex] = population[i][itemIndex]
                population[i][itemIndex] = aux
                # print(population[i])
                # print(population[auxState])
        
        #Mutation
        for i in range(len(population)-1):
            prob = random.random()
            #print(prob)
            if prob < mutationRate:
                print("Fazendo mutação")
                item = random.randint(0, len(types)-1)
                print(item)
                print(population[i])
                radioactivity = math.floor(maxSize/getTypeSize(types[item]))
                population[i][item] = random.randint(1, radioactivity)
                print(population[i])

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
        maxGen -= 1
        print(population, maxGen)
        #values = [stateValue(x, types) for x in population]
        # if max(values) <= max(parentValues):
        #     inert += 1

    best_State = bestStates(population, types, 1)[0]
    return best_State
        

nha = genetic(TIPOS, 19, 10, 20, 0.95, 0.1)
value = stateValue(nha, TIPOS)
print("Best state: ", nha, value)
