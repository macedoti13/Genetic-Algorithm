from labirinto import Labirinto
from ag import AlgoritmoGenetico, GridSearch, retorna_melhor_solucao


def main():
    lab = Labirinto('labirinto1.txt')
    ag = AlgoritmoGenetico()
    ag.fit(lab)

if __name__ == "__main__":
    main()