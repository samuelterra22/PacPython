#Para rodar deve-se baixar a biblioteca pygame:

# sudo pip install pygame

import pygame, sys, random
from pygame.locals import *


def screen_init():
    w = 800
    h = 480
    z = 0

    screen = pygame.display.set_mode((w,h))
    pygame.display.flip()
    clock = pygame.time.Clock()

    while 1:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill((0,0,0))
        pygame.display.update()

if __name__ == '__main__':

    pac = Model.Pacman(5.0,5.0)
    print(pac.getPosition())

    pass
