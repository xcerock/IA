def es_valido(coloreo, v, c):
    for i in range(len(coloreo)):
        if adj_matrix[v][i] and  (c-1 <= coloreo[i] <= c + 1 or c in x for x in coloreo):
            return False 
    return True

def colorear_mapa(coloreo, v, num_colores):
    if v == len(adj_matrix):
        return True

    for c in range(1, num_colores + 1):
        if es_valido(coloreo, v, c):
            coloreo[v] = c
            if colorear_mapa(coloreo, v + 1, num_colores):
                return True
            coloreo[v] = 0

    return False

def problema_cuatro_colores(adj_matrix):
    num_colores = 8
    coloreo = [0] * len(adj_matrix)

    if colorear_mapa(coloreo, 0, num_colores):
        return coloreo
    else:
        return None

# Matriz de adyacencia para el mapa de Australia y Tanzania
adj_matrix = [
    [0, 1, 1, 1, 0, 0, 0, 0], #1
    [1, 0, 1, 0, 1, 1, 0, 0], #2
    [1, 1, 0, 1, 1, 1, 1, 0], #3
    [1, 0, 1, 0, 0, 1, 1, 0], #4
    [0, 1, 1, 0, 0, 1, 0, 1], #5
    [0, 1, 1, 1, 1, 0, 1, 1], #6
    [0, 0, 1, 1, 0, 1, 0, 1], #7
    [0, 0, 0, 0, 1, 1, 1, 0], #8
]

print(1 in adj_matrix)

resultado = problema_cuatro_colores(adj_matrix)
regiones = ["1", "2", "3", "4", "5", "6", "7", "8"]
colores = {1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6:"6", 7:"7", 8:"8" }

if resultado:
    print("Coloreo encontrado:")
    for i, color in enumerate(resultado):
        print(f"{regiones[i]}: {colores[color]}")
else:
    print("No se pudo encontrar un coloreo válido.")
