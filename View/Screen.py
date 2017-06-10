# -*- coding: utf-8 -*-

import pygame

class Screen:

    def __init__(self):

        # -------- Inicializando Variáveis -------- #

        # Cores

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.yellow = (255, 255, 0)
        self.green = (0, 255, 0)

        self.change_rate = 10
        self.fps = 13

        # Dimensões de Tela

        # Tela dedicada para o Game

        self.width_game = 800
        self.height_game = 600

        # Tela total

        self.width = 800
        self.height = 700

        self.gameDisplay = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("PacPython \o/")

        # Dimensões do pacman e da borda

        self.pacman_radius = 15
        self.border_width_game = 5

        # Clock para definir os Frames por segundo

        self.clock = pygame.time.Clock()


    # -------- Contador do Placar -------- #

    def score_counter(self, score):

        font = pygame.font.SysFont(None, 25)
        score = "Score: " + str(score)
        screen_text = font.render(score, True, self.green)
        self.gameDisplay.blit(screen_text, [5, 650])

    # -------- Desenha o jogo, atualizando as posições -------- #

    def draw_game(self, pacman_x, pacman_y, counter):

        # Pinta o fundo da tela de preto

        self.gameDisplay.fill(self.black)

        # Desenha o Pacman

        pygame.draw.circle(self.gameDisplay, self.yellow, (pacman_x, pacman_y), self.pacman_radius, 0)

        # Desenha as bordas

        pygame.draw.line(self.gameDisplay, self.white, (0, 0), (0, self.height_game), self.border_width_game)
        pygame.draw.line(self.gameDisplay, self.white, (0, 0), (self.width_game, 0), self.border_width_game)
        pygame.draw.line(self.gameDisplay, self.white, (0, self.height_game), (self.width_game, self.height_game), self.border_width_game)
        pygame.draw.line(self.gameDisplay, self.white, (self.width_game, 0), (self.width_game, self.height_game), self.border_width_game)

        # Desenha o placar

        self.score_counter(counter)

        pygame.display.update()

        # FPS

        self.clock.tick(self.fps)

    # -------- Looping principal do jogo -------- #

    def gameLoop(self):

        pygame.init()

        # Comando de parada do jogo

        game_exit = False

        # Contador do Placar

        counter = 0

        # Limite das bordas do labirinto

        boundarie_maze = self.pacman_radius + self.border_width_game

        # Posições iniciais do Pac-Man

        pacman_x = boundarie_maze
        pacman_y = self.height_game - boundarie_maze

        # Limites até onde o pacman pode alcançar

        boundarie_x_pacman = self.width_game - boundarie_maze
        boundarie_y_pacman = self.height_game - boundarie_maze

        # Variáveis para a mudança de posição do pacman

        pacman_x_change = 0
        pacman_y_change = 0

        while not game_exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        pacman_x_change = -self.change_rate
                        pacman_y_change = 0
                    elif event.key == pygame.K_RIGHT:
                        pacman_x_change = self.change_rate
                        pacman_y_change = 0
                    elif event.key == pygame.K_UP:
                        pacman_y_change = -self.change_rate
                        pacman_x_change = 0
                    elif event.key == pygame.K_DOWN:
                        pacman_y_change = self.change_rate
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

            counter += 1

            self.draw_game(pacman_x, pacman_y, counter)

        # End While
        pygame.quit()
        quit()