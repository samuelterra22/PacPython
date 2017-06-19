class Fruits(object):

    def __init__(self, x, y, img):

        self.x = x
        self.y = y
        self.img = img

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getImg(self):
        return self.img

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def setImg(self, img):
        self.img = img