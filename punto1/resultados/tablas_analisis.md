
### Tiempos java — entrada aleatorio (ms, promedio ± desviación)

| Algoritmo | n=1,000 | n=10,000 | n=100,000 | n=1,000,000 |
|---|---|---|---|---|
| Insertion Sort | 1.041 ± 0.460 | 6.492 ± 0.140 | 736.382 ± 40.953 | 78,826.821 ± 1,429.596 |
| Dual-Pivot QuickSort | 0.283 ± 0.065 | 0.630 ± 0.061 | 7.763 ± 1.325 | 91.854 ± 7.004 |
| Merge Sort | 0.168 ± 0.036 | 1.507 ± 0.754 | 15.121 ± 1.820 | 192.903 ± 24.911 |
| Heap Sort | 0.220 ± 0.031 | 1.572 ± 0.325 | 14.387 ± 0.691 | 175.949 ± 12.364 |
| Radix Sort | 0.589 ± 0.390 | 1.575 ± 1.058 | 9.761 ± 4.248 | 83.320 ± 9.307 |
| Bucket Sort | 0.533 ± 0.077 | 1.188 ± 0.200 | 20.857 ± 3.821 | 498.618 ± 128.993 |

### Tiempos java — entrada ascendente (ms, promedio ± desviación)

| Algoritmo | n=1,000 | n=10,000 | n=100,000 | n=1,000,000 |
|---|---|---|---|---|
| Insertion Sort | 0.001 ± 0.000 | 0.012 ± 0.001 | 0.114 ± 0.011 | 1.278 ± 0.041 |
| Dual-Pivot QuickSort | 0.227 ± 0.048 | 21.097 ± 1.070 | 2,109.7 (falla*) | 210,969.7 (falla*) |
| Merge Sort | 0.033 ± 0.001 | 0.376 ± 0.030 | 4.593 ± 0.152 | 79.989 ± 10.580 |
| Heap Sort | 0.043 ± 0.004 | 0.593 ± 0.025 | 6.900 ± 0.124 | 95.731 ± 15.974 |
| Radix Sort | 0.086 ± 0.021 | 0.883 ± 0.401 | 8.187 ± 0.828 | 102.692 ± 54.074 |
| Bucket Sort | 0.035 ± 0.008 | 19.998 ± 43.628 | 6.276 ± 1.742 | 183.904 ± 57.748 |

### Tiempos java — entrada descendente (ms, promedio ± desviación)

| Algoritmo | n=1,000 | n=10,000 | n=100,000 | n=1,000,000 |
|---|---|---|---|---|
| Insertion Sort | 0.154 ± 0.022 | 14.513 ± 3.488 | 1,757.637 ± 179.625 | 162,234.264 ± 4,380.450 |
| Dual-Pivot QuickSort | 0.302 ± 0.053 | 23.528 ± 0.487 | 2,352.8 (falla*) | 235,275.8 (falla*) |
| Merge Sort | 0.054 ± 0.002 | 0.791 ± 0.178 | 9.527 ± 4.476 | 75.844 ± 16.757 |
| Heap Sort | 0.068 ± 0.022 | 0.883 ± 0.073 | 7.564 ± 0.202 | 101.989 ± 13.837 |
| Radix Sort | 0.059 ± 0.001 | 0.615 ± 0.026 | 6.288 ± 0.418 | 82.589 ± 44.828 |
| Bucket Sort | 0.035 ± 0.005 | 0.515 ± 0.031 | 5.899 ± 0.068 | 158.249 ± 103.866 |

### Tiempos python — entrada aleatorio (ms, promedio ± desviación)

| Algoritmo | n=1,000 | n=10,000 | n=100,000 | n=1,000,000 |
|---|---|---|---|---|
| Insertion Sort | 23.602 ± 2.611 | 2,472.828 ± 130.262 | 305,753.562 ± 6,516.639 | 30,575,356.2 (est.) |
| Dual-Pivot QuickSort | 0.818 ± 0.041 | 11.870 ± 0.346 | 180.420 ± 15.617 | 2,600.673 ± 80.337 |
| Merge Sort | 2.013 ± 0.116 | 24.713 ± 0.203 | 430.072 ± 34.456 | 6,090.020 ± 305.685 |
| Heap Sort | 1.953 ± 0.052 | 29.484 ± 1.885 | 592.680 ± 52.975 | 8,585.681 ± 503.718 |
| Radix Sort | 2.748 ± 1.929 | 22.683 ± 1.885 | 348.411 ± 42.410 | 5,951.966 ± 117.606 |
| Bucket Sort | 0.595 ± 0.108 | 6.418 ± 0.726 | 132.582 ± 2.045 | 1,915.109 ± 95.585 |

### Tiempos python — entrada ascendente (ms, promedio ± desviación)

| Algoritmo | n=1,000 | n=10,000 | n=100,000 | n=1,000,000 |
|---|---|---|---|---|
| Insertion Sort | 0.096 ± 0.015 | 0.959 ± 0.029 | 10.941 ± 0.216 | 97.845 ± 1.170 |
| Dual-Pivot QuickSort | 19.881 ± 0.337 | 1,988.1 (falla*) | 198,807.4 (falla*) | 19,880,741.6 (falla*) |
| Merge Sort | 1.678 ± 0.022 | 29.570 ± 7.394 | 309.698 ± 32.619 | 3,643.975 ± 216.327 |
| Heap Sort | 2.133 ± 0.062 | 30.160 ± 0.502 | 445.466 ± 35.965 | 5,052.790 ± 196.997 |
| Radix Sort | 1.834 ± 0.055 | 20.363 ± 0.748 | 383.858 ± 30.207 | 4,702.491 ± 205.529 |
| Bucket Sort | 0.967 ± 0.061 | 10.380 ± 0.280 | 100.234 ± 27.402 | 982.551 ± 67.396 |

### Tiempos python — entrada descendente (ms, promedio ± desviación)

| Algoritmo | n=1,000 | n=10,000 | n=100,000 | n=1,000,000 |
|---|---|---|---|---|
| Insertion Sort | 39.367 ± 0.124 | 4,687.469 ± 143.210 | 468,746.9 (est.) | 46,874,692.5 (est.) |
| Dual-Pivot QuickSort | 25.434 ± 1.866 | 2,543.4 (falla*) | 254,340.6 (falla*) | 25,434,063.8 (falla*) |
| Merge Sort | 1.722 ± 0.068 | 31.721 ± 7.620 | 327.519 ± 39.042 | 3,521.300 ± 180.503 |
| Heap Sort | 1.855 ± 0.040 | 27.357 ± 1.088 | 375.622 ± 12.229 | 4,988.310 ± 211.841 |
| Radix Sort | 1.853 ± 0.048 | 20.134 ± 0.740 | 335.483 ± 52.121 | 4,584.217 ± 93.505 |
| Bucket Sort | 0.564 ± 0.051 | 5.887 ± 0.217 | 66.750 ± 4.489 | 1,027.884 ± 43.827 |

### Factor de crecimiento t(10n)/t(n) — java, entrada aleatoria

| Algoritmo | Teoría | 1k→10k (obs/teo) | 10k→100k (obs/teo) | 100k→1M (obs/teo) |
|---|---|---|---|---|
| Insertion Sort | O(n²) | 6.2× / 100.0× | 113.4× / 100.0× | 107.0× / 100.0× |
| Dual-Pivot QuickSort | O(n log n) | 2.2× / 13.3× | 12.3× / 12.5× | 11.8× / 12.0× |
| Merge Sort | O(n log n) | 9.0× / 13.3× | 10.0× / 12.5× | 12.8× / 12.0× |
| Heap Sort | O(n log n) | 7.1× / 13.3× | 9.2× / 12.5× | 12.2× / 12.0× |
| Radix Sort | O(n) | 2.7× / 10.0× | 6.2× / 10.0× | 8.5× / 10.0× |
| Bucket Sort | O(n) | 2.2× / 10.0× | 17.6× / 10.0× | 23.9× / 10.0× |

### Factor de crecimiento t(10n)/t(n) — python, entrada aleatoria

| Algoritmo | Teoría | 1k→10k (obs/teo) | 10k→100k (obs/teo) | 100k→1M (obs/teo) |
|---|---|---|---|---|
| Insertion Sort | O(n²) | 104.8× / 100.0× | 123.6× / 100.0× | 100.0× / 100.0× (est.) |
| Dual-Pivot QuickSort | O(n log n) | 14.5× / 13.3× | 15.2× / 12.5× | 14.4× / 12.0× |
| Merge Sort | O(n log n) | 12.3× / 13.3× | 17.4× / 12.5× | 14.2× / 12.0× |
| Heap Sort | O(n log n) | 15.1× / 13.3× | 20.1× / 12.5× | 14.5× / 12.0× |
| Radix Sort | O(n) | 8.3× / 10.0× | 15.4× / 10.0× | 17.1× / 10.0× |
| Bucket Sort | O(n) | 10.8× / 10.0× | 20.7× / 10.0× | 14.4× / 10.0× |

### Efecto del orden (Java): tiempo con entrada ordenada ÷ tiempo aleatoria

| Algoritmo | n | ascendente/aleatorio | descendente/aleatorio |
|---|---|---|---|
| Insertion Sort | 1,000 | 0.00× | 0.15× |
| Insertion Sort | 10,000 | 0.00× | 2.24× |
| Insertion Sort | 100,000 | 0.00× | 2.39× |
| Dual-Pivot QuickSort | 1,000 | 0.80× | 1.07× |
| Dual-Pivot QuickSort | 10,000 | 33.48× | 37.34× |
| Dual-Pivot QuickSort | 100,000 | 271.78× (est.) | 303.09× (est.) |
| Merge Sort | 1,000 | 0.20× | 0.32× |
| Merge Sort | 10,000 | 0.25× | 0.52× |
| Merge Sort | 100,000 | 0.30× | 0.63× |
| Heap Sort | 1,000 | 0.20× | 0.31× |
| Heap Sort | 10,000 | 0.38× | 0.56× |
| Heap Sort | 100,000 | 0.48× | 0.53× |
| Radix Sort | 1,000 | 0.15× | 0.10× |
| Radix Sort | 10,000 | 0.56× | 0.39× |
| Radix Sort | 100,000 | 0.84× | 0.64× |
| Bucket Sort | 1,000 | 0.07× | 0.07× |
| Bucket Sort | 10,000 | 16.84× | 0.43× |
| Bucket Sort | 100,000 | 0.30× | 0.28× |

### Python ÷ Java, n = 1.000.000, entrada aleatoria

| Algoritmo | Java (ms) | Python (ms) | Python/Java |
|---|---|---|---|
| Insertion Sort | 78,826.8 | 30,575,356.2 | 388× (est.) |
| Dual-Pivot QuickSort | 91.9 | 2,600.7 | 28× |
| Merge Sort | 192.9 | 6,090.0 | 32× |
| Heap Sort | 175.9 | 8,585.7 | 49× |
| Radix Sort | 83.3 | 5,952.0 | 71× |
| Bucket Sort | 498.6 | 1,915.1 | 4× |
