#include "dvizh_ok.c"
#include <stdio.h>
#include <math.h>
#include <string.h>

#define TICK 1

void initial_pos() {
//    add_circle(25, 1, 0, 0, 0, 0);
//    add_circle(25, 1, 0, 200, 0, 0);
//    add_circle(25, 1, 0, -200, 0, 0);
//    add_circle(25, 1, 200, 000, 0, 0);
//    add_circle(25, 1, -200, 0, 0, 0);
}

int main()
{
    int WIDTH, HEIGHT;

    FILE* f_i = fopen("fp_ser_eng", "r");
    FILE* f_o = fopen("fp_eng_ser", "w");
    char *s = calloc(sizeof(char), 256);
    char cmd[16];
    printf("Starting!\n");
    fflush(stdin);
    while (1)
    {
        fscanf(f_i, "%s", s);
        if (strcmp(s, "init") == 0)
        {
            fscanf(f_i, "%d %d\n", &WIDTH, &HEIGHT);
            printf("%d, %d\n", WIDTH, HEIGHT);
            fflush(stdout);
            set_borders(-WIDTH/2,-HEIGHT/2, WIDTH/2, HEIGHT/2);
            free_all();
            init();
            initial_pos();
            continue;
        }
        if (strcmp(s, "begin") == 0)
        {
            fscanf(f_i, "%s", s);
            if (strcmp(s, "exit") == 0) {
                printf("Finished.\n");
                fflush(stdout);
                return 0;
            }
            if (strncmp(s, "player", 6) == 0)
            {
                add_circle(25, 1, -200, 0, 0, 0);
            }

            while (strcmp(s, "end") != 0)
            {
                if (strcmp(s, "ADD") == 0)
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
                        circles[id]->r += val;
                    if (strcmp(cmd, "m") == 0)
                        circles[id]->m += val;
                    if (strcmp(cmd, "X") == 0)
                        circles[id]->vx += val;
                    if (strcmp(cmd, "Y") == 0)
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
                if (strcmp(s, "SET") == 0)
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
                        circles[id]->vx = val;
                    if (strcmp(cmd, "Y") == 0)
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

                fscanf(f_i, "%s", s);
            }
            step(TICK);
            for (int i = 0; i < circles_count; i++)
            {
                fprintf(f_o, "%d %lf %lf %lf %lf %lf %lf,", circles[i]->id, circles[i]->r, circles[i]->m, circles[i]->x, circles[i]->y, circles[i]->vx, circles[i]->vy);
            }
            fprintf(f_o, ";");
            fprintf(f_o, "0 -500 -500 -500 500,");
            fprintf(f_o, "1 -500 -500 500 -500,");
            fprintf(f_o, "2 500 500 500 -500,");
            fprintf(f_o, "3 500 500 -500 500");
            fprintf(f_o, "\n");
            fflush(f_o);
            //printf("END\n");
        }
    }
    fclose(f_i);
    fclose(f_o);
}