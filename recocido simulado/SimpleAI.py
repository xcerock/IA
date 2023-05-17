import random
import math
import tsplib95
from simpleai.search import SearchProblem, simulated_annealing


# Función para cargar los datos del problema desde un archivo .vrp
def load_data(filename):
    coords = []
    demands_list = []
    with open(filename, 'r') as f:
        data = f.read()
    problem = tsplib95.parse(data)
    nodes = problem.node_coords
    for coor in nodes.values():
        coords.append(coor)
    demands = problem.demands
    for demand in demands.values():
        demands_list.append(demand)
    capacity = problem.capacity
    return coords, demands_list, capacity


# Función para generar una solución inicial aleatoria que cumpla con las restricciones del problema
def generate_initial_solution(nodes, demands, capacity):
    num_nodes = len(nodes)
    solution = []
    vehicle_loads = []
    current_load = 0
    for i in range(num_nodes):
        node_demand = demands[i]
        if current_load + node_demand > capacity:
            vehicle_loads.append(current_load)
            solution.append([i])
            current_load = node_demand
        else:
            current_load += node_demand
            if i == 0 or current_load == node_demand:
                vehicle_loads.append(current_load)
                solution.append([i])
            else:
                solution[-1].append(i)
    vehicle_loads.append(current_load)
    solution[0] += solution.pop()
    return solution


# Función para calcular la función de costo para una solución dada
def euclidean_distance(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def calculate_cost(solution, nodes):
    cost = 0
    for route in solution:
        if len(route) > 0:
            current_node = route[0]
            for next_node in route[1:]:
                cost += euclidean_distance(nodes[current_node], nodes[next_node])
                current_node = next_node
    return cost


# Definir la función de estado
class VehicleRoutingProblem(SearchProblem):
    def __init__(self, initial_state, nodes, demands, capacity):
        self.initial_state = initial_state
        self.nodes = nodes
        self.demands = demands
        self.capacity = capacity
        super(VehicleRoutingProblem, self).__init__(initial_state)

    def actions(self, state):
        actions = []
        for i in range(1, len(state)):
            for j in range(len(state[i])):
                for k in range(1, len(state)):
                    if i != k:
                        actions.append((i, j, k))
        return actions

    def result(self, state, action):
        new_state = []
        for route in state:
            new_state.append(route[:])
        node = new_state[action[0]].pop(action[1])
        new_state[action[2]].append(node)
        if len(new_state[action[0]]) == 0:
            new_state.pop(action[0])
        return new_state

    def value(self, state):
        return -calculate_cost(state, self.nodes)
    
    def generate_random_state(self):
        return generate_initial_solution(self.nodes, self.demands, self.capacity)
    
    def crossover(self, state1, state2):
        return [state1[0] + state2[1], state2[0] + state1[1]]

    def mutate(self, state):
        return generate_initial_solution(self.nodes, self.demands, self.capacity)
    
    def crossover_probability(self):
        return 0.5
    
    def mutate_probability(self):
        return 0.5
    
    def crossover_function(self):
        return self.crossover
    
    def mutate_function(self):
        return self.mutate


# Función para imprimir la solución
def print_solution(solution):
    for route in solution:
        print(route)


# Función para imprimir la solución en un archivo .txt
def print_solution_to_file(solution, filename):
    with open(filename, 'w') as f:
        for route in solution:
            for node in route:
                f.write(str(node) + ' ')
            f.write('\n')

if __name__ == '__main__':
    # Cargar los datos del problema
    nodes, demands, capacity = load_data('eil51\\eil51.vrp')
    # Generar una solución inicial aleatoria
    initial_state = generate_initial_solution(nodes, demands, capacity)
    # Definir el problema
    problem = VehicleRoutingProblem(initial_state, nodes, demands, capacity)
    # Resolver el problema
    result = simulated_annealing(problem, iterations_limit=10000)
    # Imprimir la solución
    print_solution(result.state)
    # Imprimir la solución en un archivo .txt
    print_solution_to_file(result.state, 'solution.txt')
    # Imprimir el costo de la solución
    print('Costo de la solución: ' + str(-result.value))
    num_vehicles = len(result.state)
    print('Number of vehicles used:', num_vehicles)

