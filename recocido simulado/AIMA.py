from typing import List, Tuple
import math
import random
from aima import distance, Problem, simulated_annealing


def load_data(filename: str) -> Tuple[List[Tuple[float, float]], List[int], int]:
    with open(filename, 'r') as f:
        data = f.read()
    problem = Problem.from_cvrp_string(data)
    coords = problem.node_coords
    demands = problem.demands
    capacity = problem.capacity
    return coords, demands, capacity


def generate_initial_solution(nodes: List[Tuple[float, float]], demands: List[int], capacity: int) -> List[List[int]]:
    problem = Problem.from_data(nodes, demands, capacity)
    return problem.random_solution()


# Función para calcular la función de costo para una solución dada
def euclidean_distance(a, b):
    return math.sqrt((a[0] - b[0])* 2 + (a[1] - b[1])* 2)


def calculate_cost(solution: List[List[int]], nodes: List[Tuple[float, float]]) -> float:
    cost = 0
    for route in solution:
        if len(route) > 0:
            current_node = route[0]
            for next_node in route[1:]:
                cost += distance(nodes[current_node], nodes[next_node])
                current_node = next_node
    return cost



# Función para generar una solución vecina
def generate_neighbor(solution):
    num_nodes = len(solution)
    i, j = random.sample(range(num_nodes), 2)
    neighbor = solution.copy()
    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
    return neighbor


# Función para implementar el algoritmo de recocido simulado
def simulated_annealing(nodes, demands, capacity, initial_temperature, cooling_rate, max_iterations):
    current_solution = generate_initial_solution(nodes, demands, capacity)
    print(current_solution)
    current_cost = calculate_cost(current_solution, nodes)
    best_solution = current_solution
    best_cost = current_cost
    temperature = initial_temperature
    for _ in range(max_iterations):
        neighbor = generate_neighbor(current_solution)
        neighbor_cost = calculate_cost(neighbor, nodes)
        cost_difference = neighbor_cost - current_cost
        if cost_difference < 0:
            current_solution = neighbor
            current_cost = neighbor_cost
            if neighbor_cost < best_cost:
                best_solution = neighbor
                best_cost = neighbor_cost
        else:
            if random.random() < math.exp(-cost_difference / temperature):
                current_solution = neighbor
                current_cost = neighbor_cost
        temperature *= cooling_rate
    return best_solution, best_cost


# Función para imprimir la solución
def print_solution(solution, cost):
    print('Solution: ', end='')
    for i in solution:
        print(i, end=' ')
    print('\nCost: ', cost)


if __name__ == '__main__':
    coords, demands, capacity = load_data("problemas/gil262.vrp")
    initial_state = generate_initial_solution(coords, demands, capacity)
    initial_cost = calculate_cost(initial_state, coords)
    best_state, best_cost = simulated_annealing(initial_state, initial_cost, None, lambda t: t * 0.99, 100, 1000, generate_neighbor, calculate_cost, lambda x: False)
    print('Best solution:', best_state)
    print('Cost:', best_cost)
    print('Number of vehicles used:', len(best_state))