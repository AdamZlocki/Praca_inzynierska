from main import *


def bee_algorythm(graph: GraphMatrix, vehicles: List[Vehicle], num_of_iterations: int = 10, size_of_iteration: int = 10,
                  num_of_elite: int = 2, num_of_bests: int = 3, size_of_neighbourhood_elite: int = 10,
                  size_of_neighbourhood_best: int = 5, max_LT: int = 3, switch_in_all_routes=False):
    """
    :param graph: graf reprezentujący klinetów i zajezdnię
    :param vehicles: lista pojazdów
    :param num_of_iterations: liczba iteracji
    :param size_of_iteration: liczba rozwiązań rozważanych w danej iteracji
    :param num_of_elite: liczba rozwiązań elitarnych
    :param num_of_bests: liczba rozwiązań najlepszych (gorsze)
    :param size_of_neighbourhood_elite: rozmiar sąsiedztwa rozwiązań elitarnych
    :param size_of_neighbourhood_best: rozmiar sąsiedztwa rozwiązań najlepszych
    :param max_LT: maksymalny czas życia rozwiązania
    :param switch_in_all_routes: wybór czy przy szukaniu sąsiadów zmieniamy ścieżkę dla jednego pojazdu (False) czy
                                 wszystkich (True)
    :return: best - najlepsze rozwiązanie; bests - lista kosztów najlepszych rozwiązań po danej iteracji
    """
    solutions = []
    counter_of_iterations = 0
    bests = []
    best = 0
    while counter_of_iterations < num_of_iterations:  # dopóki nie wykonano oczekiwanej liczby iteracji powtarzamy
        if solutions:  # w przypadku gdy coś znajduje się w liście rozwiązań - usunięcie rozwiązń, które przekroczyły
            # maksymalną długość życia
            for solution in solutions:
                if solution.LT > max_LT:
                    solutions.remove(solution)

        while len(solutions) < size_of_iteration:  # utworzenie zadanej ilości początkowych rozwiązań
            sol = find_solution(graph=graph, vehicles=vehicles)
            if sol not in solutions:
                solutions.append(sol)

        solutions_sorted = []  # posortowanie rozwiązań i zapamiętanie najlepszego
        while len(solutions_sorted) < size_of_iteration:
            solutions_sorted.append(solutions.pop(solutions.index(min(solutions))))
        solutions = solutions_sorted.copy()

        if not best:
            best = solutions[0]
        else:
            if solutions[0] < best:
                best = solutions[0]

        elite_solutions = []  # utworzenie listy rozwiązań elitarnych
        while len(elite_solutions) < num_of_elite:
            elite_solutions.append(solutions.pop(solutions.index(min(solutions))))

        best_solutions = []  # utworzenie listy rozwiązań najlepszych (gorsze od elitarych)
        while len(best_solutions) < num_of_bests:
            best_solutions.append(solutions.pop(solutions.index(min(solutions))))

        for solution in elite_solutions:  # utworzenie sąsiedztwa rozwiązań elitarnych i ewentualne zastąpienie ich ich
            # najlepszymi sąsiadami
            solution.neighbourhood = []
            solution.neighbourhood = neighbourhood(graph=graph, solution=solution, size=size_of_neighbourhood_elite,
                                                   switch_in_all_routes=switch_in_all_routes)
            best_neighbour = solution.neighbourhood[solution.neighbourhood.index(min(solution.neighbourhood))]
            if best_neighbour < solution:
                elite_solutions[elite_solutions.index(solution)] = best_neighbour

        for solution in best_solutions:  # utworzenie sąsiedztwa rozwiązań najlepszych i ewentualne zastąpienie ich ich
            # najlepszymi sąsiadami
            solution.neighbourhood = []
            solution.neighbourhood = neighbourhood(graph=graph, solution=solution, size=size_of_neighbourhood_best,
                                                   switch_in_all_routes=switch_in_all_routes)
            best_neighbour = solution.neighbourhood[solution.neighbourhood.index(min(solution.neighbourhood))]
            if best_neighbour < solution:
                best_solutions[best_solutions.index(solution)] = best_neighbour

        solutions = elite_solutions + best_solutions

        solutions_sorted = []  # posortowanie rozwiązań i zapamiętanie najlepszgo
        while len(solutions_sorted) < num_of_bests + num_of_elite:
            solutions_sorted.append(solutions.pop(solutions.index(min(solutions))))
        solutions = solutions_sorted.copy()
        if solutions[0] < best:
            best = solutions[0]

        for solution in solutions:
            solution.LT += 1

        counter_of_iterations += 1
        bests.append(best.cost)

    return best, bests
