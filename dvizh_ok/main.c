#include "dvizh_ok.c"
#include <stdio.h>
#include <math.h>
#include <string.h>

#define TICK 100

#define max(x, y) (((x) > (y)) ? (x) : (y))
#define min(x, y) (((x) < (y)) ? (x) : (y))

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
    char cmd[32];
    printf("Starting!");
    fflush(stdin);
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
            
            #ifdef DEBUG
                printf("BEGIN\n");
            #endif

            while (strcmp(s, "end") != 0)
            {
                #ifdef DEBUG
                    printf("%s ", s);
                #endif

                if (strcmp(s, "add") == 0)
                {
                    int id;
                    double val;
                    fscanf(f_i, "%d %s %lf", &id, cmd, &val);

                    #ifdef DEBUG
                        printf("%d %lf\n", id, val);
                    #endif

                    if (id < 0 || id > circles_count)
                    {
                        continue;
                    }

                    if (strcmp(cmd, "x") == 0)
                        circles[id]->x += val;
                    if (strcmp(cmd, "y") == 0)
                        circles[id]->y += val;
                    if (strcmp(cmd, "r") == 0)
                        circles[id]->r += val;
                    if (strcmp(cmd, "m") == 0)
                        circles[id]->m += val;
                    if (strcmp(cmd, "vx") == 0)
                        circles[id]->vx += val;
                    if (strcmp(cmd, "vy") == 0)
                        circles[id]->vy += val;
                    if (strcmp(cmd, "v") == 0)
                    {
                        double old_abs = sqrt(circles[id]->vx * circles[id]->vx + circles[id]->vy * circles[id]->vy);
                        circles[id]->vx /= old_abs;
                        circles[id]->vy /= old_abs;
                        circles[id]->vx *= (val + old_abs);
                        circles[id]->vy *= (val + old_abs);
                    }
                }
                if (strcmp(s, "set") == 0)
                {
                    int id;
                    double val;
                    fscanf(f_i, "%d %s %lf", &id, cmd, &val);

                    #ifdef DEBUG
                        printf("%d %lf\n", id, val);
                    #endif

                    if (id < 0 || id > circles_count)
                    {
                        continue;
                    }

                    if (strcmp(cmd, "x") == 0)
                        circles[id]->x = val;
                    if (strcmp(cmd, "y") == 0)
                        circles[id]->y = val;
                    if (strcmp(cmd, "r") == 0)
                        circles[id]->r = val;
                    if (strcmp(cmd, "m") == 0)
                        circles[id]->m = val;
                    if (strcmp(cmd, "vx") == 0)
                        circles[id]->vx = val;
                    if (strcmp(cmd, "vy") == 0)
                        circles[id]->vy = val;
                    if (strcmp(cmd, "v") == 0)
                    {
                        double old_abs = sqrt(circles[id]->vx * circles[id]->vx + circles[id]->vy * circles[id]->vy);
                        circles[id]->vx /= old_abs;
                        circles[id]->vy /= old_abs;
                        circles[id]->vx *= val;
                        circles[id]->vy *= val;
                    }
                }
                if (strcmp(s, "max") == 0)
                {
                    int id;
                    double val;
                    fscanf(f_i, "%d %s %lf", &id, cmd, &val);

                    #ifdef DEBUG
                        printf("%d %lf\n", id, val);
                    #endif

                    if (id < 0 || id > circles_count)
                    {
                        continue;
                    }

                    if (strcmp(cmd, "x") == 0)
                        circles[id]->x = min(val, circles[id]->x);
                    if (strcmp(cmd, "y") == 0)
                        circles[id]->y = min(val, circles[id]->y);
                    if (strcmp(cmd, "r") == 0)
                        circles[id]->r = min(val, circles[id]->r);
                    if (strcmp(cmd, "m") == 0)
                        circles[id]->m = min(val, circles[id]->m);
                    if (strcmp(cmd, "vx") == 0)
                        circles[id]->vx = min(val, circles[id]->vx);
                    if (strcmp(cmd, "vy") == 0)
                        circles[id]->vy = min(val, circles[id]->vy);
                    if (strcmp(cmd, "v") == 0)
                    {
                        double old_abs = sqrt(circles[id]->vx * circles[id]->vx + circles[id]->vy * circles[id]->vy);
                        val = min(val, old_abs);
                        circles[id]->vx /= old_abs;
                        circles[id]->vy /= old_abs;
                        circles[id]->vx *= val;
                        circles[id]->vy *= val;
                    }
                }
                if (strcmp(s, "min") == 0)
                {
                    int id;
                    double val;
                    fscanf(f_i, "%d %s %lf", &id, cmd, &val);

                    #ifdef DEBUG
                        printf("%d %lf\n", id, val);
                    #endif

                    if (id < 0 || id > circles_count)
                    {
                        continue;
                    }

                    if (strcmp(cmd, "x") == 0)
                        circles[id]->x = max(val, circles[id]->x);
                    if (strcmp(cmd, "y") == 0)
                        circles[id]->y = max(val, circles[id]->y);
                    if (strcmp(cmd, "r") == 0)
                        circles[id]->r = max(val, circles[id]->r);
                    if (strcmp(cmd, "m") == 0)
                        circles[id]->m = max(val, circles[id]->m);
                    if (strcmp(cmd, "vx") == 0)
                        circles[id]->vx = max(val, circles[id]->vx);
                    if (strcmp(cmd, "vy") == 0)
                        circles[id]->vy = max(val, circles[id]->vy);
                    if (strcmp(cmd, "v") == 0)
                    {
                        double old_abs = sqrt(circles[id]->vx * circles[id]->vx + circles[id]->vy * circles[id]->vy);
                        val = max(val, old_abs);
                        circles[id]->vx /= old_abs;
                        circles[id]->vy /= old_abs;
                        circles[id]->vx *= val;
                        circles[id]->vy *= val;
                    }
                }
                if (strcmp(s, "add_circle") == 0)
                {
                    double r, m, x, y, vx, vy;
                    fscanf(f_i, "%lf %lf %lf %lf %lf %lf", &r, &m, &x, &y, &vx, &vy);
                    add_circle(r, m, x, y, vx, vy);
                }
                if (strcmp(s, "del_circle") == 0)
                {
                    int id;
                    fscanf(f_i, "%d", &id);
                    del_circle(id);
                }

                fscanf(f_i, "%s", s);
            }
            step(TICK);
            for (int i = 0; i < circles_count; i++)
            {
                fprintf(f_o, "%d %lf %lf %lf %lf %lf %lf,", circles[i]->id, circles[i]->r, circles[i]->m, circles[i]->x, circles[i]->y, circles[i]->vx, circles[i]->vy);
            }
            fprintf(f_o, ";");
            fprintf(f_o, "0 0 0 1920 0,");
            fprintf(f_o, "1 0 0 0 1080,");
            fprintf(f_o, "2 1920 0 1920 1080,");
            fprintf(f_o, "3 0 1080 1820 1080,");
            fprintf(f_o, "\n");
            fflush(f_o);

            #ifdef DEBUG
                printf("END\n");
            #endif
        }
    }
    fclose(f_i);
    fclose(f_o);
}