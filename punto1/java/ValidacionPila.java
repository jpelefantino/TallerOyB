import java.nio.file.*;
import java.util.*;

/**
 * Experimento complementario (no forma parte del benchmark oficial).
 *
 * El Dual-Pivot QuickSort con entrada ascendente o descendente falla con la pila
 * por defecto de Java (StackOverflowError) a partir de n = 100.000, porque la
 * recursión llega a unos n/2 niveles. Aquí se ejecuta el mismo algoritmo en un
 * hilo con una pila de 2 GB, solo para comprobar qué tan buena fue la
 * estimación O(n^2) registrada en el benchmark. Una sola ejecución por caso.
 *
 * Uso: java -Xmx4g ValidacionPila <carpetaDatos> <n> <variante>
 */
public class ValidacionPila {
    public static void main(String[] args) throws Exception {
        Path datos = Paths.get(args[0]);
        int n = Integer.parseInt(args[1]);
        String var = args[2];
        int[] original = leer(datos.resolve(var + "_" + n + ".txt"));
        int[] ref = leer(datos.resolve("ascendente_" + n + ".txt"));
        double[] ms = new double[1];
        Thread t = new Thread(null, () -> {
            int[] c = Arrays.copyOf(original, original.length);
            long t0 = System.nanoTime();
            Ordenamientos.dualPivotQuickSort(c);
            ms[0] = (System.nanoTime() - t0) / 1e6;
            if (!Arrays.equals(c, ref)) throw new IllegalStateException("No quedó ordenado");
        }, "pila-grande", 2L * 1024 * 1024 * 1024);
        t.start();
        t.join();
        System.out.printf(Locale.US, "dualpivot,java,%s,%d,%.4f%n", var, n, ms[0]);
    }

    static int[] leer(Path p) throws Exception {
        List<String> l = Files.readAllLines(p);
        int[] a = new int[l.size()];
        for (int i = 0; i < a.length; i++) a[i] = Integer.parseInt(l.get(i).trim());
        return a;
    }
}
