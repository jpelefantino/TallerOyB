import java.io.*;
import java.nio.file.*;
import java.util.*;

/**
 * Benchmark del Punto 2 (Java, lenguaje compilado).
 *
 * Uso:
 *   java -Xmx4g -cp java Benchmark <algoritmo|todos> [dir_arreglos] [dir_claves] <archivo_csv>
 *   o
 *   java -Xmx4g -cp java Benchmark <algoritmo|todos> <archivo_csv>
 *
 * Algoritmos: linear | binary | ternary | jump | interpolation | exponential | todos
 *
 * Reglas que implementa:
 *  - Arreglos ordenados ascendentes del Punto 1.
 *  - 1.000 claves de búsqueda (500 presentes y 500 ausentes).
 *  - 1 ejecución de calentamiento (warmup) para el JIT antes de las 5 repeticiones oficiales.
 *  - Medición del tiempo acumulado y reporte del promedio por búsqueda individual en ns.
 *  - Experimento complementario de posición de la clave (inicio, centro, final) en n = 1.000.000.
 */
public class Benchmark {

    static final int[] TAMANIOS = {1_000, 10_000, 100_000, 1_000_000};
    static final int REPETICIONES = 5;
    static final String[] TODOS_LOS_ALGS = {"linear", "binary", "ternary", "jump", "interpolation", "exponential"};

    interface Searcher {
        int search(int[] arr, int x);
    }

    static Searcher obtenerBuscador(String alg) {
        switch (alg.toLowerCase()) {
            case "linear":        return Busquedas::linearSearch;
            case "binary":        return Busquedas::binarySearch;
            case "ternary":       return Busquedas::ternarySearch;
            case "jump":          return Busquedas::jumpSearch;
            case "interpolation": return Busquedas::interpolationSearch;
            case "exponential":   return Busquedas::exponentialSearch;
            default:
                throw new IllegalArgumentException("Algoritmo desconocido: " + alg);
        }
    }

    static double medirBloque(Searcher searcher, int[] arr, int[] claves) {
        long t0 = System.nanoTime();
        long sink = 0;
        for (int c : claves) {
            sink += searcher.search(arr, c);
        }
        long t1 = System.nanoTime();

        // Evitar que el compilador JIT elimine el bucle como código muerto
        if (sink == Long.MIN_VALUE) {
            System.out.println(sink);
        }
        return (double) (t1 - t0) / claves.length;
    }

    static void correrRepeticiones(Searcher searcher, int[] arr, int[] claves, double[] tiempos) {
        // Ejecución de calentamiento (JIT warmup)
        medirBloque(searcher, arr, claves);

        // 5 repeticiones oficiales
        for (int i = 0; i < REPETICIONES; i++) {
            tiempos[i] = medirBloque(searcher, arr, claves);
        }
    }

    static double calcularPromedio(double[] tiempos) {
        double suma = 0.0;
        for (double t : tiempos) suma += t;
        return suma / tiempos.length;
    }

    static double calcularDesv(double[] tiempos, double prom) {
        double suma = 0.0;
        for (double t : tiempos) {
            double diff = t - prom;
            suma += diff * diff;
        }
        return Math.sqrt(suma / (tiempos.length - 1));
    }

    static void guardarFila(Path rutaCsv, String[] datos) throws IOException {
        boolean nuevo = !Files.exists(rutaCsv);
        if (rutaCsv.getParent() != null) {
            Files.createDirectories(rutaCsv.getParent());
        }
        try (BufferedWriter bw = Files.newBufferedWriter(rutaCsv, StandardOpenOption.CREATE, StandardOpenOption.APPEND)) {
            if (nuevo) {
                bw.write("algoritmo,lenguaje,variante,n,t1_ns,t2_ns,t3_ns,t4_ns,t5_ns,promedio_ns,desv_ns,tipo,estado,nota\n");
            }
            bw.write(String.join(",", datos) + "\n");
        }
    }

    static int[] leerArchivo(Path ruta) throws IOException {
        String contenido = Files.readString(ruta);
        String[] tokens = contenido.trim().split("\\s+");
        int[] res = new int[tokens.length];
        for (int i = 0; i < tokens.length; i++) {
            res[i] = Integer.parseInt(tokens[i]);
        }
        return res;
    }

    static void benchmarkAlgoritmo(String alg, Path dirArreglos, Path dirClaves, Path rutaCsv) throws IOException {
        Searcher searcher = obtenerBuscador(alg);
        System.out.printf("=== Iniciando Benchmark Java: %s ===%n", alg);

        // 1. Crecimiento con n (claves mixtas: 500 presentes + 500 ausentes)
        for (int n : TAMANIOS) {
            Path rutaArr = dirArreglos.resolve(String.format("ascendente_%d.txt", n));
            Path rutaClavesN = dirClaves.resolve(String.format("claves_%d.txt", n));

            if (!Files.exists(rutaArr) || !Files.exists(rutaClavesN)) {
                System.out.printf("Saltando n=%,d: archivos no encontrados (%s o %s)%n", n, rutaArr, rutaClavesN);
                continue;
            }

            int[] arr = leerArchivo(rutaArr);
            int[] claves = leerArchivo(rutaClavesN);

            double[] tiempos = new double[REPETICIONES];
            correrRepeticiones(searcher, arr, claves, tiempos);

            double prom = calcularPromedio(tiempos);
            double desv = calcularDesv(tiempos, prom);

            String[] fila = {
                alg, "java", "claves_mixtas", String.valueOf(n),
                String.format(Locale.US, "%.2f", tiempos[0]),
                String.format(Locale.US, "%.2f", tiempos[1]),
                String.format(Locale.US, "%.2f", tiempos[2]),
                String.format(Locale.US, "%.2f", tiempos[3]),
                String.format(Locale.US, "%.2f", tiempos[4]),
                String.format(Locale.US, "%.2f", prom),
                String.format(Locale.US, "%.2f", desv),
                "medido", "ok", "\"1000 claves (500 presentes, 500 ausentes)\""
            };
            guardarFila(rutaCsv, fila);
            System.out.printf("[%s] n=%,d (claves_mixtas): prom=%.1f ns/busqueda (+-%.1f ns)%n", alg, n, prom, desv);
        }

        // 2. Experimento: Posición de la clave en n = 1.000.000
        int nMax = 1_000_000;
        Path rutaArrMax = dirArreglos.resolve(String.format("ascendente_%d.txt", nMax));
        if (Files.exists(rutaArrMax)) {
            int[] arrMax = leerArchivo(rutaArrMax);

            String[][] posiciones = {
                {"pos_inicio", String.valueOf(arrMax[0]), "\"1000 busquedas clave en arr[0]\""},
                {"pos_centro", String.valueOf(arrMax[nMax / 2]), "\"1000 busquedas clave en arr[n/2]\""},
                {"pos_final", String.valueOf(arrMax[nMax - 1]), "\"1000 busquedas clave en arr[n-1]\""}
            };

            for (String[] posInfo : posiciones) {
                String posNombre = posInfo[0];
                int claveVal = Integer.parseInt(posInfo[1]);
                String desc = posInfo[2];

                int[] clavesPos = new int[1_000];
                Arrays.fill(clavesPos, claveVal);

                double[] tiempos = new double[REPETICIONES];
                correrRepeticiones(searcher, arrMax, clavesPos, tiempos);

                double prom = calcularPromedio(tiempos);
                double desv = calcularDesv(tiempos, prom);

                String[] fila = {
                    alg, "java", posNombre, String.valueOf(nMax),
                    String.format(Locale.US, "%.2f", tiempos[0]),
                    String.format(Locale.US, "%.2f", tiempos[1]),
                    String.format(Locale.US, "%.2f", tiempos[2]),
                    String.format(Locale.US, "%.2f", tiempos[3]),
                    String.format(Locale.US, "%.2f", tiempos[4]),
                    String.format(Locale.US, "%.2f", prom),
                    String.format(Locale.US, "%.2f", desv),
                    "medido", "ok", desc
                };
                guardarFila(rutaCsv, fila);
                System.out.printf("[%s] n=%,d (%s): prom=%.1f ns/busqueda (+-%.1f ns)%n", alg, nMax, posNombre, prom, desv);
            }
        }

        System.out.printf("=== Fin Benchmark Java: %s ===%n%n", alg);
    }

    public static void main(String[] args) throws Exception {
        String alg;
        Path dirArreglos;
        Path dirClaves;
        Path rutaCsv;

        if (args.length == 2) {
            alg = args[0];
            dirArreglos = Paths.get("..", "punto1", "datos");
            if (!Files.exists(dirArreglos)) {
                dirArreglos = Paths.get("punto1", "datos");
            }
            dirClaves = Paths.get("datos");
            if (!Files.exists(dirClaves)) {
                dirClaves = Paths.get("punto2", "datos");
            }
            rutaCsv = Paths.get(args[1]);
        } else if (args.length == 4) {
            alg = args[0];
            dirArreglos = Paths.get(args[1]);
            dirClaves = Paths.get(args[2]);
            rutaCsv = Paths.get(args[3]);
        } else {
            System.err.println("Uso: java Benchmark <algoritmo|todos> [dir_arreglos] [dir_claves] <archivo_csv>");
            System.exit(1);
            return;
        }

        if (alg.equalsIgnoreCase("todos") || alg.equalsIgnoreCase("all")) {
            for (String a : TODOS_LOS_ALGS) {
                benchmarkAlgoritmo(a, dirArreglos, dirClaves, rutaCsv);
            }
        } else {
            benchmarkAlgoritmo(alg, dirArreglos, dirClaves, rutaCsv);
        }
    }
}
