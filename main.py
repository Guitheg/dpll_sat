import utils as u
from os.path import join

DATA = "data"
SAT_A = join(DATA, "uf20-01.cnf")
TEST = join(DATA, "test.cnf")

def main():
    data, nb_lit, nb_clause = u.get_C(TEST)
    print(data)
    s = u.resolve(data, nb_lit, u.no_heuristique)
    print(s)

    # print()

if __name__ == '__main__':
    main()