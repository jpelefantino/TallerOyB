# Taller de Ordenamiento y Búsqueda: Punto 2 (Búsqueda)

Comparación experimental de seis algoritmos de búsqueda en **Java** (lenguaje compilado) y **Python** (lenguaje interpretado):
1. **Búsqueda Lineal** (*Linear Search*, referencia)
2. **Búsqueda Binaria** (*Binary Search*)
3. **Búsqueda Ternaria** (*Ternary Search*)
4. **Búsqueda por Saltos** (*Jump Search*)
5. **Búsqueda por Interpolación** (*Interpolation Search*)
6. **Búsqueda Exponencial** (*Exponential Search*)

Todas las implementaciones son equivalentes línea por línea en ambos lenguajes y siguen las referencias de GeeksforGeeks.

---

## Fuentes de los Algoritmos (GeeksforGeeks)

- **Linear Search:** https://www.geeksforgeeks.org/linear-search/
- **Binary Search:** https://www.geeksforgeeks.org/binary-search/
- **Ternary Search:** https://www.geeksforgeeks.org/ternary-search/
- **Jump Search:** https://www.geeksforgeeks.org/jump-search/
- **Interpolation Search:** https://www.geeksforgeeks.org/interpolation-search/
- **Exponential Search:** https://www.geeksforgeeks.org/exponential-search/

---

## Estructura de la Carpeta

```
punto2/
├── README.md                      # Documentación y guía de reproducción
├── generar_claves.py              # Genera las 1.000 claves (500 presentes / 500 ausentes, semilla 2026)
├── datos/                         # claves_<n>.txt para n = 1.000 a 1.000.000
├── java/
│   ├── Busquedas.java             # Los 6 algoritmos de búsqueda en Java
│   ├── Benchmark.java             # Medición (warmup JIT + 5 repeticiones x 1.000 claves)
│   └── TestBusquedas.java         # Tests unitarios de exactitud y límites
├── python/
│   ├── busquedas.py               # Los 6 algoritmos de búsqueda en Python
│   ├── benchmark.py               # Medición en Python (5 repeticiones x 1.000 claves)
│   └── test_busquedas.py          # Tests unitarios de exactitud y límites
├── correr_todo.sh                 # Automatización del benchmark completo en Bash
├── correr_todo.ps1                # Automatización del benchmark completo en PowerShell
├── graficas.py                    # Generador de gráficas (escala logarítmica)
├── analisis.py                    # Generador de tablas estadísticas en Markdown
├── resultados/                    # CSVs con mediciones y tablas de análisis
│   ├── resultados_java.csv
│   ├── resultados_python.csv
│   └── tablas_analisis.md
└── graficas/                      # Gráficas generadas en formato PNG
    ├── 1_crecimiento_java.png
    ├── 1_crecimiento_python.png
    └── 2_java_vs_python_1M.png
```

---

## Cómo Reproducirlo

Requiere Java 17+, Python 3.10+ y `matplotlib` (`pip install matplotlib`).

1. **Generar claves de búsqueda:**
   ```bash
   python generar_claves.py
   ```
2. **Ejecutar tests de exactitud:**
   ```bash
   python python/test_busquedas.py
   javac java/Busquedas.java java/TestBusquedas.java && java -cp java TestBusquedas
   ```
3. **Correr benchmarks:**
   - En Linux / macOS / Git Bash:
     ```bash
     ./correr_todo.sh ambos
     ```
   - En Windows (PowerShell):
     ```powershell
     .\correr_todo.ps1 -que ambos
     ```
4. **Generar gráficas y tablas de análisis:**
   ```bash
   python graficas.py
   python analisis.py > resultados/tablas_analisis.md
   ```

---

## Reglas de Medición

- Los arreglos base provienen de `../punto1/datos/ascendente_<n>.txt` para garantizar la paridad experimental.
- Se leen las estructuras completas a memoria **antes** de iniciar los cronómetros.
- **Experimento 1 (Crecimiento):** Para mitigar el ruido del reloj (dado que una búsqueda individual toma nanosegundos), se miden en bloque las 1.000 claves de búsqueda (500 presentes y 500 ausentes) y se computa el promedio individual: $t_{\text{prom}} = \frac{t_{\text{total}}}{1.000}$.
- **Experimento 2 (Posición de la clave):** Para $n = 1.000.000$, se ejecutan 1.000 búsquedas consecutivas de la clave al inicio (`arr[0]`), centro (`arr[n/2]`) y final (`arr[n-1]`).
- Java realiza 1 ejecución de calentamiento (*warmup*) no promediada para estabilizar el compilador JIT (HotSpot).
- Se reporta el promedio y la desviación estándar muestral de 5 repeticiones independientes.
- Los acumuladores de resultados (*blackholes*) evitan la eliminación de código muerto (*Dead Code Elimination*).

---

## Formato del Archivo CSV

`algoritmo, lenguaje, variante, n, t1_ns, t2_ns, t3_ns, t4_ns, t5_ns, promedio_ns, desv_ns, tipo, estado, nota`
- `variante`: `claves_mixtas`, `pos_inicio`, `pos_centro`, `pos_final`.
- `t1_ns` ... `t5_ns`: tiempo promedio por búsqueda individual en la repetición dada (en nanosegundos).
