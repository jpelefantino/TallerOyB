"""
Tablas de apoyo para el análisis del Punto 2 (se imprimen en Markdown y se guardan en UTF-8).

  - Tiempos promedio ± desviación por algoritmo, lenguaje y tamaño n (claves_mixtas).
  - Tiempos para n = 1.000.000 según la posición de la clave (inicio, centro y final).
  - Razón Python/Java en n = 1.000.000.

Uso: python analisis.py
"""
import csv
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
ALGS = ["linear", "binary", "ternary", "jump", "interpolation", "exponential"]
NOMBRES = {
    "linear": "Búsqueda Lineal",
    "binary": "Búsqueda Binaria",
    "ternary": "Búsqueda Ternaria",
    "jump": "Búsqueda por Saltos",
    "interpolation": "Búsqueda por Interpolación",
    "exponential": "Búsqueda Exponencial"
}
TAM = [1_000, 10_000, 100_000, 1_000_000]


def cargar():
    d = {}
    for leng in ("java", "python"):
        ruta = os.path.join(BASE, "resultados", f"resultados_{leng}.csv")
        if not os.path.exists(ruta):
            continue
        with open(ruta, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                d[(r["algoritmo"], leng, r["variante"], int(r["n"]))] = r
    return d


def fmt_tiempo_ns(ns_str, desv_str=None):
    if not ns_str:
        return "—"
    ns = float(ns_str)
    if desv_str is not None:
        desv = float(desv_str)
        if ns < 1000:
            return f"{ns:.1f} ± {desv:.1f} ns"
        elif ns < 1_000_000:
            return f"{ns/1000:.2f} ± {desv/1000:.2f} µs"
        else:
            return f"{ns/1_000_000:.3f} ± {desv/1_000_000:.3f} ms"
    else:
        if ns < 1000:
            return f"{ns:.1f} ns"
        elif ns < 1_000_000:
            return f"{ns/1000:.2f} µs"
        else:
            return f"{ns/1_000_000:.3f} ms"


def generar_markdown(d):
    lineas = []
    lineas.append("# Resultados y Tablas de Análisis: Punto 2 (Algoritmos de Búsqueda)\n")

    # 1. Crecimiento con n
    for leng in ("java", "python"):
        titulo_leng = "Java (compilado)" if leng == "java" else "Python (interpretado)"
        lineas.append(f"### Tiempos de búsqueda promedio — {titulo_leng} (claves mixtas: 500 presentes / 500 ausentes)\n")
        lineas.append("| Algoritmo | " + " | ".join(f"n={n:,}" for n in TAM) + " |")
        lineas.append("|---" * (len(TAM) + 1) + "|")
        for a in ALGS:
            celdas = []
            for n in TAM:
                reg = d.get((a, leng, "claves_mixtas", n))
                if reg:
                    celdas.append(fmt_tiempo_ns(reg["promedio_ns"], reg["desv_ns"]))
                else:
                    celdas.append("—")
            lineas.append(f"| {NOMBRES[a]} | " + " | ".join(celdas) + " |")
        lineas.append("")

    # 2. Efecto de la posición de la clave en n = 1.000.000
    for leng in ("java", "python"):
        titulo_leng = "Java (compilado)" if leng == "java" else "Python (interpretado)"
        lineas.append(f"### Efecto de la posición de la clave (n = 1.000.000) — {titulo_leng}\n")
        lineas.append("| Algoritmo | Inicio (`arr[0]`) | Centro (`arr[n/2]`) | Final (`arr[n-1]`) |")
        lineas.append("|---|---|---|---|")
        for a in ALGS:
            r_ini = d.get((a, leng, "pos_inicio", 1_000_000))
            r_cen = d.get((a, leng, "pos_centro", 1_000_000))
            r_fin = d.get((a, leng, "pos_final", 1_000_000))

            t_ini = fmt_tiempo_ns(r_ini["promedio_ns"], r_ini["desv_ns"]) if r_ini else "—"
            t_cen = fmt_tiempo_ns(r_cen["promedio_ns"], r_cen["desv_ns"]) if r_cen else "—"
            t_fin = fmt_tiempo_ns(r_fin["promedio_ns"], r_fin["desv_ns"]) if r_fin else "—"

            lineas.append(f"| {NOMBRES[a]} | {t_ini} | {t_cen} | {t_fin} |")
        lineas.append("")

    # 3. Compilado vs Interpretado (n = 1.000.000, claves mixtas)
    lineas.append("### Comparación Compilado (Java) vs Interpretado (Python) en n = 1.000.000\n")
    lineas.append("| Algoritmo | Java (promedio) | Python (promedio) | Razón (Python / Java) |")
    lineas.append("|---|---|---|---|")
    for a in ALGS:
        rj = d.get((a, "java", "claves_mixtas", 1_000_000))
        rp = d.get((a, "python", "claves_mixtas", 1_000_000))
        if rj and rp:
            tj = float(rj["promedio_ns"])
            tp = float(rp["promedio_ns"])
            ratio = tp / tj if tj > 0 else 0
            lineas.append(f"| {NOMBRES[a]} | {fmt_tiempo_ns(rj['promedio_ns'])} | {fmt_tiempo_ns(rp['promedio_ns'])} | {ratio:.1f}x |")
        else:
            lineas.append(f"| {NOMBRES[a]} | — | — | — |")
    lineas.append("")

    return "\n".join(lineas)


def main():
    d = cargar()
    texto = generar_markdown(d)
    salida = os.path.join(BASE, "resultados", "tablas_analisis.md")
    with open(salida, "w", encoding="utf-8") as f:
        f.write(texto)
    print(f"Tablas de análisis generadas con éxito en: {salida}")
    print(texto)


if __name__ == "__main__":
    main()
