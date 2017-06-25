# -*- coding: utf-8 -*-
import pygame, math, time
import threading as Threads
from Controller.AFDController import AFDController
from Model.Pacman import Pacman
from Model.Ghost import Ghost
from Controller.ScreenControl import ScreenControl
from random import choice
from copy import copy
from Model.Fruits import Fruits

class Referee(object):

    def __init__(self):

        # -------- Inicializando Variáveis -------- #

        # Comando de parada do jogo

        self.game_exit = False

        # Elementos da Tela
        self.Screen = ScreenControl()

        self.gameDisplay = self.Screen.buildDisplay()

        # Powerfull fruits
        self.banana = Fruits(640, 195, "banana")
        self.cherry = Fruits(170, 190, "cherry")
        self.pineaple = Fruits(282, 490, "pineaple")

        self.fruits = [self.banana, self.cherry, self.pineaple]

        # Inicializa um Pacman

        self.pacman = Pacman()

        # Inicializa os fantasmas

        self.red_ghost = Ghost("red")  # De 5 em 5 segundos recebe a posição do pacman (absoluta)
        self.blue_ghost = Ghost("blue")  # Random
        self.orange_ghost = Ghost("orange")  # Sempre que o pacman muda de direção ele copia a direção contrária!
        self.purple_ghost = Ghost("purple")  # Vai na direção do pacman

        self.ghost_list = [self.red_ghost, self.blue_ghost, self.orange_ghost, self.purple_ghost]

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

        # Capsulas
        self.capsules = self.Screen.build_capsules()

        # Coordenadas das Barreiras
        self.barrier_points, self.barrier_points1, self.barrier_points2 = self.Screen.build_barrier_points()

        self.barriers = self.Screen.barriers

        # Vidas
        self.lifes = self.Screen.lifes

    def endGame(self, status):

        if status == "win":

            count = 5
            blink = False
            pygame.mixer.music.load(open("Sounds/flawless_victory.wav", "rb"))
            pygame.mixer.music.play()
            while count > 0:
                blink = not blink
                if blink:
                    font = pygame.font.SysFont(None, 40)
                    phrase = "YOU WIN!!!!"
                    screen_text = font.render(phrase, True, self.Screen.green)
                    self.gameDisplay.blit(screen_text, [348, 644])
                    pygame.display.update()
                    time.sleep(0.7)
                    count -= 1
                self.draw_game(self.capsules, self.barriers)
            # self.game_exit = True
        else:

            count = 5
            blink = False
            pygame.mixer.music.load(open("Sounds/oh_shit.wav", "rb"))
            pygame.mixer.music.play()
            while count > 0:
                blink = not blink
                if blink:
                    font = pygame.font.SysFont(None, 40)
                    phrase = "YOU LOOOOOSE!!!!"
                    screen_text = font.render(phrase, True, self.Screen.red)
                    self.gameDisplay.blit(screen_text, [348, 644])
                    pygame.display.update()
                    time.sleep(0.7)
                    count -= 1
                self.draw_game(self.capsules, self.barriers)
            # self.game_exit = True

    # ------- * Construtor da lista de barreiras do labirinto ------- * #

    def playKillSound(self):

        ghosts_remaining = len(self.ghost_list)

        if ghosts_remaining == 3:
            pygame.mixer.music.load(open("Sounds/first_blood.wav", "rb"))
            pygame.mixer.music.play()

        elif ghosts_remaining == 2:
            pygame.mixer.music.load(open("Sounds/killing_spree.wav", "rb"))
            pygame.mixer.music.play()

        elif ghosts_remaining == 1:
            pygame.mixer.music.load(open("Sounds/monster_kill.wav", "rb"))
            pygame.mixer.music.play()

        elif ghosts_remaining == 0:
            pygame.mixer.music.load(open("Sounds/wicked_sick.wav", "rb"))
            pygame.mixer.music.play()

    def setInitialPositions(self):

        # Posições iniciais do Pac-Man

        self.pacman.setInitialPosition()

        # Seta as posições iniciais dos ghosts

        self.red_ghost.setInitialPosition("red")
        self.blue_ghost.setInitialPosition("blue")
        self.orange_ghost.setInitialPosition("orange")
        self.purple_ghost.setInitialPosition("purple")

    # -------- Contador do Placar -------- #

    def score_counter(self):

        font = pygame.font.SysFont(None, 25)
        score = "Score: " + str(self.pacman.getCapsules())
        screen_text = font.render(score, True, self.Screen.green)
        self.gameDisplay.blit(screen_text, [5, 680])

    def life_counter(self):

        font = pygame.font.SysFont(None, 25)
        score = "Lifes: "
        x = 67
        for i in self.lifes:
            self.gameDisplay.blit(i, (x, 625))
            x += 20
        screen_text = font.render(score, True, self.Screen.yellow)
        self.gameDisplay.blit(screen_text, [7, 627])

    # -------- Desenha o jogo, atualizando as posições -------- #

    def draw_game(self, capsules, barriers):

        # Pinta o fundo da tela de preto

        self.gameDisplay.fill(self.Screen.black)

        # Desenha as capsulas

        for i in capsules:
            pygame.draw.circle(self.gameDisplay, self.Screen.yellow, (int(i[0]),int(i[1])), self.Screen.capsule_radius, 0)

        # Desenha as Barriers

        for i in barriers:
            pygame.draw.line(self.gameDisplay, self.Screen.blue,(i[0],i[1]),(i[2],i[3]),17)

        # Desenha o Pacman

        pygame.draw.circle(self.gameDisplay, self.pacman.getColor(), (self.pacman.getX(), self.pacman.getY()), self.pacman.getRadius())

        # Desenha as bordas

        pygame.draw.line(self.gameDisplay, self.Screen.white, (0, 0), (0, self.Screen.height_game), self.Screen.border_width_game)
        pygame.draw.line(self.gameDisplay, self.Screen.white, (0, 0), (self.Screen.width_game, 0), self.Screen.border_width_game)
        pygame.draw.line(self.gameDisplay, self.Screen.white, (0, self.Screen.height_game), (self.Screen.width_game, self.Screen.height_game), self.Screen.border_width_game)
        pygame.draw.line(self.gameDisplay, self.Screen.white, (self.Screen.width_game, 0), (self.Screen.width_game, self.Screen.height_game), self.Screen.border_width_game)

        # Desenha o placar

        self.score_counter()

        # Desenha o contador de vidas

        self.life_counter()

        # Desenha os fantasmas

        for i in self.ghost_list:
            self.gameDisplay.blit(i.getImage(), (i.getX(), i.getY()))

        # Desenha as frutas

        for i in self.fruits:
            self.gameDisplay.blit(i.getImage(), (i.getX(), i.getY()))

        pygame.display.update()

        # FPS

        self.Screen.clock.tick(self.Screen.fps)

    # -------- Executa o autômato do Pac-man -------- #

    def pacman_automata(self):

        # Se o pacman andou, o estado muda

        while not self.game_exit:

            if self.walk:
                self.pacman.setState(self.aut_controller.move(self.pacman.getAFD(),
                                     self.pacman.getState(), self.pacman.getDirection()))

        # Fim do Jogo

    def red_automata(self):

        while not self.go_ghosts:
            pass

        while not self.game_exit:

            self.Screen.clock.tick(self.Screen.fps_ghosts)

            if not self.lock_red:

                new_x, new_y, new_direction = self.move_ghosts("red")

                self.red_ghost.setDirection(new_direction)
                self.red_ghost.setX(new_x)
                self.red_ghost.setY(new_y)

                self.red_ghost.setState(self.aut_controller.move(self.red_ghost.getAFD(),
                                                                 self.red_ghost.getState(),
                                                                 self.red_ghost.getDirection()))
            if self.red_ghost.getDirection() == "pac":

                if not self.fruit_power:

                    if len(self.lifes) > 0:
                        del self.lifes[len(self.lifes)-1]
                        pygame.mixer.music.load(open("Sounds/kill_pacman.wav", "rb"))
                        pygame.mixer.music.play()
                        self.setInitialPositions()

                    else:
                        self.game_exit = True
                        self.endGame("lose")
                else:
                    self.ghost_list.remove(self.red_ghost)
                    self.playKillSound()
                    break

        # Fim do Jogo

    def blue_automata(self):

        while not self.go_ghosts:
            pass

        while not self.game_exit:

            self.Screen.clock.tick(self.Screen.fps_ghosts)

            new_x, new_y, new_direction = self.move_ghosts("blue")

            self.blue_ghost.setDirection(new_direction)
            self.blue_ghost.setX(new_x)
            self.blue_ghost.setY(new_y)

            self.blue_ghost.setState(self.aut_controller.move(self.blue_ghost.getAFD(),
                                                              self.blue_ghost.getState(),
                                                              self.blue_ghost.getDirection()))
            if self.blue_ghost.getDirection() == "pac":
                if not self.fruit_power:

                    if len(self.lifes) > 0:
                        del self.lifes[len(self.lifes)-1]
                        pygame.mixer.music.load(open("Sounds/kill_pacman.wav", "rb"))
                        pygame.mixer.music.play()
                        self.setInitialPositions()
                    else:
                        self.game_exit = True
                        self.endGame("lose")
                else:
                    self.ghost_list.remove(self.blue_ghost)
                    self.playKillSound()
                    break
        # Fim do Jogo

    def orange_automata(self):

        while not self.go_ghosts:
            pass

        while not self.game_exit:

            self.Screen.clock.tick(self.Screen.fps_ghosts)

            new_x, new_y, new_direction = self.move_ghosts("orange")

            self.orange_ghost.setDirection(new_direction)
            self.orange_ghost.setX(new_x)
            self.orange_ghost.setY(new_y)
            self.lock_orange = False

            self.orange_ghost.setState(self.aut_controller.move(self.orange_ghost.getAFD(),
                                                                self.orange_ghost.getState(),
                                                                self.orange_ghost.getDirection()))
            if self.orange_ghost.getDirection() == "pac":
                if not self.fruit_power:

                    if len(self.lifes) > 0:
                        del self.lifes[len(self.lifes)-1]
                        pygame.mixer.music.load(open("Sounds/kill_pacman.wav", "rb"))
                        pygame.mixer.music.play()
                        self.setInitialPositions()
                    else:
                        self.game_exit = True
                        self.endGame("lose")
                else:
                    self.ghost_list.remove(self.orange_ghost)
                    self.playKillSound()
                    break
                    # Fim do Jogo

    def purple_automata(self):

        while not self.go_ghosts:
            pass

        while not self.game_exit:

            self.Screen.clock.tick(self.Screen.fps_ghosts)

            if not self.lock_purple:
                new_x, new_y, new_direction = self.move_ghosts("purple")

                self.purple_ghost.setDirection(new_direction)
                self.purple_ghost.setX(new_x)
                self.purple_ghost.setY(new_y)

                self.purple_ghost.setState(self.aut_controller.move(self.purple_ghost.getAFD(),
                                                                    self.purple_ghost.getState(),
                                                                    self.purple_ghost.getDirection()))
            if self.purple_ghost.getDirection() == "pac":
                if not self.fruit_power:

                    if len(self.lifes) > 0:
                        del self.lifes[len(self.lifes)-1]
                        pygame.mixer.music.load(open("Sounds/kill_pacman.wav", "rb"))
                        pygame.mixer.music.play()
                        self.setInitialPositions()
                    else:
                        self.game_exit = True
                        self.endGame("lose")
                else:
                    self.ghost_list.remove(self.purple_ghost)
                    self.playKillSound()
                    break
        # Fim do Jogo

    def control_direction(self, color):

        while not self.game_exit:

            if color == "red":
                self.lock_red = False

                time.sleep(5)

                self.lock_red = True
                new_x, new_y, new_direction = self.move_ghosts("red")
                self.red_ghost.setDirection(new_direction)
                self.red_ghost.setX(new_x)
                self.red_ghost.setY(new_y)

            elif color == "purple":

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

                for g in self.ghost_list:
                    g.setImage("white")

                time.sleep(10)

                self.red_ghost.setImage("red")
                self.blue_ghost.setImage("blue")
                self.orange_ghost.setImage("orange")
                self.purple_ghost.setImage("purple")

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

        t_control_red = Threads.Thread(target=self.control_direction, args=("red",))

        t_control_purple = Threads.Thread(target=self.control_direction, args=("purple",))

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

        self.setInitialPositions()

        # Variáveis para a mudança de posição do pacman

        pacman_x_change = 0
        pacman_y_change = 0

        able = True
        aux_x = -1
        aux_y = -1

    # Loop do jogo
        x_pressed = False
        while not self.game_exit:
            self.go_ghosts = True
            if self.pacman.getCapsules() == 155:
                self.game_exit = True
                self.endGame("win")
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.game_exit = True
                        x_pressed = True
                    elif event.type == pygame.KEYDOWN:
                        self.walk = True
                        if event.key == pygame.K_LEFT:
                            pacman_x_change = -self.Screen.change_rate
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
                            pacman_x_change = self.Screen.change_rate
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
                            pacman_y_change = -self.Screen.change_rate
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
                            pacman_y_change = self.Screen.change_rate
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

                if self.pacman.getX() > self.Screen.boundarie_x_pacman:
                    self.pacman.setX(self.Screen.boundarie_x_pacman)
                    self.walk = False
                elif self.pacman.getX() < self.Screen.boundarie_maze_g:
                    self.pacman.setX(self.Screen.boundarie_maze_g)
                    self.walk = False
                if self.pacman.getY() > self.Screen.boundarie_y_pacman:
                    self.pacman.setY(self.Screen.boundarie_y_pacman)
                    self.walk = False
                elif self.pacman.getY() < self.Screen.boundarie_maze_g:
                    self.pacman.setY(self.Screen.boundarie_maze_g)
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
                    if dist < float(self.pacman.getRadius() + self.Screen.capsule_radius):
                        self.pacman.setCapsules(self.pacman.getCapsules() + 1)
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
        if x_pressed:
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
            ghost_y_change = -self.Screen.change_rate
        elif current_dir == "down":
            ghost_x_change = 0
            ghost_y_change = self.Screen.change_rate
        elif current_dir == "right":
            ghost_x_change = self.Screen.change_rate
            ghost_y_change = 0
        elif current_dir == "left":
            ghost_x_change = -self.Screen.change_rate
            ghost_y_change = 0

        ghost.setX(ghost.getX() + ghost_x_change)
        ghost.setY(ghost.getY() + ghost_y_change)

        # Verifica a coolisão com o Pacman
    
        dist = self.calcDist(self.pacman.getX(), self.pacman.getY(), ghost.getX(), ghost.getY())
        if dist < 18:
            pacman_collision = True
            new_direction = "pac"

        if not pacman_collision:

            # Verifica as bordas.

            if ghost.getX() > self.Screen.boundarie_x_pacman:
                ghost.setX(ghost.getX() - ghost_x_change)
                aux = self.Screen.directions_available[:]
                aux.remove(current_dir)
                new_direction = choice(aux)
                border_collision = True

            elif ghost.getX() < self.Screen.boundarie_maze:
                ghost.setX(self.Screen.boundarie_maze)
                aux = self.Screen.directions_available[:]
                aux.remove(current_dir)
                new_direction = choice(aux)
                border_collision = True

            if ghost.getY() > self.Screen.boundarie_y_pacman:
                ghost.setY(ghost.getY() - ghost_y_change)
                aux = self.Screen.directions_available[:]
                aux.remove(current_dir)
                new_direction = choice(aux)
                border_collision = True

            elif ghost.getY() < self.Screen.boundarie_maze:
                ghost.setY(self.Screen.boundarie_maze)
                aux = self.Screen.directions_available[:]
                aux.remove(current_dir)
                new_direction = choice(aux)
                border_collision = True

            if not border_collision:

                # Verifica a colisão com barreiras

                if self.ghost_barrier_colision(ghost):
                    ghost.setX(ghost.getX() - ghost_x_change)
                    ghost.setY(ghost.getY() - ghost_y_change)
                    aux = self.Screen.directions_available[:]
                    aux.remove(current_dir)
                    new_direction = choice(aux)

                else:
                    new_direction = current_dir
        
        return ghost.getX(), ghost.getY(), new_direction

    def calcDist(self, g_x, g_y, p_x, p_y):

        return math.sqrt(math.pow((g_x - p_x), 2.0) + math.pow((g_y - p_y), 2.0))

    def ghost_barrier_colision(self, ghost):

        if ghost.getX() > self.barrier_points1[1962][0]:
            b_points = self.barrier_points2
        else:
            b_points = self.barrier_points1

        for i in b_points:
            dist = self.calcDist(ghost.getX(), ghost.getY(), i[0], i[1])
            if dist < 25.0:
                return True
        return False

    def testGhostDirection(self, color):

        ghost = None

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

        aux = ghost_x + self.Screen.change_rate

        new_distance = self.calcDist(pac_x, pac_y, aux, ghost_y)

        if new_distance < smaller:

            smaller = new_distance
            new_direction = "right"

        # Testa para a Esquerda

        aux = ghost_x - self.Screen.change_rate

        new_distance = self.calcDist(pac_x, pac_y, aux, ghost_y)

        if new_distance < smaller:

            smaller = new_distance
            new_direction = "left"

        # Testa para cima

        aux = ghost_y - self.Screen.change_rate

        new_distance = self.calcDist(pac_x, pac_y, ghost_x, aux)

        if new_distance < smaller:

            smaller = new_distance
            new_direction = "up"

        # Testa para baixo

        aux = ghost_y + self.Screen.change_rate

        new_distance = self.calcDist(pac_x, pac_y, ghost_x, aux)

        if new_distance < smaller:

            new_direction = "down"

        return new_direction