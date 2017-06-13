#Para rodar deve-se baixar a biblioteca pygame:

# sudo pip install pygame

from Model.Pacman import Pacman
from Model.Ghost import Ghost
from Controller.Referee import Referee



if __name__ == '__main__':
    '''
    pac = Pacman(5.0, 5.0)
    g1 = Ghost(1.0, 1.0, "blue", "down")
    g2 = Ghost(3.0, 1.0, "red", "down")

    judge = Referee()

    print(judge.testDirection(g1, pac))
    '''
    Start = Referee()
    Start.gameLoop()