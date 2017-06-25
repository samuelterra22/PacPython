# -*- coding: utf-8 -*-
from Model.Pacman import Pacman
from Model.Ghost import Ghost
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

        # Cápsulas

        self.capsules = []

        # Powerfull Fruits!!

        self.banana = None
        self.cherry = None
        self.pineaple = None

        self.fruits = [self.banana, self.cherry, self.pineaple]

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

        self.red_ghost = Ghost("red")  # De 5 em 5 segundos recebe a posição do pacman (absoluta)
        self.blue_ghost = Ghost("blue")  # Random
        self.orange_ghost = Ghost("orange")  # Sempre que o pacman muda de direção ele copia a direção contrária!
        self.purple_ghost = Ghost("purple")  # Vai na direção do pacman

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