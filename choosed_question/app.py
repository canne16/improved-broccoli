#!/usr/bin/python3

#!venv/bin/python3
import ctypes
import math
from random import randint
import argparse
import pygame
import pygame.freetype
from dvizh_ok_bindings import dvizh_ok, get_circle, get_section

WIDTH = 1920
HEIGHT = 1080

WHITE = (255, 255, 255)
RED = (255, 0, 0)

MICROSTEPS = 1 # 1-10 best values, 1 is the best

FPS = 60 # Frames per second

dvizh_ok.init()

parser = argparse.ArgumentParser(
                    prog="Physic demonstration",
                    description="Demonstration of physic engine written by vlad_cool for MIPT project")

parser.add_argument("-m", "--mode", type=int, default=0,
                    help="MODES: 0 - Random position, const velovity (default), 1 - from center, random angle")
parser.add_argument("-v", "--velocity", type=int, default=256,
                    help="Velocity of particles")
parser.add_argument("-n", "--number", type=int, default=300,
                    help="Number of particles")
parser.add_argument("-p", "--precount", type=int, default=0,
                    help="Number of precount steps")
parser.add_argument("-t", "--time", type=int, default=0,
                    help="Time of experiment in seconds")
parser.add_argument("-s", "--screenshot", action=argparse.BooleanOptionalAction,
                    help="Make screenshot after finishing experiment")
parser.add_argument("-d", "--dump", action=argparse.BooleanOptionalAction,
                    help="Dump result to files agter finishing experimant")
parser.add_argument("-r", "--render", action=argparse.BooleanOptionalAction,
                    help="Render (unlimited framerate)")
parser.add_argument("-f", "--fps", action=argparse.BooleanOptionalAction,
                    help="Show FPS")

args = parser.parse_args()

match args.mode:
    case 0:
        #TIME_K = 5
        TIME_K = 5

        dvizh_ok.add_section(40, 40, 1040, 40)
        dvizh_ok.add_section(40, 40, 40, 1040)
        dvizh_ok.add_section(1040, 1040, 1040, 40)
        dvizh_ok.add_section(1040, 1040, 40, 1040)

        #dvizh_ok.add_circle(2, 100, randint(50, 950), randint(50, 950), 0, 0)
        for i in range(args.number):
            phi = randint(0, 2000000) / 1000000
            dvizh_ok.add_circle(2, 1, randint(50, 950), randint(50, 950), args.velocity * math.sin(math.pi * phi), args.velocity * math.cos(math.pi * phi))
        for i in range(args.precount):
            dvizh_ok.step(TIME_K)
            print(i)
        dvizh_ok.reset_vars()
    case 1:
        #TIME_K = 5
        TIME_K = 5

        dvizh_ok.add_section(40, 40, 1040, 40)
        dvizh_ok.add_section(40, 40, 40, 1040)
        dvizh_ok.add_section(1040, 1040, 1040, 40)
        dvizh_ok.add_section(1040, 1040, 40, 1040)

        #dvizh_ok.add_circle(2, 100, randint(50, 950), randint(50, 950), 0, 0)
        for i in range(args.number):
            phi = randint(0, 2000000) / 1000000
            dvizh_ok.add_circle(2, 1, 540, 540, args.velocity * math.sin(math.pi * phi), args.velocity * math.cos(math.pi * phi))
        for i in range(args.precount):
            dvizh_ok.step(TIME_K)
            print(i)
        dvizh_ok.reset_vars()
    case _:
        print("Unknowh mode")
        parser.print_help()
        exit(0)

##### GUI

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Physic demo")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

GAME_FONT = pygame.freetype.SysFont(None, 24)

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

fps_counter = FPSCounter(screen, font, clock, (200, 200, 200), (150, 10))
running = True
frame_counter = 0

v_sum = 0
sum = 0

vmax = 2000
nvel = [0] * 1600
n_predict = [0] * 1600
vel_disp = 600

def maxwell_exp(v):
    return math.exp(-(v ** 2) / (args.velocity ** 2))

for i in range(1600):
    n_predict[i] = maxwell_exp(vmax / len(n_predict) * (i)) - maxwell_exp(vmax / len(n_predict) * (i + 1))

while running:
    if not args.render:
        clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    if not running:
        continue

    screen.fill((0, 0, 0))

    #circle = get_circle(0)
    #pygame.draw.circle(screen, (255, 255, 245), [circle.x, circle.y], abs(circle.r), 3)
    for i in range(0, ctypes.c_int.in_dll(dvizh_ok, "circles_count").value):
        circle = get_circle(i)
        pygame.draw.circle(screen, RED, [circle.x, circle.y], abs(circle.r), 3)
    
    for i in range(ctypes.c_int.in_dll(dvizh_ok, "sections_count").value):
        section = get_section(i)
        pygame.draw.line(screen, WHITE, [section.x1, section.y1], [section.x2, section.y2])
    
    graph_x1 = 1080
    graph_x2 = 1880
    graph_y1 = 40
    graph_y2 = 520

    pygame.draw.line(screen, WHITE, [graph_x1, graph_y1], [graph_x1, graph_y2])
    pygame.draw.line(screen, WHITE, [graph_x2, graph_y1], [graph_x2, graph_y2])
    pygame.draw.line(screen, WHITE, [graph_x1, graph_y1], [graph_x2, graph_y1])
    pygame.draw.line(screen, WHITE, [graph_x2, graph_y2], [graph_x1, graph_y2])

    GAME_FONT.render_to(screen, (graph_x1, graph_y2 + 4), "0", WHITE)
    GAME_FONT.render_to(screen, ((graph_x1 + graph_x2) / 2 - GAME_FONT.get_rect(str(int(vel_disp / 2))).width / 2, graph_y2 + 4), str(int(vel_disp / 2)), WHITE)
    GAME_FONT.render_to(screen, (graph_x2 - GAME_FONT.get_rect(str(int(vel_disp))).width, graph_y2 + 4), str(int(vel_disp)), WHITE)
    
    nmax = max(n_predict[:vel_disp + 1])
    if nmax > 0:
        for i in range(vel_disp):
            pygame.draw.line(screen, (100, 100, 100), [graph_x1 + i * (graph_x2 - graph_x1) / vel_disp, graph_y2 - (graph_y2 - graph_y1 - 40) * n_predict[i] / nmax], [graph_x1 + (i + 1) * (graph_x2 - graph_x1) / vel_disp, graph_y2 - (graph_y2 - graph_y1 - 40) * n_predict[i] / nmax])
    
    nmax = max(nvel[:vel_disp + 1])
    if nmax > 0:
        for i in range(vel_disp):
            pygame.draw.line(screen, RED, [graph_x1 + i * (graph_x2 - graph_x1) / vel_disp, graph_y2 - (graph_y2 - graph_y1 - 40) * nvel[i] / nmax], [graph_x1 + (i + 1) * (graph_x2 - graph_x1) / vel_disp, graph_y2 - (graph_y2 - graph_y1 - 40) * nvel[i] / nmax])

    pygame.draw.line(screen, WHITE, [graph_x1, 560], [graph_x1, 1040])
    pygame.draw.line(screen, WHITE, [graph_x2, 560], [graph_x2, 1040])
    pygame.draw.line(screen, WHITE, [graph_x1, 560], [graph_x2, 560])
    pygame.draw.line(screen, WHITE, [graph_x2, 1040], [graph_x1, 1040])

    self_collision_count = ctypes.c_uint64.in_dll(dvizh_ok, "self_collision_count").value
    wall_collision_count = ctypes.c_uint64.in_dll(dvizh_ok, "wall_collision_count").value

    if self_collision_count > 0 and wall_collision_count > 0 and frame_counter > 0:
        GAME_FONT.render_to(screen, (graph_x1 + 10, 560 + 10 + 30 * 0), f"n = {args.number}", WHITE)
        GAME_FONT.render_to(screen, (graph_x1 + 10, 560 + 10 + 30 * 1), f"v = {args.velocity}", WHITE)
        GAME_FONT.render_to(screen, (graph_x1 + 10, 560 + 10 + 30 * 2), f"λ = {round(ctypes.c_double.in_dll(dvizh_ok, 'distance').value / (self_collision_count * 2 + wall_collision_count))}", WHITE)
        GAME_FONT.render_to(screen, (graph_x1 + 10, 560 + 10 + 30 * 3), f"λ_0 = {round(ctypes.c_double.in_dll(dvizh_ok, 'distance').value / (self_collision_count * 2))} (без учёта столкновений со стенками)", WHITE)
        GAME_FONT.render_to(screen, (graph_x1 + 10, 560 + 10 + 30 * 4), f"столкновений со стенками за секунду: {round(wall_collision_count * FPS / frame_counter / TIME_K)}", WHITE)
        GAME_FONT.render_to(screen, (graph_x1 + 10, 560 + 10 + 30 * 5), f"столкновений между собой за секунду: {round(self_collision_count * FPS / frame_counter / TIME_K)}", WHITE)
        GAME_FONT.render_to(screen, (graph_x1 + 10, 560 + 10 + 30 * 6), f"время: {frame_counter // FPS}", WHITE)
        GAME_FONT.render_to(screen, (graph_x1 + 10, 560 + 10 + 30 * 7), f"средняя скорость: {round(v_sum / sum)}", WHITE)
        GAME_FONT.render_to(screen, (graph_x1 + 10, 560 + 10 + 30 * 8), f"наиболее вероятная скорость: {round(nvel.index(max(nvel)) / len (nvel) * vmax)}", WHITE)
        GAME_FONT.render_to(screen, (graph_x1 + 10, 560 + 10 + 30 * 9), f"P: {round(ctypes.c_double.in_dll(dvizh_ok, 'p_sum').value * FPS / (4000 * frame_counter / TIME_K))}", WHITE)

    if args.fps:
        fps_counter.render()
        fps_counter.update()
    pygame.display.flip()

    dvizh_ok.step(ctypes.c_double(TIME_K/FPS))

    for i in range(ctypes.c_int.in_dll(dvizh_ok, "circles_count").value):
        circle = get_circle(i)
        vel = math.sqrt(circle.vx ** 2 + circle.vy ** 2)
        k = int(round(vel / vmax * len(nvel)))
        v_sum += vel
        sum += 1
        if k >= len(nvel):
            continue
        nvel[k] += 1


    frame_counter += 1
    if (frame_counter == args.time * FPS):
        break

if args.screenshot:
    pygame.image.save(pygame.display.get_surface(), f"screenshots/res_vel_{args.velocity}_time_{args.time}_n_{args.number}.png")

if args.dump:
    with open(f"results/res_vel_{args.velocity}_time_{args.time}_n_{args.number}", "w") as file:
        file.write(f"n = {args.number}\n")
        file.write(f"v = {args.velocity}\n")
        file.write(f"λ = {ctypes.c_double.in_dll(dvizh_ok, 'distance').value / (self_collision_count * 2 + wall_collision_count)}\n")
        file.write(f"λ_0 = {ctypes.c_double.in_dll(dvizh_ok, 'distance').value / (self_collision_count * 2)} (без учёта столкновений со стенками)\n")
        file.write(f"столкновений со стенками за секунду: {wall_collision_count * FPS / frame_counter / TIME_K}\n")
        file.write(f"столкновений между собой за секунду: {self_collision_count * FPS / frame_counter / TIME_K}\n")
        file.write(f"время: {frame_counter // FPS}\n")
        file.write(f"средняя скорость: {v_sum / sum}\n")
        file.write(f"наиболее вероятная скорость: {nvel.index(max(nvel)) / len (nvel) * vmax}\n")
        file.write(f"P: {ctypes.c_double.in_dll(dvizh_ok, 'distance').value * FPS / (4000 * frame_counter / TIME_K)}\n")
        file.write(f"nmax: {nmax}\n")
        file.write(f"{nvel}\n")
    

pygame.quit()
