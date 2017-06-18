# -*- coding: utf-8 -*-
import pygame, math, time
import threading as Threads
from Controller.AFDController import AFDController
from Model.Pacman import Pacman
from Model.Ghost import Ghost
from random import choice
from copy import copy

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

        # Inicializa um Pacman!!

        self.pacman = Pacman()

        # Inicializa os fantasmas

        self.red_ghost = Ghost("red") # De 5 em 5 segundos recebe a posição do pacman
        self.blue_ghost = Ghost("blue") # Random
        self.orange_ghost = Ghost("orange") #
        self.purple_ghost = Ghost("purple")

        # Todos os pontos do mapa que contém um obstáculo

        self.barrier_points = []
        self.barrier_points1 = []
        self.barrier_points2 = []

        # FPS e blocos que os elementos móveis se movimentam por vez.

        self.change_rate = 10
        self.fps = 15
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

        # Controller dos Autômatos

        self.aut_controller = AFDController()


    def build_barrier_points(self):

        for i in self.barriers:
            # Barreira Horizontal

            if i[1] == i[3]:
                if i[0] > i[2]:
                    for x in range(i[2], i[0] + 1):
                        self.barrier_points.append((x, i[1]))

                else:
                    for x in range(i[0], i[2] + 1):
                        self.barrier_points.append((x, i[1]))


                        # Barreira Vertical

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

        for i in range(0, 1981):
            self.barrier_points1.append(self.barrier_points[i])

        for i in range(1981, 3962):
            self.barrier_points2.append(self.barrier_points[i])

    # -------- Contador do Placar -------- #

    def score_counter(self):

        font = pygame.font.SysFont(None, 25)
        score = "Score: " + str(self.pacman.getCapsules())
        screen_text = font.render(score, True, self.green)
        self.gameDisplay.blit(screen_text, [5, 650])

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

        # Desenha os fantasmas

        pygame.draw.circle(self.gameDisplay, self.blue_ghost.getColor(), (self.blue_ghost.getX(), self.blue_ghost.getY()), self.blue_ghost.getRadius())
        pygame.draw.circle(self.gameDisplay, self.red_ghost.getColor(), (self.red_ghost.getX(), self.red_ghost.getY()), self.red_ghost.getRadius())
        pygame.draw.circle(self.gameDisplay, self.orange_ghost.getColor(), (self.orange_ghost.getX(), self.orange_ghost.getY()), self.orange_ghost.getRadius())
        pygame.draw.circle(self.gameDisplay, self.purple_ghost.getColor(), (self.purple_ghost.getX(), self.purple_ghost.getY()), self.purple_ghost.getRadius())


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

                #print("Estado: " + str(self.trans_pac_counter))

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
                print("VERMELHO PEGOU!")
                self.game_exit = True
            #print("Estado: " + self.red_ghost.getState())

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
                print("AZUL PEGOU!")
                self.game_exit = True
            print("Estado: " + self.red_ghost.getState())

    # Fim do Jogo

    def orange_automata(self):

        while not self.go_ghosts:
            pass

        while not self.game_exit:

            if self.trans_orange_counter == 0:
                self.trans_orange_counter = self.aut_controller.move(self.pacman.getAFD(), 0,
                                                                    self.pacman.getDirection())
            else:
                self.trans_orange_counter = self.aut_controller.move(self.pacman.getAFD(),
                                                                    self.trans_pac_counter,
                                                                    self.pacman.getDirection())

            # print("Estado: " + str(self.trans_pac_counter))

                # Fim do Jogo

    def purple_automata(self):

        while not self.go_ghosts:
            pass

        while not self.game_exit:

            if self.trans_purple_counter == 0:
                self.trans_purple_counter = self.aut_controller.move(self.pacman.getAFD(), 0,
                                                                    self.pacman.getDirection())
            else:
                self.trans_purple_counter = self.aut_controller.move(self.pacman.getAFD(),
                                                                    self.trans_pac_counter,
                                                                    self.pacman.getDirection())
            # print("Estado: " + str(self.trans_pac_counter))

                # Fim do Jogo
    def control_red(self):

        while not self.game_exit:
            self.lock_red = False

            time.sleep(8)

            self.lock_red = True
            new_x, new_y, new_direction = self.move_ghosts("red")
            self.red_ghost.setDirection(new_direction)
            self.red_ghost.setX(new_x)
            self.red_ghost.setY(new_y)

    # -------- Looping principal do jogo -------- #

    def thread_trigger(self):

        # Dispara as Threads

        # Thread AFD pacman

        t_pacman = Threads.Thread(target=self.pacman_automata, args=())

        # Thread Game Loop

        t_game = Threads.Thread(target=self.gameLoop, args=())

        # Thread para Autômato do fantasma vermelho

        t_red = Threads.Thread(target=self.red_automata, args=())

        t_control_red = Threads.Thread(target=self.control_red, args=())

        t_blue = Threads.Thread(target=self.blue_automata, args=())



        t_game.start()
        t_pacman.start()
        t_red.start()
        t_control_red.start()
        t_blue.start()

    def gameLoop(self):

        pygame.init()
        pygame.mixer.init()

        # Posições iniciais do Pac-Man

        self.pacman.setX(self.boundarie_maze)
        self.pacman.setY(self.height_game - self.boundarie_maze)

        # Posições Iniciais dos Ghosts

        self.red_ghost.setX(340)
        self.red_ghost.setY(265)

        self.blue_ghost.setX(365)
        self.blue_ghost.setY(265)

        self.orange_ghost.setX(400)
        self.orange_ghost.setY(265)

        self.purple_ghost.setX(435)
        self.purple_ghost.setY(265)

        # Variáveis para a mudança de posição do pacman e dos Ghosts

        pacman_x_change = 0
        pacman_y_change = 0

        able = True
        aux_x = -1
        aux_y = -1

        #Inicializa as Capsulas

        capsules = []
        dist_capsules = 20

        for i in range(0,17):
            capsules.append(((self.pacman.getX() + dist_capsules), self.boundarie_y_pacman))
            dist_capsules+= 40

        dist_capsules = 0

        for i in range(0,20):
            capsules.append(((46 + dist_capsules) , 26))
            dist_capsules += 40

        dist_capsules = 0

        for i in range(0,11):
            capsules.append((25,(452 - dist_capsules)))
            capsules.append((85, (25 + dist_capsules)))
            capsules.append((778, (158 + dist_capsules)))
            dist_capsules += 40

        dist_capsules = 0

        for i in range(0,15):
            capsules.append(((132 + dist_capsules),324))
            dist_capsules += 40

        dist_capsules = 0

        for i in range(0,8):
            capsules.append(((456 + dist_capsules), 388))
            capsules.append(((125 + dist_capsules), 85))
            capsules.append(((125 + dist_capsules), 145))

            dist_capsules += 40

        dist_capsules = 0

        for i in range(0,7):
            capsules.append(((376 - dist_capsules), 385))
            capsules.append(((298 + dist_capsules), 473))
            capsules.append(((565 + dist_capsules), 91))
            capsules.append((724, (122 + dist_capsules)))
            dist_capsules += 40

        dist_capsules = 0

        for i in range(0,3):
            capsules.append((526, (49 + dist_capsules)))
            capsules.append((526, (170 + dist_capsules)))
            capsules.append((335, (433 + dist_capsules)))
            capsules.append((173, (424 + dist_capsules)))
            capsules.append(((176 + dist_capsules), 255))
            capsules.append((696, (429 + dist_capsules)))
            capsules.append(((12 + dist_capsules), 509))
            dist_capsules += 40

        # Monta a lista de pontos contendo todos os os obstatculos do game.

        self.build_barrier_points()


        # barriers = [(100, 50, 500, 50), (60, 550, 300, 550), (360, 510, 460, 510), (410, 510, 410, 550),
        #             (510, 520, 660, 520), (730, 580, 730, 450),
        #             (5, 480, 70, 480), (135, 540, 135, 440), (200, 420, 300, 420), (200, 480, 250, 480),
        #             (360, 350, 460, 350), (410, 350, 410, 450),
        #             (505, 410, 595, 410), (650, 520, 650, 460), (580, 520, 580, 470), (670, 345, 670, 245),
        #             (555, 285, 690, 285), (300, 280, 300, 200),
        #             (290, 280, 470, 280), (470, 290, 470, 200), (145, 205, 145, 305), (205, 205, 250, 205),
        #             (525, 285, 555, 285), (125, 360, 295, 360),
        #             (50, 415, 50, 135), (140, 110, 240, 110), (145, 170, 200, 170), (560, 50, 780, 50),
        #             (295, 115, 400, 115), (475, 135, 475, 65),
        #             (540, 165, 700, 165), (620, 165, 620, 265), (750, 110, 780, 110), (750, 335, 750, 200)]


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
                        self.pacman.setDirection("left")
                        # Testa se está tentando atravessar a parede.
                        if aux_x > -1:
                            test_dist = self.calcDist(self.pacman.getX() + pacman_x_change, self.pacman.getY(), aux_x, aux_y)
                            if test_dist > 19.0:
                                able = True

                    elif event.key == pygame.K_RIGHT:
                        pacman_x_change = self.change_rate
                        pacman_y_change = 0
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
                        # Testa se está tentando atravessar a parede.
                        if aux_x > -1:
                            test_dist = self.calcDist(self.pacman.getX(), self.pacman.getY() + pacman_y_change, aux_x, aux_y)
                            if test_dist > 19.0:
                                able = True

                    elif event.key == pygame.K_DOWN:
                        pacman_y_change = self.change_rate
                        pacman_x_change = 0
                        self.pacman.setDirection("down")
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

            if self.pacman.getX() > self.barrier_points1[1980][0]:
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

            for i in capsules:
                dist = self.calcDist(self.pacman.getX(), self.pacman.getY(), i[0], i[1])
                if dist < float(self.pacman.getRadius() + self.capsule_radius):
                    self.pacman.setCapsules(self.pacman.getCapsules() + 1)
                    capsules.remove(i)
                    break


            # Atualiza o Cenário

            self.draw_game(capsules, self.barriers)

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
            current_dir = self.testGhostDirection()
            print("Juiz definiu a direção: " + current_dir)
        else:
            current_dir = ghost.getDirection()


        directions_available = ["up", "down", "left", "right"]
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
        if dist < float(self.red_ghost.getRadius() + self.pacman.getRadius() - 5):
            pacman_collision = True
            new_direction = "pac"

        if not pacman_collision:

            # Verifica as bordas.

            if ghost.getX() > self.boundarie_x_pacman:
                ghost.setX(ghost.getX() - ghost_x_change)
                aux = directions_available[:]
                aux.remove(current_dir)
                new_direction = choice(aux)
                border_collision = True
                if self.lock_red:
                    print("Direção do Juiz Falhou. Nova direção: " + new_direction)

            elif ghost.getX() < self.boundarie_maze:
                ghost.setX(self.boundarie_maze)
                aux = directions_available[:]
                aux.remove(current_dir)
                new_direction = choice(aux)
                border_collision = True
                if self.lock_red:
                    print("Direção do Juiz Falhou. Nova direção: " + new_direction)

            if ghost.getY() > self.boundarie_y_pacman:
                ghost.setY(ghost.getY() - ghost_y_change)
                aux = directions_available[:]
                aux.remove(current_dir)
                new_direction = choice(aux)
                border_collision = True
                if self.lock_red:
                    print("Direção do Juiz Falhou. Nova direção: " + new_direction)

            elif ghost.getY() < self.boundarie_maze:
                ghost.setY(self.boundarie_maze)
                aux = directions_available[:]
                aux.remove(current_dir)
                new_direction = choice(aux)
                border_collision = True
                if self.lock_red:
                    print("Direção do Juiz Falhou. Nova direção: " + new_direction)

            if not border_collision:

                # Verifica a colisão com barreiras

                if self.ghost_barrier_colision(ghost):
                    ghost.setX(ghost.getX() - ghost_x_change)
                    ghost.setY(ghost.getY() - ghost_y_change)
                    aux = directions_available[:]
                    aux.remove(current_dir)
                    new_direction = choice(aux)
                    if self.lock_red:
                        print("Direção do Juiz Falhou. Nova direção: " + new_direction)

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
            if dist < 16.0:
                return True
        return False

    def testGhostDirection(self):

        ghost_x = self.red_ghost.getX()
        ghost_y = self.red_ghost.getY()

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
