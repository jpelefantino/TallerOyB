"""
Benchmark del Punto 1 (Python, lenguaje interpretado).

Uso:  python3 benchmark.py <algoritmo> <carpeta_datos> <archivo_csv>
      algoritmo: insertion | dualpivot | merge | heap | radix | bucket

Mismas reglas que java/Benchmark.java:
  - Los datos se leen de archivo ANTES de medir; solo se mide el ordenamiento.
  - Cada repetición ordena una copia nueva del arreglo (la copia no se mide).
  - 5 repeticiones. CPython no tiene compilación JIT activa por defecto, así que
    no necesita calentamiento.
  - Verificación fuera del tiempo medido (igual a la versión ascendente).
  - Si se predice que una ejecución supera 5 minutos, no se ejecuta: se estima.
  - Si falla (p. ej. RecursionError) se registra el error y se estima el tiempo.
"""
import csv
import math
import os
import statistics
import sys
import time

from ordenamientos import ALGORITMOS

TAMANIOS = [1_000, 10_000, 100_000, 1_000_000]
VARIANTES = ["aleatorio", "ascendente", "descendente"]
REPETICIONES = 5
LIMITE_MS = 5 * 60 * 1000.0
COLUMNAS = ["algoritmo", "lenguaje", "variante", "n", "t1_ms", "t2_ms", "t3_ms", "t4_ms",
            "t5_ms", "promedio_ms", "desv_ms", "tipo", "estado", "nota"]


def clase(alg, var):
    if alg == "insertion":
        return "n" if var == "ascendente" else "n2"
    if alg == "dualpivot":
        return "nlogn" if var == "aleatorio" else "n2"
    if alg in ("merge", "heap"):
        return "nlogn"
    return "n"  # radix (d fijo = 8) y bucket (datos uniformes)


def factor(cl, n0, n1):
    r = n1 / n0
    if cl == "n2":
        return r * r
    if cl == "nlogn":
        return r * math.log(n1) / math.log(n0)
    return r


def leer(ruta):
    with open(ruta) as f:
        return [int(x) for x in f.read().split()]


def main():
    alg, datos, ruta_csv = sys.argv[1], sys.argv[2], sys.argv[3]
    ordenar = ALGORITMOS[alg]
    nuevo = not os.path.exists(ruta_csv)
    with open(ruta_csv, "a", newline="") as f:
        w = csv.writer(f)
        if nuevo:
            w.writerow(COLUMNAS)
        for var in VARIANTES:
            cl = clase(alg, var)
            n_ok, media_ok, fallo = None, None, False
            for n in TAMANIOS:
                pred = media_ok * factor(cl, n_ok, n) if n_ok else None
                nota_est = (f"estimado desde n={n_ok} ({media_ok:.4f} ms) con crecimiento {cl}"
                            if n_ok else "")
                base = [alg, "python", var, n]

                if not fallo and pred is not None and pred > LIMITE_MS:
                    w.writerow(base + [""] * 5 + [f"{pred:.4f}", "", "estimado", "supera_5min",
                                                  nota_est])
                    f.flush()
                    print(f"{alg:10} {var:12} n={n:<8} ESTIMADO {pred:.1f} ms (>5 min)", flush=True)
                    continue

                original = leer(os.path.join(datos, f"{var}_{n}.txt"))
                ref = leer(os.path.join(datos, f"ascendente_{n}.txt"))
                tiempos = []
                try:
                    for _ in range(REPETICIONES):
                        copia = list(original)                 # fuera de la medición
                        t0 = time.perf_counter_ns()
                        ordenar(copia)
                        t1 = time.perf_counter_ns()
                        tiempos.append((t1 - t0) / 1e6)
                        if copia != ref:
                            raise RuntimeError("No quedó ordenado")
                except RecursionError:
                    fallo = True
                    est = f"{pred:.4f}" if pred is not None else ""
                    w.writerow(base + [""] * 5 + [est, "", "estimado", "fallo_RecursionError",
                                                  "límite de recursión de Python; " + nota_est])
                    f.flush()
                    print(f"{alg:10} {var:12} n={n:<8} FALLO RecursionError (estimado {est} ms)",
                          flush=True)
                    continue

                media = statistics.mean(tiempos)
                desv = statistics.stdev(tiempos)   # desviación muestral
                w.writerow(base + [f"{t:.4f}" for t in tiempos]
                           + [f"{media:.4f}", f"{desv:.4f}", "medido", "ok", ""])
                f.flush()
                print(f"{alg:10} {var:12} n={n:<8} {media:12.3f} ms  (desv {desv:.3f})", flush=True)
                n_ok, media_ok = n, media


if __name__ == "__main__":
    main()
