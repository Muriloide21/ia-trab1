from hill_climbing import *
from grasp import grasp
from simulated_annealing import *
from genetic import genetic
from beam_search import beam_search
from itertools import product
from time import time

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

def training():
    for h in METAHEURISTICS[1:2]:
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
                if r[1] < best_time:
                    best_time = r[1]
            for r in p:
                normal_value = r[0]/best_value
                normal_time = r[1]/best_time
                results_normalized.append(list((normal_value, normal_time)))
            results_normalized_per_problem.append(results_normalized)
        for i in results_normalized_per_problem:
            print(i)

        
            

training()