import java.io.*;
import java.nio.file.*;
import java.util.*;

public class TestBusquedas {

    public static void main(String[] args) throws Exception {
        testCasosBorde();
        testEquivalenciaDatosReales();
        System.out.println("Todos los tests de Java pasaron satisfactoriamente.");
    }

    private static void testCasosBorde() {
        int[] arr = {10, 20, 30, 40, 50, 60, 70, 80, 90, 100};

        for (int i = 0; i < arr.length; i++) {
            int val = arr[i];
            check(Busquedas.linearSearch(arr, val) >= 0 && arr[Busquedas.linearSearch(arr, val)] == val, "linearSearch presente");
            check(Busquedas.binarySearch(arr, val) >= 0 && arr[Busquedas.binarySearch(arr, val)] == val, "binarySearch presente");
            check(Busquedas.ternarySearch(arr, val) >= 0 && arr[Busquedas.ternarySearch(arr, val)] == val, "ternarySearch presente");
            check(Busquedas.jumpSearch(arr, val) >= 0 && arr[Busquedas.jumpSearch(arr, val)] == val, "jumpSearch presente");
            check(Busquedas.interpolationSearch(arr, val) >= 0 && arr[Busquedas.interpolationSearch(arr, val)] == val, "interpolationSearch presente");
            check(Busquedas.exponentialSearch(arr, val) >= 0 && arr[Busquedas.exponentialSearch(arr, val)] == val, "exponentialSearch presente");
        }

        int[] ausentes = {5, 25, 55, 95, 105};
        for (int val : ausentes) {
            check(Busquedas.linearSearch(arr, val) == -1, "linearSearch ausente");
            check(Busquedas.binarySearch(arr, val) == -1, "binarySearch ausente");
            check(Busquedas.ternarySearch(arr, val) == -1, "ternarySearch ausente");
            check(Busquedas.jumpSearch(arr, val) == -1, "jumpSearch ausente");
            check(Busquedas.interpolationSearch(arr, val) == -1, "interpolationSearch ausente");
            check(Busquedas.exponentialSearch(arr, val) == -1, "exponentialSearch ausente");
        }

        int[] unElem = {42};
        check(Busquedas.linearSearch(unElem, 42) == 0, "linear 1 elem");
        check(Busquedas.binarySearch(unElem, 42) == 0, "binary 1 elem");
        check(Busquedas.ternarySearch(unElem, 42) == 0, "ternary 1 elem");
        check(Busquedas.jumpSearch(unElem, 42) == 0, "jump 1 elem");
        check(Busquedas.interpolationSearch(unElem, 42) == 0, "interp 1 elem");
        check(Busquedas.exponentialSearch(unElem, 42) == 0, "exp 1 elem");

        int[] vacio = {};
        check(Busquedas.linearSearch(vacio, 10) == -1, "linear vacio");
        check(Busquedas.binarySearch(vacio, 10) == -1, "binary vacio");
        check(Busquedas.ternarySearch(vacio, 10) == -1, "ternary vacio");
        check(Busquedas.jumpSearch(vacio, 10) == -1, "jump vacio");
        check(Busquedas.interpolationSearch(vacio, 10) == -1, "interp vacio");
        check(Busquedas.exponentialSearch(vacio, 10) == -1, "exp vacio");

        System.out.println("[OK] Tests de casos borde en Java completados con exito.");
    }

    private static void testEquivalenciaDatosReales() throws IOException {
        Path rutaArr = Paths.get("..", "punto1", "datos", "ascendente_1000.txt");
        if (!Files.exists(rutaArr)) {
            rutaArr = Paths.get("punto1", "datos", "ascendente_1000.txt");
        }
        Path rutaClaves = Paths.get("datos", "claves_1000.txt");
        if (!Files.exists(rutaClaves)) {
            rutaClaves = Paths.get("punto2", "datos", "claves_1000.txt");
        }

        int[] arr = leerArchivo(rutaArr);
        int[] claves = leerArchivo(rutaClaves);

        int presentes = 0;
        int ausentes = 0;

        for (int c : claves) {
            int idxLin = Busquedas.linearSearch(arr, c);
            if (idxLin != -1) {
                check(arr[idxLin] == c, "LinearSearch valor incorrecto");
                presentes++;
            } else {
                ausentes++;
            }

            int idxBin = Busquedas.binarySearch(arr, c);
            int idxTer = Busquedas.ternarySearch(arr, c);
            int idxJmp = Busquedas.jumpSearch(arr, c);
            int idxItp = Busquedas.interpolationSearch(arr, c);
            int idxExp = Busquedas.exponentialSearch(arr, c);

            if (idxLin == -1) {
                check(idxBin == -1, "BinarySearch encontro clave ausente");
                check(idxTer == -1, "TernarySearch encontro clave ausente");
                check(idxJmp == -1, "JumpSearch encontro clave ausente");
                check(idxItp == -1, "InterpolationSearch encontro clave ausente");
                check(idxExp == -1, "ExponentialSearch encontro clave ausente");
            } else {
                check(idxBin != -1 && arr[idxBin] == c, "BinarySearch no encontro clave presente");
                check(idxTer != -1 && arr[idxTer] == c, "TernarySearch no encontro clave presente");
                check(idxJmp != -1 && arr[idxJmp] == c, "JumpSearch no encontro clave presente");
                check(idxItp != -1 && arr[idxItp] == c, "InterpolationSearch no encontro clave presente");
                check(idxExp != -1 && arr[idxExp] == c, "ExponentialSearch no encontro clave presente");
            }
        }

        check(presentes == 500 && ausentes == 500, "Deben ser exactamente 500 presentes y 500 ausentes");
        System.out.println("[OK] 1.000 claves probadas en ascendente_1000.txt: 500 presentes y 500 ausentes verificadas en todos los algoritmos.");
    }

    private static int[] leerArchivo(Path ruta) throws IOException {
        String contenido = Files.readString(ruta);
        String[] tokens = contenido.trim().split("\\s+");
        int[] res = new int[tokens.length];
        for (int i = 0; i < tokens.length; i++) {
            res[i] = Integer.parseInt(tokens[i]);
        }
        return res;
    }

    private static void check(boolean cond, String msg) {
        if (!cond) {
            throw new AssertionError("Fallo en test: " + msg);
        }
    }
}
