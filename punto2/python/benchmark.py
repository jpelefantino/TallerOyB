"""
Benchmark del Punto 2 (Python, lenguaje interpretado).

Uso:
  python benchmark.py <algoritmo|todos> [dir_arreglos] [dir_claves] <archivo_csv>
  o
  python benchmark.py <algoritmo|todos> <archivo_csv>

Algoritmos: linear | binary | ternary | jump | interpolation | exponential | todos
"""
import csv
import os
import statistics
import sys
import time

from busquedas import ALGORITMOS

TAMANIOS = [1_000, 10_000, 100_000, 1_000_000]
REPETICIONES = 5
TODOS_LOS_ALGS = ["linear", "binary", "ternary", "jump", "interpolation", "exponential"]
COLUMNAS = [
    "algoritmo", "lenguaje", "variante", "n",
    "t1_ns", "t2_ns", "t3_ns", "t4_ns", "t5_ns",
    "promedio_ns", "desv_ns", "tipo", "estado", "nota"
]


def leer_archivo(ruta):
    with open(ruta) as f:
        return [int(x) for x in f.read().split()]


def medir_bloque(alg_func, arr, claves):
    """Ejecuta las búsquedas de todas las claves y retorna el tiempo promedio por búsqueda en ns."""
    t0 = time.perf_counter_ns()
    sink = 0
    for c in claves:
        sink += alg_func(arr, c)
    t1 = time.perf_counter_ns()
    if sink == -999999999:
        print(sink)
    return (t1 - t0) / len(claves)


def correr_repeticiones(alg_func, arr, claves):
    tiempos = []
    for _ in range(REPETICIONES):
        t_prom_busqueda = medir_bloque(alg_func, arr, claves)
        tiempos.append(t_prom_busqueda)
    prom = statistics.mean(tiempos)
    desv = statistics.stdev(tiempos) if len(tiempos) > 1 else 0.0
    return tiempos, prom, desv


def guardar_fila(ruta_csv, fila):
    nuevo = not os.path.exists(ruta_csv)
    os.makedirs(os.path.dirname(os.path.abspath(ruta_csv)), exist_ok=True)
    with open(ruta_csv, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNAS)
        if nuevo:
            writer.writeheader()
        writer.writerow(fila)


def benchmark_algoritmo(alg, dir_arreglos, dir_claves, ruta_csv):
    alg_func = ALGORITMOS[alg]
    print(f"=== Iniciando Benchmark Python: {alg} ===")

    # 1. Crecimiento con n (claves mixtas)
    for n in TAMANIOS:
        ruta_arr = os.path.join(dir_arreglos, f"ascendente_{n}.txt")
        ruta_claves = os.path.join(dir_claves, f"claves_{n}.txt")

        if not os.path.exists(ruta_arr) or not os.path.exists(ruta_claves):
            print(f"Saltando n={n:,}: archivos no encontrados ({ruta_arr} o {ruta_claves})")
            continue

        arr = leer_archivo(ruta_arr)
        claves = leer_archivo(ruta_claves)

        tiempos, prom, desv = correr_repeticiones(alg_func, arr, claves)
        fila = {
            "algoritmo": alg,
            "lenguaje": "python",
            "variante": "claves_mixtas",
            "n": n,
            "t1_ns": f"{tiempos[0]:.2f}",
            "t2_ns": f"{tiempos[1]:.2f}",
            "t3_ns": f"{tiempos[2]:.2f}",
            "t4_ns": f"{tiempos[3]:.2f}",
            "t5_ns": f"{tiempos[4]:.2f}",
            "promedio_ns": f"{prom:.2f}",
            "desv_ns": f"{desv:.2f}",
            "tipo": "medido",
            "estado": "ok",
            "nota": "1000 claves (500 presentes, 500 ausentes)"
        }
        guardar_fila(ruta_csv, fila)
        print(f"[{alg}] n={n:,} (claves_mixtas): prom={prom:.1f} ns/busqueda (+-{desv:.1f} ns)")

    # 2. Posición de la clave en n = 1.000.000
    n_max = 1_000_000
    ruta_arr_max = os.path.join(dir_arreglos, f"ascendente_{n_max}.txt")
    if os.path.exists(ruta_arr_max):
        arr_max = leer_archivo(ruta_arr_max)
        posiciones = [
            ("pos_inicio", [arr_max[0]] * 1_000, "1000 busquedas clave en arr[0]"),
            ("pos_centro", [arr_max[n_max // 2]] * 1_000, "1000 busquedas clave en arr[n/2]"),
            ("pos_final", [arr_max[n_max - 1]] * 1_000, "1000 busquedas clave en arr[n-1]")
        ]

        for pos_nombre, claves_pos, desc in posiciones:
            tiempos, prom, desv = correr_repeticiones(alg_func, arr_max, claves_pos)
            fila = {
                "algoritmo": alg,
                "lenguaje": "python",
                "variante": pos_nombre,
                "n": n_max,
                "t1_ns": f"{tiempos[0]:.2f}",
                "t2_ns": f"{tiempos[1]:.2f}",
                "t3_ns": f"{tiempos[2]:.2f}",
                "t4_ns": f"{tiempos[3]:.2f}",
                "t5_ns": f"{tiempos[4]:.2f}",
                "promedio_ns": f"{prom:.2f}",
                "desv_ns": f"{desv:.2f}",
                "tipo": "medido",
                "estado": "ok",
                "nota": desc
            }
            guardar_fila(ruta_csv, fila)
            print(f"[{alg}] n={n_max:,} ({pos_nombre}): prom={prom:.1f} ns/busqueda (+-{desv:.1f} ns)")

    print(f"=== Fin Benchmark Python: {alg} ===\n")


def main():
    args = sys.argv[1:]
    if len(args) == 2:
        alg = args[0]
        base_dir = os.path.dirname(os.path.abspath(__file__))
        dir_arreglos = os.path.join(os.path.dirname(base_dir), "..", "punto1", "datos")
        if not os.path.exists(dir_arreglos):
            dir_arreglos = os.path.join(os.path.dirname(base_dir), "punto1", "datos")
        dir_claves = os.path.join(base_dir, "..", "datos")
        ruta_csv = args[1]
    elif len(args) == 4:
        alg, dir_arreglos, dir_claves, ruta_csv = args[0], args[1], args[2], args[3]
    else:
        print("Uso: python benchmark.py <algoritmo|todos> [dir_arreglos] [dir_claves] <archivo_csv>")
        sys.exit(1)

    if alg.lower() in ("todos", "all"):
        for a in TODOS_LOS_ALGS:
            benchmark_algoritmo(a, dir_arreglos, dir_claves, ruta_csv)
    else:
        if alg not in ALGORITMOS:
            print(f"Error: Algoritmo desconocido '{alg}'. Opciones: {list(ALGORITMOS.keys())} o 'todos'")
            sys.exit(1)
        benchmark_algoritmo(alg, dir_arreglos, dir_claves, ruta_csv)


if __name__ == "__main__":
    main()
