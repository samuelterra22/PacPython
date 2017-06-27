# -*- coding: utf-8 -*-
"""
*************************************************************************************************
*                   Trabalho 02 - Linguagens Formais e Autômatos Finitos                        *
*                                                                                               *
*   @teacher: Walace Rodrigues                                                                  *
*   @author: Matheus Calixto - ⁠⁠⁠0011233                                                          *
*   @author: Samuel Terra    - 0011946                                                          *
*   @lastUpdate: 27/06/2017                                                                     *
*                                                                                               *
*************************************************************************************************
"""

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

        # Display do jogo

        self.gameDisplay = self.Screen.buildDisplay()

        # Frutas que dão poder ao Pac-Man

        self.banana = Fruits(640, 195, "banana")
        self.cherry = Fruits(170, 190, "cherry")
        self.pineaple = Fruits(282, 490, "pineaple")

        self.fruits = [self.banana, self.cherry, self.pineaple]

        # Inicializa um Pacman

        self.pacman = Pacman()

        # Inicializa os fantasmas

        self.red_ghost = Ghost("red")
        self.blue_ghost = Ghost("blue")
        self.orange_ghost = Ghost("orange")
        self.purple_ghost = Ghost("purple")

        self.ghost_list = [self.red_ghost, self.blue_ghost, self.orange_ghost, self.purple_ghost]

        # Flag que controla se o pacman anda ou não.

        self.walk = False

        # Flag de inicio dos fantasmas

        self.go_ghosts = False

        # Flags que travam a escolha da direção dos fantasmas quando o árbitro envia um sinal

        self.lock_red = False
        self.lock_orange = False
        self.lock_purple = False

        # Flag que controla quando o Pac-Man está sob efeito de seu poder oculto

        self.fruit_power = False

        # Próxima direção do fantasma laranja depois do Pac-man se movimentar

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

    def thread_trigger(self):

        # Função que dispara as Threads para o controle do jogo

        # Thread AFD pacman

        t_pacman = Threads.Thread(target=self.pacman_automata, args=())

        # Thread para o Looping do jogo

        t_game = Threads.Thread(target=self.gameLoop, args=())

        # Thread para os fantasmas

        t_red = Threads.Thread(target=self.red_automata, args=())

        t_blue = Threads.Thread(target=self.blue_automata, args=())

        t_orange = Threads.Thread(target=self.orange_automata, args=())

        t_purple = Threads.Thread(target=self.purple_automata, args=())

        # Thread para o controle dos sinais enviados pelo árbitro

        t_control_red = Threads.Thread(target=self.control_direction, args=("red",))

        t_control_purple = Threads.Thread(target=self.control_direction, args=("purple",))

        # Thread para controlar o efeito do poder oculto do Pac-Man

        # Inicializa-se as Threads

        t_game.start()
        t_pacman.start()
        t_red.start()
        t_blue.start()
        t_orange.start()
        t_purple.start()
        t_control_red.start()
        t_control_purple.start()

    def endGame(self, status):

        # Função que controla o fim do jogo

        # Caso for uma vitória, é reproduzido um som específico de vitória, e na tela é
        # Printada a frase 'YOU WIN!!!!', piscando algumas vezes. Depois disso, o jogo termina.

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

        # Caso for uma derrota, é reproduzido um som específico de derrota, e na tela é
        # Printada a frase 'YOU LOOOOOOSE', piscando algumas vezes. Depois disso, o jogo termina.

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

    def playKillSound(self):

        # Esta função, toca os sons determinados, para a quantidade de mortes
        # que o Pac-Man causou nos fantasmas. A cada fantasma que ele come,
        # um novo som é reproduzido, dando destaque ao feito do mesmo.

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

        # Seta as posições iniciais do Pac-Man e dos fantasmas

        # Posições iniciais do Pac-Man

        self.pacman.setInitialPosition()

        # Seta as posições iniciais dos ghosts

        self.red_ghost.setInitialPosition("red")
        self.blue_ghost.setInitialPosition("blue")
        self.orange_ghost.setInitialPosition("orange")
        self.purple_ghost.setInitialPosition("purple")

    def score_counter(self):

        # Função responsável por exibir na tela o contador das cápsulas
        # comidas pelo Pac-Man

        font = pygame.font.SysFont(None, 25)
        score = "Score: " + str(self.pacman.getCapsules())
        screen_text = font.render(score, True, self.Screen.green)
        self.gameDisplay.blit(screen_text, [5, 680])

    def life_counter(self):

        # Função responsável por mostrar o contador de vidas restantes
        # que o Pac-Man possui.

        font = pygame.font.SysFont(None, 25)
        score = "Lifes: "
        x = 67
        for i in self.lifes:
            self.gameDisplay.blit(i, (x, 625))
            x += 20
        screen_text = font.render(score, True, self.Screen.yellow)
        self.gameDisplay.blit(screen_text, [7, 627])

    def draw_game(self, capsules, barriers):

        # Esta função faz o desenho do cenário, a cada looping do jogo

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

        # Atualiza o 'relógio' do jogo.

        self.Screen.clock.tick(self.Screen.fps)

        # Após os novos desenhos, atualiza o cenário.

        pygame.display.update()

    def pacman_automata(self):

        # Função que executa o automato do Pac-Man

        # Se o pacman andou, o estado muda

        # Enquanto o jogo não termina, executa-se o autômato.
        while not self.game_exit:

            if self.walk:
                self.pacman.setState(self.aut_controller.move(self.pacman.getAFD(),
                                     self.pacman.getState(), self.pacman.getDirection()))
            time.sleep(1)

        # Fim do Jogo

    def red_automata(self):

        # Função que roda o autômato do fantasma vermelho, que se movimenta
        # de acordo com os sinais enviados pelo árbitro de 4 em 4 segundos.
        # O árbitro tem prioridade para definir a direção do ghost. Se ele enviar
        # um sinal, a flag de trava (lock_red) fica ativa.

        # Enquanto a flag de liberação dos fantasmas não estiver ativa, não podem se movimentar

        while not self.go_ghosts:
            pass

        # Deṕois da liberação, o autômato pode rodar.

        while not self.game_exit:

            # Conta o relógio dos fantasmas
            self.Screen.clock.tick(self.Screen.fps_ghosts)

            # Se caso o fantasma vermelho não estiver sob o controle do árbitro, ele
            # recebe suas novas coordenadas, e caminha.

            if not self.lock_red:

                # Recebe suas novas coordenadas e sua nova direção
                new_x, new_y, new_direction = self.move_ghosts("red")

                self.red_ghost.setDirection(new_direction)
                self.red_ghost.setX(new_x)
                self.red_ghost.setY(new_y)

                self.red_ghost.setState(self.aut_controller.move(self.red_ghost.getAFD(),
                                                                 self.red_ghost.getState(),
                                                                 self.red_ghost.getDirection()))
            # Se o fantasma vermelho topar com o Pac-Man, faz-se
            # as verificações:
            if self.red_ghost.getDirection() == "pac":

                # Se o Pac-Man, não está sob efeito do seu poder oculto,
                # o mesmo perde uma vida, e o jogo reinicia com os objetos nas posições
                # iniciais. Se não houverem mais vidas para consumir, o jogo termina e o
                # usuário perdeu! Caso contrário, se o Pac-Man estiver sob efeito de seu
                # poder, ele mata os fantasmas. O fantasma morto desaparece do mapa até o
                # final do jogo!
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

    def blue_automata(self):

        # A lógica do fantasma azul, segue basicamente a mesma lógica dos anteriores;
        # Porém, ele se movimenta de maneira randômica no labirinto.

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

    def orange_automata(self):

        # O fantasma laranja, se movimenta de acordo com a direção que o Pac-Man se movimenta.
        # Nesse caso, é sempre a direção contrária quando o Pac-Man muda de direção.

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

    def purple_automata(self):

        # O fantasma roxo, segue a mesma lógica do fantasma vermelho, porem os sinais
        # são recebidos do árbitro de 2 em 2 segundos.

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

    def control_direction(self, color):

        # Esta função é responsável pelo controle da direção dos fantasmas
        # vermelho e roxo. Depois de um determinado intervalo de tempo, o árbitro
        # define a direção dos fantasmas com base na posição absoluta do Pac-Man
        # esta função tem prioridade para definir a direção.

        while not self.game_exit:

            if color == "red":
                self.lock_red = False

                time.sleep(4)

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

    def gameLoop(self):

        # Esta é a função onde é implementado o movimento do Pac-Man
        # de acordo com as teclas pressionadas pelo usuário.

        power_count = 0
        pygame.init()
        pygame.mixer.init()

        self.setInitialPositions()

        # Variáveis para a mudança de posição do pacman

        pacman_x_change = 0
        pacman_y_change = 0

        able = True
        aux_x = -1
        aux_y = -1

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

                # Verifica o ingerir das frutas. Se o Pac-Man comer uma fruta, um contador é zerado
                # e os fantasmas se transformam, podendo ser então comidos pelo Pac-Man por um
                # determinado período de tempo

                for i in self.fruits:
                    dist = self.calcDist(self.pacman.getX(), self.pacman.getY(), i.getX(), i.getY())
                    if dist < 30.0:
                        self.fruits.remove(i)
                        self.fruit_power = True
                        for g in self.ghost_list:
                            g.setImage("white")
                        power_count = 0
                        break

                # Se o Pac-Man estiver sob efeito do seu poder oculto
                # O contador de "tempo" começa a correr

                if self.fruit_power:
                    power_count += 10

                # Se o contador de 'tempo' chegar a 1000, o Pac-Man perde
                # seu poder e os fantamas voltam ao seu estado natural, podendo
                # comer o Pac-Man

                if power_count == 1000:

                    self.red_ghost.setImage("red")
                    self.blue_ghost.setImage("blue")
                    self.orange_ghost.setImage("orange")
                    self.purple_ghost.setImage("purple")

                    self.fruit_power = False

                # Atualiza o Cenário

                self.draw_game(self.capsules, self.barriers)

        # End While
        if x_pressed:
            pygame.quit()
        quit()

    def move_ghosts(self, color):

        # Esta função testa os movimentos dos fantasmas

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

        # Se o árbitro estiver dando o comando, a direção é definida de acordo
        # com a função que testa as direções possíveis do fantasma, onde ela obtém
        # a direção em que o fantasma fica mais próximo do Pac-Man. Com excessão do
        # fantasma laranja, que se movimenta de acordo com o Pac-Man

        if self.lock_red and color == "red":
            current_dir = self.testGhostDirection("red")

        elif self.lock_orange and color == "orange":
            current_dir = self.orange_next_dir

        elif self.lock_purple and color == "purple":
            current_dir = self.testGhostDirection("purple")

        # Caso contrário, ele pega a direção atual do Pac-Man,
        # e testa qual a direção que ele pode se mover.

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

        # Atualiza a futura posição do fantasma

        ghost.setX(ghost.getX() + ghost_x_change)
        ghost.setY(ghost.getY() + ghost_y_change)

        # Verifica a coolisão com o Pacman
    
        dist = self.calcDist(self.pacman.getX(), self.pacman.getY(), ghost.getX(), ghost.getY())
        if dist < 20:
            pacman_collision = True
            new_direction = "pac"

        if not pacman_collision:

            # Verifica a coolisão com bordas, caso não haja coolisão com o Pac-Man

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

                # Se não houveram coolisões com as bordas,
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

        # Esta função calcula a distância de dois pontos

        return math.sqrt(math.pow((g_x - p_x), 2.0) + math.pow((g_y - p_y), 2.0))

    def ghost_barrier_colision(self, ghost):

        # Esta função realiza o teste de coolisão dos fantasmas com barreiras

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

        # Esta função faz o teste da direção mais próxima do fantasma em relação
        # ao Pac-Man

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