/**
 * Algoritmos de búsqueda del Punto 2 (Taller de Ordenamiento y Búsqueda).
 *
 * Implementaciones en Java (lenguaje compilado), con la misma estructura y
 * lógica línea por línea que python/busquedas.py. Todas las implementaciones siguen
 * las referencias de GeeksforGeeks (fuente principal sugerida en el taller).
 *
 * Fuentes:
 *  - Linear Search:         https://www.geeksforgeeks.org/linear-search/
 *  - Binary Search:         https://www.geeksforgeeks.org/binary-search/
 *  - Ternary Search:        https://www.geeksforgeeks.org/ternary-search/
 *  - Jump Search:           https://www.geeksforgeeks.org/jump-search/
 *  - Interpolation Search:  https://www.geeksforgeeks.org/interpolation-search/
 *  - Exponential Search:    https://www.geeksforgeeks.org/exponential-search/
 */
public class Busquedas {

    // ------------------------------------------------------------------
    // Búsqueda Lineal (referencia)
    // ------------------------------------------------------------------
    public static int linearSearch(int[] arr, int x) {
        int n = arr.length;
        for (int i = 0; i < n; i++) {
            if (arr[i] == x) {
                return i;
            }
        }
        return -1;
    }

    // ------------------------------------------------------------------
    // Búsqueda Binaria (versión iterativa)
    // ------------------------------------------------------------------
    public static int binarySearch(int[] arr, int x) {
        int low = 0;
        int high = arr.length - 1;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (arr[mid] == x) {
                return mid;
            } else if (arr[mid] < x) {
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }
        return -1;
    }

    // ------------------------------------------------------------------
    // Búsqueda Ternaria (versión iterativa)
    // ------------------------------------------------------------------
    public static int ternarySearch(int[] arr, int x) {
        int low = 0;
        int high = arr.length - 1;
        while (low <= high) {
            int mid1 = low + (high - low) / 3;
            int mid2 = high - (high - low) / 3;

            if (arr[mid1] == x) {
                return mid1;
            }
            if (arr[mid2] == x) {
                return mid2;
            }

            if (x < arr[mid1]) {
                high = mid1 - 1;
            } else if (x > arr[mid2]) {
                low = mid2 + 1;
            } else {
                low = mid1 + 1;
                high = mid2 - 1;
            }
        }
        return -1;
    }

    // ------------------------------------------------------------------
    // Búsqueda por Saltos (Jump Search)
    // ------------------------------------------------------------------
    public static int jumpSearch(int[] arr, int x) {
        int n = arr.length;
        if (n == 0) return -1;

        int step = (int) Math.floor(Math.sqrt(n));
        int prev = 0;

        while (prev < n && arr[Math.min(step, n) - 1] < x) {
            prev = step;
            step += (int) Math.floor(Math.sqrt(n));
            if (prev >= n) {
                return -1;
            }
        }

        while (prev < Math.min(step, n)) {
            if (arr[prev] == x) {
                return prev;
            }
            prev++;
        }
        return -1;
    }

    // ------------------------------------------------------------------
    // Búsqueda por Interpolación
    // ------------------------------------------------------------------
    public static int interpolationSearch(int[] arr, int x) {
        int low = 0;
        int high = arr.length - 1;

        while (low <= high && x >= arr[low] && x <= arr[high]) {
            if (low == high) {
                if (arr[low] == x) return low;
                return -1;
            }
            if (arr[high] == arr[low]) {
                if (arr[low] == x) return low;
                return -1;
            }

            // Se realiza cast a long para evitar desbordamiento aritmético con números de 8 dígitos
            int pos = low + (int) (((long) (high - low) * (x - arr[low])) / (arr[high] - arr[low]));

            if (arr[pos] == x) {
                return pos;
            }
            if (arr[pos] < x) {
                low = pos + 1;
            } else {
                high = pos - 1;
            }
        }
        return -1;
    }

    // ------------------------------------------------------------------
    // Búsqueda Exponencial
    // ------------------------------------------------------------------
    public static int exponentialSearch(int[] arr, int x) {
        int n = arr.length;
        if (n == 0) return -1;
        if (arr[0] == x) return 0;

        int i = 1;
        while (i < n && arr[i] <= x) {
            i *= 2;
        }

        // Búsqueda binaria en el rango acotado [i / 2, min(i, n - 1)]
        int low = i / 2;
        int high = Math.min(i, n - 1);
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (arr[mid] == x) {
                return mid;
            } else if (arr[mid] < x) {
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }
        return -1;
    }
}
