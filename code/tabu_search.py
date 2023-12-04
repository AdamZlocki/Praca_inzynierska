from main import *


def tabu_search(graph: GraphMatrix, vehicles: List[Vehicle], num_of_iterations: int = 100, max_Tabu_size: int = 8,
                num_of_neighbours: int = 10, switch_in_all_routes=False):
    tabu_list = []
    bests = []
    best = find_solution(graph=graph, vehicles=vehicles)
    counter_of_iterations = 0

    while counter_of_iterations < num_of_iterations:
        best_neighbourhood = neighbourhood(graph=graph, solution=best, size=num_of_neighbours,
                                           switch_in_all_routes=switch_in_all_routes)
        top_neighbour = None

        while not top_neighbour:
            if min(best_neighbourhood) not in tabu_list:
                top_neighbour = min(best_neighbourhood)
            else:
                best_neigh_idx = best_neighbourhood.index(min(best_neighbourhood))
                best_neighbourhood.pop(best_neigh_idx)

        if top_neighbour < best:
            best = top_neighbour

        tabu_list.append(top_neighbour)

        if len(tabu_list) > max_Tabu_size:
            tabu_list.pop(0)

        counter_of_iterations += 1

    return best, bests
