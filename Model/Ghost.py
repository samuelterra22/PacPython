class Ghost(object):

    def __init__(self, x, y, color, direction):

        self.x = x
        self.y = y
        self.color = color
        self.direction = direction

    def getPosition(self):

        return self.x, self.y

    def setPosition(self, x, y):

        self.x = x
        self.y = y

    def setDirection(self, direction):

        self.direction = direction
