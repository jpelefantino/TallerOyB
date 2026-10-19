"""
Gráficas del Punto 1 a partir de resultados/resultados_java.csv y
resultados/resultados_python.csv. Salida en graficas/*.png

  1_crecimiento_java.png / 1_crecimiento_python.png   (líneas, log-log, entrada aleatoria)
  2_orden_entrada_<n>.png  (n = 1000, 10000, 100000; barras, Java)
  3_java_vs_python_1M.png  (barras, n = 1.000.000, entrada aleatoria)

Convención: valores MEDIDOS = marcador relleno, línea continua, barra sólida.
            valores ESTIMADOS = marcador hueco, línea punteada, barra rayada.
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

ALGS = ["insertion", "dualpivot", "merge", "heap", "radix", "bucket"]
NOMBRES = {"insertion": "Insertion Sort", "dualpivot": "Dual-Pivot QuickSort",
           "merge": "Merge Sort", "heap": "Heap Sort", "radix": "Radix Sort",
           "bucket": "Bucket Sort"}
COLOR_ALG = {"insertion": "#2a78d6", "dualpivot": "#eb6834", "merge": "#1baf7a",
             "heap": "#eda100", "radix": "#e87ba4", "bucket": "#008300"}
COLOR_VAR = {"aleatorio": "#2a78d6", "ascendente": "#1baf7a", "descendente": "#eb6834"}
COLOR_LENG = {"java": "#2a78d6", "python": "#eb6834"}
TAMANIOS = [1_000, 10_000, 100_000, 1_000_000]
TINTA, TINTA2, REJILLA = "#0b0b0b", "#52514e", "#e4e3df"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": TINTA2,
    "axes.labelcolor": TINTA, "xtick.color": TINTA2, "ytick.color": TINTA2,
    "axes.spines.top": False, "axes.spines.right": False, "figure.facecolor": "white",
})


def cargar():
    datos = {}
    for leng in ("java", "python"):
        ruta = os.path.join(BASE, "resultados", f"resultados_{leng}.csv")
        if not os.path.exists(ruta):
            continue
        with open(ruta) as f:
            for r in csv.DictReader(f):
                if not r["promedio_ms"]:
                    continue
                datos[(r["algoritmo"], leng, r["variante"], int(r["n"]))] = r
    return datos


def fmt_tiempo(ms):
    if ms < 1:
        return f"{ms:.3f} ms"
    if ms < 1000:
        return f"{ms:.1f} ms" if ms < 100 else f"{ms:.0f} ms"
    s = ms / 1000
    if s < 60:
        return f"{s:.2f} s" if s < 10 else f"{s:.1f} s"
    m = s / 60
    if m < 60:
        return f"{m:.1f} min"
    h = m / 60
    if h < 48:
        return f"{h:.1f} h"
    return f"{h / 24:.0f} días"


def rejilla(ax):
    ax.grid(True, which="major", color=REJILLA, linewidth=0.8)
    ax.set_axisbelow(True)


def crecimiento(datos, leng):
    fig, ax = plt.subplots(figsize=(9, 5.6))
    for alg in ALGS:
        pts = []
        for n in TAMANIOS:
            r = datos.get((alg, leng, "aleatorio", n))
            if r:
                pts.append((n, float(r["promedio_ms"]), r["tipo"] == "estimado"))
        c = COLOR_ALG[alg]
        for (n0, t0, e0), (n1, t1, e1) in zip(pts, pts[1:]):
            ax.plot([n0, n1], [t0, t1], color=c, lw=2, ls="--" if (e0 or e1) else "-")
        for n, t, e in pts:
            ax.plot(n, t, "o", ms=8, color=c, mfc="white" if e else c, mew=2)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xticks(TAMANIOS)
    ax.set_xticklabels(["1.000", "10.000", "100.000", "1.000.000"])
    ax.set_xlim(700, 1_500_000)
    ax.set_xlabel("Tamaño del arreglo n (escala logarítmica)")
    ax.set_ylabel("Tiempo promedio en ms (escala logarítmica)")
    leng_nom = "Java (compilado)" if leng == "java" else "Python (interpretado)"
    ax.set_title(f"Crecimiento del tiempo con entrada aleatoria, {leng_nom}",
                 loc="left", fontsize=12, color=TINTA, pad=12)
    rejilla(ax)
    manejadores = [Line2D([], [], color=COLOR_ALG[a], lw=2, marker="o", label=NOMBRES[a])
                   for a in ALGS]
    manejadores += [Line2D([], [], color=TINTA2, lw=2, marker="o", label="Medido"),
                    Line2D([], [], color=TINTA2, lw=2, ls="--", marker="o", mfc="white",
                           label="Estimado")]
    ax.legend(handles=manejadores, loc="upper left", frameon=False, fontsize=9)
    fig.tight_layout()
    fig.savefig(os.path.join(SALIDA, f"1_crecimiento_{leng}.png"), dpi=200)
    plt.close(fig)


def barras(ax, grupos, series, colores, valores, etiquetas_serie):
    """grupos: lista de algoritmos; series: claves; valores[(g,s)] = (ms, estimado, estado)."""
    k = len(series)
    ancho = 0.8 / k
    todos = [v[0] for v in valores.values() if v]
    piso = min(todos) / 3 if todos else 1e-3
    for i, g in enumerate(grupos):
        for j, s in enumerate(series):
            v = valores.get((g, s))
            if not v:
                continue
            ms, est, estado = v
            x = i - 0.4 + ancho * (j + 0.5)
            ax.bar(x, ms - piso, bottom=piso, width=ancho * 0.92, color="white" if est else colores[s],
                   edgecolor=colores[s], hatch="////" if est else None, linewidth=1.5)
            texto = fmt_tiempo(ms)
            if est:
                texto += " (est." + (", falla" if estado.startswith("fallo") else "") + ")"
            ax.text(x, ms * 1.15, texto, rotation=90, ha="center", va="bottom", fontsize=7.5,
                    color=TINTA)
    ax.set_yscale("log")
    ax.set_ylim(piso, max(todos) * 60 if todos else 10)
    ax.set_xticks(range(len(grupos)))
    ax.set_xticklabels([NOMBRES[g].replace(" ", "\n", 1) for g in grupos], fontsize=9)
    ax.set_ylabel("Tiempo promedio en ms (escala logarítmica)")
    rejilla(ax)
    ax.grid(False, axis="x")
    manejadores = [Patch(facecolor=colores[s], edgecolor=colores[s], label=etiquetas_serie[s])
                   for s in series]
    manejadores.append(Patch(facecolor="white", edgecolor=TINTA2, hatch="////",
                             label="Estimado (no ejecutado o falló)"))
    ax.legend(handles=manejadores, loc="upper right", frameon=False, fontsize=9, ncol=2)


def orden_entrada(datos, n):
    vals = {}
    for alg in ALGS:
        for var in COLOR_VAR:
            r = datos.get((alg, "java", var, n))
            if r:
                vals[(alg, var)] = (float(r["promedio_ms"]), r["tipo"] == "estimado", r["estado"])
    fig, ax = plt.subplots(figsize=(10, 5.8))
    barras(ax, ALGS, list(COLOR_VAR), COLOR_VAR, vals,
           {"aleatorio": "Aleatoria", "ascendente": "Ascendente", "descendente": "Descendente"})
    ax.set_title("Efecto del orden de entrada en Java, n = " + f"{n:,}".replace(",", "."),
                 loc="left", fontsize=12, color=TINTA, pad=12)
    fig.tight_layout()
    fig.savefig(os.path.join(SALIDA, f"2_orden_entrada_{n}.png"), dpi=200)
    plt.close(fig)


def java_vs_python(datos):
    n = 1_000_000
    vals = {}
    for alg in ALGS:
        for leng in COLOR_LENG:
            r = datos.get((alg, leng, "aleatorio", n))
            if r:
                vals[(alg, leng)] = (float(r["promedio_ms"]), r["tipo"] == "estimado", r["estado"])
    fig, ax = plt.subplots(figsize=(10, 5.8))
    barras(ax, ALGS, list(COLOR_LENG), COLOR_LENG, vals,
           {"java": "Java (compilado)", "python": "Python (interpretado)"})
    ax.set_title("Java frente a Python, n = 1.000.000, entrada aleatoria",
                 loc="left", fontsize=12, color=TINTA, pad=12)
    fig.tight_layout()
    fig.savefig(os.path.join(SALIDA, "3_java_vs_python_1M.png"), dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    d = cargar()
    for leng in ("java", "python"):
        crecimiento(d, leng)
    for n in (1_000, 10_000, 100_000):
        orden_entrada(d, n)
    java_vs_python(d)
    print("Gráficas generadas en", SALIDA)
