#!venv/bin/python3
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
#TPS = 10 # Ticks per second, not implemented yet, using FPS instead`
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
dvizh_ok.add_circle.argtypes = [ctypes.c_double] * 6
dvizh_ok.add_section.argtypes = [ctypes.c_double] * 4
dvizh_ok.set_borders.argtypes = [ctypes.c_double] * 4

dvizh_ok.init()
dvizh_ok.set_borders(0, 0, WIDTH, HEIGHT)

mode = 0
parser = argparse.ArgumentParser(
                    prog="Physic demonstration",
                    description="Demonstration of physic engine written by vlad_cool for MIPT project")

parser.add_argument("-m", "--mode", type=int, default=0,
                    help="MODES: 0 - Brownian motion, 1 - Wave, 2 - chaotic, 3 - diffusion")

args = parser.parse_args()
mode = args.mode

match mode:
    case 0: # Brownian motion
        TIME_K = 5
        n = 400
        dvizh_ok.add_circle(200, 200, WIDTH / 2, HEIGHT / 2, 0, 0)

        for i in range(n):
            v = randint(100, 300)
            phi = randint(0, 2000000) / 1000000
            dvizh_ok.add_circle(2, 1, WIDTH / 2, HEIGHT / 2, v * math.sin(math.pi * phi), v * math.cos(math.pi * phi))
    case 1: # wave
        TIME_K = 1
        n = 36
        r = 24
        k = 2 * r
        for i in range(n - 1):
            dvizh_ok.add_circle(r, 1, WIDTH / 2 - n / 2 * k + i * k, HEIGHT / 2, 0, 0)
        dvizh_ok.add_circle(r, 1, WIDTH / 2 - n / 2 * k + n * k, HEIGHT / 2, 200, 0)
    case 2: # chaotic
        TIME_K = 10
        n = 256
        for i in range(n):
            r = randint(3, 30)
            dvizh_ok.add_circle(r, r*r, randint(int(r) + 2, WIDTH - int(r) - 2), randint(int(r) + 2, HEIGHT - int(r) - 2), randint(-50, 50), randint(-50, 50))
        dvizh_ok.add_section(0, HEIGHT / 2, WIDTH, HEIGHT / 2)
    case 3: # diffusion
        TIME_K = 1
        COLORS = [RED, BLUE]
        n_w = 24
        n_h = 16
        r = min(WIDTH // n_w, HEIGHT // n_h) // 2 - 4
        for i in range(n_h):
            for k in range(n_w // 2):
                j = k
                dvizh_ok.add_circle(r, r*r, WIDTH / n_w * (j+0.5), HEIGHT / n_h * (i+0.5), randint(-50, 50), randint(-50, 50))
                j = k + n_w // 2
                dvizh_ok.add_circle(r, r*r, WIDTH / n_w * (j+0.5), HEIGHT / n_h * (i+0.5), randint(-50, 50), randint(-50, 50))
    case 4: # test
        TIME_K = 10
        COLORS = [RED, BLUE]
        dvizh_ok.add_circle(10, 1, 100, 100, 50, 50)
    case _:
        print("Unknowh mode")
        parser.print_help()
        exit(0)

dvizh_ok.is_null_circle.restype = ctypes.c_int
dvizh_ok.get_circle_r.restype = ctypes.c_double
dvizh_ok.get_circle_m.restype = ctypes.c_double
dvizh_ok.get_circle_x.restype = ctypes.c_double
dvizh_ok.get_circle_y.restype = ctypes.c_double
dvizh_ok.get_circle_vx.restype = ctypes.c_double
dvizh_ok.get_circle_vy.restype = ctypes.c_double
dvizh_ok.get_section_x1.restype = ctypes.c_double
dvizh_ok.get_section_y1.restype = ctypes.c_double
dvizh_ok.get_section_x2.restype = ctypes.c_double
dvizh_ok.get_section_y2.restype = ctypes.c_double

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
        if dvizh_ok.is_null_circle(ctypes.c_int(i)) == 1:
            continue

        x = ctypes.c_double(dvizh_ok.get_circle_x(ctypes.c_int(i))).value
        y = ctypes.c_double(dvizh_ok.get_circle_y(ctypes.c_int(i))).value
        r = ctypes.c_double(dvizh_ok.get_circle_r(ctypes.c_int(i))).value

        pygame.draw.circle(screen, COLORS[i % len(COLORS)], [x, y], r, 3)
    
    for i in range(ctypes.c_int.in_dll(dvizh_ok, "sections_count").value):
        if dvizh_ok.is_null_section(ctypes.c_int(i)) == 1:
            continue

        x1 = ctypes.c_double(dvizh_ok.get_section_x1(ctypes.c_int(i))).value
        y1 = ctypes.c_double(dvizh_ok.get_section_y1(ctypes.c_int(i))).value
        x2 = ctypes.c_double(dvizh_ok.get_section_x2(ctypes.c_int(i))).value
        y2 = ctypes.c_double(dvizh_ok.get_section_y2(ctypes.c_int(i))).value
    
        pygame.draw.line(screen, (255, 255, 255), [x1, y1], [x2, y2])
    
    if SHOW_FPS:
        fps_counter.render()
        fps_counter.update()
    pygame.display.flip()

    for i in range(MICROSTEPS):
        dvizh_ok.step(ctypes.c_double(TIME_K/MICROSTEPS/FPS))

pygame.quit()