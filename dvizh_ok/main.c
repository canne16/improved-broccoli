#include "dvizh_ok.c"
#include <stdio.h>
#include <math.h>
#include <string.h>

#define TICK 100

void initial_pos() {
    add_circle(100, 1, 100, 100, 0, 0);
    add_circle(5, 1, 300, 100, 0, 0);
    add_circle(10, 1, 300, 100, 0, 0);
    add_circle(100, 1, 100, 100, 0, 0);
    add_circle(10, 1, 300, 100, 0, 0);
    add_circle(5, 1, 300, 100, 0, 0);
}

int main()
{
    FILE* f_i = fopen("fp_ser_eng", "r");
    FILE* f_o = fopen("fp_eng_ser", "w");
    char *s = calloc(sizeof(char), 256);
    printf("Starting!\n");
    fflush(stdout);
    while (1)
    {
        fscanf(f_i, "%s", s);
        if (strcmp(s, "init") == 0)
        {
            free_all();
            init();
            initial_pos();
            continue;
        }
        if (strcmp(s, "exit") == 0)
        {
            return 0;
        }
        if (strcmp(s, "begin") == 0)
        {
            fscanf(f_i, "%s", s);

            while (strcmp(s, "end") != 0)
            {
                if (strcmp(s, "ADD") == 0)
                {
                    int id;
                    char c;
                    double val;
                    fscanf(f_i, "%d %c %lf", &id, &c, &val);
                    printf("ADD %d %c %lf\n", id, c, val);
                    fflush(stdout);
                    if (id < 0 || id > circles_count)
                    {
                        continue;
                    }
                    switch (c)
                    {
                    case 'x':
                        circles[id]->x += val;
                        break;
                    case 'y':
                        circles[id]->y += val;
                        break;
                    case 'X': // vx
                        circles[id]->vx += val;
                        break;
                    case 'Y': // vy
                        circles[id]->vy += val;
                        break;
                    case 'r':
                        circles[id]->r += val;
                        break;
                    case 'm':
                        circles[id]->m += val;
                        break;
                    default:
                        break;
                    }
                }


                fscanf(f_i, "%s", s);
            }
            step(TICK);
            fprintf(f_o, "%d\n", circles_count + circles_size + 2);
            //fprintf(f_o, "circles %d;", circles_count);
            for (int i = 0; i < circles_count; i++)
            {
                /*
                unsigned int id;
                double r;
                double m;
                double x;
                double y;
                double vx;
                double vy;
                */
                fprintf(f_o, "%d %lf %lf %lf %lf %lf %lf,", circles[i]->id, circles[i]->r, circles[i]->m, circles[i]->x, circles[i]->y, circles[i]->vx, circles[i]->vy);
            }
            fprintf(f_o, ";");
            fprintf(f_o, "0 0 0 1920 0,");
            fprintf(f_o, "1 0 0 0 1080,");
            fprintf(f_o, "2 1920 0 1920 1080,");
            fprintf(f_o, "3 0 1080 1820 1080,");
            fprintf(f_o, "\n");
            fflush(f_o);
        }
    }
    fclose(f_i);
    fclose(f_o);
}