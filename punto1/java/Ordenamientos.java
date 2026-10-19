import java.util.ArrayList;

/**
 * Algoritmos de ordenamiento del Punto 1 (Taller de Ordenamiento y Búsqueda).
 *
 * Todas las implementaciones siguen las de GeeksforGeeks (referencia principal
 * sugerida en el taller) y son las mismas, línea por línea, que las de
 * python/ordenamientos.py.
 *
 * Fuentes:
 *  - Insertion Sort:        https://www.geeksforgeeks.org/dsa/insertion-sort-algorithm/
 *  - Dual-Pivot QuickSort:  https://www.geeksforgeeks.org/dsa/dual-pivot-quicksort/
 *  - Merge Sort:            https://www.geeksforgeeks.org/dsa/merge-sort/
 *  - Heap Sort:             https://www.geeksforgeeks.org/dsa/heap-sort/
 *  - Radix Sort:            https://www.geeksforgeeks.org/dsa/radix-sort/
 *  - Bucket Sort:           https://www.geeksforgeeks.org/dsa/bucket-sort-2/
 */
public class Ordenamientos {

    // ------------------------------------------------------------------
    // Insertion Sort
    // ------------------------------------------------------------------
    public static void insertionSort(int[] arr) {
        int n = arr.length;
        for (int i = 1; i < n; ++i) {
            int key = arr[i];
            int j = i - 1;
            // Mueve los elementos mayores que key una posición a la derecha
            while (j >= 0 && arr[j] > key) {
                arr[j + 1] = arr[j];
                j = j - 1;
            }
            arr[j + 1] = key;
        }
    }

    // ------------------------------------------------------------------
    // Dual-Pivot QuickSort (pivotes en el primer y el último elemento)
    // ------------------------------------------------------------------
    public static void dualPivotQuickSort(int[] arr) {
        dualPivotQuickSort(arr, 0, arr.length - 1);
    }

    private static void dualPivotQuickSort(int[] arr, int low, int high) {
        if (low < high) {
            int[] piv = partition(arr, low, high);
            dualPivotQuickSort(arr, low, piv[0] - 1);
            dualPivotQuickSort(arr, piv[0] + 1, piv[1] - 1);
            dualPivotQuickSort(arr, piv[1] + 1, high);
        }
    }

    private static int[] partition(int[] arr, int low, int high) {
        // p = pivote izquierdo (primer elemento), q = pivote derecho (último)
        if (arr[low] > arr[high]) {
            swap(arr, low, high);
        }
        int j = low + 1;
        int g = high - 1, k = low + 1;
        int p = arr[low], q = arr[high];
        while (k <= g) {
            if (arr[k] < p) {                 // menor que el pivote izquierdo
                swap(arr, k, j);
                j++;
            } else if (arr[k] >= q) {         // mayor o igual que el pivote derecho
                while (arr[g] > q && k < g) {
                    g--;
                }
                swap(arr, k, g);
                g--;
                if (arr[k] < p) {
                    swap(arr, k, j);
                    j++;
                }
            }
            k++;
        }
        j--;
        g++;
        swap(arr, low, j);   // pivote izquierdo a su posición final
        swap(arr, high, g);  // pivote derecho a su posición final
        return new int[] { j, g };
    }

    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }

    // ------------------------------------------------------------------
    // Merge Sort
    // ------------------------------------------------------------------
    public static void mergeSort(int[] arr) {
        mergeSort(arr, 0, arr.length - 1);
    }

    private static void mergeSort(int[] arr, int l, int r) {
        if (l < r) {
            int m = l + (r - l) / 2;
            mergeSort(arr, l, m);
            mergeSort(arr, m + 1, r);
            merge(arr, l, m, r);
        }
    }

    private static void merge(int[] arr, int l, int m, int r) {
        int n1 = m - l + 1;
        int n2 = r - m;
        int[] L = new int[n1];
        int[] R = new int[n2];
        for (int i = 0; i < n1; ++i) L[i] = arr[l + i];
        for (int j = 0; j < n2; ++j) R[j] = arr[m + 1 + j];

        int i = 0, j = 0, k = l;
        while (i < n1 && j < n2) {
            if (L[i] <= R[j]) {      // <= mantiene la estabilidad
                arr[k] = L[i];
                i++;
            } else {
                arr[k] = R[j];
                j++;
            }
            k++;
        }
        while (i < n1) { arr[k] = L[i]; i++; k++; }
        while (j < n2) { arr[k] = R[j]; j++; k++; }
    }

    // ------------------------------------------------------------------
    // Heap Sort
    // ------------------------------------------------------------------
    public static void heapSort(int[] arr) {
        int n = arr.length;
        // Construye el max-heap
        for (int i = n / 2 - 1; i >= 0; i--) {
            heapify(arr, n, i);
        }
        // Extrae uno a uno el máximo y lo lleva al final
        for (int i = n - 1; i > 0; i--) {
            swap(arr, 0, i);
            heapify(arr, i, 0);
        }
    }

    private static void heapify(int[] arr, int n, int i) {
        int largest = i;
        int l = 2 * i + 1;
        int r = 2 * i + 2;
        if (l < n && arr[l] > arr[largest]) largest = l;
        if (r < n && arr[r] > arr[largest]) largest = r;
        if (largest != i) {
            swap(arr, i, largest);
            heapify(arr, n, largest);
        }
    }

    // ------------------------------------------------------------------
    // Radix Sort (LSD, base 10, counting sort estable por dígito)
    // ------------------------------------------------------------------
    public static void radixSort(int[] arr) {
        int n = arr.length;
        int m = getMax(arr);
        for (int exp = 1; m / exp > 0; exp *= 10) {
            countSort(arr, n, exp);
        }
    }

    private static int getMax(int[] arr) {
        int mx = arr[0];
        for (int i = 1; i < arr.length; i++) {
            if (arr[i] > mx) mx = arr[i];
        }
        return mx;
    }

    private static void countSort(int[] arr, int n, int exp) {
        int[] output = new int[n];
        int[] count = new int[10];
        for (int i = 0; i < n; i++) count[(arr[i] / exp) % 10]++;
        for (int i = 1; i < 10; i++) count[i] += count[i - 1];
        for (int i = n - 1; i >= 0; i--) {          // de derecha a izquierda: estable
            output[count[(arr[i] / exp) % 10] - 1] = arr[i];
            count[(arr[i] / exp) % 10]--;
        }
        for (int i = 0; i < n; i++) arr[i] = output[i];
    }

    // ------------------------------------------------------------------
    // Bucket Sort
    //   Cubetas: n (una por elemento).
    //   Asignación: índice = (valor - min) * n / (max - min + 1)
    //   (reparte el rango [min, max] en n intervalos iguales).
    //   Cada cubeta se ordena con insertion sort y luego se concatenan.
    // ------------------------------------------------------------------
    @SuppressWarnings("unchecked")
    public static void bucketSort(int[] arr) {
        int n = arr.length;
        if (n <= 0) return;
        int min = arr[0], max = arr[0];
        for (int v : arr) {
            if (v < min) min = v;
            if (v > max) max = v;
        }
        long rango = (long) max - min + 1;

        ArrayList<Integer>[] buckets = new ArrayList[n];
        for (int i = 0; i < n; i++) buckets[i] = new ArrayList<>();

        for (int i = 0; i < n; i++) {
            int bi = (int) (((long) arr[i] - min) * n / rango);
            buckets[bi].add(arr[i]);
        }
        for (int i = 0; i < n; i++) insertionSortBucket(buckets[i]);

        int index = 0;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < buckets[i].size(); j++) {
                arr[index++] = buckets[i].get(j);
            }
        }
    }

    private static void insertionSortBucket(ArrayList<Integer> bucket) {
        for (int i = 1; i < bucket.size(); ++i) {
            int key = bucket.get(i);
            int j = i - 1;
            while (j >= 0 && bucket.get(j) > key) {
                bucket.set(j + 1, bucket.get(j));
                j--;
            }
            bucket.set(j + 1, key);
        }
    }
}
