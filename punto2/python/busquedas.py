"""
Algoritmos de búsqueda del Punto 2 (Taller de Ordenamiento y Búsqueda).

Implementaciones en Python (lenguaje interpretado), con la misma estructura y
lógica línea por línea que java/Busquedas.java. Todas las implementaciones siguen
las referencias de GeeksforGeeks (fuente principal sugerida en el taller).

Fuentes:
  - Linear Search:         https://www.geeksforgeeks.org/linear-search/
  - Binary Search:         https://www.geeksforgeeks.org/binary-search/
  - Ternary Search:        https://www.geeksforgeeks.org/ternary-search/
  - Jump Search:           https://www.geeksforgeeks.org/jump-search/
  - Interpolation Search:  https://www.geeksforgeeks.org/interpolation-search/
  - Exponential Search:    https://www.geeksforgeeks.org/exponential-search/
"""
import math


def linear_search(arr, x):
    """
    Búsqueda Lineal (referencia).
    Recorre el arreglo elemento por elemento hasta encontrar la clave o llegar al final.
    Complejidad: O(1) mejor, O(n) promedio y peor. Espacio: O(1).
    """
    n = len(arr)
    for i in range(n):
        if arr[i] == x:
            return i
    return -1


def binary_search(arr, x):
    """
    Búsqueda Binaria (versión iterativa).
    Divide repetidamente a la mitad el rango de búsqueda en un arreglo ordenado.
    Complejidad: O(1) mejor, O(log n) promedio y peor. Espacio: O(1).
    """
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] == x:
            return mid
        elif arr[mid] < x:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def ternary_search(arr, x):
    """
    Búsqueda Ternaria (versión iterativa).
    Divide el rango en 3 partes usando dos puntos medios (mid1 y mid2).
    Complejidad: O(1) mejor, O(log3 n) promedio y peor. Espacio: O(1).
    """
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid1 = low + (high - low) // 3
        mid2 = high - (high - low) // 3
        if arr[mid1] == x:
            return mid1
        if arr[mid2] == x:
            return mid2
        if x < arr[mid1]:
            high = mid1 - 1
        elif x > arr[mid2]:
            low = mid2 + 1
        else:
            low = mid1 + 1
            high = mid2 - 1
    return -1


def jump_search(arr, x):
    """
    Búsqueda por Saltos (Jump Search).
    Avanza en bloques de tamaño sqrt(n) hasta encontrar un bloque que pueda contener x,
    luego realiza una búsqueda lineal dentro de dicho bloque.
    Complejidad: O(1) mejor, O(sqrt(n)) promedio y peor. Espacio: O(1).
    """
    n = len(arr)
    if n == 0:
        return -1
    step = int(math.sqrt(n))
    prev = 0
    while prev < n and arr[min(step, n) - 1] < x:
        prev = step
        step += int(math.sqrt(n))
        if prev >= n:
            return -1
    while prev < min(step, n):
        if arr[prev] == x:
            return prev
        prev += 1
    return -1


def interpolation_search(arr, x):
    """
    Búsqueda por Interpolación.
    Calcula la posición estimada basándose en los valores extremos del rango y el valor buscado.
    Óptimo para datos uniformemente distribuidos.
    Complejidad: O(1) mejor, O(log log n) promedio uniforme, O(n) peor. Espacio: O(1).
    """
    low = 0
    high = len(arr) - 1
    while low <= high and arr[low] <= x <= arr[high]:
        if low == high:
            if arr[low] == x:
                return low
            return -1
        if arr[high] == arr[low]:
            if arr[low] == x:
                return low
            return -1
        pos = low + int(((high - low) / (arr[high] - arr[low])) * (x - arr[low]))
        if arr[pos] == x:
            return pos
        if arr[pos] < x:
            low = pos + 1
        else:
            high = pos - 1
    return -1


def exponential_search(arr, x):
    """
    Búsqueda Exponencial.
    Encuentra un rango duplicando el índice (1, 2, 4, 8...) y luego aplica búsqueda binaria
    en el intervalo identificado [i // 2, min(i, n - 1)].
    Complejidad: O(1) mejor, O(log n) promedio y peor. Espacio: O(1).
    """
    n = len(arr)
    if n == 0:
        return -1
    if arr[0] == x:
        return 0
    i = 1
    while i < n and arr[i] <= x:
        i *= 2
    # Búsqueda binaria en el rango acotado
    low = i // 2
    high = min(i, n - 1)
    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] == x:
            return mid
        elif arr[mid] < x:
            low = mid + 1
        else:
            high = mid - 1
    return -1


ALGORITMOS = {
    "linear": linear_search,
    "binary": binary_search,
    "ternary": ternary_search,
    "jump": jump_search,
    "interpolation": interpolation_search,
    "exponential": exponential_search,
}
