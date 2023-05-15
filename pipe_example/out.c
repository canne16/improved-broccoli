#include <stdio.h>

int main()
{
    FILE* fp = fopen("pipe", "r");
    printf("Starting!\n");
    while (1)
    {
        int d;
        fscanf(fp, "%d", &d);
        printf("%d\n", d);
    }
}