from utils import impn_set_tost

def remove_supersets(imp_setsets):
    to_remove = set()
    for imp_set in imp_setsets:
        for imp_set_b in imp_setsets:
            if imp_set!= imp_set_b and imp_set_b.issubset(imp_set):
                to_remove.add(imp_set)
    return imp_setsets-to_remove


def _multiply_imp_setsets(a,b):
    out = set()
    for a_imp_set in a:
        for b_imp_set in b:
            out.add(a_imp_set.union(b_imp_set))

    return out



def petrick(minterm_coveredby,essential):

    minterm_coverers=[]
    for m in minterm_coveredby:
        minterm_coverers.append(set(frozenset({t}) for t in minterm_coveredby[m]))

    setset=minterm_coverers[0]
    for idx, imp_setset in enumerate(minterm_coverers):
        if idx==0:
            continue
        setset=_multiply_imp_setsets(setset,imp_setset)
    setset=remove_supersets(setset)

    min_n = min(map(lambda s:len(s),setset))
    smallest=filter(lambda s:len(s)==min_n,setset)
    extend_essential=map(lambda impn_set:impn_set.union(essential), smallest)


    return sorted([impn_set_tost(t) for t in extend_essential])