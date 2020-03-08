import numpy as np

def get_C(path):
    """
    CNF file parser
    """
    data = []
    nb_lit = 0
    nb_clause = 0
    with open(path) as f:
        i = 0
        for line in f.readlines():
            if not (line.startswith('c') or line.split() == [] or line.startswith('0')):
                if line.startswith('p'):
                    try:
                        _, _, nl, nc = line.split()
                        nb_lit = int(nl)
                        nb_clause = int(nc)
                    except:
                        raise Exception("(p) - parameter problem : " + str(line.split()))
                elif line.startswith('%'):
                    if data[-1][0] == 0:
                        raise Exception("Pas de bon nombre de clause dans le fichier : "+path)
                else:
                    try:
                        clause = [int(lit) for lit in line.split() if int(lit) != 0]
                        data.append(clause)
                        i+=1
                    except:
                        raise Exception("line["+str(i)+"] clause - parameter problem : "+str(line.split()))
    return data, nb_lit, nb_clause

def _consistant(s, clauses):
    ret = True
    clause = True
    print("test consistant")
    for c in clauses:
        print("c:",c, "clause:", clause)
        nblit = len(c)
        for l in s:
            print("l:",l, "nblit:",nblit)
            if -l in c:
                nblit -= 1
                if nblit == 0:
                    clause = False
            if clause == False:
                break
        ret = clause
        if clause == False:
            break      
    return ret

def no_heuristique(x):
    return x.pop()

def unitaire(x):
    pass

def resolve(clauses, nbvar, choisir):
    run = True
    s = []
    x = list(range(1, nbvar+1))

    print("unitaire")
    for c in clauses:
        if len(c) == 1:
            it = abs(c[0])-1
            x.pop(it)
            s.append(c[0])

    while run:
        print("#")
        print("x", x)
        print("s", s)
        if _consistant(s, clauses):
            print(" - consistant")
            if len(s) == nbvar:
                print("|s|=n")
                run = False
            else:
                if len(x) > 0:
                    s.append(choisir(x))
                    print("new s", s)
        else:
            print(" + nope")
            while len(s) > 0 and s[len(s)-1] < 0:
                print("del s[-1] : ", s[-1])
                x.append(-s[-1])
                del s[-1]
            if len(s) > 0:
                print("|s| (", len(s),") > 0")
                print("s[len(s)-1]", s[len(s) - 1], "~>", -s[len(s) - 1])
                s[len(s) - 1] = -s[len(s) - 1]
            else:
                print("fin")
                run = False
        print("")

    return np.asarray(s)
