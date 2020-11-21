import pygame
import sys
from random import *
import time

################
"""   VARS   """
################

MAX_X = 1366
MAX_Y = 768
matrix_char_array = [] # для файлнеймов
all_chars = []
char_speed = 2
char_size = 48
bg_color = (0, 0, 0)
array_x = [] # колонки допустимые колонки
chain_len = 13

# от 1 до 12
for i in range(1,13):
    matrix_char_array.append(str(i)+'.png')
print(matrix_char_array)
# input()

# теперь все названия файлов в массиве

####################
"""   EOF VARS   """
####################

""" FUNCS """

class MatrixChar():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = char_speed
        self.img_filename = matrix_char_array[randint(0,11)]
        self.image = pygame.image.load(self.img_filename).convert_alpha() # загрузка изображения (проверить,
        self.image = pygame.transform.scale(self.image, (char_size, char_size))
    def MoveChar(self):
        self.y = self.y + self.speed

    def DrawChar(self):
        screen.blit(self.image, (self.x, self.y))

def CheckForExit():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            sys.exit()

""" EOF FUNCS """

"""         MAIN            """
pygame.init() # инизиализируем pygame
screen = pygame.display.set_mode ((MAX_X, MAX_Y), pygame.FULLSCREEN) # даем переменную экрана из назначения



x = 0
while x < 1340:
    array_x.append(x)
    x += 48




### Добавить символы в первую строку
'''for i in array_x:
    all_chars.append(MatrixChar(i, 0))

for i in all_chars:
    i.DrawChar()'''

#varbool = True
while True:

    screen.fill(bg_color)
    CheckForExit()
    #### ОСНОВНОЙ ЦИКЛ ПРОГРАММЫ ###
    for i in all_chars:
        i.MoveChar()
        i.DrawChar()
    if randint(0,55) == 0:
        ChainX = array_x[randint(0,len(array_x)-1)] # расчет колонки в виде переменной Х для класса
        for y in range(0,chain_len*char_size,char_size):
            all_chars.append(MatrixChar(ChainX, -y))



    pygame.display.flip()


    #### EOF ОСНОВНОЙ ЦИКЛ ПРОГРАММЫ ###


























    ### EOFEOF ###
