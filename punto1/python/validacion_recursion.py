"""
Experimento complementario (no forma parte del benchmark oficial).

El Dual-Pivot QuickSort con entrada ascendente/descendente supera el límite de
recursión de Python (1.000 llamadas) a partir de n = 10.000. Aquí se sube el
límite y la pila del hilo SOLO para comprobar qué tan buena fue la estimación
O(n^2) del benchmark. Una sola ejecución por caso.

Uso: python3 validacion_recursion.py <carpeta_datos> <n> <variante>
"""
import os
import sys
import threading
import time

from ordenamientos import dual_pivot_quick_sort


def main():
    datos, n, var = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    with open(os.path.join(datos, f"{var}_{n}.txt")) as f:
        original = [int(x) for x in f.read().split()]
    with open(os.path.join(datos, f"ascendente_{n}.txt")) as f:
        ref = [int(x) for x in f.read().split()]
    resultado = {}

    def tarea():
        c = list(original)
        t0 = time.perf_counter_ns()
        dual_pivot_quick_sort(c)
        resultado["ms"] = (time.perf_counter_ns() - t0) / 1e6
        resultado["ok"] = c == ref

    sys.setrecursionlimit(10 * n)
    threading.stack_size(1024 * 1024 * 1024)
    h = threading.Thread(target=tarea)
    h.start()
    h.join()
    assert resultado["ok"], "No quedó ordenado"
    print(f"dualpivot,python,{var},{n},{resultado['ms']:.4f}")


if __name__ == "__main__":
    main()
