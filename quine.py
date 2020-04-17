import copy
from collections import defaultdict
from get_primes import get_prime_implicants
from petrick import petrick
from utils import impn_set_tost, impn_covered_minterms
from parse import parse


def _s_get_one(s):
    return next(iter(s))

def account_essentials(c_imp_coverage, c_minterm_coveredby, remove_imps):
    remove_minterms=set()
    ret = copy.deepcopy(c_minterm_coveredby)
    for i in remove_imps:
        remove_minterms=remove_minterms.union(c_imp_coverage[i])
    for m in remove_minterms:
        del ret[m]
    return ret

def impn_len(impn):
    tot=0
    for c in impn:
        if c=="_":
            continue
        else:
            tot+=1
    return tot

def get_min_implicants(req_minterms, prime_implicants, dim):
    c_imp_coverage, c_minterm_coveredby = defaultdict(set), defaultdict(set)
    for i in prime_implicants:
        i_covered = impn_covered_minterms(i, dim)
        for m in i_covered:
            if m in req_minterms:
                c_imp_coverage[i].add(m)
                c_minterm_coveredby[m].add(i)
    assert set(c_minterm_coveredby.keys())== req_minterms
    essential = set()
    for m in c_minterm_coveredby:
        covering_m = c_minterm_coveredby[m]
        if len(covering_m) == 1:
            prime = _s_get_one(covering_m)
            essential.add(prime)
    account_essentials(c_imp_coverage, c_minterm_coveredby, essential)
    if not c_minterm_coveredby:
        return [impn_set_tost(essential)]
    return petrick(c_minterm_coveredby,essential)

def brute_match(ast,bst):
    minterma,_, dcarea= parse(ast)
    mintermb,_, dcareb= parse(bst)
    return minterma<=mintermb and mintermb<=minterma.union(dcarea)


def test(st):
    minterms, dim,dcareterms = parse(st)
    primes = get_prime_implicants(minterms.union(dcareterms))
    x = get_min_implicants(minterms, primes, dim)
    print("reducing ",st)
    print("calculated reductions: ",x)
    for s in x:
        print(f"Correctness test {s}","Success" if brute_match(st,s) else "Failure")

need_petrick="m(0,1,2,5,6,7)"
bleh = "x1+x2x1+x2'x4x5"
hw4 = "m(0,3,5,7,8,10,11,13,15)+D(1,6)"
if __name__ == "__main__":
    test(hw4)
    test(need_petrick)
    test(bleh)