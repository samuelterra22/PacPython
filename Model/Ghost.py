from Controller.AFDController import AFDController

class Ghost(object):


    def __init__(self, color):
        self.radius = 10
        self.color = self.set_color(color)
        self.afd = self.build_afd(color)
        self.x = 0
        self.y = 0
        self.current_direction = "up"
        self.current_state = "0"

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

    def set_color(self, color):

        g_color = (0,0,0)

        if color == "red":
            g_color = (255, 0, 0)
        elif color == "orange":
            g_color = (255, 127, 0)
        elif color == "blue":
            g_color = (0, 0, 204)
        elif color == "purple":
            g_color = (147, 112, 219)

        return g_color

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

    def getState(self):
        return self.current_state

    def setDirection(self, dir):
        self.current_direction = dir

    def setX(self, x):
         self.x = x

    def setY(self, y):
         self.y = y

    def setState(self, id):
        self.current_state = id

    def setInitialPosition(self, color):

        if color == "red":
            self.x = 340
            self.y = 265

        elif color == "orange":
            self.x = 400
            self.y = 265

        elif color == "blue":
            self.x = 365
            self.y = 265

        elif color == "purple":
            self.x = 435
            self.y = 265