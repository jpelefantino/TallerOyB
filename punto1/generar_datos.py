"""
Generador de datos de prueba - Taller de Ordenamiento y Búsqueda (Punto 1).

Genera UNA sola vez los arreglos de prueba y los guarda en archivos de texto
plano (un número por línea) dentro de la carpeta datos/:

    aleatorio_<n>.txt    números enteros aleatorios de 8 dígitos
    ascendente_<n>.txt   los mismos números ordenados de menor a mayor
    descendente_<n>.txt  los mismos números ordenados de mayor a menor

Tamaños: 1.000, 10.000, 100.000 y 1.000.000.
Rango:   10.000.000 a 99.999.999 (8 dígitos).
Semilla fija (SEMILLA) para que cualquiera pueda reproducir exactamente los datos.

Uso:  python3 generar_datos.py
"""
import os
import random

SEMILLA = 2026
TAMANIOS = [1_000, 10_000, 100_000, 1_000_000]
MINIMO, MAXIMO = 10_000_000, 99_999_999
CARPETA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos")


def guardar(nombre, datos):
    with open(os.path.join(CARPETA, nombre), "w") as f:
        f.write("\n".join(map(str, datos)))
        f.write("\n")


def main():
    os.makedirs(CARPETA, exist_ok=True)
    rng = random.Random(SEMILLA)
    for n in TAMANIOS:
        aleatorio = [rng.randint(MINIMO, MAXIMO) for _ in range(n)]
        guardar(f"aleatorio_{n}.txt", aleatorio)
        guardar(f"ascendente_{n}.txt", sorted(aleatorio))
        guardar(f"descendente_{n}.txt", sorted(aleatorio, reverse=True))
        print(f"n={n}: listo (repetidos: {n - len(set(aleatorio))})")


if __name__ == "__main__":
    main()
