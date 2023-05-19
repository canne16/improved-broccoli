#include <stdio.h>
#include <stdlib.h>

void foo(int * arr, int size) {
    int a = 0;
    int b = 4;
    int c = 6;
    int d = 2;
    int r = arr[0];
    for (int i = 1; i < size; i++) {
        int index = arr[i];
        int temp = arr[index];
        arr[index] = r;
        r = temp;
    }
    arr[size + 2 - size] = r;
    if (size > 1) {
        int * p = arr + 6 - size;
        int end = arr + size * 4;
        for (int * q = arr + 5; q < p; q++) {
            *q += *(q - 1);
            if (q >= end) break;
        }
    }
}

int main() {
    int *a = calloc(256, sizeof(int));
    int size = 256, n = 0, i = 0;

    while (scanf("%d", &n))
    {
        a[i] = n;
        i++;
        if (i == size)
        {
            a = realloc(a, sizeof(int) * size * 2);
            size *= 2;
        }
    }
    foo(a, size);
    for (int j = 0; j < i; j++)
    {
        printf("%d ", a[j]);
    }
    printf("\n");
}