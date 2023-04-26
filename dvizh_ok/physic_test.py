#!/usr/bin/python3
import ctypes
import math
from random import randint

WIDTH = 1600 # ширина игрового поля
HEIGHT = 900 # высота игрового поля
TIME_K = 10
MICROSTEPS = 1

dvizh_ok = ctypes.cdll.LoadLibrary("./dvizh_ok.so")

dvizh_ok.init()
dvizh_ok.set_borders(ctypes.c_double(0), ctypes.c_double(0), ctypes.c_double(WIDTH), ctypes.c_double(HEIGHT))

#for i in range(16):
#    dvizh_ok.add_circle(ctypes.c_double(randint(10, 50)), ctypes.c_double(1), ctypes.c_double(500 + randint(-200, 200)), ctypes.c_double(250 + randint(-100, 100)), ctypes.c_double(randint(-50, 50)), ctypes.c_double(randint(-50, 50)))

# Броумовское движение
for i in range(512):
    #dvizh_ok.add_circle(ctypes.c_double(2), ctypes.c_double(1), ctypes.c_double(500 + randint(-200, 200)), ctypes.c_double(250 + randint(-100, 100)), ctypes.c_double(randint(-50, 50)), ctypes.c_double(randint(-50, 50)))
    #dvizh_ok.add_circle(ctypes.c_double(2), ctypes.c_double(1), ctypes.c_double(WIDTH / 2), ctypes.c_double(HEIGHT / 2), ctypes.c_double(randint(-50, 50)), ctypes.c_double(randint(-50, 50)))
    v = randint(100, 300)
    phi = randint(0, 2000000) / 1000000
    dvizh_ok.add_circle(ctypes.c_double(2), ctypes.c_double(1), ctypes.c_double(WIDTH / 2), ctypes.c_double(HEIGHT / 2), ctypes.c_double(v * math.sin(math.pi * phi)), ctypes.c_double(v * math.cos(math.pi * phi)))

dvizh_ok.add_circle(ctypes.c_double(200), ctypes.c_double(200), ctypes.c_double(WIDTH / 2), ctypes.c_double(HEIGHT / 2), ctypes.c_double(0), ctypes.c_double(0))

dvizh_ok.is_null.restype = ctypes.c_int
dvizh_ok.get_r.restype = ctypes.c_double
dvizh_ok.get_m.restype = ctypes.c_double
dvizh_ok.get_x.restype = ctypes.c_double
dvizh_ok.get_y.restype = ctypes.c_double
dvizh_ok.get_vx.restype = ctypes.c_double
dvizh_ok.get_vy.restype = ctypes.c_double

##### GUI

import pygame
FPS = 60 # частота кадров в секунду
TPS = 10 # Ticks per second, not implemented yet, using FPS instead

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

COLORS = [RED, GREEN, BLUE]

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

class FPSCounter:
    def __init__(self, surface, font, clock, color, pos):
        self.surface = surface
        self.font = font
        self.clock = clock
        self.pos = pos
        self.color = color

        self.fps_text = self.font.render(str(int(self.clock.get_fps())) + "FPS", False, self.color)
        self.fps_text_rect = self.fps_text.get_rect(center=(self.pos[0], self.pos[1]))

    def render(self):
        self.surface.blit(self.fps_text, self.fps_text_rect)

    def update(self):
        text = f"{self.clock.get_fps():2.0f} FPS"
        self.fps_text = self.font.render(text, False, self.color)
        self.fps_text_rect = self.fps_text.get_rect(center=(self.pos[0], self.pos[1]))


fps_counter = FPSCounter(screen, font, clock, BLACK, (150, 10))
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

        x = ctypes.c_double(dvizh_ok.get_x(ctypes.c_int(i))).value
        y = ctypes.c_double(dvizh_ok.get_y(ctypes.c_int(i))).value
        r = ctypes.c_double(dvizh_ok.get_r(ctypes.c_int(i))).value

        pygame.draw.circle(screen, COLORS[i % len(COLORS)], [x, y], r, 3)

    fps_counter.render()
    fps_counter.update()
    pygame.display.flip()

    for i in range(MICROSTEPS):
        dvizh_ok.step(ctypes.c_double(TIME_K/MICROSTEPS/FPS))

pygame.quit()