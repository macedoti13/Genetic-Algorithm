from labirinto import Labirinto
from ag import AlgoritmoGenetico


def main():
    lab = Labirinto('labirinto1.txt')
    ag = AlgoritmoGenetico(1000, 100, 10, True, 5, True)
    ag.fit(lab)


if __name__ == "__main__":
    main()