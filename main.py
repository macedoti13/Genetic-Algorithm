from labirinto import Labirinto
from ag import AlgoritmoGenetico


def main():
    lab = Labirinto('labirinto1.txt')
    ag = AlgoritmoGenetico(100, 200, 5, True, 10)
    ag.fit(lab)


if __name__ == "__main__":
    main()