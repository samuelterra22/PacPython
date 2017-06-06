import Pacman, Ghost, math

class Referee(object):

    def __init__(self, pacman, g1, g2, g3, g4):

        self.pacman = pacman
        self.g1 = g1
        self.g2 = g2
        self.g3 = g3
        self.g4 = g4

    def getPacmanPosition(self):
        return self.pacman.getPosition()

    def getGhostPosition(self, ghost):

        if ghost == 1:
            return self.g1.getPosition()
        elif ghost == 2:
            return self.g2.getPosition()
        elif ghost == 3:
            return self.g3.getPosition()
        elif ghost == 4:
            return self.g4.getPosition()

    def calcDist(self, ghost):

        pac_x, pac_y = self.getPacmanPosition()

        if ghost == 1:
            g_x, g_y, dir =  self.getGhostPosition(1)
        elif ghost == 2:
            g_x, g_y, dir = self.getGhostPosition(2)
        elif ghost == 3:
            g_x, g_y, dir = self.getGhostPosition(3)
        elif ghost == 4:
            g_x, g_y, dir = self.getGhostPosition(4)


        dist = math.sqrt( math.pow((g_x - pac_x), 2.0) + math.pow((g_y - pac_y),2.0))

        return dist