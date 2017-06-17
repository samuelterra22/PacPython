from Controller.AFDController import AFDController

class Ghost(object):


    def __init__(self, color):
        self.radius = 10
        self.color = color
        self.afd = self.build_afd()
        self.x = 0
        self.y = 0
        self.current_direction = "None"

    def build_afd(self):
        pac_controller = AFDController()
        return pac_controller.load("AFDS/automata.jff")

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

    def setX(self, x):
         self.x = x

    def setY(self, y):
         self.y = y
