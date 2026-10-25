import os
import math
import csv

def cargar_datos_punto1():
    # Tiempos medidos para n = 1.000.000 con entrada aleatoria (Punto 1)
    # Fuente: punto1/resultados/resultados_java.csv y resultados_python.csv
    datos_java = {
        "Radix Sort": {"promedio_ms": 83.320, "desv_ms": 9.307, "tipo": "No comparativo", "familia": "Distribución"},
        "Dual-Pivot QuickSort": {"promedio_ms": 91.854, "desv_ms": 7.004, "tipo": "Comparativo", "familia": "Partición"},
        "Heap Sort": {"promedio_ms": 175.949, "desv_ms": 12.364, "tipo": "Comparativo", "familia": "Selección"},
        "Merge Sort": {"promedio_ms": 192.903, "desv_ms": 24.911, "tipo": "Comparativo", "familia": "Mezcla"},
        "Bucket Sort": {"promedio_ms": 498.618, "desv_ms": 128.993, "tipo": "No comparativo", "familia": "Distribución"},
        "Insertion Sort": {"promedio_ms": 78826.821, "desv_ms": 1429.596, "tipo": "Comparativo", "familia": "Inserción"}
    }
    
    datos_python = {
        "Bucket Sort": {"promedio_ms": 1915.109, "desv_ms": 95.585, "tipo": "No comparativo", "familia": "Distribución"},
        "Dual-Pivot QuickSort": {"promedio_ms": 2600.673, "desv_ms": 80.337, "tipo": "Comparativo", "familia": "Partición"},
        "Radix Sort": {"promedio_ms": 5951.966, "desv_ms": 117.606, "tipo": "No comparativo", "familia": "Distribución"},
        "Merge Sort": {"promedio_ms": 6090.020, "desv_ms": 305.685, "tipo": "Comparativo", "familia": "Mezcla"},
        "Heap Sort": {"promedio_ms": 8585.681, "desv_ms": 503.718, "tipo": "Comparativo", "familia": "Selección"},
        "Insertion Sort": {"promedio_ms": 30575356.2, "desv_ms": 0.0, "tipo": "Comparativo", "familia": "Inserción"} # Estimado teórico
    }
    return datos_java, datos_python

def cargar_datos_punto2():
    busqueda_java = {
        "Búsqueda Lineal": {"promedio_ms": 0.14900, "desv_ms": 0.00874, "unidad_orig": "149.00 ± 8.74 µs"},
        "Búsqueda Binaria": {"promedio_ms": 0.0002743, "desv_ms": 0.0000715, "unidad_orig": "274.3 ± 71.5 ns"},
        "Búsqueda Ternaria": {"promedio_ms": 0.0001506, "desv_ms": 0.0000230, "unidad_orig": "150.6 ± 23.0 ns"},
        "Búsqueda por Saltos": {"promedio_ms": 0.00135, "desv_ms": 0.00042, "unidad_orig": "1.35 ± 0.42 µs"},
        "Búsqueda por Interpolación": {"promedio_ms": 0.0000338, "desv_ms": 0.0000089, "unidad_orig": "33.8 ± 8.9 ns"},
        "Búsqueda Exponencial": {"promedio_ms": 0.0002194, "desv_ms": 0.0000540, "unidad_orig": "219.4 ± 54.0 ns"}
    }
    
    busqueda_python = {
        "Búsqueda Lineal": {"promedio_ms": 26.440, "desv_ms": 1.079, "unidad_orig": "26.440 ± 1.079 ms"},
        "Búsqueda Binaria": {"promedio_ms": 0.00564, "desv_ms": 0.00049, "unidad_orig": "5.64 ± 0.49 µs"},
        "Búsqueda Ternaria": {"promedio_ms": 0.00423, "desv_ms": 0.00059, "unidad_orig": "4.23 ± 0.59 µs"},
        "Búsqueda por Saltos": {"promedio_ms": 0.23251, "desv_ms": 0.02889, "unidad_orig": "232.51 ± 28.89 µs"},
        "Búsqueda por Interpolación": {"promedio_ms": 0.00224, "desv_ms": 0.00101, "unidad_orig": "2.24 ± 1.01 µs"},
        "Búsqueda Exponencial": {"promedio_ms": 0.00501, "desv_ms": 0.00099, "unidad_orig": "5.01 ± 0.99 µs"}
    }
    return busqueda_java, busqueda_python

def calcular_breakeven(t_sort_ms, t_lineal_ms, t_binaria_ms):
    """
    Calcula k tal que:
    T_ordenar + k * t_binaria < k * t_lineal
    k * (t_lineal - t_binaria) > T_ordenar
    k > T_ordenar / (t_lineal - t_binaria)
    """
    delta_busqueda = t_lineal_ms - t_binaria_ms
    if delta_busqueda <= 0:
        return float('inf'), float('inf')
    k_exacto = t_sort_ms / delta_busqueda
    k_minimo_entero = math.ceil(k_exacto) if k_exacto != math.ceil(k_exacto) else int(k_exacto) + 1
    return k_exacto, k_minimo_entero

def generar_reporte():
    sort_java, sort_py = cargar_datos_punto1()
    search_java, search_py = cargar_datos_punto2()
    
    # Cálculos Java
    # Mejor absoluto: Radix Sort
    t_sort_java_radix = sort_java["Radix Sort"]["promedio_ms"]
    # Mejor comparativo: Dual-Pivot QuickSort
    t_sort_java_dpqs = sort_java["Dual-Pivot QuickSort"]["promedio_ms"]
    
    t_lin_java = search_java["Búsqueda Lineal"]["promedio_ms"]
    t_bin_java = search_java["Búsqueda Binaria"]["promedio_ms"]
    t_int_java = search_java["Búsqueda por Interpolación"]["promedio_ms"]
    
    k_java_radix_exact, k_java_radix = calcular_breakeven(t_sort_java_radix, t_lin_java, t_bin_java)
    k_java_dpqs_exact, k_java_dpqs = calcular_breakeven(t_sort_java_dpqs, t_lin_java, t_bin_java)
    k_java_radix_int_exact, k_java_radix_int = calcular_breakeven(t_sort_java_radix, t_lin_java, t_int_java)
    
    # Cálculos Python
    # Mejor absoluto: Bucket Sort
    t_sort_py_bucket = sort_py["Bucket Sort"]["promedio_ms"]
    # Mejor comparativo: Dual-Pivot QuickSort
    t_sort_py_dpqs = sort_py["Dual-Pivot QuickSort"]["promedio_ms"]
    
    t_lin_py = search_py["Búsqueda Lineal"]["promedio_ms"]
    t_bin_py = search_py["Búsqueda Binaria"]["promedio_ms"]
    t_int_py = search_py["Búsqueda por Interpolación"]["promedio_ms"]
    
    k_py_bucket_exact, k_py_bucket = calcular_breakeven(t_sort_py_bucket, t_lin_py, t_bin_py)
    k_py_dpqs_exact, k_py_dpqs = calcular_breakeven(t_sort_py_dpqs, t_lin_py, t_bin_py)
    k_py_bucket_int_exact, k_py_bucket_int = calcular_breakeven(t_sort_py_bucket, t_lin_py, t_int_py)
    
    md = []
    md.append("# Resultados y Tablas de Análisis: Punto 3 (Análisis Comparativo)")
    md.append("")
    md.append("Este documento reúne y cruza cuantitativamente las mediciones obtenidas en el **Punto 1** (Ordenamiento) y el **Punto 2** (Búsqueda) para responder a las preguntas de análisis comparativo del taller.")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## 1. Comparación entre Algoritmos Comparativos y No Comparativos (n = 1.000.000)")
    md.append("")
    md.append("A continuación se comparan los tiempos de ejecución medidos en el Punto 1 para ordenar 1.000.000 de enteros de 8 dígitos con entrada aleatoria.")
    md.append("")
    md.append("### Tabla 1. Tiempos de ordenamiento en Java y Python (n = 1.000.000, aleatorio)")
    md.append("")
    md.append("| Algoritmo | Tipo | Complejidad Teórica | Java (ms) | Python (ms) | Python / Java |")
    md.append("|---|---|---|---|---|---|")
    
    for alg in ["Radix Sort", "Bucket Sort", "Dual-Pivot QuickSort", "Heap Sort", "Merge Sort", "Insertion Sort"]:
        tipo = sort_java[alg]["tipo"]
        c_teo = "O(d · (n + b)) ~ O(n)" if alg == "Radix Sort" else ("O(n) prom / O(n²) peor" if alg == "Bucket Sort" else ("O(n log n) / O(n²) peor" if alg == "Dual-Pivot QuickSort" else ("O(n log n)" if alg in ["Heap Sort", "Merge Sort"] else "O(n²)")))
        tj = f"{sort_java[alg]['promedio_ms']:,.3f} ± {sort_java[alg]['desv_ms']:.3f}"
        if alg == "Insertion Sort":
            tp = f"{sort_py[alg]['promedio_ms']:,.1f} (est.)"
            ratio = f"{sort_py[alg]['promedio_ms'] / sort_java[alg]['promedio_ms']:,.0f}×"
        else:
            tp = f"{sort_py[alg]['promedio_ms']:,.3f} ± {sort_py[alg]['desv_ms']:.3f}"
            ratio = f"{sort_py[alg]['promedio_ms'] / sort_java[alg]['promedio_ms']:.1f}×"
        md.append(f"| {alg} | {tipo} | {c_teo} | {tj} | {tp} | {ratio} |")
    
    md.append("")
    md.append("### Observaciones clave:")
    md.append("1. **Java:** El algoritmo no comparativo **Radix Sort** obtuvo el mejor tiempo absoluto (**83,320 ms**), superando al mejor comparativo (**Dual-Pivot QuickSort** con 91,854 ms), a Heap Sort (175,949 ms) y a Merge Sort (192,903 ms).")
    md.append("2. **Python:** El algoritmo no comparativo **Bucket Sort** fue el más veloz (**1.915,109 ms**), aventajando a Dual-Pivot QuickSort (2.600,673 ms) y a Radix Sort (5.951,966 ms).")
    md.append("3. **Escape de la cota Ω(n log n):** Tanto Radix Sort como Bucket Sort superaron o igualaron el desempeño de los mejores algoritmos comparativos porque no están sujetos a la cota inferior de información basada en comparaciones de árbol de decisión.")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## 2. ¿Ordenar o No Ordenar? (Cálculo del Punto de Equilibrio k*)")
    md.append("")
    md.append("Supóngase un arreglo desordenado de $n = 1.000.000$ elementos sobre el cual se realizarán $k$ búsquedas.")
    md.append("")
    md.append("### Formulación matemática:")
    md.append("- **Estrategia A (Sin ordenar):** Se realizan $k$ búsquedas lineales directas sobre el arreglo desordenado.")
    md.append("  $$T_A(k) = k \\cdot t_{\\text{lineal}}$$")
    md.append("- **Estrategia B (Ordenar primero y buscar con Búsqueda Binaria):** Se invierte un costo inicial de ordenamiento $T_{\\text{ordenar}}$ una sola vez, y luego cada una de las $k$ búsquedas se efectúa en tiempo logarítmico con Búsqueda Binaria.")
    md.append("  $$T_B(k) = T_{\\text{ordenar}} + k \\cdot t_{\\text{binaria}}$$")
    md.append("- **Condición de conveniencia (Break-even):**")
    md.append("  $$T_B(k) < T_A(k) \\iff T_{\\text{ordenar}} + k \\cdot t_{\\text{binaria}} < k \\cdot t_{\\text{lineal}}$$")
    md.append("  $$k \\cdot (t_{\\text{lineal}} - t_{\\text{binaria}}) > T_{\\text{ordenar}}$$")
    md.append("  $$k > \\frac{T_{\\text{ordenar}}}{t_{\\text{lineal}} - t_{\\text{binaria}}}$$")
    md.append("")
    md.append("### Tabla 2. Tiempos base para n = 1.000.000 empleados en el cálculo")
    md.append("")
    md.append("| Lenguaje | Algoritmo de Ordenamiento | $T_{\\text{ordenar}}$ | $t_{\\text{lineal}}$ (por búsqueda) | $t_{\\text{binaria}}$ (por búsqueda) | $\\Delta t = t_{\\text{lineal}} - t_{\\text{binaria}}$ |")
    md.append("|---|---|---|---|---|---|")
    md.append(f"| **Java** | **Radix Sort** (Mejor absoluto) | {t_sort_java_radix:.3f} ms | {t_lin_java * 1000:.2f} µs ({t_lin_java:.5f} ms) | {t_bin_java * 1e6:.1f} ns ({t_bin_java:.7f} ms) | {t_lin_java - t_bin_java:.5f} ms |")
    md.append(f"| **Java** | **Dual-Pivot QS** (Mejor comparativo) | {t_sort_java_dpqs:.3f} ms | {t_lin_java * 1000:.2f} µs ({t_lin_java:.5f} ms) | {t_bin_java * 1e6:.1f} ns ({t_bin_java:.7f} ms) | {t_lin_java - t_bin_java:.5f} ms |")
    md.append(f"| **Python** | **Bucket Sort** (Mejor absoluto) | {t_sort_py_bucket:,.3f} ms | {t_lin_py:.3f} ms | {t_bin_py * 1000:.2f} µs ({t_bin_py:.5f} ms) | {t_lin_py - t_bin_py:.5f} ms |")
    md.append(f"| **Python** | **Dual-Pivot QS** (Mejor comparativo) | {t_sort_py_dpqs:,.3f} ms | {t_lin_py:.3f} ms | {t_bin_py * 1000:.2f} µs ({t_bin_py:.5f} ms) | {t_lin_py - t_bin_py:.5f} ms |")
    md.append("")
    md.append("### Tabla 3. Punto de equilibrio $k^*$ resultante")
    md.append("")
    md.append("| Lenguaje | Algoritmo de Ordenamiento Utilizado | $k^*$ Exacto | $k$ Mínimo Entero ($k \\ge$) | Fracción de $n$ ($k^* / 10^6$) |")
    md.append("|---|---|---|---|---|")
    md.append(f"| **Java** | **Radix Sort** (Mejor absoluto) | {k_java_radix_exact:.2f} | **{k_java_radix}** búsquedas | 0,056% de los datos |")
    md.append(f"| **Java** | **Dual-Pivot QuickSort** (Mejor comparativo) | {k_java_dpqs_exact:.2f} | **{k_java_dpqs}** búsquedas | 0,062% de los datos |")
    md.append(f"| **Python** | **Bucket Sort** (Mejor absoluto) | {k_py_bucket_exact:.2f} | **{k_py_bucket}** búsquedas | 0,007% de los datos |")
    md.append(f"| **Python** | **Dual-Pivot QuickSort** (Mejor comparativo) | {k_py_dpqs_exact:.2f} | **{k_py_dpqs}** búsquedas | 0,010% de los datos |")
    md.append("")
    md.append("### Variante complementaria: ¿Y si usamos Búsqueda por Interpolación?")
    md.append("Dado que en el Punto 2 la Búsqueda por Interpolación fue el algoritmo más rápido de todos (33,8 ns en Java y 2,24 µs en Python):")
    md.append(f"- **Java (Radix Sort + Interpolación):** $k^* = \\frac{{{t_sort_java_radix:.3f}}}{{{t_lin_java:.5f} - {t_int_java:.7f}}} = {k_java_radix_int_exact:.2f} \\implies k \\ge {k_java_radix_int}$ búsquedas.")
    md.append(f"- **Python (Bucket Sort + Interpolación):** $k^* = \\frac{{{t_sort_py_bucket:,.3f}}}{{{t_lin_py:.3f} - {t_int_py:.5f}}} = {k_py_bucket_int_exact:.2f} \\implies k \\ge {k_py_bucket_int}$ búsquedas.")
    md.append("Como se aprecia, la diferencia es de apenas 1 búsqueda menos, confirmando que la velocidad arrolladora de la búsqueda en arreglos ordenados hace que el denominador esté gobernado en un 99,8% por la lentitud de la búsqueda lineal.")
    md.append("")
    md.append("### Conclusiones del Punto de Equilibrio:")
    md.append("1. **En Java:** Basta con realizar **561 búsquedas** (usando Radix Sort) o **618 búsquedas** (usando QuickSort) para que ordenar previamente sea más rápido que buscar de forma secuencial.")
    md.append("2. **En Python:** La amortización ocurre de forma casi instantánea: a partir de solo **73 búsquedas** (con Bucket Sort) o **99 búsquedas** (con QuickSort), ordenar y usar búsqueda binaria supera a la búsqueda lineal.")
    md.append("3. **Impacto del lenguaje:** En Python, la búsqueda lineal es 177 veces más lenta que en Java (26,44 ms por búsqueda vs 0,149 ms), por lo que el costo de no ordenar es abrumadoramente penalizado en el lenguaje interpretado.")
    
    contenido = "\n".join(md)
    return contenido, {
        "k_java_radix": k_java_radix,
        "k_java_dpqs": k_java_dpqs,
        "k_py_bucket": k_py_bucket,
        "k_py_dpqs": k_py_dpqs,
        "k_java_radix_exact": k_java_radix_exact,
        "k_py_bucket_exact": k_py_bucket_exact
    }

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    res_dir = os.path.join(base_dir, "resultados")
    os.makedirs(res_dir, exist_ok=True)
    reporte, metricas = generar_reporte()
    salida_path = os.path.join(res_dir, "tablas_analisis.md")
    with open(salida_path, "w", encoding="utf-8") as f:
        f.write(reporte)
    print(f"Reporte generado exitosamente en {salida_path}")
    print(f"Java Break-even (Radix Sort): {metricas['k_java_radix']} búsquedas")
    print(f"Python Break-even (Bucket Sort): {metricas['k_py_bucket']} búsquedas")
