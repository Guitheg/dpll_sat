from utils import Talk

def affectation(l, S):
    for (X, v, _) in S:
        if l == X and v == -1:
            return True
        if l == -X and v == +1:
            return True
    return False

def consistance(S, C):
    """
    S : pile des affectations courantes
    C : ensemble des clauses
    => retourne vrai si S est consistant à C, faux sinon.
    
    S est consistant à C si S ne rend aucune clause de C fausse
    une clause c est fausse pour S si pour chaque littéral l de c on a:
    soit l = X et S contient une affectation (X, -1, _) 
    soit l = non X et S contient une affectation (X, +1, _)
    """
    for c in C:
        clauseFalse = True
        for l in c:
            clauseFalse = affectation(l, S) & clauseFalse
            if not clauseFalse: break
        if clauseFalse :
            return False
    return True

def base_defaut(N):
    B = []
    for i in range(0, N):
        B.append((i+1, +1, -1))
    return B

def choix_defaut(B, i):
    return B[i]

def dpll(C, N, choix = choix_defaut, base = base_defaut, verbose = False):
    """
    C : ensemble des clauses
    N : nombre de litteraux
    choix : fonction pour déterminer le X à choisir
    base : fonction de creation de la base à partir de laquelle on pioche les X
    => retourne l'ensemble S des affectations qui satisfait C

    Implémentation de l'algorithme DPLL sous forme itérative
    avec une pile S contenant les affectations partielles courantes.
    """
    talk = Talk(verbose)
    talk("N: {}", N)
    S = [] # pile des affectations partielles courantes
    fin = False

    B = base(N)
    talk("B: {}", B)

    while not fin :
        talk("S: {}", S)
        if consistance(S, C):
            if len(S) == N:
                fin = True
            else:
                X = choix(B, len(S))
                S.append(X)
        else:
            (x, v, w) = S.pop()
            while len(S) > 0 and w == None:
                (x, v, w) = S.pop()
            if w != None:
                S.append((x, w, None))
            else:
                fin = True

    return [x*v for x, v, _ in S]
