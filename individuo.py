import random
from labirinto import Labirinto
import numpy as np

class Individuo:

    def __init__(self) -> None:
        """Inicializa o objeto individuo."""        
        self.movimentos = []
        self.movimentos_corretos = []
        self.posicoes_percorridas = []
        self.pontuacao = 0
        self.comidas = 0
    

    def gera_movimentos(self, x: int = 10) -> None:
        """Gera uma sequencia de x movimentos aleatorios para um individuo.

        Args:
            x (int, optional): Quantidade de movimentos. Defaults to 10.
        """        
        self.movimentos = [random.randint(0, 7) for _ in range(x)]


    def _movimenta(self, movimento: int, pos_inicial: tuple) -> tuple:
        """Gera uma coordenada final para um determindado movimento feito de uma 
           coordenada inicial. 

        Args:
            movimento (int): Id do movimento. 
            pos_inicial (tuple): Coordenada inicial do movimento.

        Returns:
            tuple: Coordenada final do movimento. 
        """        
        if movimento == 0: 
            return (pos_inicial[0]-1, pos_inicial[1]-1)
        elif movimento == 1: 
            return (pos_inicial[0]-1, pos_inicial[1])
        elif movimento == 2: 
            return (pos_inicial[0]-1, pos_inicial[1]+1)
        elif movimento == 3: 
            return (pos_inicial[0], pos_inicial[1]-1)
        elif movimento == 4: 
            return (pos_inicial[0], pos_inicial[1]+1)
        elif movimento == 5: 
            return (pos_inicial[0]+1, pos_inicial[1]-1)
        elif movimento == 6: 
            return (pos_inicial[0]+1, pos_inicial[1])
        elif movimento == 7: 
            return (pos_inicial[0]+1, pos_inicial[1]+1)


    def anda(self, lab: Labirinto, movimento: int, pos_inicial: tuple) -> tuple:
        """Executa um movimento e retorna uma posicao final correta. Se o movimento bateu em 
           uma parede, devolve a mesma posicao inicial (nao andou). Se o movimento levou o individuo
           a sair do labirinto, devolve uma posicao nula. 

        Args:
            lab (Labirinto): Labirinto onde o movimento acontece.
            movimento (int): Id do movimento.
            pos_inicial (tuple): Coordenadas da posicao inicial. 

        Returns:
            tuple: Coordenadas da posicao final.
        """        
        nova_pos = self._movimenta(movimento, pos_inicial)

        if (nova_pos[0] >= 0 and nova_pos[0] < lab.caminho.shape[0]) and (nova_pos[1] >= 0 and nova_pos[1] < lab.caminho.shape[0]): 
            
            if lab.caminho[nova_pos[0]][nova_pos[1]] == 1:
                return pos_inicial 
            else:
                return nova_pos 
        else:
            return (np.nan, np.nan)


    def _pontua(self, lab: Labirinto, pos_inicial: tuple, pos_final: tuple, posicoes: list) -> int:
        """Gera uma pontuacao para um movimento especifico. Verifica se a posicao final eh valida e caso 
           for, se o indiviuo ja passou por a aquela posicao.

        Args:
            lab (Labirinto): Labirinto onde o movimento eh executado. 
            pos_inicial (tuple): Coordenadas iniciais do movimento. 
            pos_final (tuple): Coordenadas finais do movimento.
            posicoes (list): Posicoes percorridas pelo individuo.

        Returns:
            int: Pontos gerado pelo movimento. 
        """        
        if pos_final == pos_inicial:
            return -1 # bateu em uma parede
        else:
            if pos_final in posicoes:
                return 0 # foi para um lugar que ja havia visitado
            else:
                if pos_final in lab.pos_comidas:
                    return 10 # comeu uma comida em um lugar novo
                else:
                    return 3 # foi para um lugar novo


    def explora(self, lab: Labirinto) -> None:
        """Executa todos os movimentos de um individuo e soma em sua pontuacao total, 
           os pontos gerados por cada um, atualizando a lista de posicoes percorridas 
           e de movimentos corretos. 

        Args:
            lab (Labirinto): Labirinto onde os movimentos sao executados. 
        """        
        i = 0
        pos_anterior = lab.pos_inicial
        self.posicoes_percorridas.append(lab.pos_inicial)

        while i < len(self.movimentos) and self.comidas < lab.caminho.shape[0]/2:

            # gera nova posicao 
            nova_pos = self.anda(lab, self.movimentos[i], pos_anterior)

            # verificia se saiu do labirinto
            if nova_pos == (np.nan, np.nan):
                break

            # pontua o movimento
            pontos = self._pontua(lab, pos_anterior, nova_pos, self.posicoes_percorridas)

            # verifica o movimento 
            if pontos >= 0:
                self.movimentos_corretos.append(self.movimentos[i])
                if pontos > 0:
                    self.posicoes_percorridas.append(nova_pos)
                    if pontos == 10:
                        self.comidas += 1
            
            # pontua 
            self.pontuacao += pontos

            # atualiza a posicao de partida
            pos_anterior = (nova_pos[0], nova_pos[1])

            # aumenta o index
            i += 1


    def copy(self):
        """Copia um indivio para outro objeto."""     
        i = Individuo()
        i.movimentos = self.movimentos_corretos

        return i


    def escreve_movimentos(self) -> list:
        """Coloca em uma lista uma string explicando cada movimento feito por um 
           individuo.

        Returns:
            list: Lista com as strings.
        """        
        # inicializa varivaveis 
        frases = []
        i = 0

        # coloca cada movimento na lista de frases
        for movimento in self.movimentos_corretos:
            frase = self.mapeia_movimentos(movimento)
            frases.append(f'{i}: {frase}')
            i += 1

        return frases


    @staticmethod
    def mapeia_movimentos(movimento: int) -> str:
        """Mapeia um movimento para uma string"""
        if movimento == 0: 
            return 'Andou para esquerda em cima\n'
        elif movimento == 1: 
            return 'Andou para cima\n'
        elif movimento == 2: 
            return 'Andou para direita em cima\n'
        elif movimento == 3: 
            return 'Andou para esquerda\n'
        elif movimento == 4: 
            return 'Andou para direita\n'
        elif movimento == 5: 
            return 'Andou para esquerda em baixo\n'
        elif movimento == 6: 
            return 'Andou para baixo\n'
        elif movimento == 7: 
            return 'Andou para direita em baixo\n'
        pass
