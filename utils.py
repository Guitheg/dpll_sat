import numpy as np

def cnf_parser(path):
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

def col_parser(path):
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
                        nb_som = int(nl)
                        nb_ar = int(nc)
                    except:
                        raise Exception("(p) - parameter problem : " + str(line.split()))
                elif line.startswith('e'):
                    try:
                        clause = [int(lit) for lit in line.split()[1:] if int(lit) != 0]
                        data.append(clause)
                        i += 1
                    except:
                        raise Exception("line["+str(i)+"] clause - parameter problem : "+str(line.split()))
                else:
                    if data[-1][0] == 0:
                        raise Exception("Pas de bon nombre de clause dans le fichier : "+path)
    return data, nb_som, nb_ar

def col_to_cnf(data_col, nb_som, nb_col):
    P = np.linspace(np.arange(nb_col), np.arange(nb_som*nb_col-nb_col, nb_som*nb_col), nb_som, dtype=np.int)+1
    cnf = []
    for i in range(nb_som):
        cnf.append([int(P[i,j]) for j in range(nb_col)])
    for i in range(nb_som):
        for j in range(nb_col-1):
            for k in range(j+1, nb_col):
                cnf.append([ int(-P[i, j]), int(-P[i, k]) ])
    for arc in data_col:
        for c in range(nb_col):
            cnf.append([ int(-P[arc[0]-1, c]), int(-P[arc[1]-1, c]) ])
    return cnf, P[-1,-1]