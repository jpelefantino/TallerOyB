#!/usr/bin/env bash
# Ejecuta el benchmark completo del Punto 1 en Java y en Python.
# Uso:  ./correr_todo.sh [java|python|ambos]
# Los resultados quedan en resultados/resultados_java.csv y resultados/resultados_python.csv
set -e
cd "$(dirname "$0")"
QUE="${1:-ambos}"
ALGS="radix bucket merge heap dualpivot insertion"
mkdir -p resultados

if [ "$QUE" = "java" ] || [ "$QUE" = "ambos" ]; then
  (cd java && javac -encoding UTF-8 Ordenamientos.java Benchmark.java)
  for a in $ALGS; do
    java -Xmx4g -cp java Benchmark "$a" datos resultados/resultados_java.csv
  done
fi

if [ "$QUE" = "python" ] || [ "$QUE" = "ambos" ]; then
  for a in $ALGS; do
    python3 -u python/benchmark.py "$a" datos resultados/resultados_python.csv
  done
fi
