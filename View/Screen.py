# -*- coding: utf-8 -*-

import pygame, sys, random
from pygame.locals import *

pygame.init()

# Cores

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
yellow = (255,255,0)

change_rate = 10
tick = 13

# Dimensões da Tela

width = 800
height = 600

# Dimensões do pacman e da borda

pacman_radius = 15
border_width = 5

# Limite das bordas do labirinto

boundarie_maze = pacman_radius + border_width

# Limites até onde o pacman pode alcançar

boundarie_x_pacman = width - boundarie_maze
boundarie_y_pacman = height - boundarie_maze

gameDisplay = pygame.display.set_mode((width, height))
pygame.display.set_caption("PacPython \o/")

# Comando de parada do jogo
gameExit = False

# Posições iniciais do Pac-Man

pacman_x = boundarie_maze
pacman_y = height - boundarie_maze

# Variáveis para a mudança de posição do pacman

pacman_x_change = 0
pacman_y_change = 0

# Clock para definir os Frames por segundo

clock = pygame.time.Clock()

# Desenha as bordas

pygame.draw.line(gameDisplay, white, (0, 0),(0, height), border_width)
pygame.draw.line(gameDisplay, white, (0, 0), (width, 0), border_width)
pygame.draw.line(gameDisplay, white, (0, height), (width, height), border_width)
pygame.draw.line(gameDisplay, white, (width, 0), (width, height), border_width)

# Atualiza a tela

pygame.display.update()

# Looping principal do jogo

while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pacman_x_change = -change_rate
                pacman_y_change = 0
            elif event.key == pygame.K_RIGHT:
                pacman_x_change = change_rate
                pacman_y_change = 0
            elif event.key == pygame.K_UP:
                pacman_y_change = -change_rate
                pacman_x_change = 0
            elif event.key == pygame.K_DOWN:
                pacman_y_change = change_rate
                pacman_x_change = 0

    # Atualiza a posição do pacman

    pacman_x += pacman_x_change
    pacman_y += pacman_y_change

    # Verifica as bordas.

    if pacman_x > boundarie_x_pacman:
        pacman_x = boundarie_x_pacman
    elif pacman_x < boundarie_maze:
        pacman_x = boundarie_maze

    if pacman_y > boundarie_y_pacman:
        pacman_y = boundarie_y_pacman
    elif pacman_y < boundarie_maze:
        pacman_y = boundarie_maze

    # Pinta o fundo da tela de preto

    gameDisplay.fill(black)

    # Desenha o Pacman

    pygame.draw.circle(gameDisplay, yellow, (pacman_x,pacman_y), pacman_radius, 0)

    pygame.display.update()

    # FPS

    clock.tick(tick)


pygame.quit()
quit()
