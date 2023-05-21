#!venv/bin/python3
import ctypes
import math
from random import randint
import argparse
import pygame

SHOW_FPS = True
WIDTH = 1920 // 2
HEIGHT = 1080 // 2
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

dvizh_ok = ctypes.cdll.LoadLibrary("./dvizh_ok_new.so")
dvizh_ok.add_circle.argtypes = [ctypes.c_double] * 6
dvizh_ok.add_section.argtypes = [ctypes.c_double] * 4

dvizh_ok.init()
#dvizh_ok.set_borders(0, 0, WIDTH, HEIGHT)

mode = 0
parser = argparse.ArgumentParser(
                    prog="Physic demonstration",
                    description="Demonstration of physic engine written by vlad_cool for MIPT project")

parser.add_argument("-m", "--mode", type=int, default=0,
                    help="MODES: Not available")

args = parser.parse_args()
mode = args.mode

match mode:
    case 0:
        TIME_K = 20
        dvizh_ok.add_circle(200, 200, 700, HEIGHT / 2, -20, 0)
        #dvizh_ok.add_section(100, 100, 200, 200)
        #dvizh_ok.add_section(0, 0, HEIGHT, HEIGHT)
        #dvizh_ok.add_section(200, 0, 0, HEIGHT)
        dvizh_ok.add_section(200, 0, 200, HEIGHT / 2 - 1)
        #dvizh_ok.add_section(0, HEIGHT, 200, 0)
        #dvizh_ok.add_section(0, 0, 1000, 1000)
        #dvizh_ok.add_section(0, 0, 1000, 1000)
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
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
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