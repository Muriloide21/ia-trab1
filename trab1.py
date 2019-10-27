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

METAHEURISTICS = [ 
    ("Hill Climbing", hillClimb, [[]]),
    ("Beam Search", beam_search, [[10, 25, 50, 100]]),
    ("Simulated Annealing", simulated_annealing, [[500, 100, 50], [0.95, 0.85, 0.7], [350, 500]]),
    ("GRASP", grasp, [[50, 100, 200, 350, 500], [2, 5, 10, 15]]),
    ("Genetic", genetic, [[10, 20, 30], [0.75, 0.85, 0.95], [0.10, 0.20, 0.30]])
]

TEST_METAHEURISTICS = [
    ("Hill Climbing", hillClimb_test),
    ("Beam Search", beam_search),
    ("Simulated Annealing", simulated_annealing_test),
    ("GRASP", grasp_test),
    ("Genetic", genetic_test)
]

TRAINED_HYPERPARAMETERS = []

def save_plot(filename,data,x_labels):
    fig = plt.figure() #Create the figure
    
    graph = sns.boxplot(data=data,showmeans=True) #Do the boxplot
    graph.set_xticklabels(x_labels) #Label the x axe
    plt.setp(graph.get_xticklabels(),rotation = 15)

    if len(data) >= 10:
        fig.set_size_inches(14,5) #Set the size to fit all boxplots
        sns.set(font_scale=0.8) #Shrink the fontsize of the label
    
    fig.savefig('graficos/'+filename+'.eps', dpi=fig.dpi)

def training():
    hyperparameters = []
    for h in METAHEURISTICS[4:]:
        name = h[0]
        f = h[1]
        combinations = list(product(*h[2]))
        #print(combinations)
        results_per_heuristic = []
        results_per_problem = []
        for c in combinations:
            results_per_combination = []
            for t in TRAIN:
                maxSize = t[0]
                types = t[1]
                start = time()
                result = f(types, maxSize, c)
                tempo = time() - start
                print(name+" - Custo da solução: "+str(stateSize(result, types))+", Valor da solução: "+str(stateValue(result, types)))
                print("Tempo de execução: ", tempo)
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
            for r in p:
                normal_value = r[0]/best_value
                results_normalized.append(list((normal_value, r[1])))
            results_normalized_per_problem.append(results_normalized)
        # for i in results_normalized_per_problem:
        #     print(i)
        results_normalized_per_combination = list(zip(*results_normalized_per_problem))


        combination_normalized_results = [
            (list(map(lambda result: result[0],comb_results)),combinations[i_comb])
            for i_comb,comb_results in enumerate(results_normalized_per_combination)
        ]
        #print(combination_normalized_results)
        data,x_labels = list(zip(*combination_normalized_results))
        #print(data)
        save_plot(name, data, x_labels)

        # print("---------------------------------------------")
        
        mean_combinations = []
        for rc in results_normalized_per_combination:
            mean_combinations.append(st.mean(list(map(lambda x:x[0],rc))))
        #print(mean_combinations)
        mean_normalized_per_combination = list(zip(mean_combinations, combinations))
        TRAINED_HYPERPARAMETERS.append(max(mean_normalized_per_combination)[1])
        #print(max(mean_normalized_per_combination))
        sorted_means = sorted(mean_normalized_per_combination)[-10:]
    print("Melhores hiperparâmetros - ", TRAINED_HYPERPARAMETERS)
        

def ranking(results):
    sorted_results = sorted(results, key=lambda tup: tup[1], reverse = True)
    new_format_results = []
    for s in sorted_results:
        rank_result = []
        for elem in s:
            rank_result.append(elem)
        new_format_results.append(rank_result)

    rank = []
    r = 1
    rank.append([new_format_results[0][0], new_format_results[0][1], r])
    for i in range(1, len(new_format_results)):
        if new_format_results[i-1][1] != new_format_results[i][1]:
            r = i+1
        rank.append([new_format_results[i][0], new_format_results[i][1], r])

    for i in range(1,len(rank)+1):
        empates = 0
        for r in rank:
            if(r[2] == i):
                empates += 1
        if empates == 0:
            continue
        mean = sum(range(i, i+empates))/empates
        for r in rank:
            if(r[2] == i):
                r.append(mean)
    return rank

def test():
    results = []
    names = []
    mean_value_per_heuristic = []
    stdev_value_per_heuristic = []
    mean_time_per_heuristic = []
    stdev_time_per_heuristic = []
    for h in TEST_METAHEURISTICS:       # Para cada Meta-heuristica
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
            print(name+" - Custo da solução: "+str(stateSize(result, types))+", Valor da solução: "+str(stateValue(result, types)))

        # Calculando média e desvio padrão dos resultados e tempos de execução
        results.append(results_per_heuristic.copy())
        results_per_heuristic_values = list(map(lambda x:x[0],results_per_heuristic))
        #print(results_per_heuristic_values)
        results_per_heuristic_times = list(map(lambda x:x[1],results_per_heuristic))
        print(results_per_heuristic_times)
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
    results_normalized_per_problem = []
    for r in results_per_problem:
        best_value = 0
        best_time = 100000
        results_normalized = []
        for rh in r:
            if rh[0] > best_value:
                best_value = rh[0]
        for rh in r:
            normal_value = rh[0]/best_value
            results_normalized.append((normal_value, rh[1]))
        results_normalized_per_problem.append(results_normalized)
    results_normalized_per_heuristic = list(zip(*results_normalized_per_problem))
    mean_results_normalized_per_heuristic = []
    stdev_results_normalized_per_heuristic = []
    for r in results_normalized_per_heuristic:
        normalized_values_per_heuristic = list(map(lambda x:x[0], r))
        mean_results_normalized_per_heuristic.append(st.mean(normalized_values_per_heuristic))
        stdev_results_normalized_per_heuristic.append(st.stdev(normalized_values_per_heuristic))

    # Gerando Tabela
    table = []
    for i in range(len(TEST_METAHEURISTICS[4:])):
        table.append([names[i], mean_time_per_heuristic[i], stdev_value_per_heuristic[i],
            mean_time_per_heuristic[i], stdev_time_per_heuristic[i], 
            mean_results_normalized_per_heuristic[i], stdev_results_normalized_per_heuristic[i]]
        )

    header = ['Metaheurística',
    'Média Absoluta','DP Absoluta',
    'Média do Tempo','DP do Tempo',
    'Média Normalizada','DP Normalizada']
    # DESCOMENTAR POSTERIORMENTE
    print(tabulate(table,header,stralign="center",numalign="center",tablefmt="latex"))
    rank_per_problem = []
    named_results_per_problem = []
    for r in results_per_problem:
        named_results = list(zip(names, list(map(lambda x:x[0],r))))
        rank_per_problem.append(ranking(named_results))
    # for r in rank_per_problem:
    #     print(r)

    # Ranqueamento das metaheurísticas segundo resultado absoluto
    named_means_positions = []
    for n in names:
        positions_ranks_heuristic = []
        for rank in rank_per_problem:
            for elem in rank:
                if elem[0] == n:
                    positions_ranks_heuristic.append(elem[3])

        # Obter média dos ranqueamentos das metaheurísticas segundo resultado absoluto
        mean_positions_ranks_heuristic = st.mean(positions_ranks_heuristic)
        named_means_positions.append([n, mean_positions_ranks_heuristic])

    # Apresentar as metaheurísticas em ordem crescente de média de ranqueamento
    named_means_positions = sorted(named_means_positions, key= lambda x: x[1])
    print("Médias de ranqueamento: ", named_means_positions)

    # Obter média dos resultados normalizados de cada metaheurística
    mean_results_normalized_per_heuristic = list(zip(names, mean_results_normalized_per_heuristic))
    # Apresentar as metaheurísticas em ordem crescente de média dos resultados normalizados
    mean_results_normalized_per_heuristic = sorted(mean_results_normalized_per_heuristic, key= lambda x: x[1])
    print("Médias dos resultados normalizados: ",mean_results_normalized_per_heuristic)

    # Gerar boxplot dos resultados normalizados alcançados pelas metaheurísticas
    # print(results_normalized_per_heuristic)
    values_normalized_per_heuristic = []
    times_per_heuristic = []
    for elem in results_normalized_per_heuristic:
        aux = list(map(lambda x: x[0], elem))
        aux2 = list(map(lambda x: x[1], elem))
        values_normalized_per_heuristic.append(aux)
        times_per_heuristic.append(aux2)
    # print(values_normalized_per_heuristic)
    # print(times_per_heuristic)
    #values_normalized_per_heuristic = list()
    data = values_normalized_per_heuristic
    labels = names
    save_plot("Normalized_results", data, labels)
    # Gerar boxplot dos tempos alcançados pelas metaheurísticas
    data = times_per_heuristic
    save_plot("Execution_Times", data, labels)


training()
#TRAINED_HYPERPARAMETERS = [(100,), (50, 0.85, 350)]
#test()