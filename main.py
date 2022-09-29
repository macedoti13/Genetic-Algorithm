from labirinto import Labirinto
from ag import AlgoritmoGenetico


def main():
    lab = Labirinto('labirinto1.txt')
    ag = AlgoritmoGenetico(1000, 100, 1, False, 5, 0.008, False)
    ag.fit(lab)


if __name__ == "__main__":
    main()