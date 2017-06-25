from Controller.AFDController import AFDController
import pygame

class Ghost(object):


    def __init__(self, color):
        self.radius = 10
        self.color = color
        self.afd = self.build_afd(color)
        self.x = 0
        self.y = 0
        self.current_direction = "up"
        self.state = "0"
        self.image = self.buildImage(color)

    def build_afd(self, color):

        pac_controller = AFDController()
        g_afd = ""

        if color == "red":
            g_afd = "AFDS/red_ghost.jff"

        elif color == "orange":
            g_afd = "AFDS/orange_ghost.jff"

        elif color == "blue":
            g_afd = "AFDS/blue_ghost.jff"

        elif color == "purple":
            g_afd = "AFDS/purple_ghost.jff"

        return pac_controller.load(g_afd)

    def buildImage(self, color):

        img = ""

        if color == "red":
            img = "Images/red.png"

        elif color == "orange":
            img = "Images/orange.png"

        elif color == "blue":
            img = "Images/blue.png"

        elif color == "purple":
            img = "Images/purple.png"

        return pygame.image.load(img)

    def get_color(self):
        return self.color

    def getRadius(self):
        return self.radius

    def getColor(self):
        return self.color

    def getImage(self):
        return self.image

    def getAFD(self):
        return self.afd

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getDirection(self):
        return self.current_direction

    def getState(self):
        return self.state

    def setDirection(self, dir):
        self.current_direction = dir

    def setX(self, x):
         self.x = x

    def setY(self, y):
         self.y = y

    def setState(self, id):
        self.state = id

    def setImage(self, color):

        img = ""

        if color == "red":
            img = "Images/red.png"

        elif color == "orange":
            img = "Images/orange.png"

        elif color == "blue":
            img = "Images/blue.png"

        elif color == "purple":
            img = "Images/purple.png"

        elif color == "white":
            img = "Images/white.png"

        self.image = pygame.image.load(img)

    def setInitialPosition(self, color):

        if color == "red":
            self.x = 340
            self.y = 250

        elif color == "orange":
            self.x = 400
            self.y = 250

        elif color == "blue":
            self.x = 365
            self.y = 250

        elif color == "purple":
            self.x = 435
            self.y = 250

        self.current_direction = "up"
        self.state = "0"