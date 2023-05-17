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
