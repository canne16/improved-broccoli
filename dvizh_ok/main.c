#include "dvizh_ok.c"
#include <stdio.h>
#include <math.h>
#include <string.h>

#define TICK 1

#define max(x, y) (((x) > (y)) ? (x) : (y))
#define min(x, y) (((x) < (y)) ? (x) : (y))

int main()
{
    int WIDTH, HEIGHT;

    FILE* f_i = fopen("fp_ser_eng", "r");
    FILE* f_o = fopen("fp_eng_ser", "w");
    char *s = calloc(sizeof(char), 256);
    char cmd[32];
    printf("Starting!");
    fflush(stdout);
    while (1)
    {
        if (fscanf(f_i, "%s", s) < 1)
        {
            printf("Broken pipe! Exiting\n");
            return -1;
        }
        if (strcmp(s, "init") == 0)
        {
            fscanf(f_i, "%d %d\n", &WIDTH, &HEIGHT);
            printf("%d, %d\n", WIDTH, HEIGHT);
            fflush(stdout);
            free_all();
            init();
            continue;
        }
        if (strcmp(s, "exit") == 0)
        {
            printf("finishing\n");
            return 0;
        }
        if (strcmp(s, "begin") == 0)
        {
            if (fscanf(f_i, "%s", s) < 1)
            {
                printf("Broken pipe!\n");
                return -1;
            }
            
            #ifdef DEBUG
                printf("BEGIN\n");
            #endif

            while (strcmp(s, "end") != 0)
            {
                #ifdef DEBUG
                    printf("%s ", s);
                    fflush(stdout);
                #endif

                if (strcmp(s, "add") == 0)
                {
                    int id;
                    double val;
                    if (fscanf(f_i, "%d %s %lf", &id, cmd, &val) < 3)
                    {
                        printf("Broken pipe!\n");
                        return -1;
                    }

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
                    if (fscanf(f_i, "%d %s %lf", &id, cmd, &val) < 3)
                    {
                        printf("Broken pipe!\n");
                        return -1;
                    }
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
                    if (fscanf(f_i, "%d %s %lf", &id, cmd, &val) < 3)
                    {
                        printf("Broken pipe!\n");
                        continue;
                    }
                    #ifdef DEBUG
                        printf("%d %lf\n", id, val);
                    #endif

                    if (id < 0 || id > circles_count)
                    {
                        continue;
                    }

                    if (strcmp(cmd, "x") == 0)
                    {
                        if (circles[id]->x > val)
                        {
                            circles[id]->x =val;
                            circles[id]->vx = min(0, circles[id]->vx);
                        }
                    }
                    if (strcmp(cmd, "y") == 0)
                    {
                        if (circles[id]->x > val)
                        {
                            circles[id]->x =val;
                            circles[id]->vy = min(0, circles[id]->vy);
                        }
                    }
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
                    if (fscanf(f_i, "%d %s %lf", &id, cmd, &val) < 3)
                    {
                        printf("Broken pipe!\n");
                        return -1;
                    }
                    #ifdef DEBUG
                        printf("%d %lf\n", id, val);
                    #endif

                    if (id < 0 || id > circles_count)
                    {
                        continue;
                    }

                    if (strcmp(cmd, "x") == 0)
                    {
                        if (circles[id]->x < val)
                        {
                            circles[id]->x =val;
                            circles[id]->vx = max(0, circles[id]->vx);
                        }
                    }
                    if (strcmp(cmd, "y") == 0)
                    {
                        if (circles[id]->x < val)
                        {
                            circles[id]->x =val;
                            circles[id]->vy = max(0, circles[id]->vy);
                        }
                    }
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
                if (strcmp(s, "add_section") == 0)
                {
                    double x1, y1, x2, y2;
                    fscanf(f_i, "%lf %lf %lf %lf", &x1, &y1, &x2, &y2);
                    add_section(x1, y1, x2, y2);
                }
                if (strcmp(s, "del_section") == 0)
                {
                    int id;
                    fscanf(f_i, "%d", &id);
                    del_section(id);
                }

                fscanf(f_i, "%s", s);
            }
            fflush(stdout);
            step(TICK);
            fflush(stdout);
            for (int i = 0; i < circles_count; i++)
            {
                fprintf(f_o, "%d %lf %lf %lf %lf %lf %lf,", circles[i]->id, circles[i]->r, circles[i]->m, circles[i]->x, circles[i]->y, circles[i]->vx, circles[i]->vy);
                //printf("%d %lf %lf %lf %lf %lf %lf,", circles[i]->id, circles[i]->r, circles[i]->m, circles[i]->x, circles[i]->y, circles[i]->vx, circles[i]->vy);
            }
            fprintf(f_o, ";");
            for (int i = 0; i < sections_count; i++)
            {
                fprintf(f_o, "%d %lf %lf %lf %lf,", sections[i]->id, sections[i]->x1, sections[i]->y1, sections[i]->x2, sections[i]->y2);
                //printf("%d %lf %lf %lf %lf,", sections[i]->id, sections[i]->x1, sections[i]->y1, sections[i]->x2, sections[i]->y2);
            }
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