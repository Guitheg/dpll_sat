import sys, os
from os.path import join

from dpll import dpll, consistance

from tlbpy import Duration, get_files, get_file_ext

from utils import cnf_parser, col_parser, col_to_cnf

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
        print("Liste des fichiers disponibles :", get_files(DATA, ext=["cnf"]))
        print("Liste des fichiers disponibles :", get_files(DATA, ext=["col"]))
    else :
        filename = sys.argv[1]
        verbose = False
        if len(sys.argv) == 1 + 2:
            try:
                verbose = bool(int(sys.argv[2]))
            except:
                Exception("usage <verbose> : 0 1")
        
        if get_file_ext(filename) == "col":
            data, nb_som, _ = col_parser(filename)
            cnf , n = col_to_cnf(data, nb_som, 2)
        elif get_file_ext(filename) == "cnf":
            cnf, n, _ = cnf_parser(filename)
        else:
            Exception("only .col or .cnf file are granted")
        
        print("Ensemble des clauses : \n", cnf)
        print("Nombre de littéraux :", n)
        print(type(cnf[0][0]))
        duration()
        s = dpll(cnf, n, verbose=verbose)
        duree = duration()
        print("Solution : ", s)
        print("Solution", "a priori vraie" if verif_solution(s, cnf, n) else "fausse")
        print("Temps de résolution :", duree, "secondes")

if __name__ == '__main__':
    main()