import java.nio.file.*;
import java.util.*;

/**
 * Demo corta del Punto 1 para la sustentación (tarda unos segundos).
 *
 *  1. Ordena los datos aleatorios de 1.000, 10.000 y 100.000 elementos con los
 *     6 algoritmos, verifica que quedaron ordenados y muestra el tiempo.
 *  2. Muestra el efecto del orden de entrada con 10.000 elementos.
 *  3. Reproduce el fallo del Dual-Pivot QuickSort con 100.000 elementos ordenados.
 *
 * Uso (desde la carpeta punto1):
 *     javac -d java java/Ordenamientos.java java/Demo.java
 *     java -cp java Demo
 */
public class Demo {

    static final String[] NOMBRES = {"Insertion", "Dual-Pivot", "Merge", "Heap", "Radix", "Bucket"};

    static void ordenar(int alg, int[] a) {
        switch (alg) {
            case 0: Ordenamientos.insertionSort(a); break;
            case 1: Ordenamientos.dualPivotQuickSort(a); break;
            case 2: Ordenamientos.mergeSort(a); break;
            case 3: Ordenamientos.heapSort(a); break;
            case 4: Ordenamientos.radixSort(a); break;
            default: Ordenamientos.bucketSort(a);
        }
    }

    static int[] leer(String var, int n) throws Exception {
        List<String> l = Files.readAllLines(Paths.get("datos", var + "_" + n + ".txt"));
        int[] a = new int[l.size()];
        for (int i = 0; i < a.length; i++) a[i] = Integer.parseInt(l.get(i).trim());
        return a;
    }

    static boolean ordenado(int[] a) {
        for (int i = 1; i < a.length; i++) if (a[i - 1] > a[i]) return false;
        return true;
    }

    /** Ordena una copia y devuelve el tiempo en ms (negativo si no quedó ordenado). */
    static double medir(int alg, int[] original) {
        int[] copia = Arrays.copyOf(original, original.length);
        long t0 = System.nanoTime();
        ordenar(alg, copia);
        double ms = (System.nanoTime() - t0) / 1e6;
        return ordenado(copia) ? ms : -1;
    }

    static String fmt(double ms) {
        return ms < 0 ? "  ERROR" : String.format(Locale.US, "%10.3f", ms);
    }

    public static void main(String[] args) throws Exception {
        int[] tam = {1_000, 10_000, 100_000};

        // Calentamiento del JIT (no se muestra)
        int[] w = leer("aleatorio", 10_000);
        for (int alg = 0; alg < 6; alg++) medir(alg, w);

        System.out.println("\n1) ENTRADA ALEATORIA (tiempo en ms, verificado)");
        System.out.printf("%-12s", "Algoritmo");
        for (int n : tam) System.out.printf("%12s", "n=" + n);
        System.out.println();
        int[][] datos = new int[tam.length][];
        for (int i = 0; i < tam.length; i++) datos[i] = leer("aleatorio", tam[i]);
        for (int alg = 0; alg < 6; alg++) {
            System.out.printf("%-12s", NOMBRES[alg]);
            for (int[] d : datos) System.out.printf("%12s", fmt(medir(alg, d)));
            System.out.println();
        }

        System.out.println("\n2) EFECTO DEL ORDEN DE ENTRADA, n = 10.000 (ms)");
        System.out.printf("%-12s%12s%12s%12s%n", "Algoritmo", "aleatoria", "ascendente", "descendente");
        String[] vars = {"aleatorio", "ascendente", "descendente"};
        int[][] porVar = new int[3][];
        for (int v = 0; v < 3; v++) porVar[v] = leer(vars[v], 10_000);
        for (int alg = 0; alg < 6; alg++) {
            System.out.printf("%-12s", NOMBRES[alg]);
            for (int[] d : porVar) System.out.printf("%12s", fmt(medir(alg, d)));
            System.out.println();
        }

        System.out.println("\n3) DUAL-PIVOT QUICKSORT CON 100.000 ELEMENTOS ASCENDENTES");
        int[] asc = leer("ascendente", 100_000);
        try {
            Ordenamientos.dualPivotQuickSort(asc);
            System.out.println("Termino sin error.");
        } catch (StackOverflowError e) {
            System.out.println("StackOverflowError: la recursion llego a unos n/2 = 50.000 niveles");
            System.out.println("porque los pivotes (primer y ultimo elemento) son el minimo y el maximo.");
        }
    }
}
