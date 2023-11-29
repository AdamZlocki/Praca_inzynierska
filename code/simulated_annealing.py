from main import *
from random import uniform
from numpy import exp

def simulated_anealing(graph: GraphMatrix, vehicles: List[Vehicle], num_of_iterations: int = 100,
                       num_of_attempt_on_each_temp=5, temp: float = 100, min_temp: float = 5, alfa: float = 0.98):
    counter_of_iterations = 0
    bests = []
    best = find_solution(graph=graph, vehicles=vehicles)
    bests.append(best.time)
    while counter_of_iterations < num_of_iterations and temp > min_temp:  # algorytm wykonywany do osiągniećia
        # maksymalnej liczby iteracji lub przekroczeniu minimalnej temperatury
        continue_algorithm = True
        if len(bests) > 5:  # sprawdzenie czy na przestrzeni ostatnich 5 iteracji nastąpiła znaczna poprawa jakości
            # rozwiązań (minimum 15 minut zysku)
            if not abs(bests[-1] - bests[-5]) > 0.25:
                continue_algorithm = False
        if not continue_algorithm:  # jeśli nie było poprawy przerywamy algorytm
            break
        else:  # jeśli jest poprawa - kontynuacja danej iteracji
            attempts = 0
            while attempts < num_of_attempt_on_each_temp:
                new_solution = neighbourhood(graph=graph, solution=best, size=1)
                if new_solution < best:
                    best = new_solution
                else:
                    prob_of_choosing_new_sol = exp(abs(new_solution.time - best.time) / temp)
                    if prob_of_choosing_new_sol > uniform(0, 1):
                        best = new_solution
                attempts += 1
            temp *= alfa
            counter_of_iterations += 1
            bests.append(best)
    return best, bests
