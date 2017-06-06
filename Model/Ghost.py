class Ghost(object):

    def __init__(self, id, x, y, color, direction):

        self.id = id
        self.x = x
        self.y = y
        self.color = color
        self.direction = direction

    def getPosition(self):

        return self.x, self.y, self.direction

    def setPosition(self, x, y):

        self.x = x
        self.y = y

    def setDirection(self, direction):

        self.direction = direction
