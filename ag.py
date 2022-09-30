from labirinto import Labirinto
from individuo import Individuo
import random

class AlgoritmoGenetico:
    
    def __init__(self, max_geracoes: int = 1000, pop_size: int = 100, n_elites: int = 1, reposition: bool = False, reposition_n: int = 1, taxa_mutacao: float = 0.01, smart_first_gen: bool = True) -> None:
        """Inicializa o objeto algoritmo genetico. 

        Args:
            max_geracoes (int, optional): Quantidade maxima de geracoes. Defaults to 1000.
            pop_size (int, optional): Quantidade de individuos em cada populacao. Defaults to 100.
            n_elites (int, optional): Quantidade de individuos que serao escolhidos no elitismo. Defaults to 1.
            reposition (bool, optional): Se o elitismo usa reposicao (faz mais de uma copia de cada individuo). Defaults to False.
            reposition_n (int, optional): Quantidade de copias de cada individuo quando ha reposicao no elitismo. Defaults to 1.
            taxa_mutacao (float, optional): Taxa de mutacao (% de individuos mutados). Defaults to 0.01.
            smart_first_gen (bool, optional): Inicializa a primeira populacao de forma inteligente (somente individuos com posicao != 0). Defaults to True.
        """        
        self.solucao = None
        self.geracoes = 0
        self.max_geracoes = max_geracoes
        self.pop_size = pop_size
        self.n_elites = n_elites
        self.reposition = reposition
        self.reposition_n = reposition_n
        self.taxa_mutacao = taxa_mutacao
        self.smart_first_gen = smart_first_gen

    
    def gera_primeira_pop(self, n: int, lab: Labirinto) -> list:
        """Gera a primeira posicao de n individuos.

        Args:
            n (int): Quantidade de individuos na primeira populacao.
            lab (Labirinto): Labirinto que os individuos irao explorar.

        Returns:
            list: Lista com individuos: populacao.
        """        
        pop = []

        while len(pop) < n:
            a = Individuo()
            a.gera_movimentos(lab.caminho.shape[0]**2*3)
            a.explora(lab)
            if self.smart_first_gen == True:
                if a.pontuacao > 0:
                    pop.append(a)
            else:
                pop.append(a)

        self.geracoes += 1

        return pop


    def gera_nova_pop(self, pop_anterior: list, lab: Labirinto) -> list:
        """A partir de uma populacao, aplica os metodos elitismo, torneio, crossover e mutacao para gerar
           uma nova populacao. 

        Args:
            pop_anterior (list): Lista com individuos que representa a popoulacao anterior.
            lab (Labirinto): Labirinto da nova popoulacao. 

        Returns:
            list: Lista com novos individuos descendentes da populacao anterior.
        """        
        nova_pop = []

        # faz elitismo
        elites = self._elitismo(pop_anterior, self.n_elites, self.reposition, self.reposition_n)

        # muta os elites
        for ind in elites:
            self._mutacao_elite(ind, lab)
            if len(nova_pop) < len(pop_anterior):
                nova_pop.append(ind)

        while len(nova_pop) < len(pop_anterior):
            # faz torneio
            pai = self._torneio(pop_anterior)
            mae = self._torneio(pop_anterior)

            # gera dois filhos por crossover
            filho1, filho2 = self._crossover(pai, mae)

            # muta um dos dois filhos 
            if random.randint(1, 2) == 1:
                self._mutacao(filho1, 0.01)
            else:
                self._mutacao(filho2, 0.01)

            # coloca os filhos mutados na pop
            if len(nova_pop) < len(pop_anterior):
                nova_pop.append(filho1)

            if len(nova_pop) < len(pop_anterior):
                nova_pop.append(filho2)

        # recalcula a aptidao de cada individuo na nova pop
        for ind in nova_pop:
            ind.explora(lab)

        # soma 1 nas geracoes
        self.geracoes += 1
        
        return nova_pop


    def fit(self, lab: Labirinto) -> None:
        """Metodo principal do programa. Recebe um labirinto e gera toda a execucao para a criacao do algoritmo
           genetico e entrega, se encontrou, a solucao, escrevendo-a em um arquivo de saida, junto com as informacoes sobre 
           cada uma das populacoes anteriores. 

        Args:
            lab (Labirinto): Labirinto que se deseja pegar todos as comidas.

        Returns:
            None: Nao retorna nada, apenas escreve no arquivo de saida. 
        """        
        # gera primeira populacao e procura solucao 
        pop = self.gera_primeira_pop(self.pop_size, lab)
        solucao = self._procura_solucao(pop, lab)

        # inicializa arquivo
        open('saida.txt', 'w')

        # escreve no arquivo de saida infos da pop 0
        self.escreve_geracao(pop, 'saida.txt')

        # verifica se solucao esta na primeira pop
        if solucao is not None:
            # escreve no arquivo detalhes da solucao
            return solucao

        while solucao is None and self.geracoes < self.max_geracoes:
            # procura solucao na populacao formada
            solucao = self._procura_solucao(pop, lab)

            # se encontrou uma solucao, escreve ela no arquivo e para
            if solucao is not None:
                self.escreve_solucao(solucao, 'saida.txt', lab)
                return None

            # verifica se a populacao convergiu
            convergiu = self.convergencia(pop)
            if convergiu:
                with open('saida.txt', 'a') as f:
                    f.write('\nPopulacao Convergiu!!!!')
                break

            # gera nova populacao e coloca ela no arquivo
            pop = self.gera_nova_pop(pop, lab)
            self.escreve_geracao(pop, 'saida.txt')

        # so chega aqui se atingiu o maximo de geracoes
        return None 


    @staticmethod
    def _elitismo(populacao: list, n: int = 1, reposition: bool = False, reposition_n: int = 1) -> list:
        """Pega os n melhores individuos de uma populacao e retorna um lista com eles.

        Args:
            populacao (list): Lista de individuos que ser quer os melhores. 
            n (int, optional): Quantidade de individuos que se quer pegar da populacao. Defaults to 1.
            reposition (bool, optional): Decide se havera mais de uma copia de cada individuo. Defaults to False.
            reposition_n (int, optional): Quantidade de copias de cada individuo, se houverem. Defaults to 1.

        Returns:
            list: Lista com os melhores individuos.
        """        
        # cria dicionario com pontuacao de cada individuo
        pop = {}
        for ind in populacao:
            pop[ind] = ind.pontuacao

        # ordena o dicionario por pontuacao 
        pop = sorted(pop.items(), key=lambda x: x[1], reverse=True)

        # inicializa variaves 
        melhores = []
        contador = 0

        # faz reposicao dos melhores (pega mais de uma vez cada um)
        if reposition:
            for i in pop:
                for _ in range(reposition_n):
                    new_i = i[0].copy()
                    melhores.append(new_i)
                contador += 1
                if contador == n:
                    break
        # pega uma vez cada um dos n melhores
        else:
            for i in pop:
                melhores.append(i[0])
                contador += 1
                if contador == n:
                    break

        return melhores


    @staticmethod
    def _torneio(populacao: list) -> Individuo:
        """Sorteia dois individuos aleatoriamente e retorna o que tiver a maior pontuacao"""
        # sorteia dois indices aleatorios
        index1 = random.randrange(0, len(populacao))
        index2 = random.randrange(0, len(populacao))

        # pega os dois individuos de acordo com os indices sorteados
        ind1 = populacao[index1]
        ind2 = populacao[index2]

        # retorna o que tiver a maior pontuacao
        if ind1.pontuacao > ind2.pontuacao:
            return ind1
        else:
            return ind2

    
    @staticmethod
    def _crossover(pai: Individuo, mae: Individuo) -> Individuo:
        """Pega os movimentos corretos do pai e junta com o restante dos movimentos da mae para formar o filho 1.
           Pega os movimentos corretos da mae e junta com o restante dos movimentos do pai para formar o filho 2."""
        mc_pai = pai.movimentos_corretos
        mc_mae = mae.movimentos_corretos

        ind1 = Individuo()
        ind1.movimentos = mc_pai + mae.movimentos[len(mc_pai):]

        ind2 = Individuo()
        ind2.movimentos = mc_mae + pai.movimentos[len(mc_mae):]

        return ind1, ind2 


    @staticmethod
    def _mutacao_elite(ind: Individuo, lab: Labirinto) -> None:
        """Para um individuo, pega os movimentos corretos que ele fez e gera uma nova sequencia de movimentos
           aleatorios a partir deles."""
        mc = ind.movimentos
        ind.gera_movimentos(lab.caminho.shape[0]**2*3 - len(mc))
        ind.movimentos = mc + ind.movimentos


    @staticmethod
    def _mutacao(ind: Individuo, taxa: float) -> None:
        """Muta uma porcentagem dos movimentos de um individuo por movimentos aleatorios. A porcentagem eh escolhida 
           pela taxa."""
        taxa = taxa * 1000
        for i in range(len(ind.movimentos)):
            numero = random.randrange(0, 1000)
            if numero < taxa:
                ind.movimentos[i] = random.randint(0,7)
    

    @staticmethod
    def _procura_solucao(pop: list, lab: Labirinto) -> Individuo:
        """Checa todos os individuos de uma populacao e caso algum deles tenha pego todas as comidas, retorna esse individuo."""
        for ind in pop:
            if ind.comidas == lab.caminho.shape[0]/2:
                return ind

    
    def escreve_geracao(self, pop: list, arquivo: str) -> None:
        """Abre o arquivo de saida e escreve os dados de cada individuo de uma populacao especifica."""
        with open(arquivo, 'a') as f:
            i = 0
            f.write(f'Geracao {self.geracoes}\n')
            for ind in pop:
                f.write(f'Individuo {i} \n')
                f.write(f'Pontuacao: {ind.pontuacao} \n')
                f.write(f'Quantidade de Comidas: {ind.comidas} \n')
                f.write('-'*50+' \n')
                i += 1
            f.write('\n\n\n\n\n')


    def escreve_solucao(self, solucao: Individuo, arquivo: str, lab: Labirinto) -> None:
        """Abre o arquivo de saida e escreve todos os dados do individuo solucao e seu passo a passo no 
           no arquivo."""
        with open(arquivo, 'a') as f:
            # escreve estatisticas da solucao
            f.write('Encontrei a Solucao!!! \n')
            f.write(f'Quantidade de geracoes necessarias: {self.geracoes}\n')
            f.write(f'Quantidade de comidas obtidas: {solucao.comidas}\n')
            f.write(f'Posicoes exploradas: {solucao.posicoes_percorridas}\n')
            f.write(f'Movimentos corretos para percorrer o Labirinto: {solucao.movimentos_corretos}\n\n')
            f.write(f'Sequencia de movimentos ate a resposta:\n')

            # escreve passo a passo da solucao
            frases = solucao.escreve_movimentos()
            for frase in frases:
                f.write(frase)

            # escreve o labirinto percorrido
            f.write(f'\n\nLabirinto percorrido pela solucao:\n')
            f.write(f'\'.\' -> posicoes onde passou\n')
            f.write(f'\'*\' -> posicoes onde pegou uma comida\n')
            lab.marca_posicoes_percorridas(solucao.posicoes_percorridas)
            frases = lab.print()
            for frase in frases:
                f.write(frase)


    @staticmethod
    def convergencia(pop: list) -> bool:
        """Verifica se a maioriaa dos individuos da populacao tem a mesma pontuacao. Se tivirem, retorna 
           verdadeiro."""
        pontuacoes = []
        # coloca cada uma das pontuacoes distintas na lista de pontuacao
        for ind in pop:
            if ind.pontuacao in pontuacoes:
                pass
            else:
                pontuacoes.append(ind.pontuacao)

        # verifica se menos de 5% dos individuos sao diferentes
        if len(pontuacoes) < 2:
            return True

        return False
