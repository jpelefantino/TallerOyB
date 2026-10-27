# Taller de Ordenamiento y Búsqueda: Punto 1 (Ordenamiento)

Comparación experimental de seis algoritmos de ordenamiento en **Java** (compilado) y
**Python** (interpretado): Insertion Sort, Dual-Pivot QuickSort (pivotes en el primer y
el último elemento), Merge Sort, Heap Sort, Radix Sort y Bucket Sort.
Las implementaciones son las mismas en los dos lenguajes y siguen GeeksforGeeks
(los enlaces están en la cabecera de cada archivo).

## Estructura

```
generar_datos.py          Genera los datos de prueba (semilla fija 2026)
datos/                    aleatorio_, ascendente_ y descendente_<n>.txt para n = 1e3 a 1e6
java/Ordenamientos.java   Los 6 algoritmos en Java
java/Benchmark.java       Medición en Java (calentamiento + 5 repeticiones)
java/ValidacionPila.java  Experimento complementario: Dual-Pivot con pila de 2 GB
python/ordenamientos.py   Los 6 algoritmos en Python
python/benchmark.py       Medición en Python (5 repeticiones)
python/validacion_recursion.py  Experimento complementario: límite de recursión mayor
correr_todo.sh            Ejecuta todo el benchmark (java | python | ambos)
validar_estimaciones.sh   Ejecuta el experimento complementario
graficas.py               Genera las 6 gráficas en graficas/
analisis.py               Genera resultados/tablas_analisis.md
resultados/               CSV de Java y Python, validación de estimaciones y logs
graficas/                 Las 6 gráficas del Punto 1 (PNG)
```

## Demo rápida (para la sustentación)

Tarda unos segundos en cada lenguaje. Ordena con los 6 algoritmos, verifica el resultado,
muestra el efecto del orden de entrada y reproduce el fallo del Dual-Pivot QuickSort.
Se ejecuta desde la carpeta `punto1`:

```bash
# Java
javac -encoding UTF-8 -d java java/Ordenamientos.java java/Demo.java
java -cp java Demo

# Python
python python/demo.py
```

## Cómo reproducirlo

Requiere Java 17 o superior, Python 3.10 o superior y matplotlib (`pip install matplotlib`).

```bash
python3 generar_datos.py        # solo si se borró la carpeta datos/
./correr_todo.sh java           # unos 30 minutos
./correr_todo.sh python         # unas 2 horas (Insertion Sort domina)
python3 graficas.py
python3 analisis.py > resultados/tablas_analisis.md
```

## Reglas de medición

- Los datos se leen antes de iniciar el cronómetro; no se mide lectura ni escritura.
- Cada repetición ordena una copia nueva del arreglo; la copia no se mide.
- Java hace 1 ejecución de calentamiento que no se promedia; luego 5 repeticiones.
- Después de cada repetición se verifica, fuera del tiempo medido, que el arreglo quedó
  igual al archivo ascendente.
- Si la predicción (tamaño anterior × crecimiento teórico) supera 5 minutos, no se ejecuta
  y se registra como `estimado`. Si el algoritmo falla, se registra el error y se estima.

## Columnas de los CSV

`algoritmo, lenguaje, variante, n, t1_ms … t5_ms, promedio_ms, desv_ms, tipo, estado, nota`

- `tipo`: `medido` o `estimado`.
- `estado`: `ok`, `supera_5min`, `fallo_StackOverflowError` o `fallo_RecursionError`.
- `desv_ms`: desviación estándar muestral de las 5 repeticiones.

## Entorno de las mediciones publicadas

Linux x86-64, 2 núcleos, 7 GB de RAM, OpenJDK 21.0.12 (`-Xmx4g`) y CPython 3.13.16.
