#!/usr/bin/env bash
# Ejecuta el benchmark completo del Punto 2 en Java y en Python.
# Uso:  ./correr_todo.sh [java|python|ambos]
# Los resultados quedan en resultados/resultados_java.csv y resultados/resultados_python.csv
set -e
cd "$(dirname "$0")"
QUE="${1:-ambos}"
ALGS="linear binary ternary jump interpolation exponential"
mkdir -p resultados

if [ "$QUE" = "java" ] || [ "$QUE" = "ambos" ]; then
  echo "Compilando clases Java..."
  (cd java && javac -encoding UTF-8 Busquedas.java Benchmark.java)
  rm -f resultados/resultados_java.csv
  for a in $ALGS; do
    java -Xmx4g -cp java Benchmark "$a" ../punto1/datos datos resultados/resultados_java.csv
  done
fi

if [ "$QUE" = "python" ] || [ "$QUE" = "ambos" ]; then
  rm -f resultados/resultados_python.csv
  for a in $ALGS; do
    python3 -u python/benchmark.py "$a" ../punto1/datos datos resultados/resultados_python.csv
  done
fi

echo "Benchmark del Punto 2 completado con éxito."
