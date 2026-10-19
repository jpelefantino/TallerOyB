#!/usr/bin/env bash
# Experimento complementario: ejecuta UNA vez los casos del Dual-Pivot QuickSort que
# fallaron en el benchmark, pero con una pila más grande, para comparar con la estimación.
cd "$(dirname "$0")"
OUT=resultados/validacion_estimaciones.csv
echo "algoritmo,lenguaje,variante,n,tiempo_real_ms" > $OUT
for n in 100000 1000000; do for v in ascendente descendente; do
  java -Xmx4g -cp java ValidacionPila datos $n $v 2>&1 | grep -v JAVA_TOOL >> $OUT
done; done
for n in 10000 100000; do for v in ascendente descendente; do
  python3 python/validacion_recursion.py datos $n $v >> $OUT 2>&1
done; done
echo FIN_VALIDACION >> $OUT
