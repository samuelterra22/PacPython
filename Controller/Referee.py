# -*- coding: utf-8 -*-
import pygame, math, random, time
import threading as Threads
from Controller.AFDController import AFDController
from Model.Pacman import Pacman
from Model.Ghost import Ghost

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

        self.change_rate = 10
        self.fps = 15

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

        # Inicializa um Pacman!!

        self.pacman = Pacman()

        # Inicializa os fantasmas

        self.red_ghost = Ghost(self.red)
        self.blue_ghost = Ghost(self.blue)
        self.orange_ghost = Ghost(self.orange)
        self.purple_ghost = Ghost(self.purple)


        # Controller dos Autômatos

        self.aut_controller = AFDController()

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

    def ghosts_automata(self, afd):

        while not self.game_exit:

            if self.walk:
                if self.trans_pac_counter == 0:
                    self.trans_pac_counter = self.aut_controller.move(self.pacman.getAFD(), 0,
                                                                      self.pacman.getDirection())
                else:
                    self.trans_pac_counter = self.aut_controller.move(self.pacman.getAFD(),
                                                                      self.trans_pac_counter,
                                                                      self.pacman.getDirection())

                    # print("Estado: " + str(self.trans_pac_counter))

                    # Fim do Jogo

    # -------- Looping principal do jogo -------- #

    def thread_trigger(self):

        # Dispara as Threads

        # Thread AFD pacman

        t_pacman = Threads.Thread(target=self.pacman_automata, args=())

        # Thread Game Loop

        t_game = Threads.Thread(target=self.gameLoop, args=())

        t_game.start()
        t_pacman.start()

    def gameLoop(self):

        pygame.init()

        # Limite das bordas do labirinto

        boundarie_maze = self.pacman.getRadius() + self.border_width_game

        # Posições iniciais do Pac-Man

        self.pacman.setX(boundarie_maze)
        self.pacman.setY(self.height_game - boundarie_maze)

        # Posições Iniciais dos Ghosts

        self.red_ghost.setX(329)
        self.red_ghost.setY(265)

        self.blue_ghost.setX(365)
        self.blue_ghost.setY(265)

        self.orange_ghost.setX(400)
        self.orange_ghost.setY(265)

        self.purple_ghost.setX(435)
        self.purple_ghost.setY(265)

        # Limites até onde o pacman pode alcançar

        boundarie_x_pacman = self.width_game - boundarie_maze
        boundarie_y_pacman = self.height_game - boundarie_maze

        # Variáveis para a mudança de posição do pacman

        pacman_x_change = 0
        pacman_y_change = 0
        able = True
        aux_x = -1
        aux_y = -1

        #Inicializa as Capsulas

        capsules = []
        dist_capsules = 20

        for i in range(0,17):
            capsules.append(((self.pacman.getX() + dist_capsules), boundarie_y_pacman))
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

        # Barreiras

        barriers = [(100, 50, 500, 50), (60, 540, 300, 540), (360, 510, 460, 510), (410, 510, 410, 550), (510, 520, 660, 520), (730, 580, 730, 450),
                    (5, 480, 70, 480), (135, 542, 135, 440), (200, 416, 300, 416), (200, 480, 250, 480), (359, 347, 460, 347), (408, 354, 408, 450),
                    (505, 412, 595, 412), (654, 523, 654, 460), (580, 518, 580, 468), (688, 344, 688, 244), (553, 286, 688, 286), (300, 280, 300, 200),
                    (292, 280, 470, 280), (470, 288, 470, 200), (145, 203, 145, 303), (207, 203, 247, 203), (526, 286, 556, 286), (123, 360, 293, 360),
                    (52, 414, 52, 134), (141, 110, 240, 110), (146, 170, 200, 170), (562, 52, 780, 52), (294, 114, 400, 114), (474, 136, 474, 66),
                    (541, 163, 700, 163), (620, 166, 620, 266), (750, 112, 780, 112), (750, 335, 750, 200)]

        # Todos os pontos do mapa que contém um obstáculo

        barrier_points = []


        for i in barriers:

            # Barreira Horizontal

            if i[1] == i[3]:
                if i[0] > i[2]:
                    for x in range(i[2], i[0]+1):
                        barrier_points.append((x,i[1]))
                else:
                    for x in range(i[0], i[2] + 1):
                        barrier_points.append((x, i[1]))

            #  Barreira Vertical

            if i[0] == i[2]:
                if i[1] > i[3]:
                    for y in range(i[3], i[1] + 1):
                        barrier_points.append((i[0], y))
                else:
                    for y in range(i[1], i[3] + 1):
                        barrier_points.append((i[0], y))


        while not self.game_exit:
            for event in pygame.event.get():
                # print(event)
                if event.type == pygame.QUIT:
                    self.game_exit = True
                elif event.type == pygame.KEYDOWN:
                    self.walk = True
                    if event.key == pygame.K_LEFT:
                        pacman_x_change = -self.change_rate
                        pacman_y_change = 0
                        self.pacman.setDirection("left")
                        if aux_x > -1:
                            test_dist = self.calcDist(self.pacman.getX() + pacman_x_change, self.pacman.getY(), aux_x, aux_y)
                            if test_dist > 19.0:
                                able = True

                    elif event.key == pygame.K_RIGHT:
                        pacman_x_change = self.change_rate
                        pacman_y_change = 0
                        self.pacman.setDirection("right")
                        if aux_x > -1:
                            test_dist = self.calcDist(self.pacman.getX() + pacman_x_change, self.pacman.getY(), aux_x, aux_y)
                            if test_dist > 19.0:
                                able = True

                    elif event.key == pygame.K_UP:
                        pacman_y_change = -self.change_rate
                        pacman_x_change = 0
                        self.pacman.setDirection("up")
                        if aux_x > -1:
                            test_dist = self.calcDist(self.pacman.getX(), self.pacman.getY() + pacman_y_change, aux_x, aux_y)
                            if test_dist > 19.0:
                                able = True

                    elif event.key == pygame.K_DOWN:
                        pacman_y_change = self.change_rate
                        pacman_x_change = 0
                        self.pacman.setDirection("down")
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

            if self.pacman.getX() > boundarie_x_pacman:
                self.pacman.setX(boundarie_x_pacman)
            elif self.pacman.getX() < boundarie_maze:
                self.pacman.setX(boundarie_maze)

            if self.pacman.getY() > boundarie_y_pacman:
                self.pacman.setY(boundarie_y_pacman)
            elif self.pacman.getY() < boundarie_maze:
                self.pacman.setY(boundarie_maze)

            # Verifica a coolisão com barreiras.

            for i in barrier_points:
                dist = self.calcDist(self.pacman.getX(), self.pacman.getY(), i[0], i[1])
                if dist < 19.0:
                    pacman_y_change = 0
                    pacman_x_change = 0
                    able = False
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

            self.draw_game(capsules, barriers)

        # End While
        pygame.quit()
        quit()

    def calcDist(self, g_x, g_y, p_x, p_y):

        return math.sqrt(math.pow((g_x - p_x), 2.0) + math.pow((g_y - p_y), 2.0))

    # def testDirection(self, ghost, pacman):
    #
    #     p_x, p_y = self.getPacmanPosition(pacman)
    #     g_x, g_y = self.getGhostPosition(ghost)
    #     current_dist = self.calcDist(g_x, g_y, p_x, p_y)
    #
    #     smaller = current_dist
    #     new_direction = ""
    #
    #     # Para a direita:
    #
    #     aux_x = g_x + 1.0
    #     aux_y = g_y
    #
    #     new_dist = self.calcDist(aux_x, aux_y, p_x, p_y)
    #
    #     if new_dist < smaller:
    #         smaller = new_dist
    #         new_direction = "r"
    #
    #     # Para a esquerda:
    #
    #     aux_x = g_x - 1.0
    #     aux_y = g_y
    #
    #     new_dist = self.calcDist(aux_x, aux_y, p_x, p_y)
    #
    #     if new_dist < smaller:
    #         smaller = new_dist
    #         new_direction = "l"
    #
    #     # Para baixo:
    #
    #     aux_x = g_x
    #     aux_y = g_y - 1.0
    #
    #     new_dist = self.calcDist(aux_x, aux_y, p_x, p_y)
    #
    #     if new_dist < smaller:
    #         smaller = new_dist
    #         new_direction = "d"
    #
    #     # Para cima:
    #
    #     aux_x = g_x
    #     aux_y = g_y + 1.0
    #
    #     new_dist = self.calcDist(aux_x, aux_y, p_x, p_y)
    #
    #     if new_dist < smaller:
    #         smaller = new_dist
    #         new_direction = "d"
    #
    #     return smaller, new_direction
