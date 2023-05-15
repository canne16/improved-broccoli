#include <stdio.h>

int main()
{
    FILE* fp = fopen("pipe", "w");
    printf("Starting!\n");
    while (1)
    {
        int d;
        scanf("%d", &d);
        fprintf(fp, "%d\n", d);
        fflush(fp);
    }
}