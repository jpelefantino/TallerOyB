"""
Tablas de apoyo para el análisis del Punto 1 (se imprimen en Markdown).

  - Tiempos promedio ± desviación por algoritmo, lenguaje, variante y n.
  - Factor de crecimiento observado t(10n)/t(n) frente al teórico.
  - Cambio por orden de entrada (ascendente/aleatorio, descendente/aleatorio).
  - Razón Python/Java en n = 1.000.000.

Uso: python3 analisis.py > resultados/tablas_analisis.md
"""
import csv
import math
import os

BASE = os.path.dirname(os.path.abspath(__file__))
ALGS = ["insertion", "dualpivot", "merge", "heap", "radix", "bucket"]
NOMBRES = {"insertion": "Insertion Sort", "dualpivot": "Dual-Pivot QuickSort",
           "merge": "Merge Sort", "heap": "Heap Sort", "radix": "Radix Sort",
           "bucket": "Bucket Sort"}
TAM = [1_000, 10_000, 100_000, 1_000_000]
VARS = ["aleatorio", "ascendente", "descendente"]
CLASE_ALEATORIO = {"insertion": "n2", "dualpivot": "nlogn", "merge": "nlogn",
                   "heap": "nlogn", "radix": "n", "bucket": "n"}
NOM_CLASE = {"n2": "O(n²)", "nlogn": "O(n log n)", "n": "O(n)"}


def cargar():
    d = {}
    for leng in ("java", "python"):
        with open(os.path.join(BASE, "resultados", f"resultados_{leng}.csv")) as f:
            for r in csv.DictReader(f):
                d[(r["algoritmo"], leng, r["variante"], int(r["n"]))] = r
    return d


def teorico(cl, n0, n1):
    r = n1 / n0
    if cl == "n2":
        return r * r
    if cl == "nlogn":
        return r * math.log(n1) / math.log(n0)
    return r


def celda(r):
    if not r or not r["promedio_ms"]:
        return "—"
    p = float(r["promedio_ms"])
    if r["tipo"] == "estimado":
        etiqueta = "falla*" if r["estado"].startswith("fallo") else "est."
        return f"{p:,.1f} ({etiqueta})"
    return f"{p:,.3f} ± {float(r['desv_ms']):,.3f}"


def main():
    d = cargar()
    for leng in ("java", "python"):
        for var in VARS:
            print(f"\n### Tiempos {leng} — entrada {var} (ms, promedio ± desviación)\n")
            print("| Algoritmo | " + " | ".join(f"n={n:,}" for n in TAM) + " |")
            print("|---" * (len(TAM) + 1) + "|")
            for a in ALGS:
                print(f"| {NOMBRES[a]} | " + " | ".join(celda(d.get((a, leng, var, n)))
                                                      for n in TAM) + " |")

    for leng in ("java", "python"):
        print(f"\n### Factor de crecimiento t(10n)/t(n) — {leng}, entrada aleatoria\n")
        print("| Algoritmo | Teoría | 1k→10k (obs/teo) | 10k→100k (obs/teo) | 100k→1M (obs/teo) |")
        print("|---|---|---|---|---|")
        for a in ALGS:
            cl = CLASE_ALEATORIO[a]
            celdas = []
            for n0, n1 in zip(TAM, TAM[1:]):
                r0, r1 = d.get((a, leng, "aleatorio", n0)), d.get((a, leng, "aleatorio", n1))
                t0 = float(r0["promedio_ms"]) if r0 and r0["promedio_ms"] else None
                t1 = float(r1["promedio_ms"]) if r1 and r1["promedio_ms"] else None
                est = (r1 and r1["tipo"] == "estimado") or (r0 and r0["tipo"] == "estimado")
                if t0 and t1:
                    celdas.append(f"{t1 / t0:.1f}× / {teorico(cl, n0, n1):.1f}×"
                                  + (" (est.)" if est else ""))
                else:
                    celdas.append("—")
            print(f"| {NOMBRES[a]} | {NOM_CLASE[cl]} | " + " | ".join(celdas) + " |")

    print("\n### Efecto del orden (Java): tiempo con entrada ordenada ÷ tiempo aleatoria\n")
    print("| Algoritmo | n | ascendente/aleatorio | descendente/aleatorio |")
    print("|---|---|---|---|")
    for a in ALGS:
        for n in TAM[:3]:
            ra = d.get((a, "java", "aleatorio", n))
            fila = []
            for v in ("ascendente", "descendente"):
                rv = d.get((a, "java", v, n))
                if ra and rv and ra["promedio_ms"] and rv["promedio_ms"]:
                    x = float(rv["promedio_ms"]) / float(ra["promedio_ms"])
                    fila.append(f"{x:.2f}×" + (" (est.)" if rv["tipo"] == "estimado" else ""))
                else:
                    fila.append("—")
            print(f"| {NOMBRES[a]} | {n:,} | " + " | ".join(fila) + " |")

    print("\n### Python ÷ Java, n = 1.000.000, entrada aleatoria\n")
    print("| Algoritmo | Java (ms) | Python (ms) | Python/Java |")
    print("|---|---|---|---|")
    for a in ALGS:
        rj = d.get((a, "java", "aleatorio", 1_000_000))
        rp = d.get((a, "python", "aleatorio", 1_000_000))
        if rj and rp and rj["promedio_ms"] and rp["promedio_ms"]:
            j, p = float(rj["promedio_ms"]), float(rp["promedio_ms"])
            marca = " (est.)" if "estimado" in (rj["tipo"], rp["tipo"]) else ""
            print(f"| {NOMBRES[a]} | {j:,.1f} | {p:,.1f} | {p / j:,.0f}×{marca} |")


if __name__ == "__main__":
    main()
