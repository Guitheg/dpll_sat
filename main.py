import os
from os.path import join

import utils as u
from dpll import dpll

MAIN = os.path.abspath(os.path.dirname(__file__))
DATA = join(MAIN, "data")
SAT_A = join(DATA, "uf20-01.cnf")
TEST = join(DATA, "test.cnf")

def main():

    data, nb_lit, nb_clause = u.cnf_parser(TEST)
    print(data)
    s = dpll(data, nb_lit, verbose=False)
    print(s)



if __name__ == '__main__':
    main()