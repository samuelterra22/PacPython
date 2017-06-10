# -*- coding: utf-8 -*-

import pygame, time

pygame.init()

# -------- Inicializando Variáveis -------- #

# Cores

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
yellow = (255,255,0)
green = (0,255,0)

change_rate = 10
tick = 13

# Dimensões de Tela

# Tela dedicada para o Game

width_game = 800
height_game = 600

# Tela total

width = 800
height = 700

gameDisplay = pygame.display.set_mode((width, height))
pygame.display.set_caption("PacPython \o/")

# Dimensões do pacman e da borda

pacman_radius = 15
border_width_game = 5

# Variáveis para a mudança de posição do pacman

pacman_x_change = 0
pacman_y_change = 0


# Limite das bordas do labirinto

boundarie_maze = pacman_radius + border_width_game

# Limites até onde o pacman pode alcançar

boundarie_x_pacman = width_game - boundarie_maze
boundarie_y_pacman = height_game - boundarie_maze

# Comando de parada do jogo

gameExit = False

# Posições iniciais do Pac-Man

pacman_x = boundarie_maze
pacman_y = height_game - boundarie_maze

# Clock para definir os Frames por segundo

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 25)

# Atualiza a tela

pygame.display.update()
counter = 0

# -------- Fim da Inicialização de Variáveis -------- #


def score_counter(score):

    score = "Score: " + str(score)
    screen_text = font.render(score, True, green)
    gameDisplay.blit(screen_text, [5, 650])


def draw_game():

    # Desenha o Pacman

    pygame.draw.circle(gameDisplay, yellow, (pacman_x, pacman_y), pacman_radius, 0)

    # Desenha as bordas

    pygame.draw.line(gameDisplay, white, (0, 0), (0, height_game), border_width_game)
    pygame.draw.line(gameDisplay, white, (0, 0), (width_game, 0), border_width_game)
    pygame.draw.line(gameDisplay, white, (0, height_game), (width_game, height_game), border_width_game)
    pygame.draw.line(gameDisplay, white, (width_game, 0), (width_game, height_game), border_width_game)

    score_counter(counter)

# -------- Looping principal do jogo -------- #

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

    counter += 1

    draw_game()

    pygame.display.update()

    # FPS

    clock.tick(tick)

pygame.quit()
quit()

# -------- Fim do Jogo -------- #