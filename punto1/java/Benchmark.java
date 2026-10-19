import java.io.*;
import java.nio.file.*;
import java.util.*;

/**
 * Benchmark del Punto 1 (Java, lenguaje compilado).
 *
 * Uso:  java -Xmx4g Benchmark <algoritmo> <carpetaDatos> <archivoCsv>
 *       algoritmo: insertion | dualpivot | merge | heap | radix | bucket
 *
 * Reglas que implementa (tomadas del enunciado del taller):
 *  - Los datos se leen de archivo ANTES de medir; solo se mide el ordenamiento.
 *  - Cada repetición ordena una copia nueva del arreglo (la copia no se mide).
 *  - 1 ejecución de calentamiento (JIT) que no entra al promedio + 5 repeticiones.
 *  - Después de cada repetición, fuera del tiempo medido, se verifica que el
 *    arreglo quedó igual a la versión ascendente (correctamente ordenado).
 *  - Si con la medición del tamaño anterior y la complejidad teórica se predice
 *    que una ejecución tardaría más de 5 minutos, no se ejecuta: se estima.
 *  - Si el algoritmo falla (p. ej. StackOverflowError) se registra el error y se
 *    estima el tiempo desde el último tamaño que sí terminó.
 */
public class Benchmark {

    static final int[] TAMANIOS = {1_000, 10_000, 100_000, 1_000_000};
    static final String[] VARIANTES = {"aleatorio", "ascendente", "descendente"};
    static final int REPETICIONES = 5;
    static final double LIMITE_MS = 5 * 60 * 1000.0;   // 5 minutos

    interface Sorter { void sort(int[] a); }

    static Sorter sorter(String alg) {
        switch (alg) {
            case "insertion": return Ordenamientos::insertionSort;
            case "dualpivot": return Ordenamientos::dualPivotQuickSort;
            case "merge":     return Ordenamientos::mergeSort;
            case "heap":      return Ordenamientos::heapSort;
            case "radix":     return Ordenamientos::radixSort;
            case "bucket":    return Ordenamientos::bucketSort;
        }
        throw new IllegalArgumentException("Algoritmo desconocido: " + alg);
    }

    /** Clase de complejidad teórica esperada para cada algoritmo y variante. */
    static String clase(String alg, String var) {
        switch (alg) {
            case "insertion": return var.equals("ascendente") ? "n" : "n2";
            case "dualpivot": return var.equals("aleatorio") ? "nlogn" : "n2";
            case "merge": case "heap": return "nlogn";
            default: return "n";   // radix (d fijo = 8) y bucket (datos uniformes)
        }
    }

    /** Factor de crecimiento teórico al pasar de n0 a n1. */
    static double factor(String clase, long n0, long n1) {
        double r = (double) n1 / n0;
        switch (clase) {
            case "n2": return r * r;
            case "nlogn": return r * Math.log(n1) / Math.log(n0);
            default: return r;
        }
    }

    static int[] leer(Path p) throws IOException {
        List<String> lineas = Files.readAllLines(p);
        int[] a = new int[lineas.size()];
        for (int i = 0; i < a.length; i++) a[i] = Integer.parseInt(lineas.get(i).trim());
        return a;
    }

    static String fmt(double v) { return String.format(Locale.US, "%.4f", v); }

    public static void main(String[] args) throws Exception {
        String alg = args[0];
        Path datos = Paths.get(args[1]);
        Path csv = Paths.get(args[2]);
        Sorter s = sorter(alg);

        boolean nuevo = !Files.exists(csv);
        try (PrintWriter out = new PrintWriter(new FileWriter(csv.toFile(), true))) {
            if (nuevo) out.println("algoritmo,lenguaje,variante,n,t1_ms,t2_ms,t3_ms,t4_ms,t5_ms,"
                    + "promedio_ms,desv_ms,tipo,estado,nota");

            for (String var : VARIANTES) {
                String cl = clase(alg, var);
                long nOk = -1; double mediaOk = -1;   // último tamaño que terminó bien
                boolean fallo = false;

                for (int n : TAMANIOS) {
                    String base = alg + ",java," + var + "," + n + ",";
                    double pred = nOk > 0 ? mediaOk * factor(cl, nOk, n) : -1;
                    String notaEst = nOk > 0 ? "estimado desde n=" + nOk + " (" + fmt(mediaOk)
                            + " ms) con crecimiento " + cl : "";

                    // Regla de los 5 minutos (solo si no venimos de un fallo, que se documenta)
                    if (!fallo && pred > LIMITE_MS) {
                        out.println(base + ",,,,," + fmt(pred) + ",,estimado,supera_5min," + notaEst);
                        out.flush();
                        System.out.printf("%-10s %-12s n=%-8d ESTIMADO %.1f ms (>5 min)%n", alg, var, n, pred);
                        continue;
                    }

                    int[] original = leer(datos.resolve(var + "_" + n + ".txt"));
                    int[] ref = leer(datos.resolve("ascendente_" + n + ".txt"));
                    double[] t = new double[REPETICIONES];
                    try {
                        // Calentamiento (no se promedia)
                        int[] w = Arrays.copyOf(original, original.length);
                        s.sort(w);
                        if (!Arrays.equals(w, ref)) throw new IllegalStateException("No quedó ordenado");

                        for (int r = 0; r < REPETICIONES; r++) {
                            int[] copia = Arrays.copyOf(original, original.length); // fuera de la medición
                            long t0 = System.nanoTime();
                            s.sort(copia);
                            long t1 = System.nanoTime();
                            t[r] = (t1 - t0) / 1e6;
                            if (!Arrays.equals(copia, ref)) throw new IllegalStateException("No quedó ordenado");
                        }
                    } catch (StackOverflowError e) {
                        fallo = true;
                        String est = pred > 0 ? fmt(pred) : "";
                        out.println(base + ",,,,," + est + ",,estimado,fallo_StackOverflowError,"
                                + "desbordamiento de pila; " + notaEst);
                        out.flush();
                        System.out.printf("%-10s %-12s n=%-8d FALLO StackOverflowError (estimado %s ms)%n",
                                alg, var, n, est);
                        continue;
                    }

                    double media = 0;
                    for (double x : t) media += x;
                    media /= REPETICIONES;
                    double sq = 0;
                    for (double x : t) sq += (x - media) * (x - media);
                    double desv = Math.sqrt(sq / (REPETICIONES - 1));   // desviación muestral

                    StringBuilder sb = new StringBuilder(base);
                    for (double x : t) sb.append(fmt(x)).append(',');
                    sb.append(fmt(media)).append(',').append(fmt(desv)).append(",medido,ok,");
                    out.println(sb);
                    out.flush();
                    System.out.printf("%-10s %-12s n=%-8d %12.3f ms  (desv %.3f)%n", alg, var, n, media, desv);
                    nOk = n; mediaOk = media;
                }
            }
        }
    }
}
