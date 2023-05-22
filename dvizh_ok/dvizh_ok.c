#include <stdlib.h>
#include <time.h>
#include <math.h>

#define DEBUG

#ifdef DEBUG
    #include <stdio.h>
#endif

#define EPS 1e-5

unsigned int circles_size = 4;
unsigned int sections_size = 4;
int border_id = -1;
struct timespec time_prev;

typedef struct _Circle {
    unsigned int id;
    double r;
    double m;
    double x;
    double y;
    double vx;
    double vy;
    double ax;
    double ay;
} Circle;

typedef struct _Section {
    unsigned int id;
    double x1;
    double y1;
    double x2;
    double y2;
} Section;


Circle** circles;
Section** sections;
unsigned int circles_count = 0;
unsigned int sections_count = 0;

int init()
{
    circles = calloc(circles_size, sizeof(Circle*));
    sections = calloc(sections_size, sizeof(Section*));
    return 0;
}

int add_circle(double r, double m, double x, double y, double vx, double vy)
{
    Circle* circle = calloc(1, sizeof(Circle));
    *circle = (Circle){circles_count, r, m, x, y, vx, vy};
    if (circles_size == circles_count + 1)
    {
        circles_size *= 2;
        circles = realloc(circles, sizeof(Circle*) * circles_size);
    }
    circles[circles_count++] = circle;
    fflush(stdout);
    return circles_count;
} 

int del_circle(int id)
{
    free(circles[id]);
    circles[id] = NULL;
}

int add_section(double x1, double y1, double x2, double y2)
{
    Section* section = calloc(1, sizeof(Section));
    *section = (Section){sections_count, x1, y1, x2, y2};

    if (sections_size == sections_count + 1)
    {
        sections_size *= 2;
        sections = realloc(sections, sizeof(Circle*) * sections_size);
    }

    sections[sections_count++] = section;
    return sections_count;
}

int del_section(int id)
{
    free(sections[id]);
    sections[id] = NULL;
}

void set_borders(double x1, double y1, double x2, double y2)
{
    if (border_id != -1)
    {
        for (int i = 0; i < 4; i++)
        del_section(border_id + i);
    }
    fflush(stdout);
    border_id = add_section(x1, y1, x2, y1);
    add_section(x1, y1, x1, y2);
    add_section(x2, y2, x2, y1);
    add_section(x2, y2, x1, y2);
    fflush(stdout);
}

void step(double delta_max)
{
    if (delta_max <= 0)
        return;

    double dt_min = delta_max, dt = delta_max;
    int i_min = -1, j_min = -1;
    int type = -1; // -1 - undefined, 1 - circles+circles, 2 - circle+section, 3 - circle+section_end1, 4-circle+section_end2
    

    for (int i = 0; i < circles_count; i++)
    {
        if (circles[i] == NULL)
            continue;

        if((circles[i]->vx*circles[i]->ax >= 0 && abs(circles[i]->vx) < 0.4) || circles[i]->vx*circles[i]->ax < 0)    
            circles[i]->vx += circles[i]->ax;
        if((circles[i]->vy*circles[i]->ay >= 0 && abs(circles[i]->vy) < 0.4) || circles[i]->vy*circles[i]->ay < 0)    
            circles[i]->vy += circles[i]->ay;

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

            dt = -(delta_vx * delta_x + delta_vy * delta_y + sqrt(D)) / (delta_vx * delta_vx + delta_vy * delta_vy);

            if (dt < -EPS)
                continue;

            if (dt_min > dt)
            {
                dt_min = dt;
                i_min = i;
                j_min = j;
                type = 1;
            }
        }
    }

    for (int i = 0; i < circles_count; i++)
    {
        if (circles[i] == NULL)
            continue;
        for (int j = 0; j < sections_count; j++)
        {
            if (sections[j] == NULL)
                continue;

            double nx = -(sections[j]->y1 - sections[j]->y2);
            double ny = +(sections[j]->x1 - sections[j]->x2);
            double l = sqrt(nx * nx + ny * ny);
            nx /= l;
            ny /= l;

            double d = (circles[i]->x - sections[j]->x1) * nx + (circles[i]->y - sections[j]->y1) * ny;


            if (circles[i]->r <= fabs(d))
            {
                if (d < 0)
                {
                    d += circles[i]->r;
                    if (circles[i]->vx * nx + circles[i]->vy * ny < 0)
                        continue;
                }
                else
                {
                    d -= circles[i]->r;
                    if (circles[i]->vx * nx + circles[i]->vy * ny > 0)
                        continue;
                }

                dt = d / (circles[i]->vx * nx + circles[i]->vy * ny);
                if (dt >= dt_min || dt <= -dt_min)
                {
                    continue;
                }
                
                //printf("nx: %lf, ny: %lf, dt: %lf, d: %lf\n", nx, ny, dt, d);

                double touch_x, touch_y;

                if (circles[i]->vx * nx + circles[i]->vy * ny >= 0)
                {
                    touch_x = circles[i]->x - circles[i]->vx * dt + circles[i]->r * nx;
                    touch_y = circles[i]->y - circles[i]->vy * dt + circles[i]->r * ny;
                }
                if (circles[i]->vx * nx + circles[i]->vy * ny < 0)
                {
                    touch_x = circles[i]->x - circles[i]->vx * dt - circles[i]->r * nx;
                    touch_y = circles[i]->y - circles[i]->vy * dt - circles[i]->r * ny;
                }

                double delta_x = sections[j]->x1 - sections[j]->x2;
                double delta_y = sections[j]->y1 - sections[j]->y2;
                double a = sqrt(delta_x * delta_x + delta_y * delta_y);
                double b = sqrt((sections[j]->x1 - touch_x) * (sections[j]->x1 - touch_x) + (sections[j]->y1 - touch_y) * (sections[j]->y1 - touch_y));
                double c = sqrt((sections[j]->x2 - touch_x) * (sections[j]->x2 - touch_x) + (sections[j]->y2 - touch_y) * (sections[j]->y2 - touch_y));

                //printf("a: %lf, b: %lf, c: %lf, tx: %lf, ty: %lf\n", a, b, c, touch_x, touch_y);

                if (a < b + c - EPS)
                    continue;

                dt = fabs(dt);

                if (dt_min > dt)
                {
                    dt_min = dt;
                    i_min = i;
                    j_min = j;
                    type = 2;
                }
            }
        }
    }

    for (int i = 0; i < circles_count; i++)
    {
        if (circles[i] == NULL)
            continue;
        for (int j = 0; j < sections_count; j++)
        {
            double r = circles[i]->r ;

            double delta_x = circles[i]->x - sections[j]->x1;
            double delta_y = circles[i]->y - sections[j]->y1;
            double delta_vx = circles[i]->vx;
            double delta_vy = circles[i]->vy;

            double D = (delta_vx * delta_x + delta_vy * delta_y) * (delta_vx * delta_x + delta_vy * delta_y) - (delta_vx * delta_vx + delta_vy * delta_vy) * (delta_x * delta_x + delta_y * delta_y - r * r);
            
            if (D < 0)
                continue;

            dt = -(delta_vx * delta_x + delta_vy * delta_y + sqrt(D)) / (delta_vx * delta_vx + delta_vy * delta_vy);

            if (dt < -EPS)
                continue;

            if (dt_min > dt)
            {
                dt_min = dt;
                i_min = i;
                j_min = j;
                type = 3;
            }
        }
    }

    for (int i = 0; i < circles_count; i++)
    {
        if (circles[i] == NULL)
            continue;
        for (int j = 0; j < sections_count; j++)
        {
            double r = circles[i]->r ;

            double delta_x = circles[i]->x - sections[j]->x2;
            double delta_y = circles[i]->y - sections[j]->y2;
            double delta_vx = circles[i]->vx;
            double delta_vy = circles[i]->vy;

            double D = (delta_vx * delta_x + delta_vy * delta_y) * (delta_vx * delta_x + delta_vy * delta_y) - (delta_vx * delta_vx + delta_vy * delta_vy) * (delta_x * delta_x + delta_y * delta_y - r * r);
            
            if (D < 0)
                continue;

            dt = -(delta_vx * delta_x + delta_vy * delta_y + sqrt(D)) / (delta_vx * delta_vx + delta_vy * delta_vy);

            if (dt < -EPS)
                continue;

            if (dt_min > dt)
            {
                dt_min = dt;
                i_min = i;
                j_min = j;
                type = 4;
            }
        }
    }

    for (int i = 0; i < circles_count; i++)
    {
        if (circles[i] == NULL)
            continue;
        circles[i]->x += circles[i]->vx * dt_min;
        circles[i]->y += circles[i]->vy * dt_min;
    }

    if (i_min == -1)
        return;
    switch (type)
    {
    case 1:
        double r = circles[i_min]->r + circles[j_min]->r;
        double sin_phi = (circles[j_min]->y - circles[i_min]->y) / r;
        double cos_phi = (circles[j_min]->x - circles[i_min]->x) / r;

        double vn1 = circles[i_min]->vx * cos_phi + circles[i_min]->vy * sin_phi;
        double vn2 = circles[j_min]->vx * cos_phi + circles[j_min]->vy * sin_phi;

        double vt1 = circles[i_min]->vy * cos_phi - circles[i_min]->vx * sin_phi;
        double vt2 = circles[j_min]->vy * cos_phi - circles[j_min]->vx * sin_phi;

        double m1 = circles[i_min]->m;
        double m2 = circles[j_min]->m;

        double a, b, c; // ax^2 + 2bx + c = 0
        a = m1 + m2;
        b = -(m1 * vn1 + m2 * vn2);
        c = vn1 * vn1 * (m1 - m2) + 2 * vn1 * vn2 * m2;

        double vn1_new = (-b - sqrt(b * b - a * c)) / a;
        
        a = m1 + m2;
        b = -(m1 * vn1 + m2 * vn2);
        c = vn2 * vn2 * (m2 - m1) + 2 * vn1 * vn2 * m1;

        double vn2_new = (-b + sqrt(b * b - a * c)) / a;
        
        circles[i_min]->vx = vn1_new * cos_phi - vt1 * sin_phi;
        circles[i_min]->vy = vn1_new * sin_phi + vt1 * cos_phi;
        circles[j_min]->vx = vn2_new * cos_phi - vt2 * sin_phi;
        circles[j_min]->vy = vn2_new * sin_phi + vt2 * cos_phi;
        break;
    case 2:
        {
            double nx = +(sections[j_min]->y1 - sections[j_min]->y2);
            double ny = -(sections[j_min]->x1 - sections[j_min]->x2);
            double l = sqrt(nx * nx + ny * ny);
            nx /= l;
            ny /= l;

            double alpha = circles[i_min]->vx * nx + circles[i_min]->vy * ny;
            
            circles[i_min]->vx -= 2 * nx * alpha;
            circles[i_min]->vy -= 2 * ny * alpha;
        }
        break;
    case 3:
        {
            double r = circles[i_min]->r;
            double sin_phi = (sections[j_min]->y1 - circles[i_min]->y) / r;
            double cos_phi = (sections[j_min]->x1 - circles[i_min]->x) / r;

            double vx = circles[i_min]->vx;
            double vy = circles[i_min]->vy;

            double alpha = circles[i_min]->vx * cos_phi + circles[i_min]->vy * sin_phi;
            
            circles[i_min]->vx -= 2 * cos_phi * alpha;
            circles[i_min]->vy -= 2 * sin_phi * alpha;
        }
        break;
    case 4:
        {
            double r = circles[i_min]->r;
            double sin_phi = (sections[j_min]->y2 - circles[i_min]->y) / r;
            double cos_phi = (sections[j_min]->x2 - circles[i_min]->x) / r;

            double vx = circles[i_min]->vx;
            double vy = circles[i_min]->vy;

            double alpha = circles[i_min]->vx * cos_phi + circles[i_min]->vy * sin_phi;
            
            circles[i_min]->vx -= 2 * cos_phi * alpha;
            circles[i_min]->vy -= 2 * sin_phi * alpha;
        }
        break;
    default:
        break;
    }
    if (delta_max == dt_min)
        return;
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

int is_null_circle(int i)
{
    return circles[i] == NULL;
}

int is_null_section(int i)
{
    return sections[i] == NULL;
}

double get_circle_r(int i)
{
    return circles[i]->r;
}

double get_circle_m(int i)
{
    return circles[i]->m;
}

double get_circle_x(int i)
{
    return circles[i]->x;
}

double get_circle_y(int i)
{
    return circles[i]->y;
}

double get_circle_vx(int i)
{
    return circles[i]->vx;
}

double get_circle_vy(int i)
{
    return circles[i]->vy;
}

double get_section_x1(int i)
{
    return sections[i]->x1;
}

double get_section_y1(int i)
{
    return sections[i]->y1;
}

double get_section_x2(int i)
{
    return sections[i]->x2;
}

double get_section_y2(int i)
{
    return sections[i]->y2;
}

#endif