"""
Gráficas del Punto 2 a partir de resultados/resultados_java.csv y
resultados/resultados_python.csv. Salida en graficas/*.png

  1_crecimiento_java.png / 1_crecimiento_python.png   (líneas, log-log, claves_mixtas)
  2_java_vs_python_1M.png                             (barras, n = 1.000.000, claves_mixtas)

Convención: escala logarítmica en el eje de tiempos, colores consistentes y
valores legibles sobre las barras.
"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

BASE = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(BASE, "graficas")
os.makedirs(SALIDA, exist_ok=True)

ALGS = ["linear", "binary", "ternary", "jump", "interpolation", "exponential"]
NOMBRES = {
    "linear": "Búsqueda Lineal",
    "binary": "Búsqueda Binaria",
    "ternary": "Búsqueda Ternaria",
    "jump": "Búsqueda por Saltos",
    "interpolation": "Búsqueda por Interpolación",
    "exponential": "Búsqueda Exponencial"
}

COLOR_ALG = {
    "linear": "#2a78d6",
    "binary": "#1baf7a",
    "ternary": "#eb6834",
    "jump": "#eda100",
    "interpolation": "#8e44ad",
    "exponential": "#e87ba4"
}

COLOR_LENG = {"java": "#2a78d6", "python": "#eb6834"}
TAMANIOS = [1_000, 10_000, 100_000, 1_000_000]
TINTA, TINTA2, REJILLA = "#0b0b0b", "#52514e", "#e4e3df"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.edgecolor": TINTA2,
    "axes.labelcolor": TINTA,
    "xtick.color": TINTA2,
    "ytick.color": TINTA2,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.facecolor": "white",
})


def cargar():
    datos = {}
    for leng in ("java", "python"):
        ruta = os.path.join(BASE, "resultados", f"resultados_{leng}.csv")
        if not os.path.exists(ruta):
            continue
        with open(ruta, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if not r["promedio_ns"]:
                    continue
                datos[(r["algoritmo"], leng, r["variante"], int(r["n"]))] = r
    return datos


def fmt_tiempo_ns(ns):
    if ns < 1000:
        return f"{ns:.0f} ns" if ns >= 10 else f"{ns:.1f} ns"
    us = ns / 1000
    if us < 1000:
        return f"{us:.1f} µs" if us < 100 else f"{us:.0f} µs"
    ms = us / 1000
    if ms < 1000:
        return f"{ms:.2f} ms" if ms < 10 else f"{ms:.1f} ms"
    s = ms / 1000
    return f"{s:.2f} s"


def graficar_crecimiento(datos, leng):
    titulo_leng = "Java (compilado)" if leng == "java" else "Python (interpretado)"
    fig, ax = plt.subplots(figsize=(8.5, 5.5))

    for a in ALGS:
        xs, ys = [], []
        for n in TAMANIOS:
            clave = (a, leng, "claves_mixtas", n)
            if clave in datos:
                xs.append(n)
                ys.append(float(datos[clave]["promedio_ns"]))
        if xs:
            ax.plot(
                xs, ys, marker="o", color=COLOR_ALG[a],
                label=NOMBRES[a], linewidth=1.8, markersize=5
            )

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xticks(TAMANIOS)
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.ticklabel_format(style="plain", axis="x")
    ax.set_xlabel("Tamaño del arreglo n (escala logarítmica)")
    ax.set_ylabel("Tiempo promedio por búsqueda en ns (escala logarítmica)")
    ax.set_title(f"Crecimiento del tiempo por búsqueda — {titulo_leng}", pad=14, fontweight="bold")
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, color=REJILLA)
    ax.legend(frameon=True, facecolor="white", edgecolor="none", fontsize=9)

    fig.tight_layout()
    ruta_salida = os.path.join(SALIDA, f"1_crecimiento_{leng}.png")
    fig.savefig(ruta_salida, dpi=180)
    plt.close(fig)
    print(f"Guardada: {ruta_salida}")


def graficar_java_vs_python_1M(datos):
    fig, ax = plt.subplots(figsize=(10, 6))
    ancho = 0.35
    indices = range(len(ALGS))

    vals_java = []
    vals_py = []
    for a in ALGS:
        cj = (a, "java", "claves_mixtas", 1_000_000)
        cp = (a, "python", "claves_mixtas", 1_000_000)
        vals_java.append(float(datos[cj]["promedio_ns"]) if cj in datos else 0.0)
        vals_py.append(float(datos[cp]["promedio_ns"]) if cp in datos else 0.0)

    rects1 = ax.bar([i - ancho/2 for i in indices], vals_java, ancho,
                    label="Java (compilado)", color=COLOR_LENG["java"])
    rects2 = ax.bar([i + ancho/2 for i in indices], vals_py, ancho,
                    label="Python (interpretado)", color=COLOR_LENG["python"])

    ax.set_yscale("log")
    ax.set_ylabel("Tiempo promedio por búsqueda en ns (escala logarítmica)")
    ax.set_title("Java frente a Python con n = 1.000.000 (1.000 claves mixtas)", pad=14, fontweight="bold")
    ax.set_xticks(list(indices))
    ax.set_xticklabels([NOMBRES[a] for a in ALGS], rotation=15, ha="right")
    ax.grid(True, which="both", axis="y", linestyle="--", linewidth=0.5, color=REJILLA)
    ax.legend(frameon=True, facecolor="white", edgecolor="none")

    # Etiquetas de texto con valores legibles sobre las barras
    for rect in rects1:
        h = rect.get_height()
        if h > 0:
            ax.annotate(fmt_tiempo_ns(h),
                        xy=(rect.get_x() + rect.get_width() / 2, h),
                        xytext=(0, 4), textcoords="offset points",
                        ha="center", va="bottom", fontsize=8, color=TINTA2)

    for rect in rects2:
        h = rect.get_height()
        if h > 0:
            ax.annotate(fmt_tiempo_ns(h),
                        xy=(rect.get_x() + rect.get_width() / 2, h),
                        xytext=(0, 4), textcoords="offset points",
                        ha="center", va="bottom", fontsize=8, color=TINTA2)

    fig.tight_layout()
    ruta_salida = os.path.join(SALIDA, "2_java_vs_python_1M.png")
    fig.savefig(ruta_salida, dpi=180)
    plt.close(fig)
    print(f"Guardada: {ruta_salida}")


def main():
    datos = cargar()
    if not datos:
        print("No hay datos CSV disponibles para graficar.")
        return
    for leng in ("java", "python"):
        graficar_crecimiento(datos, leng)
    graficar_java_vs_python_1M(datos)


if __name__ == "__main__":
    main()
