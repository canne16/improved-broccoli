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
    printf("Starting!\n");
    fflush(stdout);
    while (1)
    {
        fscanf(f_i, "%s", s);
        if (strcmp(s, "init") == 0)
        {
            fscanf(f_i, "%d %d\n", &WIDTH, &HEIGHT);
            printf("%d, %d\n", WIDTH, HEIGHT);
            fflush(stdout);
            free_all();
            init();
            set_borders(-WIDTH/2, -HEIGHT/2, WIDTH/2, HEIGHT/2);
            continue;
        }
        if (strcmp(s, "begin") == 0)
            {
            //printf("begin\n");
            //fflush(stdout);
            fscanf(f_i, "%s", s);
            if (strcmp(s, "exit") == 0)
            {
                printf("Finishing...\n");
                break;
            }

            while (strcmp(s, "end") != 0)
            {
                
                if (strcmp(s, "add") == 0)
                {
                    int id;
                    double val;
                    fscanf(f_i, "%d %s %lf", &id, cmd, &val);

                    if (id < 0 || id > circles_count)
                    {
                        continue;
                    }

                    if (strcmp(cmd, "x") == 0)
                        circles[id]->x += val;
                    if (strcmp(cmd, "y") == 0)
                        circles[id]->y += val;
                    if (strcmp(cmd, "r") == 0)
                        if(circles[id]->r + val > 0)
                            circles[id]->r += val;
                    if (strcmp(cmd, "m") == 0)
                        if(circles[id]->m + val > 0)
                            circles[id]->m += val;
                    if (strcmp(cmd, "X") == 0)
                        if(circles[id]->ax*val <= 0)
                            circles[id]->ax += val;
                    if (strcmp(cmd, "Y") == 0)
                        if(circles[id]->ay*val <= 0)
                            circles[id]->ay += val;
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
                    if (strcmp(cmd, "X") == 0)
                        circles[id]->ax = val;
                    if (strcmp(cmd, "Y") == 0)
                        circles[id]->ay = val;
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
                    printf("%d\n", id);
                    fflush(stdout);
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
                if(circles[i]==NULL)
                    continue;
                fprintf(f_o, "%d %lf %lf %lf %lf %lf %lf,", circles[i]->id, circles[i]->r, circles[i]->m, circles[i]->x, circles[i]->y, circles[i]->vx, circles[i]->vy);
            }
            fprintf(f_o, ";");
            for (int i = 0; i < sections_count; i++)
            {
                if(sections[i]==NULL)
                    continue;
                fprintf(f_o, "%d %lf %lf %lf %lf,", sections[i]->id, sections[i]->x1, sections[i]->y1, sections[i]->x2, sections[i]->y2);
            }
            fprintf(f_o, "\n");
            fflush(f_o);

        }
    }
    fclose(f_i);
    fclose(f_o);
}