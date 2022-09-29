import numpy as np

class Labirinto:

    def __init__(self, arquivo: str) -> None:
        """Inicializa o objeto labirinto com um arquivo que sera utilizado para a 
           criacao do caminho.

        Args:
            arquivo (str): Nome do arquivo. 
        """        
        self.caminho = self._cria_lab_de_arquivo(arquivo)
        self.pos_inicial = self._retorna_pos_inicial()
        self.pos_comidas = self._retorna_pos_comidas()


    def _cria_lab_de_arquivo(self, arquivo: str) -> np.ndarray:
        """A partir de um arquivo, gera uma matriz da biblioteca numpy.

        Args:
            arquivo (str): Nome do arquivo.

        Returns:
            np.ndarray: Matriz do numpy representando o labirinto. 
        """        
        with open(arquivo, 'r') as f:
            linhas = f.readlines()
            dim = int(linhas[0])
            lab = []

            for linha in linhas[1:]:
                linha = linha.split('\n')[0].split(' ')
                linha = [int(i) if i not in ['E', 'C'] else (-1 if i == 'E' else 2) for i in linha]
                lab.append(linha)

            lab = np.array(lab).reshape(dim, dim)
        
        return lab


    def _retorna_pos_inicial(self) -> tuple:
        """Retorna a posicao inicial de onde o indivio comeca a exploracao."""
        posicao = np.where(self.caminho == -1)
        pos_inicial = (posicao[0][0], posicao[1][0])

        return pos_inicial


    def _retorna_pos_comidas(self) -> list:
        """Coloca em uma lista as posicoes onde estao localizadas as comidas.

        Returns:
            list: Lista com as coordenadas das comidas.
        """
        posicoes = np.where(self.caminho == 2)
        pos_comidas = []

        for linha, coluna in zip(posicoes[0], posicoes[1]):
            comida = (linha, coluna)
            pos_comidas.append(comida)

        return pos_comidas

    
    def marca_posicoes_percorridas(self, lista_posicoes: list) -> None:
        """Muda o valor das posicoes do labirinto de acordo com uma lista de posicoes. 

        Args:
            lista_posicoes (list): Lista de posicoes percorridas por um Individuo.
        """        
        for posicao in lista_posicoes:
            linha = posicao[0]
            coluna = posicao[1]
            if self.caminho[linha][coluna] == 2:
                self.caminho[linha][coluna] = -2
            else:
                self.caminho[linha][coluna] = -1


    def print(self) -> None:
        """Coloca em uma lista varias strings que em conjunto, mostram o labirinto."""
        frases = []
        frases.append('-'*34)
        for linha in self.caminho:
            frases.append('\n| ')

            for casa in linha:
                if casa == -2:
                    frases.append(' * ')
                elif casa == -1:
                    frases.append(' . ')
                else:
                    frases.append(f' {casa} ')

            frases.append(' |')
        frases.append('\n'+'-'*34)

        return frases
