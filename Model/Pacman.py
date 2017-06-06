
class Pacman(object):

    def __init__(self, x, y):

        self.x = x
        self.y = y

    def getPosition(self):
        return self.x, self.y

    def setPosition(self, x, y):
        self.x = x
        self.y = y
