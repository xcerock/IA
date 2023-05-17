import random
import math
import tsplib95

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
        print(route)
        if len(route) > 0:
            current_node = route[0]
            for next_node in route[1:]:
                cost += euclidean_distance(nodes[current_node], nodes[next_node])
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
    coords, demands, capacity = load_data(".\eilC76.vrp\eilC76.vrp")
    solution, cost = simulated_annealing(coords, demands, capacity, 100, 0.99, 1000)
    print_solution(solution ,cost)
num_vehicles = len(solution)
print('Number of vehicles used:', num_vehicles)

   

    
