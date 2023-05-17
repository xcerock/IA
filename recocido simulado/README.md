# Sumulated Annealing - CVRP
## abstract
El recocido simulado es una técnica de optimización metaheurística inspirada en el proceso de enfriamiento y recalentamiento de un material durante su fabricación. Esta técnica se utiliza para resolver problemas de optimización combinatoria donde se busca encontrar una solución de alta calidad en un espacio de búsqueda grande.

En el contexto del Problema de Enrutamiento de Vehículos (Vehicle Routing Problem, VRP), el recocido simulado se aplica para encontrar la mejor ruta de entrega para un conjunto de vehículos que deben visitar múltiples ubicaciones mientras se minimiza la distancia total recorrida. El VRP es un problema NP-duro que tiene aplicaciones en logística, distribución y planificación de rutas.

## Ejecucion de los problemas

En los códigos proporcionados, se implementa el recocido simulado para resolver el VRP. Se cargan los datos del problema desde un archivo en formato .vrp y se genera una solución inicial aleatoria que cumple con las restricciones del problema. Luego, se define una clase VehicleRoutingProblem que representa el problema como un problema de búsqueda. Se utiliza la biblioteca tsplib95 para cargar los datos del problema VRP y la biblioteca simpleai para implementar el algoritmo de recocido simulado.

El recocido simulado se ejecuta iterativamente, generando soluciones vecinas y evaluando su costo en función de la distancia euclidiana entre los nodos. Si se encuentra una solución vecina con un costo menor, se acepta automáticamente. Si la solución vecina tiene un costo mayor, se acepta con una probabilidad que disminuye a medida que la temperatura del sistema disminuye. Este proceso de exploración y explotación se repite hasta alcanzar un número máximo de iteraciones.

Al finalizar, se muestra la mejor solución encontrada y su costo. También se guarda la solución en un archivo de texto. El código puede ser personalizado modificando los parámetros iniciales del algoritmo, como la temperatura inicial, la tasa de enfriamiento y el número máximo de iteraciones.


## codigos con resultados

### AIMA

El uso de la biblioteca AIMA (Artificial Intelligence: A Modern Approach) para implementar algoritmos de inteligencia artificial (IA) ofrece varios beneficios.

Amplia cobertura de temas de IA: AIMA abarca una variedad de temas y algoritmos de IA, brindando acceso a una amplia gama de herramientas y técnicas en un solo lugar.
Implementaciones listas para usar: AIMA proporciona implementaciones predefinidas de muchos algoritmos y estructuras de datos comunes utilizados en IA, lo que ahorra tiempo y esfuerzo en el desarrollo desde cero.
Base teórica sólida: AIMA se basa en principios sólidos de IA respaldados por teoría y es ampliamente utilizado en programas académicos de IA.
Flexibilidad y personalización: AIMA ofrece una estructura modular que permite la personalización y adaptación de los algoritmos según las necesidades específicas.
Comunidad y recursos: AIMA cuenta con una comunidad activa de usuarios y desarrolladores que comparten conocimientos, recursos y apoyo.
En resumen, el uso de AIMA simplifica la implementación de algoritmos de IA al proporcionar implementaciones listas para usar, una base teórica sólida y una comunidad activa que ofrece apoyo y recursos adicionales.

Aunque nosotros tuvimos un problema bastante grande ya que no pudimos hacer implentar el codigo de AIMA debido a problemas que tuvimos con la compatibilidad entre las versiones de python y la biblioteca de AIMA, por lo que no pudimos hacer la implementacion de este codigo.

Codigo

```PY
from typing import List, Tuple
import math
import random
from aima.search import Problem, SimulatedAnnealingSearch
from aima.search import distance


class CVRPProblem(Problem):
    def __init__(self, nodes: List[Tuple[float, float]], demands: List[int], capacity: int):
        self.nodes = nodes
        self.demands = demands
        self.capacity = capacity
        super().__init__(self.generate_initial_solution())

    def generate_initial_solution(nodes: List[Tuple[float, float]], demands: List[int], capacity: int) -> List[List[int]]:
        problem = Problem.from_data(nodes, demands, capacity)
        return problem.random_solution()

    def actions(self, state):
        num_nodes = len(state)
        return [(i, j) for i in range(num_nodes) for j in range(i + 1, num_nodes)]

    def result(self, state, action):
        i, j = action
        new_state = state.copy()
        new_state[i], new_state[j] = new_state[j], new_state[i]
        return new_state

    def value(self, state):
        cost = 0
        for route in state:
            if len(route) > 0:
                current_node = route[0]
                for next_node in route[1:]:
                    cost += distance(self.nodes[current_node], self.nodes[next_node])
                    current_node = next_node
        return -cost


def load_data(filename: str) -> Tuple[List[Tuple[float, float]], List[int], int]:
    with open(filename, 'r') as f:
        data = f.read()
    problem = Problem.from_cvrp_string(data)
    coords = problem.node_coords
    demands = problem.demands
    capacity = problem.capacity
    return coords, demands, capacity


if __name__ == "__main__":
    coords, demands, capacity = load_data("problemas/gil262.vrp")
    problem = CVRPProblem(coords, demands, capacity)

    search = SimulatedAnnealingSearch(schedule=lambda t: t * 0.99)
    result = search.solve(problem)

    print("Mejor solución:", result.state)
    print("Costo:", -problem.value(result.state))
    print("Número de vehículos utilizados:", len(result.state))
```

```bash
#solucion



```

### tsplib95

La biblioteca tsplib95 facilita el trabajo con el Problema del Viajante de Comercio (TSP) al proporcionar conjuntos de datos estándar, una interfaz sencilla para cargar y acceder a los datos, información completa sobre el problema, compatibilidad con estándares y capacidad de personalización. Estos beneficios permiten una evaluación justa de los algoritmos, simplifican la implementación y el análisis, y fomentan la colaboración con otras herramientas y sistemas relacionados con el TSP. En resumen, tsplib95 mejora la eficiencia y la calidad de los proyectos de TSP al proporcionar una base sólida y funcionalidades avanzadas.

Codigo

```PY
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
    coords, demands, capacity = load_data(".\\datos\\eil30.vrp")
    solution, cost = simulated_annealing(coords, demands, capacity, 100, 0.99, 1000)
    print_solution(solution ,cost)
num_vehicles = len(solution)
print('Number of vehicles used:', num_vehicles)
```

```bash
#Solucion

Solution: [0, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75] [27, 28, 29, 30, 31, 32, 33, 34] [54, 55, 56, 57, 58, 59, 60, 61, 62, 63] [45, 46, 47, 48, 49, 50, 51, 52, 53] [35, 36, 37, 38, 39, 40, 41, 42, 43, 44] [17, 18, 19, 20, 21, 22, 23, 24, 25, 26] [1, 2, 3, 4, 5, 6, 7, 8] [9, 10, 11, 12, 13, 14, 15, 16]
Cost:  1833.3983602866442
Number of vehicles used: 8

```

### SimpleAI

En resumen, SimpleAI es una biblioteca de inteligencia artificial que se destaca por su enfoque en la simplicidad y la facilidad de uso. Ofrece una amplia variedad de algoritmos de IA, lo que permite abordar diferentes problemas, desde búsqueda y optimización hasta clasificación y toma de decisiones basada en datos. La biblioteca es altamente personalizable y extensible, lo que facilita adaptarla a necesidades específicas. Además, su enfoque didáctico y los ejemplos de código claros y comprensibles hacen que sea una herramienta ideal para principiantes que deseen aprender sobre inteligencia artificial de manera práctica. En general, SimpleAI es una opción valiosa para desarrolladores y entusiastas de la IA que buscan una solución accesible y eficiente.

Codigo

```PY
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
```

```bash
[0, 49, 50]
[23, 7, 14, 19, 41, 27, 28, 31, 26, 8, 1, 2, 22, 3, 20, 29, 21]
[36, 35, 9, 30, 34, 16, 38, 11, 32, 6]
[39, 10, 5, 37, 45, 33, 15]
[17, 4, 13]
[40, 42, 44, 47, 48, 43, 24, 25, 18, 46, 12]
Costo de la solución: 596.0824519684854
Number of vehicles used: 6
```

## conclusiones

El recocido simulado es una técnica de optimización que ha demostrado ser efectiva en la resolución del Problema de Enrutamiento de Vehículos con Capacidad (CVRP). A partir de las conclusiones obtenidas de su aplicación en el CVRP, se pueden destacar los siguientes puntos:

Capacidad para encontrar soluciones de alta calidad: El recocido simulado tiene la capacidad de explorar y buscar soluciones óptimas o cercanas a óptimas en el CVRP. A través de iteraciones y la exploración de soluciones vecinas, puede escapar de óptimos locales y encontrar soluciones de alta calidad.

Flexibilidad para adaptarse a diferentes instancias: El recocido simulado es adecuado para diferentes instancias del CVRP. Puede manejar tamaños de problema variables, diferentes configuraciones de vehículos y restricciones de capacidad, lo que lo convierte en una técnica versátil.

Tolerancia a la fluctuación de la función objetivo: El recocido simulado puede aceptar soluciones que empeoren la función objetivo en una etapa temprana de la búsqueda. Esto permite una mayor exploración del espacio de soluciones y evita quedar atrapado en óptimos locales subóptimos.

Control de la exploración y explotación: Mediante el uso de un parámetro de temperatura y una estrategia de enfriamiento adecuada, el recocido simulado puede equilibrar la exploración de nuevas soluciones y la explotación de soluciones prometedoras. Esto permite un equilibrio óptimo entre la exploración y la explotación.

Tiempo de ejecución: Aunque el recocido simulado puede encontrar soluciones de alta calidad, su tiempo de ejecución puede ser mayor en comparación con otros algoritmos más rápidos. Sin embargo, con una adecuada configuración de los parámetros, puede obtener resultados satisfactorios en tiempos razonables.

En resumen, el recocido simulado es una técnica efectiva y flexible para abordar el Problema de Enrutamiento de Vehículos con Capacidad. Es capaz de encontrar soluciones de alta calidad, adaptarse a diferentes instancias y controlar la exploración y explotación del espacio de soluciones. Si bien puede requerir más tiempo de ejecución, los beneficios obtenidos en términos de calidad de la solución hacen que valga la pena considerarlo como una opción viable para abordar el CVRP.