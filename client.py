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
pygame.display.set_caption("шщшшщшщшщ")
clock = pygame.time.Clock()
###########################################################################

class figure:  
    """Базовый класс для всех сотрудников"""  
    FigCount = 0

    def __init__(self, type, center, R, clr):  
        self.type = 0
        self.center = [0,0]
        self.R = 100
        self.clr = BLUE
        figure.FigCount += 1  

    def draw(self, screen):

        if self.type == 0:
            pygame.draw.circle(screen, self.clr, centCO(self.center), self.R)
        

# начальные параметры: кружок со скоростью
# json

circ1 = figure(0, [0,0], 100, WHITE) # как не прописывать всю строку?

v = [10, 10]

ScrnClr = GREEN
ticks = 0
sumticks = 0

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
    
    ###############################

    # работа с сервером
    ticks = pygame.time.get_ticks() - ticks
    sumticks += ticks
    print(ticks)

    if 10000 < sumticks:
        sumticks = 0
        print(" тут будет get_new и обработка доп параметров")

        #with open("testdata.json", "r") as fnew: 
        #    Dt = json.load(fnew)
        #fnew.close()
        Dt = {'center': [0,0], 'v': [100,-50], 'clr': (255, 0, 0) } 

        ScrnClr = WHITE
        circ1.center = Dt['center']
        circ1.clr = Dt['clr']
        v = Dt['v']


    elif (1000 < ticks):   #посмотреть, как часто требуется обновлять
        print(" тут будет get_changes")

        #with open("data.json", "r") as fchanges: 
        #data = json.load(fchanges)
        #fchanges.close()
    ###############################
    # перевод полученного сообщения в переменные
    
    V = [v[0]/FPS, v[1]/FPS]
    ###############################
    # отрисовка
    
    screen.fill(ScrnClr)
    
    circ1.draw(screen)
    circ1.center[0] += V[0]
    circ1.center[1] += V[1]
    #print(xy[0], V[0], xy[1], V[1], centCO(xy))
    pygame.display.flip()
    ###############################



pygame.quit()