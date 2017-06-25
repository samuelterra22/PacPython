import pygame

class Fruits(object):

    def __init__(self, x, y, fruit):

        self.x = x
        self.y = y
        self.image = self.buildImage(fruit)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getImage(self):
        return self.image

    def buildImage(self, fruit):

        img = ""

        if fruit == "banana":
            img = "Images/banana.png"

        elif fruit == "pineaple":
            img = "Images/pineaple.png"

        elif fruit == "cherry":
            img = "Images/cherry.png"

        return pygame.image.load(img)


    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y