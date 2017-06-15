#Para rodar deve-se baixar a biblioteca pygame:

# sudo pip install pygame

from Model.Ghost import Ghost
from Controller.Referee import Referee



if __name__ == '__main__':
    '''
    g1 = Ghost(1.0, 1.0, "blue", "down")
    g2 = Ghost(3.0, 1.0, "red", "down")

    judge = Referee()

    print(judge.testDirection(g1, pac))
    '''
    Start = Referee()
    # Start.pacman_automata(1,1)
    Start.thread_trigger()