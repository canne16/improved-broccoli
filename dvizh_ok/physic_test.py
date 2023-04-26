#!/usr/bin/python3
import ctypes
from random import randint

dvizh_ok = ctypes.cdll.LoadLibrary("./dvizh_ok.so")

#dvizh_ok.add_circle(double r, double m, double x, double y, double vx, double vy)
dvizh_ok.init()

#dvizh_ok.add_circle(ctypes.c_double(20), ctypes.c_double(randint(-10, 20)), ctypes.c_double(500 + randint(-200, 200)), ctypes.c_double(250 + randint(-100, 100)), ctypes.c_double(randint(-25, 25)), ctypes.c_double(randint(-25, 25)))
#dvizh_ok.add_circle(ctypes.c_double(20), ctypes.c_double(randint(-10, 20)), ctypes.c_double(500 + randint(-200, 200)), ctypes.c_double(250 + randint(-100, 100)), ctypes.c_double(randint(-25, 25)), ctypes.c_double(randint(-25, 25)))
#dvizh_ok.add_circle(ctypes.c_double(20), ctypes.c_double(randint(-10, 20)), ctypes.c_double(500 + randint(-200, 200)), ctypes.c_double(250 + randint(-100, 100)), ctypes.c_double(randint(-25, 25)), ctypes.c_double(randint(-25, 25)))
#dvizh_ok.add_circle(ctypes.c_double(20), ctypes.c_double(randint(-10, 20)), ctypes.c_double(500 + randint(-200, 200)), ctypes.c_double(250 + randint(-100, 100)), ctypes.c_double(randint(-25, 25)), ctypes.c_double(randint(-25, 25)))
#dvizh_ok.add_circle(ctypes.c_double(20), ctypes.c_double(randint(-10, 20)), ctypes.c_double(500 + randint(-200, 200)), ctypes.c_double(250 + randint(-100, 100)), ctypes.c_double(randint(-25, 25)), ctypes.c_double(randint(-25, 25)))
#dvizh_ok.add_circle(ctypes.c_double(20), ctypes.c_double(randint(-10, 20)), ctypes.c_double(500 + randint(-200, 200)), ctypes.c_double(250 + randint(-100, 100)), ctypes.c_double(randint(-25, 25)), ctypes.c_double(randint(-25, 25)))
#dvizh_ok.add_circle(ctypes.c_double(50), ctypes.c_double(randint(-10, 20)), ctypes.c_double(500 + randint(-200, 200)), ctypes.c_double(250 + randint(-100, 100)), ctypes.c_double(randint(-25, 25)), ctypes.c_double(randint(-25, 25)))
#dvizh_ok.add_circle(ctypes.c_double(50), ctypes.c_double(randint(-10, 20)), ctypes.c_double(500 + randint(-200, 200)), ctypes.c_double(250 + randint(-100, 100)), ctypes.c_double(randint(-25, 25)), ctypes.c_double(randint(-25, 25)))
#dvizh_ok.add_circle(ctypes.c_double(50), ctypes.c_double(randint(-10, 20)), ctypes.c_double(500 + randint(-200, 200)), ctypes.c_double(250 + randint(-100, 100)), ctypes.c_double(randint(-25, 25)), ctypes.c_double(randint(-25, 25)))
#dvizh_ok.add_circle(ctypes.c_double(50), ctypes.c_double(randint(-10, 20)), ctypes.c_double(500 + randint(-200, 200)), ctypes.c_double(250 + randint(-100, 100)), ctypes.c_double(randint(-25, 25)), ctypes.c_double(randint(-25, 25)))
#dvizh_ok.add_circle(ctypes.c_double(50), ctypes.c_double(randint(-10, 20)), ctypes.c_double(500 + randint(-200, 200)), ctypes.c_double(250 + randint(-100, 100)), ctypes.c_double(randint(-25, 25)), ctypes.c_double(randint(-25, 25)))
#dvizh_ok.add_circle(ctypes.c_double(50), ctypes.c_double(randint(-10, 20)), ctypes.c_double(500 + randint(-200, 200)), ctypes.c_double(250 + randint(-100, 100)), ctypes.c_double(randint(-25, 25)), ctypes.c_double(randint(-25, 25)))

dvizh_ok.add_circle(ctypes.c_double(30), ctypes.c_double(25), ctypes.c_double(100), ctypes.c_double(200), ctypes.c_double(50), ctypes.c_double(0))
dvizh_ok.add_circle(ctypes.c_double(30), ctypes.c_double(10), ctypes.c_double(200), ctypes.c_double(220), ctypes.c_double(0), ctypes.c_double(0))

##dvizh_ok.add_circle(ctypes.c_double(10), ctypes.c_double(1), ctypes.c_double(100), ctypes.c_double(100), ctypes.c_double(randint(-2, 2)), ctypes.c_double(randint(-2, 2)))
#
#print("ABOBUS")
#
##print(dvizh_ok.circles)
#dvizh_ok.debug_print()
#
#print("ABOBUS1")
#dvizh_ok.del_circle(1)
#dvizh_ok.del_circle(3)
#
#print("ABOBUS2")
#dvizh_ok.debug_print()


print(ctypes.c_int.in_dll(dvizh_ok, "circles_count").value)

#double r;
#double m;
#double x;
#double y;
#double vx;
#double vy;

dvizh_ok.is_null.restype = ctypes.c_int
dvizh_ok.get_r.restype = ctypes.c_double
dvizh_ok.get_m.restype = ctypes.c_double
dvizh_ok.get_x.restype = ctypes.c_double
dvizh_ok.get_y.restype = ctypes.c_double
dvizh_ok.get_vx.restype = ctypes.c_double
dvizh_ok.get_vy.restype = ctypes.c_double

for i in range(ctypes.c_int.in_dll(dvizh_ok, "circles_count").value):
    if dvizh_ok.is_null(ctypes.c_int(i)) == 1:
        continue
    
    print(f"r:  {ctypes.c_double(dvizh_ok.get_r (ctypes.c_int(i))).value}")
    print(f"m:  {ctypes.c_double(dvizh_ok.get_m (ctypes.c_int(i))).value}")
    print(f"x:  {ctypes.c_double(dvizh_ok.get_x (ctypes.c_int(i))).value}")
    print(f"y:  {ctypes.c_double(dvizh_ok.get_y (ctypes.c_int(i))).value}")
    print(f"vx: {ctypes.c_double(dvizh_ok.get_vx(ctypes.c_int(i))).value}")
    print(f"vy: {ctypes.c_double(dvizh_ok.get_vy(ctypes.c_int(i))).value}")
    print("ABOBA")

##### GUI

import pygame

##########################################################################
WIDTH = 1000  # ширина игрового окна
HEIGHT = 500 # высота игрового окна
FPS = 60 # частота кадров в секунду
TPS = 10 


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

COLORS = [RED, GREEN, BLUE]

##########################################################################

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

###########################################################################

running = True
frame_counter = 0
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()


    screen.fill(WHITE)

    for i in range(ctypes.c_int.in_dll(dvizh_ok, "circles_count").value):
        if dvizh_ok.is_null(ctypes.c_int(i)) == 1:
            continue
    
        #print(f"r:  {ctypes.c_double(dvizh_ok.get_r (ctypes.c_int(i))).value}")
        #print(f"m:  {ctypes.c_double(dvizh_ok.get_m (ctypes.c_int(i))).value}")
        #print(f"x:  {ctypes.c_double(dvizh_ok.get_x (ctypes.c_int(i))).value}")
        #print(f"y:  {ctypes.c_double(dvizh_ok.get_y (ctypes.c_int(i))).value}")
        print(f"vx: {ctypes.c_double(dvizh_ok.get_vx(ctypes.c_int(i))).value}")
        print(f"vy: {ctypes.c_double(dvizh_ok.get_vy(ctypes.c_int(i))).value}")

        #x = ctypes.c_double(dvizh_ok.get_x(ctypes.c_int(i))).value + ctypes.c_double(dvizh_ok.get_vx(ctypes.c_int(i))).value * (frame_counter % (FPS / TPS)) / FPS
        #y = ctypes.c_double(dvizh_ok.get_y(ctypes.c_int(i))).value + ctypes.c_double(dvizh_ok.get_vy(ctypes.c_int(i))).value * (frame_counter % (FPS / TPS)) / FPS
        x = ctypes.c_double(dvizh_ok.get_x(ctypes.c_int(i))).value
        y = ctypes.c_double(dvizh_ok.get_y(ctypes.c_int(i))).value
        r = ctypes.c_double(dvizh_ok.get_r(ctypes.c_int(i))).value

        pygame.draw.circle(screen, COLORS[i % len(COLORS)], [x, y], r, 5)

    pygame.display.flip()

    #if frame_counter % (FPS // TPS) == 0:
    #    dvizh_ok.step(ctypes.c_double(1/TPS))
    #frame_counter += 1
    dvizh_ok.step(ctypes.c_double(1/FPS))

pygame.quit()