# coding=utf-8
from Controller.AFDController import AFDController

class Pacman(object):

    def __init__(self):

        self.pacman_radius = 13
        self.pacman_color = (255, 255, 0) # Amarelo
        self.pacman_afd = self.build_afd()
        self.pacman_x = 0
        self.pacman_y = 0
        self.pacman_current_direction = "None"
        self.pacman_capsules_earned = 0

    def build_afd(self):
        pac_controller = AFDController()
        return pac_controller.load("AFDS/pacman.jff")

    def getRadius(self):
        return self.pacman_radius

    def getColor(self):
        return self.pacman_color

    def getAFD(self):
        return self.pacman_afd

    def getX(self):
        return self.pacman_x

    def getY(self):
        return self.pacman_y

    def getDirection(self):
        return self.pacman_current_direction

    def setDirection(self, dir):
        self.pacman_current_direction = dir

    def getCapsules(self):
        return self.pacman_capsules_earned

    def setCapsules(self, capsules):
        self.pacman_capsules_earned = capsules

    def setX(self, x):
         self.pacman_x = x

    def setY(self, y):
         self.pacman_y = y



