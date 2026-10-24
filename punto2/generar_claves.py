"""
Generador de claves de prueba - Taller de Ordenamiento y Búsqueda (Punto 2).

Genera los conjuntos de 1.000 claves de búsqueda (500 presentes y 500 ausentes)
para cada tamaño n a partir de los arreglos ordenados del Punto 1 (datos/ascendente_<n>.txt).

Archivos generados en datos/:
    claves_1000.txt
    claves_10000.txt
    claves_100000.txt
    claves_1000000.txt

Semilla fija (SEMILLA = 2026) para total reproducibilidad.
Uso: python generar_claves.py
"""
import os
import random

SEMILLA = 2026
TAMANIOS = [1_000, 10_000, 100_000, 1_000_000]
MINIMO, MAXIMO = 10_000_000, 99_999_999
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_DATOS_P1 = os.path.join(os.path.dirname(BASE_DIR), "punto1", "datos")
CARPETA_DATOS = os.path.join(BASE_DIR, "datos")


def leer_arreglo(n):
    ruta = os.path.join(RUTA_DATOS_P1, f"ascendente_{n}.txt")
    with open(ruta) as f:
        return [int(x) for x in f.read().split()]


def guardar_claves(nombre, claves):
    with open(os.path.join(CARPETA_DATOS, nombre), "w") as f:
        f.write("\n".join(map(str, claves)))
        f.write("\n")


def main():
    os.makedirs(CARPETA_DATOS, exist_ok=True)
    rng = random.Random(SEMILLA)

    for n in TAMANIOS:
        arr = leer_arreglo(n)
        conjunto_arr = set(arr)

        # 500 claves presentes (muestreadas del conjunto de valores únicos)
        presentes = rng.sample(list(conjunto_arr), 500)

        # 500 claves ausentes garantizadas que no estén en el arreglo
        ausentes = set()
        while len(ausentes) < 500:
            candidato = rng.randint(MINIMO, MAXIMO)
            if candidato not in conjunto_arr and candidato not in ausentes:
                ausentes.add(candidato)

        claves = presentes + list(ausentes)
        rng.shuffle(claves)  # Mezclar aleatoriamente

        guardar_claves(f"claves_{n}.txt", claves)
        print(f"n={n:,}: 1.000 claves generadas (500 presentes, 500 ausentes) -> claves_{n}.txt")


if __name__ == "__main__":
    main()
