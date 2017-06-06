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

class Transition(object):
    """
    Esta classe representa uma Transição (ligação) de Estados em um Automato.
    """
    def __init__(self, Id, From, To, Read):
        self.Id = Id
        self.From = From
        self.To = To
        self.Read = Read

    def getFrom(self):
        return self.From

    def getTo(self):
        return self.To

    def getRead(self):
        return self.Read

    def getId(self):
        return self.Id

    def setFrom(self, From):
        self.From = From

    def setId(self, Id):
        self.Id = Id

    def setTo(self, To):
        self.To = To

    def setRead(self, Read):
        self.Read = Read

    def printTransition(self):
        print("(" + str(self.Id) + ")  " + self.From + "->" + self.To + "," + self.Read + " | ")