import math

class Referee(object):

    def getPacmanPosition(self, pacman):

        return pacman.getPosition()

    def getGhostPosition(self, ghost):

        return ghost.getPosition()

    def calcDist(self, g_x, g_y, p_x, p_y):

        return math.sqrt(math.pow((g_x - p_x), 2.0) + math.pow((g_y - p_y), 2.0))

    def testDirection(self, ghost, pacman):

        p_x, p_y = self.getPacmanPosition(pacman)
        g_x, g_y = self.getGhostPosition(ghost)
        current_dist = self.calcDist(g_x, g_y, p_x, p_y)

        smaller = current_dist
        new_direction = ""

        # Para a direita:

        aux_x = g_x + 1.0
        aux_y = g_y

        new_dist = self.calcDist(aux_x, aux_y, p_x, p_y)

        if new_dist < smaller:
            smaller = new_dist
            new_direction = "r"

        # Para a esquerda:

        aux_x = g_x - 1.0
        aux_y = g_y

        new_dist = self.calcDist(aux_x, aux_y, p_x, p_y)

        if new_dist < smaller:
            smaller = new_dist
            new_direction = "l"

        # Para baixo:

        aux_x = g_x
        aux_y = g_y - 1.0

        new_dist = self.calcDist(aux_x, aux_y, p_x, p_y)

        if new_dist < smaller:
            smaller = new_dist
            new_direction = "d"

        # Para cima:

        aux_x = g_x
        aux_y = g_y + 1.0

        new_dist = self.calcDist(aux_x, aux_y, p_x, p_y)

        if new_dist < smaller:
            smaller = new_dist
            new_direction = "d"

        return smaller, new_direction
