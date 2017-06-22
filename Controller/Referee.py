# -*- coding: utf-8 -*-
import pygame, math, time
import threading as Threads
from Controller.AFDController import AFDController
from Model.Pacman import Pacman
from Model.Ghost import Ghost
from random import choice
from copy import copy
from Model.Fruits import Fruits

class Referee(object):

    def __init__(self):

        # -------- Inicializando Variáveis -------- #

        # Cores

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.yellow = (255, 255, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 204)
        self.orange = (255, 127, 0)
        self.purple = (147, 112, 219)

        # Barreiras

        self.barriers = [(100, 50, 479, 50), (60, 540, 300, 540), (360, 510, 460, 510), (410, 510, 410, 550),
                    (510, 520, 660, 520), (730, 580, 730, 450),
                    (5, 480, 70, 480), (135, 542, 135, 440), (200, 416, 300, 416), (200, 480, 250, 480),
                    (359, 347, 460, 347), (408, 354, 408, 450),
                    (505, 412, 595, 412), (654, 523, 654, 460), (580, 518, 580, 468), (688, 344, 688, 244),
                    (553, 286, 688, 286), (300, 280, 300, 200),
                    (292, 280, 470, 280), (470, 288, 470, 200), (145, 203, 145, 303), (207, 203, 247, 203),
                    (526, 286, 556, 286), (123, 360, 293, 360),
                    (52, 414, 52, 134), (141, 110, 240, 110), (146, 170, 200, 170), (562, 52, 780, 52),
                    (294, 114, 400, 114), (474, 136, 474, 66),
                    (541, 163, 700, 163), (620, 166, 620, 266), (750, 112, 780, 112), (750, 335, 750, 200)]

        # Cápsulas

        self.capsules = []

        self.capsules1 = []
        self.capsules2 = []

        # Powerfull Fruits!!

        self.fruits = []

        self.banana = None
        self.cherry = None

        # Vidas

        self.lifes = []

        # Imagens dos fantasmas

        self.blue_img = None
        self.red_img = None
        self.orange_img = None
        self.purple_img = None

        # Inicializa um Pacman!!

        self.pacman = Pacman()

        # Inicializa os fantasmas

        self.red_ghost = Ghost("red") # De 5 em 5 segundos recebe a posição do pacman (absoluta)
        self.blue_ghost = Ghost("blue") # Random
        self.orange_ghost = Ghost("orange") # Sempre que o pacman muda de direção ele copia a direção contrária!
        self.purple_ghost = Ghost("purple") # Vai na direção do pacman

        self.ghost_list = [self.red_ghost, self.blue_ghost, self.orange_ghost, self.purple_ghost]

        # Direções disponíveis:

        self.directions_available = ["up", "down", "left", "right"]

        # Todos os pontos do mapa que contém um obstáculo

        self.barrier_points = []
        self.barrier_points1 = []
        self.barrier_points2 = []

        # FPS e blocos que os elementos móveis se movimentam por vez.

        self.change_rate = 10
        self.fps = 30
        self.fps_ghosts = 10

        # Dimensões de Tela

        # Tela dedicada para o Game

        self.width_game = 800
        self.height_game = 600

        # Tela total

        self.width = 800
        self.height = 700

        self.gameDisplay = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("PacPython \o/")

        # Largura da borda

        self.border_width_game = 5

        # Limite das bordas do labirinto

        self.boundarie_maze = self.pacman.getRadius() + self.border_width_game
        self.boundarie_maze_g = self.red_ghost.getRadius() + self.border_width_game

        # Limites até onde o pacman pode alcançar

        self.boundarie_x_pacman = self.width_game - self.boundarie_maze
        self.boundarie_y_pacman = self.height_game - self.boundarie_maze

        # Dimensão da cápsula

        self.capsule_radius = 5

        # Clock para definir os Frames por segundo

        self.clock = pygame.time.Clock()

        # Comando de parada do jogo

        self.game_exit = False

        # Controle de transições do AFD do Pacman

        self.trans_pac_counter = 0

        # Flag que controla se o pacman anda ou não.

        self.walk = False

        # Flag de inicio dos fantasmas

        self.go_ghosts = False

        self.lock_red = False
        self.lock_orange = False
        self.lock_purple = False

        self.fruit_power = False

        self.orange_next_dir = "up"

        # Controller dos Autômatos

        self.aut_controller = AFDController()

    # ------- * Construtor da lista de barreiras do labirinto ------- * #

    def build_barrier_points(self):

        for i in self.barriers:
            # Barreiras Horizontais

            if i[1] == i[3]:
                if i[0] > i[2]:
                    for x in range(i[2], i[0] + 1):
                        self.barrier_points.append((x, i[1]))
                else:
                    for x in range(i[0], i[2] + 1):
                        self.barrier_points.append((x, i[1]))

            # Barreiras Verticais

            if i[0] == i[2]:
                if i[1] > i[3]:
                    for y in range(i[3], i[1] + 1):
                        self.barrier_points.append((i[0], y))
                else:
                    for y in range(i[1], i[3] + 1):
                        self.barrier_points.append((i[0], y))
                        # Ordena a lista de obstáculos pelo valor de x (x,y)

        self.barrier_points.sort(key=lambda tup: tup[0])

        # Divide a lista ao meio para acelerar o processamento

        for i in range(0, len(self.barrier_points) / 2):
            self.barrier_points1.append(self.barrier_points[i])

        for i in range(len(self.barrier_points) / 2, len(self.barrier_points)):
            self.barrier_points2.append(self.barrier_points[i])

    # ------- * Construtor da lista de cápsulas do labirinto ------- * #

    def build_capsules(self):

        dist_capsules = 20

        for i in range(0, 17):
            self.capsules.append(((self.pacman.getX() + dist_capsules), self.boundarie_y_pacman))
            dist_capsules += 40

        dist_capsules = 0

        for i in range(0, 20):
            self.capsules.append(((46 + dist_capsules), 26))
            dist_capsules += 40

        dist_capsules = 0

        for i in range(0, 11):
            self.capsules.append((25, (452 - dist_capsules)))
            self.capsules.append((85, (25 + dist_capsules)))
            self.capsules.append((778, (158 + dist_capsules)))
            dist_capsules += 40

        dist_capsules = 0

        for i in range(0, 15):
            self.capsules.append(((132 + dist_capsules), 324))
            dist_capsules += 40

        dist_capsules = 0

        for i in range(0, 8):
            self.capsules.append(((456 + dist_capsules), 388))
            self.capsules.append(((125 + dist_capsules), 85))
            self.capsules.append(((125 + dist_capsules), 145))

            dist_capsules += 40

        dist_capsules = 0

        for i in range(0, 7):
            self.capsules.append(((376 - dist_capsules), 385))
            self.capsules.append(((298 + dist_capsules), 473))
            self.capsules.append(((565 + dist_capsules), 91))
            self.capsules.append((724, (122 + dist_capsules)))
            dist_capsules += 40

        dist_capsules = 0

        for i in range(0, 3):
            self.capsules.append((526, (49 + dist_capsules)))
            self.capsules.append((526, (170 + dist_capsules)))
            self.capsules.append((335, (433 + dist_capsules)))
            self.capsules.append((173, (424 + dist_capsules)))
            self.capsules.append(((176 + dist_capsules), 255))
            self.capsules.append((696, (429 + dist_capsules)))
            self.capsules.append(((12 + dist_capsules), 509))
            dist_capsules += 40

        # # Divide a lista de cápsulas em 2, para agilizar o procesamento.
        #
        # self.capsules.sort(key=lambda tup: tup[0])
        #
        # for i in range(0, len(self.capsules) / 2):
        #     self.capsules1.append(self.capsules[i])
        #
        # for i in range(len(self.capsules) / 2, len(self.capsules)):
        #     self.capsules2.append(self.capsules[i])

    def loadObjectImages(self):

        blue_img = pygame.image.load("Images/blue.png")
        red_img = pygame.image.load("Images/red.png")
        purple_img = pygame.image.load("Images/purple.png")
        orange_img = pygame.image.load("Images/orange.png")

        banana_img = pygame.image.load("Images/fruit1.png")
        cherry_img = pygame.image.load("Images/fruit2.png")

        life = pygame.image.load("Images/pacman.png")

        banana = Fruits(640, 195, banana_img)
        cherry = Fruits(170, 190, cherry_img)

        self.lifes.append(life)
        self.lifes.append(life)
        self.lifes.append(life)

        self.fruits.append(banana)
        self.fruits.append(cherry)

        self.banana = banana
        self.cherry = cherry

        self.blue_img = blue_img
        self.orange_img = orange_img
        self.red_img = red_img
        self.purple_img = purple_img

    def setInitialPositions(self):

        # Posições iniciais do Pac-Man

        self.pacman.setInitialPosition(self.boundarie_maze, self.height_game - self.boundarie_maze)

        # Seta as posições iniciais dos ghosts

        self.red_ghost.setInitialPosition("red")
        self.blue_ghost.setInitialPosition("blue")
        self.orange_ghost.setInitialPosition("orange")
        self.purple_ghost.setInitialPosition("purple")

    # -------- Contador do Placar -------- #

    def score_counter(self):

        font = pygame.font.SysFont(None, 25)
        score = "Score: " + str(self.pacman.getCapsules())
        screen_text = font.render(score, True, self.green)
        self.gameDisplay.blit(screen_text, [5, 680])

    def life_counter(self):

        font = pygame.font.SysFont(None, 25)
        score = "Lifes: "
        x = 67
        for i in self.lifes:
            self.gameDisplay.blit(i, (x, 625))
            x+= 20
        screen_text = font.render(score, True, self.yellow)
        self.gameDisplay.blit(screen_text, [7, 627])

    # -------- Desenha o jogo, atualizando as posições -------- #

    def draw_game(self, capsules, barriers):

        # Pinta o fundo da tela de preto

        self.gameDisplay.fill(self.black)

        # Desenha as capsulas

        for i in capsules:
            pygame.draw.circle(self.gameDisplay, self.yellow, (int(i[0]),int(i[1])), self.capsule_radius, 0)

        # Desenha as Barriers

        for i in barriers:
            pygame.draw.line(self.gameDisplay, self.blue,(i[0],i[1]),(i[2],i[3]),17)

        # Desenha o Pacman

        pygame.draw.circle(self.gameDisplay, self.pacman.getColor(), (self.pacman.getX(), self.pacman.getY()), self.pacman.getRadius())

        # Desenha as bordas

        pygame.draw.line(self.gameDisplay, self.white, (0, 0), (0, self.height_game), self.border_width_game)
        pygame.draw.line(self.gameDisplay, self.white, (0, 0), (self.width_game, 0), self.border_width_game)
        pygame.draw.line(self.gameDisplay, self.white, (0, self.height_game), (self.width_game, self.height_game), self.border_width_game)
        pygame.draw.line(self.gameDisplay, self.white, (self.width_game, 0), (self.width_game, self.height_game), self.border_width_game)

        # Desenha o placar

        self.score_counter()

        # Desenha o contador de vidas

        self.life_counter()

        # Desenha os fantasmas

        for i in self.ghost_list:

            ghost_color = i.getColor()

            if ghost_color == "red":
                self.gameDisplay.blit(self.red_img, (self.red_ghost.getX(), self.red_ghost.getY()))
            elif ghost_color == "blue":
                self.gameDisplay.blit(self.blue_img, (self.blue_ghost.getX(), self.blue_ghost.getY()))
            elif ghost_color == "orange":
                self.gameDisplay.blit(self.orange_img, (self.orange_ghost.getX(), self.orange_ghost.getY()))
            elif ghost_color == "purple":
                self.gameDisplay.blit(self.purple_img, (self.purple_ghost.getX(), self.purple_ghost.getY()))

        # pygame.draw.circle(self.gameDisplay, self.blue_ghost.getColor(), (self.blue_ghost.getX(), self.blue_ghost.getY()), self.blue_ghost.getRadius())
        # pygame.draw.circle(self.gameDisplay, self.red_ghost.getColor(), (self.red_ghost.getX(), self.red_ghost.getY()), self.red_ghost.getRadius())
        # pygame.draw.circle(self.gameDisplay, self.orange_ghost.getColor(), (self.orange_ghost.getX(), self.orange_ghost.getY()), self.orange_ghost.getRadius())
        # pygame.draw.circle(self.gameDisplay, self.purple_ghost.getColor(), (self.purple_ghost.getX(), self.purple_ghost.getY()), self.purple_ghost.getRadius())

        # Desenha as frutas

        for i in self.fruits:
            self.gameDisplay.blit(i.getImg(), (i.getX(), i.getY()))

        pygame.display.update()

        # FPS

        self.clock.tick(self.fps)


    # -------- Executa o autômato do Pac-man -------- #

    def pacman_automata(self):

        # Se o pacman andou, o estado muda

        while not self.game_exit:

            if self.walk:
                if self.trans_pac_counter == 0:
                    self.trans_pac_counter = self.aut_controller.move(self.pacman.getAFD(), 0, self.pacman.getDirection())
                else:
                    self.trans_pac_counter = self.aut_controller.move(self.pacman.getAFD(), self.trans_pac_counter, self.pacman.getDirection())
        # Fim do Jogo

    def red_automata(self):

        while not self.go_ghosts:
            pass

        while not self.game_exit:

            self.clock.tick(self.fps_ghosts)

            if not self.lock_red:

                new_x, new_y, new_direction = self.move_ghosts("red")

                self.red_ghost.setDirection(new_direction)
                self.red_ghost.setX(new_x)
                self.red_ghost.setY(new_y)

            if self.red_ghost.getState() == "0":
                self.red_ghost.setState(self.aut_controller.move(self.red_ghost.getAFD(), 0,
                                                                  self.red_ghost.getDirection()))
            else:
                self.red_ghost.setState(self.aut_controller.move(self.red_ghost.getAFD(),
                                                                  int(self.red_ghost.getState()),
                                                                  self.red_ghost.getDirection()))
            if self.red_ghost.getState() == "5":

                if not self.fruit_power:

                    if len(self.lifes) > 1:
                        del self.lifes[len(self.lifes)-1]
                        self.setInitialPositions()
                    else:
                        print("GAME OVER!")
                        self.game_exit = True
                else:
                    self.ghost_list.remove(self.red_ghost)
                    break

        # Fim do Jogo

    def blue_automata(self):

        while not self.go_ghosts:
            pass

        while not self.game_exit:

            self.clock.tick(self.fps_ghosts)

            new_x, new_y, new_direction = self.move_ghosts("blue")

            self.blue_ghost.setDirection(new_direction)
            self.blue_ghost.setX(new_x)
            self.blue_ghost.setY(new_y)

            if self.blue_ghost.getState() == "0":
                self.blue_ghost.setState(self.aut_controller.move(self.blue_ghost.getAFD(), 0,
                                                             self.blue_ghost.getDirection()))
            else:
                self.blue_ghost.setState(self.aut_controller.move(self.blue_ghost.getAFD(),
                                                             int(self.blue_ghost.getState()),
                                                             self.blue_ghost.getDirection()))
            if self.blue_ghost.getState() == "5":
                if not self.fruit_power:

                    if len(self.lifes) > 1:
                        del self.lifes[len(self.lifes)-1]
                        self.setInitialPositions()
                    else:
                        print("GAME OVER!")
                        self.game_exit = True
                else:
                    self.ghost_list.remove(self.blue_ghost)
                    break
        # Fim do Jogo

    def orange_automata(self):

        while not self.go_ghosts:
            pass

        while not self.game_exit:

            self.clock.tick(self.fps_ghosts)

            new_x, new_y, new_direction = self.move_ghosts("orange")

            self.orange_ghost.setDirection(new_direction)
            self.orange_ghost.setX(new_x)
            self.orange_ghost.setY(new_y)
            self.lock_orange = False

            if self.orange_ghost.getState() == "0":
                self.orange_ghost.setState(self.aut_controller.move(self.orange_ghost.getAFD(), 0,
                                                                  self.orange_ghost.getDirection()))
            else:
                self.orange_ghost.setState(self.aut_controller.move(self.orange_ghost.getAFD(),
                                                                  int(self.orange_ghost.getState()),
                                                                  self.orange_ghost.getDirection()))
            if self.orange_ghost.getState() == "5":
                if not self.fruit_power:

                    if len(self.lifes) > 1:
                        del self.lifes[len(self.lifes)-1]
                        self.setInitialPositions()
                    else:
                        print("GAME OVER!")
                        self.game_exit = True
                else:
                    self.ghost_list.remove(self.orange_ghost)
                    break
                    # Fim do Jogo

    def purple_automata(self):

        while not self.go_ghosts:
            pass

        while not self.game_exit:

            self.clock.tick(self.fps_ghosts)

            if not self.lock_purple:
                new_x, new_y, new_direction = self.move_ghosts("purple")

                self.purple_ghost.setDirection(new_direction)
                self.purple_ghost.setX(new_x)
                self.purple_ghost.setY(new_y)

            if self.purple_ghost.getState() == "0":
                self.purple_ghost.setState(self.aut_controller.move(self.purple_ghost.getAFD(), 0,
                                                                  self.purple_ghost.getDirection()))
            else:
                self.purple_ghost.setState(self.aut_controller.move(self.purple_ghost.getAFD(),
                                                                  int(self.purple_ghost.getState()),
                                                                  self.purple_ghost.getDirection()))
            if self.purple_ghost.getState() == "5":
                if not self.fruit_power:

                    if len(self.lifes) > 1:
                        del self.lifes[len(self.lifes)-1]
                        self.setInitialPositions()
                    else:
                        print("GAME OVER!")
                        self.game_exit = True
                else:
                    self.ghost_list.remove(self.purple_ghost)
                    break
        # Fim do Jogo

    def control_red(self):

        while not self.game_exit:
            self.lock_red = False

            time.sleep(5)

            self.lock_red = True
            new_x, new_y, new_direction = self.move_ghosts("red")
            self.red_ghost.setDirection(new_direction)
            self.red_ghost.setX(new_x)
            self.red_ghost.setY(new_y)

    def control_purple(self):

        while not self.game_exit:
            self.lock_purple = False

            time.sleep(2)

            self.lock_purple = True
            new_x, new_y, new_direction = self.move_ghosts("purple")
            self.purple_ghost.setDirection(new_direction)
            self.purple_ghost.setX(new_x)
            self.purple_ghost.setY(new_y)

    def power_pacman(self):

        while not self.game_exit:
            if self.fruit_power:
                white_img = pygame.image.load("Images/white.png")

                self.red_img = white_img
                self.blue_img = white_img
                self.orange_img = white_img
                self.purple_img = white_img

                time.sleep(10)

                blue_img = pygame.image.load("Images/blue.png")
                red_img = pygame.image.load("Images/red.png")
                purple_img = pygame.image.load("Images/purple.png")
                orange_img = pygame.image.load("Images/orange.png")

                self.red_img = red_img
                self.blue_img = blue_img
                self.orange_img = orange_img
                self.purple_img = purple_img

                self.fruit_power = False

    # -------- Looping principal do jogo -------- #

    def thread_trigger(self):

        # Dispara as Threads

        # Thread AFD pacman

        t_pacman = Threads.Thread(target=self.pacman_automata, args=())

        # Thread Game Loop

        t_game = Threads.Thread(target=self.gameLoop, args=())

        # Thread para Autômato do fantasma vermelho

        t_red = Threads.Thread(target=self.red_automata, args=())

        t_blue = Threads.Thread(target=self.blue_automata, args=())

        t_orange = Threads.Thread(target=self.orange_automata, args=())

        t_purple = Threads.Thread(target=self.purple_automata, args=())

        t_control_red = Threads.Thread(target=self.control_red, args=())

        t_control_purple = Threads.Thread(target=self.control_purple, args=())

        t_power_mode = Threads.Thread(target=self.power_pacman, args=())

        t_game.start()
        t_pacman.start()
        t_red.start()
        t_blue.start()
        t_orange.start()
        t_purple.start()
        t_control_red.start()
        t_control_purple.start()
        t_power_mode.start()

    def gameLoop(self):

        pygame.init()
        pygame.mixer.init()

        self.loadObjectImages()

        self.setInitialPositions()

        # Variáveis para a mudança de posição do pacman

        pacman_x_change = 0
        pacman_y_change = 0

        able = True
        aux_x = -1
        aux_y = -1

        # Monta a lista de pontos contendo todos os os obstatculos do game.

        self.build_barrier_points()

        # Monta a lista de cápsulas presentes no game

        self.build_capsules()

    # Loop do jogo

        while not self.game_exit:
            self.go_ghosts = True
            if self.pacman.getCapsules() == 155:
                print('GANHOU!')
                self.game_exit = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_exit = True
                elif event.type == pygame.KEYDOWN:
                    self.walk = True
                    if event.key == pygame.K_LEFT:
                        pacman_x_change = -self.change_rate
                        pacman_y_change = 0
                        self.orange_next_dir = "right"
                        self.lock_orange = True
                        self.pacman.setDirection("left")
                        # Testa se está tentando atravessar a parede.
                        if aux_x > -1:
                            test_dist = self.calcDist(self.pacman.getX() + pacman_x_change, self.pacman.getY(), aux_x, aux_y)
                            if test_dist > 19.0:
                                able = True

                    elif event.key == pygame.K_RIGHT:
                        pacman_x_change = self.change_rate
                        pacman_y_change = 0
                        self.orange_next_dir = "left"
                        self.lock_orange = True
                        self.pacman.setDirection("right")
                        # Testa se está tentando atravessar a parede.
                        if aux_x > -1:
                            test_dist = self.calcDist(self.pacman.getX() + pacman_x_change, self.pacman.getY(), aux_x, aux_y)
                            if test_dist > 19.0:
                                able = True

                    elif event.key == pygame.K_UP:
                        pacman_y_change = -self.change_rate
                        pacman_x_change = 0
                        self.pacman.setDirection("up")
                        self.lock_orange = True
                        self.orange_next_dir = "down"
                        # Testa se está tentando atravessar a parede.
                        if aux_x > -1:
                            test_dist = self.calcDist(self.pacman.getX(), self.pacman.getY() + pacman_y_change, aux_x, aux_y)
                            if test_dist > 19.0:
                                able = True

                    elif event.key == pygame.K_DOWN:
                        pacman_y_change = self.change_rate
                        pacman_x_change = 0
                        self.pacman.setDirection("down")
                        self.lock_orange = True
                        self.orange_next_dir = "up"
                        # Testa se está tentando atravessar a parede.
                        if aux_x > -1:
                            test_dist = self.calcDist(self.pacman.getX(), self.pacman.getY() + pacman_y_change, aux_x, aux_y)
                            if test_dist > 19.0:
                                able = True

                # Se nenhuma tecla foi pressionada
                else:
                    self.walk = False
                    self.pacman.setDirection("None")

            # Atualiza a posição do pacman
            if able:
                self.pacman.setX(self.pacman.getX() + pacman_x_change)
                self.pacman.setY(self.pacman.getY() + pacman_y_change)

            # Verifica as bordas.

            if self.pacman.getX() > self.boundarie_x_pacman:
                self.pacman.setX(self.boundarie_x_pacman)
                self.walk = False
            elif self.pacman.getX() < self.boundarie_maze_g:
                self.pacman.setX(self.boundarie_maze_g)
                self.walk = False
            if self.pacman.getY() > self.boundarie_y_pacman:
                self.pacman.setY(self.boundarie_y_pacman)
                self.walk = False
            elif self.pacman.getY() < self.boundarie_maze_g:
                self.pacman.setY(self.boundarie_maze_g)
                self.walk = False

            # Verifica a coolisão com barreiras.

            if self.pacman.getX() > self.barrier_points1[len(self.barrier_points)/2 - 1][0]:
                b_points = self.barrier_points2
            else: b_points = self.barrier_points1

            for i in b_points:
                dist = self.calcDist(self.pacman.getX(), self.pacman.getY(), i[0], i[1])
                if dist < 19.0:
                    pacman_y_change = 0
                    pacman_x_change = 0
                    able = False
                    self.walk = False
                    aux_x = i[0]
                    aux_y = i[1]
                    break
                else:
                    able = True

            # Verifica o ingerir de capsulas

            for i in self.capsules:
                dist = self.calcDist(self.pacman.getX(), self.pacman.getY(), i[0], i[1])
                if dist < float(self.pacman.getRadius() + self.capsule_radius):
                    self.pacman.setCapsules(self.pacman.getCapsules() + 1)
                    #pygame.mixer.music.load(open("Sounds/eat_capsules.wav", "rb"))
                    #pygame.mixer.music.play()
                    #while pygame.mixer.music.get_busy():
                    #     time.sleep(0.5)
                    self.capsules.remove(i)
                    break

            # Verifica o ingerir das frutas

            for i in self.fruits:
                dist = self.calcDist(self.pacman.getX(), self.pacman.getY(), i.getX(), i.getY())
                if dist < 30.0:
                    self.fruits.remove(i)
                    self.fruit_power = True
                    break

            # Atualiza o Cenário

            self.draw_game(self.capsules, self.barriers)

        # End While
        pygame.quit()
        quit()

    def move_ghosts(self, color):

        ghost = None
        border_collision = False
        pacman_collision = False

        if color == "red":
            ghost = copy(self.red_ghost)

        elif color == "orange":
            ghost = copy(self.orange_ghost)

        elif color == "blue":
            ghost = copy(self.blue_ghost)

        elif color == "purple":
            ghost = copy(self.purple_ghost)

        if self.lock_red and color == "red":
            current_dir = self.testGhostDirection("red")
           # print("Juiz definiu a direção: " + current_dir)

        elif self.lock_orange and color == "orange":
            current_dir = self.orange_next_dir

        elif self.lock_purple and color == "purple":
            current_dir = self.testGhostDirection("purple")

        else:
            current_dir = ghost.getDirection()

        ghost_x_change = 0
        ghost_y_change = 0

        if current_dir == "up":
            ghost_x_change = 0
            ghost_y_change = -self.change_rate
        elif current_dir == "down":
            ghost_x_change = 0
            ghost_y_change = self.change_rate
        elif current_dir == "right":
            ghost_x_change = self.change_rate
            ghost_y_change = 0
        elif current_dir == "left":
            ghost_x_change = -self.change_rate
            ghost_y_change = 0

        ghost.setX(ghost.getX() + ghost_x_change)
        ghost.setY(ghost.getY() + ghost_y_change)

        # Verifica a coolisão com o Pacman

        dist = self.calcDist(self.pacman.getX(), self.pacman.getY(), ghost.getX(), ghost.getY())
        if dist < 20:
            pacman_collision = True
            new_direction = "pac"

        if not pacman_collision:

            # Verifica as bordas.

            if ghost.getX() > self.boundarie_x_pacman:
                ghost.setX(ghost.getX() - ghost_x_change)
                aux = self.directions_available[:]
                aux.remove(current_dir)
                new_direction = choice(aux)
                border_collision = True

                # if self.lock_red:
                #     #print("Direção do Juiz Falhou. Nova direção: " + new_direction)

            elif ghost.getX() < self.boundarie_maze:
                ghost.setX(self.boundarie_maze)
                aux = self.directions_available[:]
                aux.remove(current_dir)
                new_direction = choice(aux)
                border_collision = True

                # if self.lock_red:
                #     #print("Direção do Juiz Falhou. Nova direção: " + new_direction)

            if ghost.getY() > self.boundarie_y_pacman:
                ghost.setY(ghost.getY() - ghost_y_change)
                aux = self.directions_available[:]
                aux.remove(current_dir)
                new_direction = choice(aux)
                border_collision = True

                # if self.lock_red:
                #     #print("Direção do Juiz Falhou. Nova direção: " + new_direction)

            elif ghost.getY() < self.boundarie_maze:
                ghost.setY(self.boundarie_maze)
                aux = self.directions_available[:]
                aux.remove(current_dir)
                new_direction = choice(aux)
                border_collision = True

                # if self.lock_red:
                #     print("Direção do Juiz Falhou. Nova direção: " + new_direction)

            if not border_collision:

                # Verifica a colisão com barreiras

                if self.ghost_barrier_colision(ghost):
                    ghost.setX(ghost.getX() - ghost_x_change)
                    ghost.setY(ghost.getY() - ghost_y_change)
                    aux = self.directions_available[:]
                    aux.remove(current_dir)
                    new_direction = choice(aux)

                    # if self.lock_red:
                    #     #print("Direção do Juiz Falhou. Nova direção: " + new_direction)

                else:

                    new_direction = current_dir

        return ghost.getX(), ghost.getY(), new_direction


    def calcDist(self, g_x, g_y, p_x, p_y):

        return math.sqrt(math.pow((g_x - p_x), 2.0) + math.pow((g_y - p_y), 2.0))

    def ghost_barrier_colision(self, ghost):

        if ghost.getX() > self.barrier_points1[1980][0]:
            b_points = self.barrier_points2
        else:
            b_points = self.barrier_points1

        for i in b_points:
            dist = self.calcDist(ghost.getX(), ghost.getY(), i[0], i[1])
            if dist < 25.0:
                return True
        return False

    def testGhostDirection(self, color):

        if color == "red":
            ghost = copy(self.red_ghost)
        elif color == "purple":
            ghost = copy(self.purple_ghost)

        ghost_x = ghost.getX()
        ghost_y = ghost.getY()

        pac_x = self.pacman.getX()
        pac_y = self.pacman.getY()

        new_direction = ""

        current_distance = self.calcDist(pac_x, pac_y, ghost_x, ghost_y)

        smaller = current_distance

        # Testa para a direita

        aux = ghost_x + self.change_rate

        new_distance = self.calcDist(pac_x, pac_y, aux, ghost_y)

        if new_distance < smaller:

            smaller = new_distance
            new_direction = "right"

        # Testa para a Esquerda

        aux = ghost_x - self.change_rate

        new_distance = self.calcDist(pac_x, pac_y, aux, ghost_y)

        if new_distance < smaller:

            smaller = new_distance
            new_direction = "left"

        # Testa para cima

        aux = ghost_y - self.change_rate

        new_distance = self.calcDist(pac_x, pac_y, ghost_x, aux)

        if new_distance < smaller:

            smaller = new_distance
            new_direction = "up"

        # Testa para baixo

        aux = ghost_y + self.change_rate

        new_distance = self.calcDist(pac_x, pac_y, ghost_x, aux)

        if new_distance < smaller:

            new_direction = "down"

        return new_direction