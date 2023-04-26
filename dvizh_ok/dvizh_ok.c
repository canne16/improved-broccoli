#include <stdlib.h>
#include <time.h>
#include <math.h>

#define DEBUG

#ifdef DEBUG
    #include <stdio.h>
#endif

const unsigned long long tick = 100; // tick duration in milliseconds

unsigned int circles_size = 4;
unsigned int polygons_size = 4;
struct timespec time_prev;

typedef struct _Circle {
    unsigned int id;
    double r;
    double m;
    double x;
    double y;
    double vx;
    double vy;
} Circle;

typedef struct _Polygon {
    unsigned int id;
} Polygon;


Circle** circles;
Polygon** polygons;
unsigned int circles_count = 0;
unsigned int polygons_count = 0;

int init()
{
    circles = calloc(circles_size, sizeof(Circle*));
    polygons = calloc(polygons_size, sizeof(Polygon*));
    return 0;
}

// Returns id of new circle
// Rewrite to optimize memory: scan for null_ptrs
int add_circle(double r, double m, double x, double y, double vx, double vy)
{
    #ifdef DEBUG
        printf("---\nr: %lf\nm: %lf\nx: %lf\ny: %lf\nvx: %lf\nvy: %lf\n---\n", r, m, x, y, vx, vy);
    #endif
    Circle* circle = calloc(1, sizeof(Circle));
    *circle = (Circle){circles_count, r, m, x, y, vx, vy};

    if (circles_size == circles_count + 1)
    {
        circles_size *= 2;
        circles = realloc(circles, sizeof(Circle*) * circles_size);
    }

    circles[circles_count++] = circle;
    return circles_count;
}

int del_circle(int id)
{
    free(circles[id]);
    circles[id] = 0;
}

void step(double delta_max)
{
    if (delta_max <= 0)
        return;

    double dt_min = delta_max;
    int i_min = -1, j_min = -1;

    printf("Finding \"nearest\" circles\n");

    for (int i = 0; i < circles_count; i++)
    {
        if (circles[i] == NULL)
            continue;
        for (int j = i + 1; j < circles_count; j++)
        {
            if (circles[j] == NULL)
                continue;

            double r = circles[i]->r + circles[j]->r;

            double delta_x = circles[i]->x - circles[j]->x;
            double delta_y = circles[i]->y - circles[j]->y;
            double delta_vx = circles[i]->vx - circles[j]->vx;
            double delta_vy = circles[i]->vy - circles[j]->vy;

            double D = (delta_vx * delta_x + delta_vy * delta_y) * (delta_vx * delta_x + delta_vy * delta_y) - (delta_vx * delta_vx + delta_vy * delta_vy) * (delta_x * delta_x + delta_y * delta_y - r * r);
            
            if (D < 0)
                continue;

            double dt = -(delta_vx * delta_x + delta_vy * delta_y + sqrt(D)) / (delta_vx * delta_vx + delta_vy * delta_vy);

            printf("dt: %lf\n", dt);

            if (dt < 0)
                continue;

            if (dt_min > dt)
            {
                dt_min = dt;
                i_min = i;
                j_min = j;
            }
        }
    }

    printf("circles %d, %d finded, moving circles\n", i_min, j_min);

    for (int i = 0; i < circles_count; i++)
    {
        if (circles[i] == NULL)
            continue;
        circles[i]->x += circles[i]->vx * dt_min;
        circles[i]->y += circles[i]->vy * dt_min;
    }

    if (i_min == -1)
        return;

    printf("Counting impulses\n");

    printf("Step 1\n");
    fflush(stdin);

    double r = circles[i_min]->r + circles[j_min]->r;
    double sin_phi = (circles[j_min]->y - circles[i_min]->y) / r;
    double cos_phi = (circles[j_min]->x - circles[i_min]->x) / r;

    double vn1 = circles[i_min]->vx * cos_phi + circles[i_min]->vy * sin_phi;
    double vn2 = circles[j_min]->vx * cos_phi + circles[j_min]->vy * sin_phi;

    double vt1 = circles[i_min]->vy * cos_phi - circles[i_min]->vx * sin_phi;
    double vt2 = circles[j_min]->vy * cos_phi - circles[j_min]->vx * sin_phi;

    double m1 = circles[i_min]->m;
    double m2 = circles[j_min]->m;
    
    printf("Step 2.1\n");
    fflush(stdin);

    double a, b, c; // ax^2 + 2bx + c = 0
    a = m1 + m2;
    b = -(m1 * vn1 + m2 * vn2);
    c = vn1 * vn1 * (m1 - m2) + 2 * vn1 * vn2 * m2;

    printf("Step 2.2\n");
    fflush(stdin);

    double vn1_new = (-b - sqrt(b * b - a * c)) / a;
    
    printf("Step 3.1\n");
    fflush(stdin);

    a = m1 + m2;
    b = -(m1 * vn1 + m2 * vn2);
    c = vn2 * vn2 * (m2 - m1) + 2 * vn1 * vn2 * m1;

    printf("Step 3.2\n");
    fflush(stdin);

    double vn2_new = (-b + sqrt(b * b - a * c)) / a;
    
    printf("Step 4\n");
    fflush(stdin);

    circles[i_min]->vx = vn1_new * cos_phi - vt1 * sin_phi;
    circles[i_min]->vy = vn1_new * sin_phi + vt1 * cos_phi;
    circles[j_min]->vx = vn2_new * cos_phi - vt2 * sin_phi;
    circles[j_min]->vy = vn2_new * sin_phi + vt2 * cos_phi;

    step(delta_max - dt_min);
}

void free_all()
{
    for (int i = 0; i < circles_count; i++)
    {
        free(circles[i]);
    }
    free(circles);
}

#ifdef DEBUG
void debug_print()
{
    for (int i = 0; i < circles_count; i++)
    {
        if (circles[i] == NULL)
            continue;
        printf("---\nr: %lf\nm: %lf\nx: %lf\ny: %lf\nvx: %lf\nvy: %lf\n---\n", circles[i]->r, circles[i]->m, circles[i]->x, circles[i]->y, circles[i]->vx, circles[i]->vy);
    }
}

/*
double r;
double m;
double x;
double y;
double vx;
double vy;
*/

int is_null(int i)
{
    return circles[i] == NULL;
}

double get_r(int i)
{
    return circles[i]->r;
}

double get_m(int i)
{
    return circles[i]->m;
}

double get_x(int i)
{
    return circles[i]->x;
}

double get_y(int i)
{
    return circles[i]->y;
}

double get_vx(int i)
{
    return circles[i]->vx;
}

double get_vy(int i)
{
    return circles[i]->vy;
}

#endif