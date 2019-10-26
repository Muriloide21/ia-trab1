from hill_climbing import *
from grasp import *
from simulated_annealing import *
from genetic import *
from beam_search import *
from itertools import product
from time import time
import seaborn as sns
import matplotlib.pyplot as plt
import statistics as st
from tabulate import tabulate

TRAIN = [
    (19, [(1,3),(4,6),(5,7)]),
    (58, [(1,3),(4,6),(5,7),(3,4)]),
    (58, [(1,3),(4,6),(5,7),(3,4),(8,10),(4,8),(3,5),(6,9)]),
    (58, [(1,3),(4,6),(5,7),(3,4),(8,10),(4,8),(3,5),(6,9),(2,1)]),
    (120, [(1,2),(2,3),(4,5),(5,10),(14,15),(15,20),(24,25),(29,30),(50,50)]),
    (120, [(1,2),(2,3),(3,5),(7,10),(10,15),(13,20),(24,25),(29,30),(50,50)]),
    (120, [(24,25),(29,30),(50,50)]),
    (138, [(1,3),(4,6),(5,7),(3,4), (2,6), (2,3), (6,8), (1,2), (2,3), (3,5), (7,10), (10,15), (13,20), (24,25),(29,30), (50,50)]),
    (13890000, [(1,3),(4,6),(5,7),(3,4), (2,6), (2,3), (6,8), (1,2),(3,5),(7,10),(10,15),(13,20),(24,25),(29,37)]),
    (45678901, [(1,3),(4,6),(5,7),(3,4),(2,6),(1,2),(3,5),(7,10),(10,15),(13,20),(15,20)] )
]

TEST = [
    (192, [(1,3),(4,6),(5,7)]),
    (287, [(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(8,9),(9,10)]),
    (120, [(1,2),(2,3),(4,5),(5,10),(14,15),(13,20),(24,25),(29,30),(50,50)]),
    (1240, [(1,2),(2,3),(3,5),(7,10),(10,15),(13,20),(24,25),(29,30),(50,50)]),
    (104, [(25,26),(29,30),(49,50)]),
    (138, [(1,3),(4,6),(5,7),(3,4), (2,6), (2,3), (6,8)]),
    (13890, [(1,3),(4,6),(5,7),(3,4), (2,6), (2,3), (6,8), (1,2), (2,3), (3,5), (7,10), (10,15), (13,20), (24,25),(29,30), (50,50)]),
    (13890, [(1,3),(4,6),(5,7),(3,4), (2,6), (2,3), (6,8), (1,2),(3,5),(7,10),(10,15),(13,20),(24,25),(29,37)]),
    (190000, [(1,3),(4,6),(5,7)]),
    (4567, [(1,3),(4,6),(5,7),(3,4),(2,6),(1,2),(3,5),(7,10),(10,15),(13,20),(15,20)])
]

# BEAM_SEARCH_HYPERPARAMETERS = [[10, 25, 50, 100]]
# SA_HYPERPARAMETERS = [[500, 100, 50], [0.95, 0.85, 0.7], [350, 500]]
# GRASP_HYPERPARAMETERS = [[50, 100, 200, 350, 500], [2, 5, 10, 15]]
# GENETIC_HYPERPARAMETERS = [[10, 20, 30], [0.75, 0.85, 0.95], [0.10, 0.20, 0.30]]

METAHEURISTICS = [ 
    ("Hill Climbing", hillClimb, [[]]),
    ("Beam Search", beam_search, [[10, 25, 50, 100]]),
    ("Simulated Annealing", simulated_annealing, [[500, 100, 50], [0.95, 0.85, 0.7], [350, 500]]),
    ("GRASP", grasp, [[50, 100, 200, 350, 500], [2, 5, 10, 15]]),
    ("Genetic", genetic, [[10, 20, 30], [0.75, 0.85, 0.95], [0.10, 0.20, 0.30]])
]

TEST_METAHEURISTICS = [
    ("Hill Climbing", hillClimb_test),
    ("Beam Search", beam_search_test),
    ("Simulated Annealing", simulated_annealing_test),
    ("GRASP", grasp_test),
    ("Genetic", genetic_test)
]

TRAINED_HYPERPARAMETERS = []

def save_plot(filename,data,x_labels):
    fig = plt.figure() #Create the figure
    
    graph = sns.boxplot(data=data,showmeans=True) #Do the boxplot
    graph.set_xticklabels(x_labels) #Label the x axe
    plt.setp(graph.get_xticklabels(),rotation = 45)

    if len(data) >= 10:
        fig.set_size_inches(14,5) #Set the size to fit all boxplots
        sns.set(font_scale=0.8) #Shrink the fontsize of the label
    
    fig.savefig('graficos/{filename}.eps', dpi=fig.dpi)

def training():
    #print("Hello World")
    hyperparameters = []
    for h in METAHEURISTICS[1:3]:
        name = h[0]
        f = h[1]
        combinations = list(product(*h[2]))
        results_per_heuristic = []
        results_per_problem = []
        for c in combinations:
            results_per_combination = []
            for t in TRAIN[:8]:
                maxSize = t[0]
                types = t[1]
                start = time()
                result = f(types, maxSize, c)
                tempo = time() - start
                print(name)
                print(stateValue(result, types), tempo)
                results_per_combination.append((stateValue(result, types), tempo))
            results_per_heuristic.append(results_per_combination)
        results_per_problem = list(zip(*results_per_heuristic))
        best_value = 0
        best_time = 100000
        results_normalized_per_problem = []
        for p in results_per_problem:
            best_value = 0
            best_time = 100000
            results_normalized = []
            for r in p: 
                if r[0] > best_value:
                    best_value = r[0]
                # if r[1] < best_time:
                #     best_time = r[1]
            for r in p:
                normal_value = r[0]/best_value
                # normal_time = best_time/r[1]
                results_normalized.append(list((normal_value, r[1])))
            results_normalized_per_problem.append(results_normalized)
        # for i in results_normalized_per_problem:
        #     print(i)
        results_normalized_per_combination = list(zip(*results_normalized_per_problem))
        #print(results_normalized_per_combination)

        combination_normalized_results = [
            (list(map(lambda result: result[0],comb_results)),combinations[i_comb])
            for i_comb,comb_results in enumerate(results_normalized_per_combination)
        ]

        data,x_labels = list(zip(*combination_normalized_results))
        save_plot(name, data, x_labels)

        # print("---------------------------------------------")
        
        mean_combinations = []
        for rc in results_normalized_per_combination:
            mean_combinations.append(st.mean(list(map(lambda x:x[0],rc))))
        #print(mean_combinations)
        mean_normalized_per_combination = list(zip(mean_combinations, combinations))
        TRAINED_HYPERPARAMETERS.append(max(mean_normalized_per_combination)[1])
        print(max(mean_normalized_per_combination))
        sorted_means = sorted(mean_normalized_per_combination)[-10:]
        #print(sorted_means)

    #print(TRAINED_HYPERPARAMETERS)

def test():
    results = []
    names = []
    mean_value_per_heuristic = []
    stdev_value_per_heuristic = []
    mean_time_per_heuristic = []
    stdev_time_per_heuristic = []
    for h in METAHEURISTICS[1:3]:       # Para cada Meta-heuristicas
        name = h[0]
        names.append(h[0])
        f = h[1]
        if(name == "Hill Climbing"):
            param = ()
        else:
            param = TRAINED_HYPERPARAMETERS.pop(0)
        results_per_heuristic = []
        for t in TEST:                  # Para cada problema do conjunto de teste       
            maxSize = t[0]
            types = t[1]
            start = time()
            result = f(types, maxSize, param) # Execução do algoritmo
            tempo = time() - start
            results_per_heuristic.append((stateValue(result,types), tempo))
            #print(maxSize)
            #print(name+" - Custo da solução: "+str(stateSize(result, types))+", Valor da solução: "+str(stateValue(result, types)))

        # Calculando média e desvio padrão dos resultados e tempos de execução
        results.append(results_per_heuristic.copy())
        results_per_heuristic_values = list(map(lambda x:x[0],results_per_heuristic))
        #print(results_per_heuristic_values)
        results_per_heuristic_times = list(map(lambda x:x[1],results_per_heuristic))
        # Média dos resultados 
        mean_value = st.mean(results_per_heuristic_values)
        mean_value_per_heuristic.append(mean_value)
        # Desvio Padrão dos resultados
        stdev_value = st.stdev(results_per_heuristic_values)
        stdev_value_per_heuristic.append(stdev_value)
        # Média dos tempos de execução
        mean_time = st.mean(results_per_heuristic_times)
        mean_time_per_heuristic.append(mean_time)
        # Desvio Padrão dos tempos de execução
        stdev_time = st.stdev(results_per_heuristic_times)   
        stdev_time_per_heuristic.append(stdev_time)         
    
    # Normalizando resultados por problema
    results_per_problem = list(zip(*results))
    # for r in results_per_problem:
    #     print(r)
    results_normalized_per_problem = []
    for r in results_per_problem:
        #print(r)
        best_value = 0
        best_time = 100000
        results_normalized = []
        for rh in r:
            #print(rh[0])
            if rh[0] > best_value:
                best_value = rh[0]
        for rh in r:
            normal_value = rh[0]/best_value
            results_normalized.append((normal_value, rh[1]))
        results_normalized_per_problem.append(results_normalized)
    # for rn in results_normalized_per_problem:
    #     print(rn)
    results_normalized_per_heuristic = list(zip(*results_normalized_per_problem))
    # for r in results_normalized_per_heuristic:
    #     print(r)
    mean_results_normalized_per_heuristic = []
    stdev_results_normalized_per_heuristic = []
    # mean_times_per_heuristic = []
    # stdev_times_per_heuristic = []
    for r in results_normalized_per_heuristic:
        normalized_values_per_heuristic = list(map(lambda x:x[0], r))
        # times_per_heuristic = list(map(lambda x:x[1], r))
        mean_results_normalized_per_heuristic.append(st.mean(normalized_values_per_heuristic))
        stdev_results_normalized_per_heuristic.append(st.stdev(normalized_values_per_heuristic))
        # mean_times_per_heuristic.append(st.mean(times_per_heuristic))
        # stdev_times_per_heuristic.append(st.stdev(times_per_heuristic))
    # print(mean_results_normalized_per_heuristic)
    # print(stdev_results_normalized_per_heuristic)
    # print(mean_times_per_heuristic)
    # print(stdev_times_per_heuristic)

    # Gerando Tabela
    table = []
    for i in range(len(TEST_METAHEURISTICS[1:3])):
        table.append([names[i], mean_time_per_heuristic[i], stdev_value_per_heuristic[i],
                     mean_time_per_heuristic[i], stdev_time_per_heuristic[i], 
                     mean_results_normalized_per_heuristic[i], stdev_results_normalized_per_heuristic[i]]
                    )
        # table.append(mean_value_per_heuristic)
        # table.append(stdev_value_per_heuristic)
        # table.append(mean_time_per_heuristic)
        # table.append(stdev_time_per_heuristic)
        # table.append(mean_results_normalized_per_heuristic)
        # table.append(stdev_results_normalized_per_heuristic)
    header = ['Metaheurística',
    'Média Absoluta','DP Absoluta',
    'Média do Tempo','DP do Tempo',
    'Média Normalizada','DP Normalizada']
    print(tabulate(table,header,stralign="center",numalign="center",tablefmt="latex"))

# training()
# print(TRAINED_HYPERPARAMETERS)
TRAINED_HYPERPARAMETERS = [(100,), (50, 0.85, 350)]
test()