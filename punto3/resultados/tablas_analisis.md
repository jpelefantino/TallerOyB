# Resultados y Tablas de Análisis: Punto 3 (Análisis Comparativo)

Este documento reúne y cruza cuantitativamente las mediciones obtenidas en el **Punto 1** (Ordenamiento) y el **Punto 2** (Búsqueda) para responder a las preguntas de análisis comparativo del taller.

---

## 1. Comparación entre Algoritmos Comparativos y No Comparativos (n = 1.000.000)

A continuación se comparan los tiempos de ejecución medidos en el Punto 1 para ordenar 1.000.000 de enteros de 8 dígitos con entrada aleatoria.

### Tabla 1. Tiempos de ordenamiento en Java y Python (n = 1.000.000, aleatorio)

| Algoritmo | Tipo | Complejidad Teórica | Java (ms) | Python (ms) | Python / Java |
|---|---|---|---|---|---|
| Radix Sort | No comparativo | O(d · (n + b)) ~ O(n) | 83.320 ± 9.307 | 5,951.966 ± 117.606 | 71.4× |
| Bucket Sort | No comparativo | O(n) prom / O(n²) peor | 498.618 ± 128.993 | 1,915.109 ± 95.585 | 3.8× |
| Dual-Pivot QuickSort | Comparativo | O(n log n) / O(n²) peor | 91.854 ± 7.004 | 2,600.673 ± 80.337 | 28.3× |
| Heap Sort | Comparativo | O(n log n) | 175.949 ± 12.364 | 8,585.681 ± 503.718 | 48.8× |
| Merge Sort | Comparativo | O(n log n) | 192.903 ± 24.911 | 6,090.020 ± 305.685 | 31.6× |
| Insertion Sort | Comparativo | O(n²) | 78,826.821 ± 1429.596 | 30,575,356.2 (est.) | 388× |

### Observaciones clave:
1. **Java:** El algoritmo no comparativo **Radix Sort** obtuvo el mejor tiempo absoluto (**83,320 ms**), superando al mejor comparativo (**Dual-Pivot QuickSort** con 91,854 ms), a Heap Sort (175,949 ms) y a Merge Sort (192,903 ms).
2. **Python:** El algoritmo no comparativo **Bucket Sort** fue el más veloz (**1.915,109 ms**), aventajando a Dual-Pivot QuickSort (2.600,673 ms) y a Radix Sort (5.951,966 ms).
3. **Escape de la cota Ω(n log n):** Tanto Radix Sort como Bucket Sort superaron o igualaron el desempeño de los mejores algoritmos comparativos porque no están sujetos a la cota inferior de información basada en comparaciones de árbol de decisión.

---

## 2. ¿Ordenar o No Ordenar? (Cálculo del Punto de Equilibrio k*)

Supóngase un arreglo desordenado de $n = 1.000.000$ elementos sobre el cual se realizarán $k$ búsquedas.

### Formulación matemática:
- **Estrategia A (Sin ordenar):** Se realizan $k$ búsquedas lineales directas sobre el arreglo desordenado.
  $$T_A(k) = k \cdot t_{\text{lineal}}$$
- **Estrategia B (Ordenar primero y buscar con Búsqueda Binaria):** Se invierte un costo inicial de ordenamiento $T_{\text{ordenar}}$ una sola vez, y luego cada una de las $k$ búsquedas se efectúa en tiempo logarítmico con Búsqueda Binaria.
  $$T_B(k) = T_{\text{ordenar}} + k \cdot t_{\text{binaria}}$$
- **Condición de conveniencia (Break-even):**
  $$T_B(k) < T_A(k) \iff T_{\text{ordenar}} + k \cdot t_{\text{binaria}} < k \cdot t_{\text{lineal}}$$
  $$k \cdot (t_{\text{lineal}} - t_{\text{binaria}}) > T_{\text{ordenar}}$$
  $$k > \frac{T_{\text{ordenar}}}{t_{\text{lineal}} - t_{\text{binaria}}}$$

### Tabla 2. Tiempos base para n = 1.000.000 empleados en el cálculo

| Lenguaje | Algoritmo de Ordenamiento | $T_{\text{ordenar}}$ | $t_{\text{lineal}}$ (por búsqueda) | $t_{\text{binaria}}$ (por búsqueda) | $\Delta t = t_{\text{lineal}} - t_{\text{binaria}}$ |
|---|---|---|---|---|---|
| **Java** | **Radix Sort** (Mejor absoluto) | 83.320 ms | 149.00 µs (0.14900 ms) | 274.3 ns (0.0002743 ms) | 0.14873 ms |
| **Java** | **Dual-Pivot QS** (Mejor comparativo) | 91.854 ms | 149.00 µs (0.14900 ms) | 274.3 ns (0.0002743 ms) | 0.14873 ms |
| **Python** | **Bucket Sort** (Mejor absoluto) | 1,915.109 ms | 26.440 ms | 5.64 µs (0.00564 ms) | 26.43436 ms |
| **Python** | **Dual-Pivot QS** (Mejor comparativo) | 2,600.673 ms | 26.440 ms | 5.64 µs (0.00564 ms) | 26.43436 ms |

### Tabla 3. Punto de equilibrio $k^*$ resultante

| Lenguaje | Algoritmo de Ordenamiento Utilizado | $k^*$ Exacto | $k$ Mínimo Entero ($k \ge$) | Fracción de $n$ ($k^* / 10^6$) |
|---|---|---|---|---|
| **Java** | **Radix Sort** (Mejor absoluto) | 560.23 | **561** búsquedas | 0,056% de los datos |
| **Java** | **Dual-Pivot QuickSort** (Mejor comparativo) | 617.61 | **618** búsquedas | 0,062% de los datos |
| **Python** | **Bucket Sort** (Mejor absoluto) | 72.45 | **73** búsquedas | 0,007% de los datos |
| **Python** | **Dual-Pivot QuickSort** (Mejor comparativo) | 98.38 | **99** búsquedas | 0,010% de los datos |

### Variante complementaria: ¿Y si usamos Búsqueda por Interpolación?
Dado que en el Punto 2 la Búsqueda por Interpolación fue el algoritmo más rápido de todos (33,8 ns en Java y 2,24 µs en Python):
- **Java (Radix Sort + Interpolación):** $k^* = \frac{83.320}{0.14900 - 0.0000338} = 559.32 \implies k \ge 560$ búsquedas.
- **Python (Bucket Sort + Interpolación):** $k^* = \frac{1,915.109}{26.440 - 0.00224} = 72.44 \implies k \ge 73$ búsquedas.
Como se aprecia, la diferencia es de apenas 1 búsqueda menos, confirmando que la velocidad arrolladora de la búsqueda en arreglos ordenados hace que el denominador esté gobernado en un 99,8% por la lentitud de la búsqueda lineal.

### Conclusiones del Punto de Equilibrio:
1. **En Java:** Basta con realizar **561 búsquedas** (usando Radix Sort) o **618 búsquedas** (usando QuickSort) para que ordenar previamente sea más rápido que buscar de forma secuencial.
2. **En Python:** La amortización ocurre de forma casi instantánea: a partir de solo **73 búsquedas** (con Bucket Sort) o **99 búsquedas** (con QuickSort), ordenar y usar búsqueda binaria supera a la búsqueda lineal.
3. **Impacto del lenguaje:** En Python, la búsqueda lineal es 177 veces más lenta que en Java (26,44 ms por búsqueda vs 0,149 ms), por lo que el costo de no ordenar es abrumadoramente penalizado en el lenguaje interpretado.