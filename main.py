from labirinto import Labirinto
from ag import AlgoritmoGenetico


def main():
    lab = Labirinto('labirinto1.txt')
    ag = AlgoritmoGenetico(1000, 50, 1, False, 15)
    ag.fit(lab)


if __name__ == "__main__":
    main()