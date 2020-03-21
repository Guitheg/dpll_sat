from tlbpy import Talk
import numpy as np

def affectation_xvw(l, S):
    for (X, v, _) in S:
        if l == X and v == -1:
            return True
        if l == -X and v == +1:
            return True
    return False

def consistance(S, C, affectation = affectation_xvw):
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

def choix_defaut(B, S, C, N):
    return B[len(S)]

def neg(X):
    (x, v, w) = X
    return (x, w, v)

def unique(X):
    (x, v, _) = X
    return (x, v, None)

def build_pure(C):
    P = []
    notPure = []
    for c in C:
        for l in c:
            if l not in P and l not in notPure:
                br = False
                for k in C:
                    for m in k:
                        if l + m == 0:
                            notPure.append(l)
                            br = True
                            break
                    if br : break
                if not br:
                    P.append(l)
    return P
                    
def choix_heuristique(B, S, C, P, N):
    #unique
    for b in B:
        if not consistance([b]+S,C):
            B.remove(b)
            return neg(b)
        if not consistance([neg(b)]+S,C):
            B.remove(b)
            return b

    #heuristique
    L = np.arange(N)
    for c in C:
        tmp = []
        for l in c:
            if l not in S:
                tmp.append(abs(l))
            elif -l in S:
                continue
            else:
                tmp = []
                break
        for l in tmp:
            L[l-1] += 1
    select = np.argmax(L)+1
    for (x, v, w) in B:
        if (x*v) == select:
            B.remove((x, v, w))
            return (x, v, w)
        if -(x*v) == select:
            B.remove((x, v, w))
            return neg((x, v, w))
    return B.pop(0)

def dpll(C, N, choix = choix_heuristique, base = base_defaut, verbose = False):
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
    P = build_pure(C)
    
    while not fin :
        if len(S)+len(B) != N:
            talk("!!!!!!!!!")
        talk("P [{}]: {}", len(P), P)
        talk("B [{}]: {}", len(B), [x*v for x, v, _ in B])
        talk("S [{}]: {}\n", len(S), [x*v for x, v, _ in S])
        
        if consistance(S, C):
            if len(S) == N:
                fin = True
            else:
                X = choix(B, S, C, P, N)
                S.append(X)
        else:
            (x, v, w) = S.pop()
            while len(S) > 0 and w == None:
                B.append((x, 1, -1))
                (x, v, w) = S.pop()

            if w != None:
                S.append((x, w, None))
            else:
                fin = True
    return [x*v for x, v, _ in S]