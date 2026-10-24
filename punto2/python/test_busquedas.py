"""
Tests de verificación de exactitud de los algoritmos de búsqueda (Python).
Prueba casos borde y comprueba equivalencia con los datos reales del taller.
"""
import os
import sys

from busquedas import ALGORITMOS


def test_casos_borde():
    arr = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    for nombre, alg in ALGORITMOS.items():
        # Elementos presentes
        for idx, val in enumerate(arr):
            res = alg(arr, val)
            assert res != -1 and arr[res] == val, f"{nombre} fallo al buscar {val}"

        # Elementos ausentes
        for val in [5, 25, 55, 95, 105]:
            res = alg(arr, val)
            assert res == -1, f"{nombre} encontro incorrectamente {val} (retorno {res})"

        # Arreglo de un elemento
        assert alg([42], 42) == 0, f"{nombre} fallo con 1 elemento presente"
        assert alg([42], 99) == -1, f"{nombre} fallo con 1 elemento ausente"

        # Arreglo vacio
        assert alg([], 10) == -1, f"{nombre} fallo con arreglo vacio"

    print("[OK] Tests de casos borde completados con exito.")


def test_equivalencia_datos_reales():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    p1_datos = os.path.join(os.path.dirname(base_dir), "..", "punto1", "datos")
    p2_datos = os.path.join(base_dir, "..", "datos")

    ruta_arr = os.path.join(p1_datos, "ascendente_1000.txt")
    ruta_claves = os.path.join(p2_datos, "claves_1000.txt")

    with open(ruta_arr) as f:
        arr = [int(x) for x in f.read().split()]
    with open(ruta_claves) as f:
        claves = [int(x) for x in f.read().split()]

    assert len(claves) == 1000
    presentes = 0
    ausentes = 0

    for c in claves:
        idx_lin = ALGORITMOS["linear"](arr, c)
        if idx_lin != -1:
            assert arr[idx_lin] == c
            presentes += 1
        else:
            ausentes += 1

        for nombre in ["binary", "ternary", "jump", "interpolation", "exponential"]:
            idx = ALGORITMOS[nombre](arr, c)
            if idx_lin == -1:
                assert idx == -1, f"{nombre} encontro una clave que era ausente: {c}"
            else:
                assert idx != -1 and arr[idx] == c, f"{nombre} no encontro una clave presente: {c}"

    assert presentes == 500 and ausentes == 500
    print(f"[OK] 1.000 claves probadas en ascendente_1000.txt: 500 presentes y 500 ausentes verificadas en todos los algoritmos.")


if __name__ == "__main__":
    test_casos_borde()
    test_equivalencia_datos_reales()
    print("Todos los tests de Python pasaron satisfactoriamente.")
