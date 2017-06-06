"""
*************************************************************************************************
*                   Trabalho 01 - Linguagens Formais e Autômatos Finitos                        *
*                                                                                               *
*   @teacher: Walace Rodrigues                                                                  *
*   @author: Matheus Calixto - ⁠⁠⁠0011233                                                          *
*   @author: Samuel Terra    - 0011946                                                          *
*   @lastUpdate: 25/05/2017                                                                     *
*                                                                                               *
*************************************************************************************************
"""

class AFD(object):
    """
    Classe que representa o modelo de Autômato Finito Determinístico
    """

    def __init__(self, States, Transitions, Initial, Finals, Alphabet):
        self.States = States
        self.Transitions = Transitions
        self.Initial = Initial
        self.Finals = Finals
        self.Alphabet = Alphabet

    def printAutomata(self):
        """
        Metodo responsavel por printar os estados do autômato e suas características.
        """
        self.printStates()
        print("Transições: ")
        self.printTransitions()
        print("Alfabeto: " + str(self.Alphabet))

    def getStates(self):
        return self.States

    def getAlphabet(self):
        return self.Alphabet

    def getTransitions(self):
        return self.Transitions

    def getFinals(self):
        return self.Finals

    def getInitial(self):
        return self.Initial

    def setStates(self, States, Finals):
        self.States = States
        self.Finals = Finals

    def setTransitions(self, Transitions):
        self.Transitions = Transitions

    def setFinals(self, Finals):
        self.Finals = Finals

    #Função criada para facilitar a impressão dos estados do autômato

    def printStates(self):
        for e in self.getStates():
            e.printState()

    # Função criada para facilitar a impressão das transições do autômato

    def printTransitions(self):
        for t in self.getTransitions():
            t.printTransition()