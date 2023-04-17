def es_valido(coloreo, v, c):
    for i in range(len(coloreo)):
        if adj_matrix[v][i] and coloreo[i] == c:
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
    num_colores = 4
    coloreo = [0] * len(adj_matrix)

    if colorear_mapa(coloreo, 0, num_colores):
        return coloreo
    else:
        return None

# Matriz de adyacencia para el mapa de Australia y Tanzania
adj_matrix = [
    [0, 1, 1, 0, 0, 0, 0],  # WA
    [1, 0, 1, 1, 0, 0, 0],  # NT
    [1, 1, 0, 1, 1, 1, 0],  # SA
    [0, 1, 1, 0, 1, 0, 0],  # QLD
    [0, 0, 1, 1, 0, 1, 0],  # NSW
    [0, 0, 1, 0, 1, 0, 0],  # VIC
    [0, 0, 0, 0, 0, 0, 0]   # T
]

resultado = problema_cuatro_colores(adj_matrix)
regiones = ["WA", "NT", "SA", "QLD", "NSW", "VIC", "T"]
colores = {1: "Rojo", 2: "Amarillo", 3: "Verde", 4: "Azul"}

if resultado:
    print("Coloreo encontrado:")
    for i, color in enumerate(resultado):
        print(f"{regiones[i]}: {colores[color]}")
else:
    print("No se pudo encontrar un coloreo válido.")
