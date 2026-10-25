import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

BASE = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(BASE, "graficas")
os.makedirs(SALIDA, exist_ok=True)

COLOR_JAVA = "#2a78d6"
COLOR_PYTHON = "#eb6834"
COLOR_COMP = "#3498db"
COLOR_NO_COMP = "#2ecc71"
COLOR_LINEAL = "#e74c3c"
COLOR_BINARIA = "#1baf7a"
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


def grafica_comparativos_vs_no_comparativos():
    
    algs = [
        "Radix Sort\n(No Comp)",
        "Bucket Sort\n(No Comp)",
        "Dual-Pivot QS\n(Comp)",
        "Heap Sort\n(Comp)",
        "Merge Sort\n(Comp)",
        "Insertion Sort\n(Comp)"
    ]
    
    # Tiempos en ms para n = 1.000.000 (aleatorio)
    tiempos_java = [83.320, 498.618, 91.854, 175.949, 192.903, 78826.821]
    tiempos_python = [5951.966, 1915.109, 2600.673, 8585.681, 6090.020, 30575356.2]
    
    x = np.arange(len(algs))
    ancho = 0.38
    
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    
    barras_j = ax.bar(x - ancho/2, tiempos_java, ancho, label="Java (compilado)", color=COLOR_JAVA, alpha=0.9, edgecolor="none")
    barras_p = ax.bar(x + ancho/2, tiempos_python, ancho, label="Python (interpretado)", color=COLOR_PYTHON, alpha=0.9, edgecolor="none")
    
    ax.set_yscale("log")
    ax.set_ylabel("Tiempo de ejecución (ms) — Escala logarítmica", fontweight="bold")
    ax.set_title("Comparación de Algoritmos de Ordenamiento (n = 1.000.000, aleatorio)\nComparativos frente a No Comparativos", fontweight="bold", pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(algs, fontweight="bold")
    ax.grid(axis="y", linestyle="--", color=REJILLA, alpha=0.7)
    
    # Resaltar la división de familias
    ax.axvline(1.5, color=TINTA2, linestyle=":", linewidth=1.5, alpha=0.7)
    ax.text(0.5, 3e7, "Familias No Comparativas\n(Escapan a cota Ω(n log n))", ha="center", va="center", bbox=dict(boxstyle="round,pad=0.4", fc="#e8f8f5", ec="#2ecc71", lw=1.2), fontsize=9)
    ax.text(3.5, 3e7, "Familias Basadas en Comparaciones\n(Sujetas a cota Ω(n log n))", ha="center", va="center", bbox=dict(boxstyle="round,pad=0.4", fc="#ebf5fb", ec="#3498db", lw=1.2), fontsize=9)
    
    # Etiquetas de valor en barras
    for bar in barras_j:
        h = bar.get_height()
        texto = f"{h:,.0f} ms" if h >= 1000 else f"{h:.1f} ms"
        ax.text(bar.get_x() + bar.get_width()/2, h * 1.3, texto, ha="center", va="bottom", fontsize=7.5, color=COLOR_JAVA, fontweight="bold", rotation=0)
        
    for bar in barras_p:
        h = bar.get_height()
        texto = f"{h/1000:,.1f} s" if h >= 1000 else f"{h:.1f} ms"
        if h > 1e6:
            texto = f"{h/3.6e6:.1f} h (est.)"
        ax.text(bar.get_x() + bar.get_width()/2, h * 1.3, texto, ha="center", va="bottom", fontsize=7.5, color=COLOR_PYTHON, fontweight="bold", rotation=0)
        
    ax.set_ylim(10, 2e8)
    ax.legend(loc="upper left", frameon=True, facecolor="white", edgecolor=REJILLA)
    plt.tight_layout()
    salida = os.path.join(SALIDA, "1_comparativos_vs_no_comparativos.png")
    plt.savefig(salida)
    plt.close()
    print(f"Gráfica guardada: {salida}")


def grafica_breakeven():
   
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5), dpi=150)
    
    # ------------------ SUBPLOT 1: JAVA ------------------
    # Tiempos Java:
    t_sort_java = 83.320       # ms (Radix Sort)
    t_sort_java_dpqs = 91.854  # ms (Dual-Pivot)
    t_lin_java = 0.14900       # ms (149.00 µs)
    t_bin_java = 0.0002743     # ms (274.3 ns)
    
    k_vals_java = np.linspace(1, 1200, 500)
    t_sin_ordenar_java = k_vals_java * t_lin_java
    t_con_ordenar_radix_java = t_sort_java + k_vals_java * t_bin_java
    t_con_ordenar_dpqs_java = t_sort_java_dpqs + k_vals_java * t_bin_java
    
    k_star_java = t_sort_java / (t_lin_java - t_bin_java)
    y_star_java = k_star_java * t_lin_java
    
    ax1.plot(k_vals_java, t_sin_ordenar_java, label="Búsqueda Lineal sin ordenar ($k \\cdot t_{\\text{lin}}$)", color=COLOR_LINEAL, linewidth=2.2)
    ax1.plot(k_vals_java, t_con_ordenar_radix_java, label="Radix Sort + Búsqueda Binaria", color=COLOR_BINARIA, linewidth=2.2)
    ax1.plot(k_vals_java, t_con_ordenar_dpqs_java, label="Dual-Pivot QS + Búsqueda Binaria", color="#2980b9", linestyle="--", linewidth=1.8, alpha=0.85)
    
    # Marcar punto de corte
    ax1.plot(k_star_java, y_star_java, "o", color=COLOR_LINEAL, markersize=7, zorder=5)
    ax1.axvline(k_star_java, color="gray", linestyle=":", linewidth=1.2)
    ax1.axhline(y_star_java, color="gray", linestyle=":", linewidth=1.2)
    
    ax1.annotate(f"Punto de corte:\n$k^* \\approx 561$ búsquedas\n($T \\approx 83.5$ ms)",
                 xy=(k_star_java, y_star_java), xytext=(k_star_java + 80, y_star_java - 30),
                 arrowprops=dict(facecolor="black", shrink=0.08, width=1, headwidth=6),
                 bbox=dict(boxstyle="round,pad=0.4", fc="#fef9e7", ec="#f39c12", lw=1),
                 fontsize=9, fontweight="bold")
    
    ax1.set_title("Java: Punto de Equilibrio ($n = 1.000.000$)", fontweight="bold", pad=12)
    ax1.set_xlabel("Número de búsquedas ($k$)", fontweight="bold")
    ax1.set_ylabel("Tiempo total acumulado (ms)", fontweight="bold")
    ax1.grid(True, linestyle="--", color=REJILLA, alpha=0.7)
    ax1.set_xlim(0, 1200)
    ax1.set_ylim(0, 180)
    ax1.legend(loc="upper left", frameon=True, facecolor="white", edgecolor=REJILLA, fontsize=8.5)
    
    # ------------------ SUBPLOT 2: PYTHON ------------------
    # Tiempos Python:
    t_sort_py = 1915.109       # ms (Bucket Sort)
    t_sort_py_dpqs = 2600.673  # ms (Dual-Pivot)
    t_lin_py = 26.440          # ms
    t_bin_py = 0.00564         # ms (5.64 µs)
    
    k_vals_py = np.linspace(1, 200, 500)
    t_sin_ordenar_py = k_vals_py * t_lin_py
    t_con_ordenar_bucket_py = t_sort_py + k_vals_py * t_bin_py
    t_con_ordenar_dpqs_py = t_sort_py_dpqs + k_vals_py * t_bin_py
    
    k_star_py = t_sort_py / (t_lin_py - t_bin_py)
    y_star_py = k_star_py * t_lin_py
    
    ax2.plot(k_vals_py, t_sin_ordenar_py, label="Búsqueda Lineal sin ordenar ($k \\cdot t_{\\text{lin}}$)", color=COLOR_LINEAL, linewidth=2.2)
    ax2.plot(k_vals_py, t_con_ordenar_bucket_py, label="Bucket Sort + Búsqueda Binaria", color=COLOR_BINARIA, linewidth=2.2)
    ax2.plot(k_vals_py, t_con_ordenar_dpqs_py, label="Dual-Pivot QS + Búsqueda Binaria", color="#2980b9", linestyle="--", linewidth=1.8, alpha=0.85)
    
    # Marcar punto de corte
    ax2.plot(k_star_py, y_star_py, "o", color=COLOR_LINEAL, markersize=7, zorder=5)
    ax2.axvline(k_star_py, color="gray", linestyle=":", linewidth=1.2)
    ax2.axhline(y_star_py, color="gray", linestyle=":", linewidth=1.2)
    
    ax2.annotate(f"Punto de corte:\n$k^* \\approx 73$ búsquedas\n($T \\approx 1.916$ ms)",
                 xy=(k_star_py, y_star_py), xytext=(k_star_py + 20, y_star_py - 700),
                 arrowprops=dict(facecolor="black", shrink=0.08, width=1, headwidth=6),
                 bbox=dict(boxstyle="round,pad=0.4", fc="#fef9e7", ec="#f39c12", lw=1),
                 fontsize=9, fontweight="bold")
    
    ax2.set_title("Python: Punto de Equilibrio ($n = 1.000.000$)", fontweight="bold", pad=12)
    ax2.set_xlabel("Número de búsquedas ($k$)", fontweight="bold")
    ax2.set_ylabel("Tiempo total acumulado (ms)", fontweight="bold")
    ax2.grid(True, linestyle="--", color=REJILLA, alpha=0.7)
    ax2.set_xlim(0, 200)
    ax2.set_ylim(0, 5000)
    ax2.legend(loc="upper left", frameon=True, facecolor="white", edgecolor=REJILLA, fontsize=8.5)
    
    plt.tight_layout()
    salida = os.path.join(SALIDA, "2_ordenar_vs_no_ordenar_breakeven.png")
    plt.savefig(salida)
    plt.close()
    print(f"Gráfica guardada: {salida}")


if __name__ == "__main__":
    grafica_comparativos_vs_no_comparativos()
    grafica_breakeven()
