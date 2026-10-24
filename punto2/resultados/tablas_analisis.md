# Resultados y Tablas de Análisis: Punto 2 (Algoritmos de Búsqueda)

### Tiempos de búsqueda promedio — Java (compilado) (claves mixtas: 500 presentes / 500 ausentes)

| Algoritmo | n=1,000 | n=10,000 | n=100,000 | n=1,000,000 |
|---|---|---|---|---|
| Búsqueda Lineal | 2.31 ± 0.87 µs | 1.62 ± 0.17 µs | 14.10 ± 0.65 µs | 149.00 ± 8.74 µs |
| Búsqueda Binaria | 166.3 ± 12.5 ns | 121.3 ± 8.4 ns | 157.0 ± 7.1 ns | 274.3 ± 71.5 ns |
| Búsqueda Ternaria | 128.2 ± 15.9 ns | 94.7 ± 7.2 ns | 150.0 ± 20.3 ns | 150.6 ± 23.0 ns |
| Búsqueda por Saltos | 620.2 ± 131.7 ns | 1.40 ± 0.37 µs | 424.3 ± 92.1 ns | 1.35 ± 0.42 µs |
| Búsqueda por Interpolación | 82.1 ± 60.5 ns | 23.5 ± 7.2 ns | 25.3 ± 8.9 ns | 33.8 ± 8.9 ns |
| Búsqueda Exponencial | 219.3 ± 76.5 ns | 95.2 ± 7.9 ns | 99.8 ± 5.8 ns | 219.4 ± 54.0 ns |

### Tiempos de búsqueda promedio — Python (interpretado) (claves mixtas: 500 presentes / 500 ausentes)

| Algoritmo | n=1,000 | n=10,000 | n=100,000 | n=1,000,000 |
|---|---|---|---|---|
| Búsqueda Lineal | 20.97 ± 0.48 µs | 194.65 ± 3.51 µs | 2.471 ± 0.280 ms | 26.440 ± 1.079 ms |
| Búsqueda Binaria | 1.12 ± 0.25 µs | 1.73 ± 0.36 µs | 2.03 ± 0.29 µs | 5.64 ± 0.49 µs |
| Búsqueda Ternaria | 980.5 ± 59.0 ns | 1.58 ± 0.37 µs | 2.36 ± 0.59 µs | 4.23 ± 0.59 µs |
| Búsqueda por Saltos | 8.32 ± 1.51 µs | 22.12 ± 3.27 µs | 67.57 ± 6.31 µs | 232.51 ± 28.89 µs |
| Búsqueda por Interpolación | 932.6 ± 19.4 ns | 1.14 ± 0.19 µs | 1.41 ± 0.20 µs | 2.24 ± 1.01 µs |
| Búsqueda Exponencial | 1.30 ± 0.13 µs | 2.56 ± 0.75 µs | 3.05 ± 0.97 µs | 5.01 ± 0.99 µs |

### Efecto de la posición de la clave (n = 1.000.000) — Java (compilado)

| Algoritmo | Inicio (`arr[0]`) | Centro (`arr[n/2]`) | Final (`arr[n-1]`) |
|---|---|---|---|
| Búsqueda Lineal | 29.4 ± 0.1 ns | 96.18 ± 4.69 µs | 201.86 ± 20.85 µs |
| Búsqueda Binaria | 31.2 ± 1.7 ns | 28.1 ± 1.7 ns | 78.0 ± 49.2 ns |
| Búsqueda Ternaria | 94.8 ± 76.4 ns | 93.3 ± 42.7 ns | 157.7 ± 84.4 ns |
| Búsqueda por Saltos | 9.1 ± 0.4 ns | 525.5 ± 201.3 ns | 1.44 ± 0.17 µs |
| Búsqueda por Interpolación | 5.8 ± 0.6 ns | 16.8 ± 1.1 ns | 5.6 ± 4.0 ns |
| Búsqueda Exponencial | 4.9 ± 0.0 ns | 36.9 ± 0.0 ns | 110.9 ± 52.1 ns |

### Efecto de la posición de la clave (n = 1.000.000) — Python (interpretado)

| Algoritmo | Inicio (`arr[0]`) | Centro (`arr[n/2]`) | Final (`arr[n-1]`) |
|---|---|---|---|
| Búsqueda Lineal | 245.8 ± 99.3 ns | 17.723 ± 0.441 ms | 34.115 ± 1.043 ms |
| Búsqueda Binaria | 1.76 ± 0.16 µs | 2.42 ± 0.73 µs | 1.79 ± 0.03 µs |
| Búsqueda Ternaria | 3.13 ± 0.87 µs | 2.70 ± 0.66 µs | 2.55 ± 0.38 µs |
| Búsqueda por Saltos | 343.4 ± 7.3 ns | 125.01 ± 4.76 µs | 409.89 ± 45.27 µs |
| Búsqueda por Interpolación | 705.8 ± 314.9 ns | 1.80 ± 0.31 µs | 623.0 ± 67.9 ns |
| Búsqueda Exponencial | 79.1 ± 3.1 ns | 2.30 ± 0.14 µs | 3.47 ± 0.54 µs |

### Comparación Compilado (Java) vs Interpretado (Python) en n = 1.000.000

| Algoritmo | Java (promedio) | Python (promedio) | Razón (Python / Java) |
|---|---|---|---|
| Búsqueda Lineal | 149.00 µs | 26.440 ms | 177.4x |
| Búsqueda Binaria | 274.3 ns | 5.64 µs | 20.5x |
| Búsqueda Ternaria | 150.6 ns | 4.23 µs | 28.1x |
| Búsqueda por Saltos | 1.35 µs | 232.51 µs | 171.6x |
| Búsqueda por Interpolación | 33.8 ns | 2.24 µs | 66.3x |
| Búsqueda Exponencial | 219.4 ns | 5.01 µs | 22.8x |
