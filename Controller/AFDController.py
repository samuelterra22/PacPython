# coding=utf-8
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
import xml.etree.ElementTree as ET
from Model.AFD import AFD
from Model.State import State
from Model.Transition import Transition


class AFDController(object):
    """
    Classe que implementa todas as funcionalidade um Automoto Finito Deterministico.
    """

    def load(self, jffFile):
        """
        Metodo responsavel por ler um arquivo XML em formato jff conteudo o AFD. 
        :return: Retorna uma instancia criada de um AFD
        :rtype: AFD
        :param jffFile
        :rtype AFD
        """
        states = []  # Lista de estados
        transitions = []  # Lista de transições
        finals = []  # Lista de estados finais
        alphabet = []  # alfabeto que o automato suporta

        # Guardará o ID do estado inicial
        s_initial = ""
        # Recebendo o arquivo de entrada via parametro da função.
        # Não tem prefixo porque agora irá pegar dinamicamento no sistema operacional
        doc = ET.parse(jffFile)
        root = doc.getroot()  # Recebendo a tag root

        # iterando em cada tag State para pegar as informações
        for i in root.iter('state'):

            x = i.find('x').text
            y = i.find('y').text
            name = i.attrib['name']
            id = i.attrib['id']

            # Se nesse estado houver a tag inicial, seta o estado como inicial.
            if i.find('initial') is not None:
                initial = True
                s_initial = id
            else:
                initial = False

            # Se nesse estado houver a tag final, seta o estado como final.
            if i.find('final') is not None:
                final = True
                finals.append(id)
            else:
                final = False

            # Cria um objeto Estado
            state = State(id, name, x, y, initial, final)

            # Adiciona na lista de estados
            states.append(state)

        # Fim da obtenção das informações referentes aos estados

        # Iterando na tag <transition>
        # Pegando as transições
        cont_trans = 0
        for i in root.iter('transition'):
            From = i.find('from').text
            To = i.find('to').text
            Read = i.find('read').text

            if Read is None:  # Trata o movimento vazio, representado pelo caractere §
                Read = '§'

            # Adiciona o caractere lido na lista do alfabeto
            alphabet.append(Read)

            transition = Transition(cont_trans, From, To, Read)
            transitions.append(transition)
            cont_trans += 1
        # Fim da obtenção das informações referentes às transições.

        alphabet = list(set(alphabet))
        automato = AFD(states, transitions, s_initial, finals,
                       alphabet)  # Cria um automato

        return automato


    def accept(self, afd, word):

        '''
        Metodo responsavel por verificar se uma determinada palavra é aceita pelo AFD.
        :param afd
        :param word
        :rtype boolean
        '''

        inicial = afd.getInitial()

        return self.move(afd, inicial, word)

    def initial(self, afd):
        """
        Metodo responsavel por retornar o estado inicial do AFD.
        :rtype State
        """
        id = afd.getInitial()
        estados = afd.getStates()
        # Inicializa a variavel
        inicial = False

        for e in estados:
            if id == e.getId():
                inicial = e
                break

        return inicial

    def move(self, afd, id, word):
        """
        Método responsável por testar um movimento a partir de um estado e retornar se aceita ou não
        :param afd
        :param id
        :param word (palavra)

        """

        transicoes = afd.getTransitions()  # Pega a lista de transições do AFD
        estados_finais = afd.getFinals()  # Pega a lista de estados finais do AFD

        # Percorre todas as transições procurando a transição entre o caractere da palavra e o estado passado
        for t in transicoes:
            if t.getFrom() == id and t.getRead() == word:  # se for o estado desejado e o caractere desejado
                id = t.getTo()  # movo para o próximo estado

        # if id in estados_finais:  # Se parou em um estado final, aceita
        #     print("Palavra ACEITA! Parou no estado (" + id + ")")

        return id


    def final(self, afd):
        """
        Metodo responsavel por retornar os estados finais do AFD.
        :rtype List
        """

        idEstadosFinais = afd.getFinals()
        estadosAfd = afd.getStates()
        nomesEstadosFinais = []

        for e in estadosAfd:
            if e.getId() in idEstadosFinais:
                nomesEstadosFinais.append(e.getName())

        return nomesEstadosFinais