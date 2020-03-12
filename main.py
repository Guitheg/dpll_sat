import sys, os
from os.path import join

from dpll import dpll, consistance

from tlbpy import Duration, get_files, cnf_parser

import cProfile
import re

MAIN = os.path.abspath(os.path.dirname(__file__))
DATA = join(MAIN, "data")

def verif_solution(S, C, N):
    if len(S) != N:
        return False
    for i,s1 in enumerate(S):
        for j,s2 in enumerate(S):
            if abs(s1) == abs(s2) and i != j:
                print("erreur détecté : ", s1,"("+str(i)+") = ", s2, "("+str(j)+")")
                return False
    return consistance(S, C, affectation=lambda l, S: -l in S)

def main():
    duration = Duration()

    if len(sys.argv) < 1 + 1 or len(sys.argv) > 1 + 2:
        print("usage:", sys.argv[0],"<filename(str)> [optionnal : <verbose(bool)>]")
        print("Liste des fichiers disponibles :", get_files(DATA, ext=["cnf"], basename=True))
    else :
        filename = sys.argv[1]
        verbose = False
        if len(sys.argv) == 1 + 2:
            try:
                verbose = bool(int(sys.argv[2]))
            except:
                Exception("usage <verbose> : 0 1")
        
        data, n, _ = cnf_parser(filename)

        print("Ensemble des clauses : ", data)
        duration()
        s = dpll(data, n, verbose=verbose)
        duree = duration()
        print("Solution : ", s)
        print("Solution", "a priori vraie" if verif_solution(s, data, n) else "fausse")
        print("Temps de résolution :", duree, "secondes")

        # cProfile.run("dpll(data, n, verbose=verbose)")

if __name__ == '__main__':
    main()