import pygame
import random
import json 


##########################################################################
WIDTH = 1000  # ширина игрового окна
HEIGHT = 500 # высота игрового окна
FPS = 30 # частота кадров в секунду

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
##########################################################################

# создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
###########################################################################

# начальные параметры: кружок со скоростью
# json
R = 100
v = [10, 10]
V = [v[0]/FPS, v[1]/FPS]
xy = [0, 0]

###########################################################################
def centCO(XY):
    XY1 = [0]*2
    XY1[0] = XY[0] + WIDTH/2
    XY1[1] = XY[1] + HEIGHT/2
    return XY1

# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(WHITE)
    
    pygame.draw.circle(screen, RED, centCO(xy), R)
    xy[0] += V[0]
    xy[1] += V[1]
    print(xy[0], V[0], xy[1], V[1], centCO(xy))
    pygame.display.flip()

# Обновление

# Рендеринг

# После отрисовки всего, переворачиваем экран</span>



pygame.quit()