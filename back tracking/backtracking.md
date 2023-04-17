# Backtracking

## Codigo para n regiones

El backtracking es un enfoque general para resolver problemas de satisfacción de restricciones. En este caso, lo usamos para resolver el problema de los cuatro colores, donde tratamos de colorear un mapa con solo cuatro colores de tal manera que ninguna región adyacente tenga el mismo color. La idea principal detrás del backtracking es construir soluciones candidatas de manera incremental, y eliminar candidatos (volver atrás) tan pronto como determinamos que no pueden llevar a una solución completa.

Aquí tienes el código documentado y una explicación paso a paso para cualquier número 'n' de regiones:

```Py
# Función para comprobar si un color 'c' se puede asignar a la región 'v'
def es_valido(coloreo, v, c):
    # Recorre todas las regiones en el coloreo
    for i in range(len(coloreo)):
        # Si la región 'i' es adyacente a 'v' y ya tiene el color 'c', no es válido asignar 'c' a 'v'
        if adj_matrix[v][i] and coloreo[i] == c:
            return False
    # Si no hay conflictos, devuelve True
    return True

# Función recursiva de backtracking para colorear el mapa
def colorear_mapa(coloreo, v, num_colores):
    # Si hemos coloreado todas las regiones, la solución es completa y válida
    if v == len(adj_matrix):
        return True

    # Prueba a asignar colores del 1 al 'num_colores' a la región 'v'
    for c in range(1, num_colores + 1):
        # Verifica si es válido asignar el color 'c' a la región 'v'
        if es_valido(coloreo, v, c):
            # Si es válido, asigna el color 'c' a la región 'v'
            coloreo[v] = c
            # Continúa con la siguiente región
            if colorear_mapa(coloreo, v + 1, num_colores):
                return True
            # Si asignar el color 'c' a la región 'v' no lleva a una solución, deshacer la asignación (volver atrás)
            coloreo[v] = 0

    # Si no se puede asignar un color válido a la región 'v', devuelve False
    return False

# Función principal para resolver el problema de los cuatro colores
def problema_cuatro_colores(adj_matrix):
    num_colores = 4
    # Inicializa el arreglo de coloreo con ceros (ningún color asignado)
    coloreo = [0] * len(adj_matrix)

    # Llama a la función de backtracking
    if colorear_mapa(coloreo, 0, num_colores):
        return coloreo
    else:
        return None

# Matriz de adyacencia para un grafo que representa un mapa con 'n' regiones
# (debes reemplazar esta matriz con la matriz de adyacencia de tu propio grafo)
adj_matrix = [
    # ...
]

resultado = problema_cuatro_colores(adj_matrix)
```

Explicación paso a paso:

1. La función `es_valido(coloreo, v, c)` verifica si es posible asignar el color `c` a la región `v` sin violar las restricciones del problema de los cuatro colores. Comprueba si hay alguna región adyacente a `v` que ya tenga el color `c`. Si encuentra alguna, devuelve False; de lo contrario, devuelve `True`.
2. La función `colorear_mapa(coloreo, v, num_colores)` es la función principal de backtracking que intenta colorear el mapa. Es una función recursiva que toma el arreglo actual de coloreo, el índice de la región actual `v` y el número de colores disponibles.
3. La base de la recursión se alcanza cuando todas las regiones han sido coloreadas (es decir, cuando `v` es igual al número total de regiones). En este caso, la función devuelve `True`, indicando que se ha encontrado una solución válida.
4. Para cada región `v`, la función `colorear_mapa` intenta asignar colores del 1 al `num_colores` (en nuestro caso, 4). Para cada color, verifica si es válido asignarlo a la región `v` llamando a la función `es_valido`. Si es válido, asigna el color y realiza una llamada recursiva a `colorear_mapa` con la siguiente región `(v + 1)`.
5. Si la llamada recursiva devuelve `True`, entonces se ha encontrado una solución válida, y la función actual también devuelve `True`. Si no se encuentra una solución válida, se deshace la asignación del color a la región `v` `(coloreo[v] = 0)` y se prueba con el siguiente color. Si no se puede asignar ningún color válido a la región v, la función devuelve `False`, lo que indica que no se ha encontrado una solución válida.
6. La función `problema_cuatro_colores(adj_matrix)` es la función principal que llama a la función de backtracking `colorear_mapa` con la primera región (índice 0) y el número de colores (en nuestro caso, 4). Si se encuentra una solución válida, devuelve el arreglo de coloreo; de lo contrario, devuelve `None`.
7. Para aplicar este código a un mapa con cualquier número `n` de regiones, simplemente debes proporcionar una matriz de adyacencia adecuada (`adj_matrix`) que represente las adyacencias entre las regiones en tu mapa. La matriz de adyacencia es una matriz cuadrada de tamaño `n x n`, donde un valor de 1 en la posición (i, j) indica que las regiones i y j son adyacentes, y un valor de 0 indica que no lo son.

Una vez que hayas proporcionado la matriz de adyacencia, el algoritmo de backtracking funcionará para cualquier número de regiones.

## Ejercicio de australia y los 4 colores

Hay siete regiones en total: Australia Occidental (WA), Territorio del Norte (NT), Australia Meridional (SA), Queensland (QLD), Nueva Gales del Sur (NSW) , Victoria (VIC) y Tanzania(T). La matriz de adyacencia se ha ajustado para reflejar las adyacencias entre estas regiones.

```Py
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

# Matriz de adyacencia para el mapa de Australia
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
```
