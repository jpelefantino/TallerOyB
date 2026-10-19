"""
Algoritmos de ordenamiento del Punto 1 (Taller de Ordenamiento y Búsqueda).

Mismas implementaciones que java/Ordenamientos.java, tomadas de GeeksforGeeks:
  - Insertion Sort:        https://www.geeksforgeeks.org/dsa/insertion-sort-algorithm/
  - Dual-Pivot QuickSort:  https://www.geeksforgeeks.org/dsa/dual-pivot-quicksort/
  - Merge Sort:            https://www.geeksforgeeks.org/dsa/merge-sort/
  - Heap Sort:             https://www.geeksforgeeks.org/dsa/heap-sort/
  - Radix Sort:            https://www.geeksforgeeks.org/dsa/radix-sort/
  - Bucket Sort:           https://www.geeksforgeeks.org/dsa/bucket-sort-2/
"""


# ----------------------------------------------------------------------
# Insertion Sort
# ----------------------------------------------------------------------
def insertion_sort(arr):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        # Mueve los elementos mayores que key una posición a la derecha
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


# ----------------------------------------------------------------------
# Dual-Pivot QuickSort (pivotes en el primer y el último elemento)
# ----------------------------------------------------------------------
def dual_pivot_quick_sort(arr):
    _dual_pivot_quick_sort(arr, 0, len(arr) - 1)


def _dual_pivot_quick_sort(arr, low, high):
    if low < high:
        lp, rp = _partition(arr, low, high)
        _dual_pivot_quick_sort(arr, low, lp - 1)
        _dual_pivot_quick_sort(arr, lp + 1, rp - 1)
        _dual_pivot_quick_sort(arr, rp + 1, high)


def _partition(arr, low, high):
    # p = pivote izquierdo (primer elemento), q = pivote derecho (último)
    if arr[low] > arr[high]:
        arr[low], arr[high] = arr[high], arr[low]
    j = low + 1
    g = high - 1
    k = low + 1
    p = arr[low]
    q = arr[high]
    while k <= g:
        if arr[k] < p:                      # menor que el pivote izquierdo
            arr[k], arr[j] = arr[j], arr[k]
            j += 1
        elif arr[k] >= q:                   # mayor o igual que el pivote derecho
            while arr[g] > q and k < g:
                g -= 1
            arr[k], arr[g] = arr[g], arr[k]
            g -= 1
            if arr[k] < p:
                arr[k], arr[j] = arr[j], arr[k]
                j += 1
        k += 1
    j -= 1
    g += 1
    arr[low], arr[j] = arr[j], arr[low]     # pivote izquierdo a su posición final
    arr[high], arr[g] = arr[g], arr[high]   # pivote derecho a su posición final
    return j, g


# ----------------------------------------------------------------------
# Merge Sort
# ----------------------------------------------------------------------
def merge_sort(arr):
    _merge_sort(arr, 0, len(arr) - 1)


def _merge_sort(arr, l, r):
    if l < r:
        m = l + (r - l) // 2
        _merge_sort(arr, l, m)
        _merge_sort(arr, m + 1, r)
        _merge(arr, l, m, r)


def _merge(arr, l, m, r):
    n1 = m - l + 1
    n2 = r - m
    L = [0] * n1
    R = [0] * n2
    for i in range(n1):
        L[i] = arr[l + i]
    for j in range(n2):
        R[j] = arr[m + 1 + j]

    i = j = 0
    k = l
    while i < n1 and j < n2:
        if L[i] <= R[j]:            # <= mantiene la estabilidad
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1


# ----------------------------------------------------------------------
# Heap Sort
# ----------------------------------------------------------------------
def heap_sort(arr):
    n = len(arr)
    # Construye el max-heap
    for i in range(n // 2 - 1, -1, -1):
        _heapify(arr, n, i)
    # Extrae uno a uno el máximo y lo lleva al final
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        _heapify(arr, i, 0)


def _heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and arr[l] > arr[largest]:
        largest = l
    if r < n and arr[r] > arr[largest]:
        largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        _heapify(arr, n, largest)


# ----------------------------------------------------------------------
# Radix Sort (LSD, base 10, counting sort estable por dígito)
# ----------------------------------------------------------------------
def radix_sort(arr):
    n = len(arr)
    m = _get_max(arr)
    exp = 1
    while m // exp > 0:
        _count_sort(arr, n, exp)
        exp *= 10


def _get_max(arr):
    mx = arr[0]
    for i in range(1, len(arr)):
        if arr[i] > mx:
            mx = arr[i]
    return mx


def _count_sort(arr, n, exp):
    output = [0] * n
    count = [0] * 10
    for i in range(n):
        count[(arr[i] // exp) % 10] += 1
    for i in range(1, 10):
        count[i] += count[i - 1]
    for i in range(n - 1, -1, -1):          # de derecha a izquierda: estable
        idx = (arr[i] // exp) % 10
        output[count[idx] - 1] = arr[i]
        count[idx] -= 1
    for i in range(n):
        arr[i] = output[i]


# ----------------------------------------------------------------------
# Bucket Sort
#   Cubetas: n (una por elemento).
#   Asignación: índice = (valor - min) * n // (max - min + 1)
#   (reparte el rango [min, max] en n intervalos iguales).
#   Cada cubeta se ordena con insertion sort y luego se concatenan.
# ----------------------------------------------------------------------
def bucket_sort(arr):
    n = len(arr)
    if n <= 0:
        return
    mn = arr[0]
    mx = arr[0]
    for v in arr:
        if v < mn:
            mn = v
        if v > mx:
            mx = v
    rango = mx - mn + 1

    buckets = [[] for _ in range(n)]
    for i in range(n):
        bi = (arr[i] - mn) * n // rango
        buckets[bi].append(arr[i])
    for i in range(n):
        _insertion_sort_bucket(buckets[i])

    index = 0
    for i in range(n):
        for j in range(len(buckets[i])):
            arr[index] = buckets[i][j]
            index += 1


def _insertion_sort_bucket(bucket):
    for i in range(1, len(bucket)):
        key = bucket[i]
        j = i - 1
        while j >= 0 and bucket[j] > key:
            bucket[j + 1] = bucket[j]
            j -= 1
        bucket[j + 1] = key


ALGORITMOS = {
    "insertion": insertion_sort,
    "dualpivot": dual_pivot_quick_sort,
    "merge": merge_sort,
    "heap": heap_sort,
    "radix": radix_sort,
    "bucket": bucket_sort,
}
