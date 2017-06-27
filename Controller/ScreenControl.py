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
import pygame

class ScreenControl(object):

    def __init__(self):

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
                         (294, 114, 400, 114), (474, 100, 474, 66),
                         (541, 163, 700, 163), (620, 166, 620, 266), (750, 112, 780, 112), (750, 335, 750, 200)]

        # Direções disponíveis:

        self.directions_available = ["up", "down", "left", "right"]

        # Vidas

        life = pygame.image.load("Images/pacman.png")

        self.lifes = [life, life, life]

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

        # Largura da borda

        self.border_width_game = 5

        # Limite das bordas do labirinto

        self.boundarie_maze = 18
        self.boundarie_maze_g = 15

        # Limites até onde o pacman pode alcançar

        self.boundarie_x_pacman = self.width_game - self.boundarie_maze
        self.boundarie_y_pacman = self.height_game - self.boundarie_maze

        # Dimensão da cápsula

        self.capsule_radius = 5

        # Clock para definir os Frames por segundo

        self.clock = pygame.time.Clock()

    def build_barrier_points(self):

        barrier_points = []
        barrier_points1 = []
        barrier_points2 = []

        for i in self.barriers:
            # Barreiras Horizontais

            if i[1] == i[3]:
                if i[0] > i[2]:
                    for x in range(i[2], i[0] + 1):
                        barrier_points.append((x, i[1]))
                else:
                    for x in range(i[0], i[2] + 1):
                        barrier_points.append((x, i[1]))

            # Barreiras Verticais

            if i[0] == i[2]:
                if i[1] > i[3]:
                    for y in range(i[3], i[1] + 1):
                        barrier_points.append((i[0], y))
                else:
                    for y in range(i[1], i[3] + 1):
                        barrier_points.append((i[0], y))
                        # Ordena a lista de obstáculos pelo valor de x (x,y)

        barrier_points.sort(key=lambda tup: tup[0])

        # Divide a lista ao meio para acelerar o processamento

        for i in range(0, len(barrier_points) / 2):
            barrier_points1.append(barrier_points[i])

        for i in range(len(barrier_points) / 2, len(barrier_points)):
            barrier_points2.append(barrier_points[i])

        return barrier_points, barrier_points1, barrier_points2

    # ------- * Construtor da lista de cápsulas do labirinto ------- * #

    def build_capsules(self):

        capsules = []
        dist_capsules = 20

        for i in range(0, 17):
            capsules.append(((self.boundarie_maze + dist_capsules), self.boundarie_y_pacman))
            dist_capsules += 40

        dist_capsules = 0

        for i in range(0, 20):
            capsules.append(((46 + dist_capsules), 26))
            dist_capsules += 40

        dist_capsules = 0

        for i in range(0, 11):
            capsules.append((25, (452 - dist_capsules)))
            capsules.append((85, (25 + dist_capsules)))
            capsules.append((778, (158 + dist_capsules)))
            dist_capsules += 40

        dist_capsules = 0

        for i in range(0, 15):
            capsules.append(((132 + dist_capsules), 324))
            dist_capsules += 40

        dist_capsules = 0

        for i in range(0, 8):
            capsules.append(((456 + dist_capsules), 388))
            capsules.append(((125 + dist_capsules), 85))
            capsules.append(((125 + dist_capsules), 145))

            dist_capsules += 40

        dist_capsules = 0

        for i in range(0, 7):
            capsules.append(((376 - dist_capsules), 385))
            capsules.append(((298 + dist_capsules), 473))
            capsules.append(((565 + dist_capsules), 91))
            capsules.append((724, (122 + dist_capsules)))
            dist_capsules += 40

        dist_capsules = 0

        for i in range(0, 3):
            capsules.append((526, (49 + dist_capsules)))
            capsules.append((526, (170 + dist_capsules)))
            capsules.append((335, (433 + dist_capsules)))
            capsules.append((173, (424 + dist_capsules)))
            capsules.append(((176 + dist_capsules), 255))
            capsules.append((696, (429 + dist_capsules)))
            capsules.append(((12 + dist_capsules), 509))
            dist_capsules += 40

        return capsules

    def buildDisplay(self):

        gameDisplay = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("PacPython \o/")

        return gameDisplay