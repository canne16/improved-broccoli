#!/usr/bin/python3
import ctypes
import math
from random import randint
import argparse
import pygame

SHOW_FPS = True
WIDTH = 1920
HEIGHT = 1080
MICROSTEPS = 1 # 1-10 best values, 1 is the best

FPS = 60 # Frames per second
TPS = 10 # Ticks per second, not implemented yet, using FPS instead`
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
C1 = (0, 255, 255)
C2 = (255, 0, 255)
YELLOW = (255, 255, 0)

COLORS = []
for i in range(36):
    color = pygame.Color(0)
    color.hsva = (i * 10, 100, 100, 100)
    COLORS.append(color)

dvizh_ok = ctypes.cdll.LoadLibrary("./dvizh_ok.so")

dvizh_ok.init()
dvizh_ok.set_borders(ctypes.c_double(0), ctypes.c_double(0), ctypes.c_double(WIDTH), ctypes.c_double(HEIGHT))

mode = 0
parser = argparse.ArgumentParser(
                    prog="Physic demonstration",
                    description="Demonstration of physic engine written by vlad_cool for MIPT project")
#parser.add_argument("-m", "--mode")      # option that takes a value

#parser.add_argument("-m", "--mode", dest="accumulate", action="store_const",
#                    const=mode, default=0,
#                    help="Modes, from 0 to 4")
parser.add_argument("-m", "--mode", type=int,
                    help="Modes, from 0 to 4")

args = parser.parse_args()
mode = args.mode

if mode == 0: # Броумовское движение
    TIME_K = 5
    dvizh_ok.add_circle(ctypes.c_double(200), ctypes.c_double(200), ctypes.c_double(WIDTH / 2), ctypes.c_double(HEIGHT / 2), ctypes.c_double(0), ctypes.c_double(0))

    for i in range(400):
        v = randint(100, 300)
        phi = randint(0, 2000000) / 1000000
        dvizh_ok.add_circle(ctypes.c_double(2), ctypes.c_double(1), ctypes.c_double(WIDTH / 2), ctypes.c_double(HEIGHT / 2), ctypes.c_double(v * math.sin(math.pi * phi)), ctypes.c_double(v * math.cos(math.pi * phi)))
elif mode == 1:
    TIME_K = 1
    n = 36
    for i in range(n - 1):
        dvizh_ok.add_circle(ctypes.c_double(16), ctypes.c_double(1), ctypes.c_double(WIDTH / 2 - n / 2 * 50 + i * 50), ctypes.c_double(HEIGHT / 2), ctypes.c_double(0), ctypes.c_double(0))
    dvizh_ok.add_circle(ctypes.c_double(16), ctypes.c_double(1), ctypes.c_double(WIDTH / 2 - n / 2 * 50 + n * 50), ctypes.c_double(HEIGHT / 2), ctypes.c_double(256), ctypes.c_double(0))
elif mode == 2:
    TIME_K = 10
    for i in range(256):
        r = randint(3, 30)
        dvizh_ok.add_circle(ctypes.c_double(r), ctypes.c_double(r*r), ctypes.c_double(randint(int(r) + 2, WIDTH - int(r) - 2)), ctypes.c_double(randint(int(r) + 2, HEIGHT - int(r) - 2)), ctypes.c_double(randint(-50, 50)), ctypes.c_double(randint(-50, 50)))
elif mode == 3:
    TIME_K = 1
    for i in range(24):
        for j in range(36):
            r = randint(3, 20)
            dvizh_ok.add_circle(ctypes.c_double(r), ctypes.c_double(r*r), ctypes.c_double(WIDTH / 36 * (j+0.5)), ctypes.c_double(HEIGHT / 24 * (i+0.5)), ctypes.c_double(randint(-5, 5)), ctypes.c_double(randint(-5, 5)))
elif mode == 4:
    TIME_K = 1
    COLORS = [RED, BLUE]
    for i in range(24):
        for k in range(18):
            j = k
            r = 15
            #r = randint(3, 20)
            dvizh_ok.add_circle(ctypes.c_double(r), ctypes.c_double(r*r), ctypes.c_double(WIDTH / 36 * (j+0.5)), ctypes.c_double(HEIGHT / 24 * (i+0.5)), ctypes.c_double(randint(-5, 5)), ctypes.c_double(randint(-5, 5)))

            j = k + 18
            #r = randint(3, 20)
            dvizh_ok.add_circle(ctypes.c_double(r), ctypes.c_double(r*r), ctypes.c_double(WIDTH / 36 * (j+0.5)), ctypes.c_double(HEIGHT / 24 * (i+0.5)), ctypes.c_double(randint(-5, 5)), ctypes.c_double(randint(-5, 5)))

dvizh_ok.is_null.restype = ctypes.c_int
dvizh_ok.get_r.restype = ctypes.c_double
dvizh_ok.get_m.restype = ctypes.c_double
dvizh_ok.get_x.restype = ctypes.c_double
dvizh_ok.get_y.restype = ctypes.c_double
dvizh_ok.get_vx.restype = ctypes.c_double
dvizh_ok.get_vy.restype = ctypes.c_double

##### GUI

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
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

fps_counter = FPSCounter(screen, font, clock, C2, (150, 10))
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
                exit(0)

    screen.fill(BLACK)

    for i in range(ctypes.c_int.in_dll(dvizh_ok, "circles_count").value):
        if dvizh_ok.is_null(ctypes.c_int(i)) == 1:
            continue

        x = ctypes.c_double(dvizh_ok.get_x(ctypes.c_int(i))).value
        y = ctypes.c_double(dvizh_ok.get_y(ctypes.c_int(i))).value
        r = ctypes.c_double(dvizh_ok.get_r(ctypes.c_int(i))).value

        pygame.draw.circle(screen, COLORS[i % len(COLORS)], [x, y], r, 3)
    
    if SHOW_FPS:
        fps_counter.render()
        fps_counter.update()
    pygame.display.flip()

    for i in range(MICROSTEPS):
        dvizh_ok.step(ctypes.c_double(TIME_K/MICROSTEPS/FPS))

pygame.quit()