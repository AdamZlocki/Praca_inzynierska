from random import choice, randint
from typing import Dict, List


class Vertex:  # wierzchołek - reprezentowany przez id, informuje o swoim zapotrzebowaniu i okanch czasowych
    def __init__(self, Id, time_window: tuple, is_base=False):
        if not is_base:
            self.Id = Id
            self.visited = 0
            self.time_window = time_window
        else:
            self.Id = 0
            self.name = "Base"

    def __eq__(self, other):
        if self.Id == other.Id:
            return True
        else:
            return False

    def __repr__(self):
        if self.Id != 0:
            return f"{self.Id}, {self.time_window}"
        else:
            return f"{self.Id}"

    def __hash__(self):
        return hash(self.Id)


class Edge:  # połączenie między wierzchołkami; reprezentuje czas przejazdu
    def __init__(self, start, end, time: float = 0):
        self.start = start
        self.end = end
        self.time = time

    def __eq__(self, other):
        if self.start == other.start and self.end == other.end:
            return True
        else:
            return False

    def __repr__(self):
        return f"({self.start} -- {self.time} --> {self.end})"


class Vehicle:  # pojazd; reprezentowany przez id i informuje ile czasu może jeździć do wykonania serwisu
    def __init__(self, Id, free_at=6):
        self.Id = Id
        self.free_at = free_at
        self.service_time = 0

    def __eq__(self, other):
        if self.Id == other.Id:
            return True
        else:
            return False

    def reset_free_at(self):
        self.free_at = 6


class GraphMatrix:
    def __init__(self):
        self.list = []
        self.dict = {}
        self.matrix: List[List[Edge or int]] = [[]]

    def insertVertex(self, vertex: Vertex):
        self.list.append(vertex)
        self.dict[vertex] = self.order() - 1
        if self.order() != 1:
            for i in range(len(self.matrix)):
                self.matrix[i].append(0)
            self.matrix.append([0] * len(self.matrix[0]))
        else:
            self.matrix[0].append(0)

    def insertEdge(self, vertex1_idx: int, vertex2_idx: int, edge: Edge):
        if vertex1_idx is not None and vertex2_idx is not None and edge is not None:
            self.matrix[vertex1_idx][vertex2_idx] = edge

    # def deleteVertex(self, vertex):
    #     vertex_idx = self.getVertexIdx(vertex)
    #     for i in range(self.order()):
    #         if i != vertex_idx:
    #             self.matrix[i].pop(vertex_idx)
    #     self.matrix.pop(vertex_idx)
    #     self.list.pop(vertex_idx)
    #     self.dict.pop(vertex)
    #     for i in range(vertex_idx, self.order()):
    #         actual = self.list[i]
    #         self.dict[actual] -= 1
    #
    # def deleteEdge(self, vertex1, vertex2):
    #     vertex1_idx = self.getVertexIdx(vertex1)
    #     vertex2_idx = self.getVertexIdx(vertex2)
    #     for i in range(len(self.matrix[vertex1_idx])):
    #         if self.matrix[vertex1_idx][vertex2_idx] != 0:
    #             self.matrix[vertex1_idx][vertex2_idx] = 0

    def getVertexIdx(self, vertex):
        return self.dict[vertex]

    def getVertex(self, vertex_idx) -> Vertex:
        return self.list[vertex_idx]

    def neighbours(self, vertex_idx) -> List[int]:  # zwraca indeksy w macierzy sąsiadów wybranego wierzchołka
        result = []
        for i in range(len(self.matrix[vertex_idx])):
            if self.matrix[vertex_idx][i]:
                result.append(i)
        return result

    def order(self):
        return len(self.list)

    def size(self):
        result = 0
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                if self.matrix[i][j] != 0:
                    result += 1
        return result

    def edges(self):
        result = []
        for i in range(self.order()):
            for j in range(self.order()):
                if self.matrix[i][j]:
                    result.append(self.matrix[i][j])
        return result


class Solution:
    def __init__(self, routes: Dict[Vehicle, List[int]], waiting_times: Dict[Vehicle, Dict[int, float]], time=0,
                 LT: int = 0):
        self.routes = routes  # zakładając że mamy więcej pojazdów niż 1 - kluczami w słowniku są id pojazdów,
        # a wartościami listy obsłużonych wierzchołków/pokonanych krawędzi
        self.time = time
        self.waiting_times = waiting_times
        self.LT = LT

    def __eq__(self, other):
        if self.time == other.time:
            if self.routes == other.routes:
                return True
            else:
                return False
        else:
            return False

    def __repr__(self):
        return f"{self.routes}, {self.time}"

    def __gt__(self, other):
        if self.time > other.time:
            return True
        else:
            return False


def calc_solution_time(times: dict) -> int:
    return max(times.values())


def calc_vehicle_time(vehicle: Vehicle, edges, waiting_times) -> float:  # czas = ilość wierzchołków * czas serwisu +
    # łączny czas oczekiwania + łączny czas krawędzi
    time = len(edges) * vehicle.service_time + sum(waiting_times.values())
    for edge in edges:
        time += edge.time
    return time


def is_matrix_square(matrix):
    N = len(matrix)
    for row in range(N):
        if len(matrix[row]) != N:
            return False
    return True


def is_matrix_symetrical(matrix):
    N = len(matrix)
    for i in range(N):
        for j in range(N):
            if matrix[i][j] != matrix[j][i]:
                return False
    return True


def has_matrix_0_diagonal(matrix):
    N = len(matrix)
    for i in range(N):
        if matrix[i][i] != '0':
            return False
    return True


def all_visited(graph: GraphMatrix):
    result = True
    for vertex in graph.list:
        if vertex.visited == 0:
            result = False
            break
    return result


def find_solution(graph: GraphMatrix,
                  vehicles: List[Vehicle]):  # vehicles - lista ID pojazdów !!!!DONE dla jednego dnia!!!!
    routes: Dict[Vehicle, list] = {}
    edges: Dict[Vehicle, list] = {}
    currents: Dict[Vehicle, int] = {}
    times: Dict[Vehicle, float] = {}
    waiting_times: Dict[Vehicle, Dict[int, float]] = {}
    for vehicle in vehicles:  # inicjalizacja list dla każdego pojazdu w słownikach
        routes[vehicle] = [0]
        edges[vehicle] = []
        currents[vehicle] = 0
        times[vehicle] = 0
        waiting_times[vehicle] = {}

    while not all_visited(graph):  # pętla wykonywana dopóki nie wszystkie wierzchołki są odwiedzone
        for vehicle in vehicles:
            current = currents[vehicle]

            neighbours = graph.neighbours(current)  # wyszukanie sąsiadów i usunięcie wierzchołka Bazy
            if 0 in neighbours:
                neighbours.remove(0)

            neighbours_to_delete = []  # wyszukanie już odwiedzonych sąsiadów lub sąsiadów z niepasującym oknem czasowym
            for neigh in neighbours:
                edge_time = graph.matrix[current][neigh].time
                neigh_Vertex = graph.getVertex(neigh)
                time_at_place = vehicle.free_at + edge_time
                if neigh_Vertex.visited == 1 or not (time_at_place < neigh_Vertex.time_window[1]):
                    neighbours_to_delete.append(neigh)

            for neigh in neighbours_to_delete:  # usunięcie niedozwolonych sąsiadów
                neighbours.remove(neigh)

            if len(neighbours):  # jeśli zostali jeszcze jacyś sąsiedzi wylosowanie nastepnego wierzchołka
                neighbour = choice(neighbours)
                neigh_Vertex = graph.getVertex(neighbour)
                edge_time = graph.matrix[current][neighbour].time
                time_at_place = vehicle.free_at + edge_time
                if time_at_place < neigh_Vertex.time_window[
                    0]:  # sprawdzenie czy pojazd nie przyjedzie przed rozpoczęciem okna czasowego
                    waiting_times[vehicle][neighbour] = neigh_Vertex.time_window[0] - time_at_place
                else:
                    waiting_times[vehicle][neighbour] = 0
                graph.getVertex(neighbour).visited = 1
                vehicle.free_at += edge_time + vehicle.service_time + waiting_times[vehicle][neighbour]
            else:  # jeśli nie -> wybranie 0 i powrót do bazy
                neighbour = 0

            edges[vehicle].append(graph.matrix[current][neighbour])  # aktualizacja tablic dla danego pojazdu
            routes[vehicle].append(neighbour)
            currents[vehicle] = neighbour

    for vehicle in vehicles:
        times[vehicle] = calc_vehicle_time(vehicle=vehicle, edges=edges[vehicle], waiting_times=waiting_times[vehicle])

    time = calc_solution_time(times)

    solution = Solution(routes=routes, time=time, waiting_times=waiting_times)

    for vertex in graph.list[1:]:  # reset grafu i pojazdów
        vertex.visited = 0
    for vehicle in vehicles:
        vehicle.reset_free_at()

    return solution


def neighbourhood(graph: GraphMatrix, solution: Solution, size: int = 5, switch_in_all_routes=False):
    neighbours: List[Solution] = []
    if not switch_in_all_routes:  # zamiana kolejności wierzchołków na trasie jednego pojazdu
        vehicle = choice(list(solution.routes.keys()))
        route = solution.routes[vehicle]
        new_waiting_times = solution.waiting_times.copy()
        n = len(route)
        while len(neighbours) < size:  # pętla powtarzana do utworzenia oczekiwanej liczby sąsiadów
            a, b = 0, 0
            while a == b:  # wylosowanie punktów do podmiany
                a, b = randint(1, n - 1), randint(1, n - 1)

            new_route = route.copy()  # podmiana wybranych wierzchołków
            new_route[a], new_route[b] = new_route[b], new_route[a]

            new_edges: List[Edge] = []  # utworzenie nowej listy krawędzi
            for i in range(1, len(new_route)):
                vertex_idx1 = new_route[i - 1]
                vertex_idx2 = new_route[i]
                new_edges.append(graph.matrix[vertex_idx1][vertex_idx2])

            vehicle_route_is_fine = True  # sprawdzenie czy nadal pojazd przyjeżdża o odpowiedniej porze
            vehicle.reset_free_at()
            for i in range(1, len(new_route)):
                edge_time = new_edges[i - 1].time
                next_Vertex = graph.getVertex(new_route[i])
                time_at_place = vehicle.free_at + edge_time
                if not (time_at_place < next_Vertex.time_window[1]):  # pojazd przyjeżdża zbyt późno
                    vehicle_route_is_fine = False
                    break
                else:
                    if time_at_place < next_Vertex.time_window[0]:  # pojazd przyeżdża zbyt wcześnie
                        new_waiting_times[vehicle][new_route[i]] = next_Vertex.time_window[0] - time_at_place
                    else:  # pojazd przyjeżdża w oknie czasowym
                        new_waiting_times[vehicle][new_route[i]] = 0
                    vehicle.free_at += edge_time + vehicle.service_time + new_waiting_times[vehicle][new_route[i]]

            if vehicle_route_is_fine:
                new_time = calc_vehicle_time(vehicle=vehicle, edges=new_edges,
                                             waiting_times=new_waiting_times) if calc_vehicle_time(vehicle=vehicle,
                                                                                                   edges=new_edges,
                                                                                                   waiting_times=
                                                                                                   new_waiting_times[
                                                                                                       vehicle]) > solution.time else solution.time
                routes = solution.routes.copy()
                routes[vehicle] = new_route
                neighbour = Solution(routes=routes, time=new_time, waiting_times=new_waiting_times)
                if neighbour not in neighbours:  # wstawienie nowego sąsiada jeśli nie ma go w sąsiedztwie
                    neighbours.append(neighbour)

    else:  # zmiana kolejności na trasie każdego pojazdu
        while len(neighbours) < size:  # pętla powtarzana do utworzenia oczekiwanej liczby sąsiadów
            new_times = {}
            new_routes = solution.routes.copy()
            new_waiting_times = solution.waiting_times.copy()
            for vehicle in solution.routes.keys():  # dla każdego pojazdu zmieniana jest jego trasa
                while new_routes[vehicle] == solution.routes[vehicle]:  # próby zmiany trasy do skutku
                    new_route = solution.routes[vehicle].copy()  # podmiana wybranych wierzchołków
                    n = len(new_route)
                    a, b = 0, 0
                    while a == b:  # wylosowanie punktów do podmiany
                        a, b = randint(1, n - 1), randint(1, n - 1)
                    new_route[a], new_route[b] = new_route[b], new_route[a]

                    new_edges: List[Edge] = []  # utworzenie nowej listy krawędzi
                    for i in range(1, len(new_route)):
                        vertex_idx1 = new_route[i - 1]
                        vertex_idx2 = new_route[i]
                        new_edges.append(graph.matrix[vertex_idx1][vertex_idx2])

                    vehicle_route_is_fine = True  # sprawdzenie czy nadal pojazd przyjeżdża o odpowiedniej porze
                    vehicle.reset_free_at()
                    for i in range(1, len(new_route)):
                        edge_time = new_edges[i - 1].time
                        next_Vertex = graph.getVertex(new_route[i])
                        time_at_place = vehicle.free_at + edge_time
                        if not (time_at_place < next_Vertex.time_window[1]):  # pojazd przyjeżdża zbyt późno
                            vehicle_route_is_fine = False
                            break
                        else:
                            if time_at_place < next_Vertex.time_window[0]:  # pojazd przyeżdża zbyt wcześnie
                                new_waiting_times[vehicle][new_route[i]] = next_Vertex.time_window[0] - time_at_place
                            else:  # pojazd przyjeżdża w oknie czasowym
                                new_waiting_times[vehicle][new_route[i]] = 0
                            vehicle.free_at += edge_time + vehicle.service_time + new_waiting_times[vehicle][
                                new_route[i]]

                    if vehicle_route_is_fine:
                        new_times[vehicle] = calc_vehicle_time(vehicle=vehicle, edges=new_edges,
                                                               waiting_times=new_waiting_times[vehicle])
                        new_routes[vehicle] = new_route

            neighbour = Solution(routes=new_routes, time=calc_solution_time(new_times), waiting_times=new_waiting_times)
            if neighbour not in neighbours:  # wstawienie nowego sąsiada jeśli nie ma go w sąsiedztwie
                neighbours.append(neighbour)
    return neighbours
