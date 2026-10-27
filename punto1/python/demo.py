"""
Demo corta del Punto 1 para la sustentación (tarda menos de un minuto).

  1. Ordena los datos aleatorios de 1.000 y 10.000 elementos con los 6
     algoritmos, verifica que quedaron ordenados y muestra el tiempo.
  2. Muestra el efecto del orden de entrada con 1.000 elementos.
  3. Reproduce el fallo del Dual-Pivot QuickSort con 10.000 elementos ordenados.

Uso (desde la carpeta punto1):
    python python/demo.py
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ordenamientos import ALGORITMOS, dual_pivot_quick_sort  # noqa: E402

NOMBRES = {"insertion": "Insertion", "dualpivot": "Dual-Pivot", "merge": "Merge",
           "heap": "Heap", "radix": "Radix", "bucket": "Bucket"}


def leer(var, n):
    with open(os.path.join("datos", f"{var}_{n}.txt")) as f:
        return [int(x) for x in f.read().split()]


def medir(ordenar, original):
    copia = list(original)
    t0 = time.perf_counter_ns()
    ordenar(copia)
    ms = (time.perf_counter_ns() - t0) / 1e6
    ok = all(copia[i - 1] <= copia[i] for i in range(1, len(copia)))
    return f"{ms:10.3f}" if ok else "     ERROR"


def fila(nombre, celdas):
    print(f"{nombre:<12}" + "".join(f"{c:>12}" for c in celdas))


def main():
    print("\n1) ENTRADA ALEATORIA (tiempo en ms, verificado)")
    tam = [1_000, 10_000]
    fila("Algoritmo", [f"n={n}" for n in tam])
    datos = [leer("aleatorio", n) for n in tam]
    for clave, ordenar in ALGORITMOS.items():
        fila(NOMBRES[clave], [medir(ordenar, d) for d in datos])

    print("\n2) EFECTO DEL ORDEN DE ENTRADA, n = 1.000 (ms)")
    fila("Algoritmo", ["aleatoria", "ascendente", "descendente"])
    por_var = [leer(v, 1_000) for v in ("aleatorio", "ascendente", "descendente")]
    for clave, ordenar in ALGORITMOS.items():
        fila(NOMBRES[clave], [medir(ordenar, d) for d in por_var])

    print("\n3) DUAL-PIVOT QUICKSORT CON 10.000 ELEMENTOS ASCENDENTES")
    asc = leer("ascendente", 10_000)
    try:
        dual_pivot_quick_sort(asc)
        print("Terminó sin error.")
    except RecursionError:
        print(f"RecursionError: Python permite {sys.getrecursionlimit()} llamadas anidadas y la")
        print("recursión necesita unas n/2 = 5.000, porque los pivotes son el mínimo y el máximo.")


if __name__ == "__main__":
    main()
