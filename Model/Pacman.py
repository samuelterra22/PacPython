# coding=utf-8
from Controller.AFDController import AFDController

class Pacman(object):

    def __init__(self):

        self.radius = 13
        self.color = (255, 255, 0) # Amarelo
        self.afd = self.build_afd()
        self.x = 0
        self.y = 0
        self.current_direction = "None"
        self.capsules_earned = 0

    def build_afd(self):
        pac_controller = AFDController()
        return pac_controller.load("AFDS/pacman.jff")

    def getRadius(self):
        return self.radius

    def getColor(self):
        return self.color

    def getAFD(self):
        return self.afd

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getDirection(self):
        return self.current_direction

    def setDirection(self, dir):
        self.current_direction = dir

    def getCapsules(self):
        return self.capsules_earned

    def setCapsules(self, capsules):
        self.capsules_earned = capsules

    def setX(self, x):
         self.x = x

    def setY(self, y):
         self.y = y

    def setInitialPosition(self, x, y):
        self.x = x
        self.y = y



