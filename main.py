from labirinto import Labirinto
from ag import AlgoritmoGenetico


def main():
    lab = Labirinto('labirinto1.txt')
    ag = AlgoritmoGenetico(max_geracoes=1000,
                           pop_size=100,
                           n_elites=5,
                           reposition=True,
                           reposition_n=10,
                           taxa_mutacao=0.01,
                           smart_first_gen=True)
    ag.fit(lab)


if __name__ == "__main__":
    main()