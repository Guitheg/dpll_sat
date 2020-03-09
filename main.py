import sys, os
from os.path import join

import utils as u
from dpll import dpll

MAIN = os.path.abspath(os.path.dirname(__file__))
DATA = join(MAIN, "data")

def main():
    if len(sys.argv) < 1 + 1 or len(sys.argv) > 1 + 2:
        print("usage:", sys.argv[0],"<filename(str)> [optionnal : <verbose(bool)>]")
        print("Liste des fichiers disponibles :", u.get_env(DATA))
    else :
        filename = sys.argv[1]
        verbose = False
        if len(sys.argv) == 1 + 2:
            try:
                verbose = bool(int(sys.argv[2]))
            except:
                Exception("usage <verbose> : 0 1")
        
        data, n, _ = u.cnf_parser(filename)

        print("Ensemble des clauses : ", data)

        s = dpll(data, n, verbose=verbose)

        print("Solution : ", s)

if __name__ == '__main__':
    main()