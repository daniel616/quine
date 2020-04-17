import copy
from collections import defaultdict
from get_primes import get_prime_implicants
from petrick import petrick
from utils import impn_set_tost

def to_dim_and_not(imp_st):
    dim_and_not = imp_st.split("x")
    dim_and_not = list(filter(lambda t: t, dim_and_not))
    return dim_and_not

def _implicant_dim(imp_st):
    dim_and_not = to_dim_and_not(imp_st)
    dims = []
    for s in dim_and_not:
        if len(s) == 1:
            n = int(s)
        else:
            assert len(s) == 2
            assert s[1] == "'"
            n = int(s[0])
        dims.append(n)

    return max(dims)

def impst_to_dict(imp_st):
    dim_and_not = to_dim_and_not(imp_st)
    out = {}
    for s in dim_and_not:
        if len(s) == 1:
            out[int(s)] = True
        else:
            assert len(s) == 2 and s[1] == "'"
            out[int(s[0])] = False
    return out


def impn_to_dict(impn):
    out = {}
    for _, c in enumerate(impn):
        idx = _ + 1
        if c=="_":continue
        assert c=="1" or c=="0"
        out[idx] = True if c == "1" else False
    return out


def _covered_by_dict(imp_dict, dim):
    # {1:True,2:False, 4:True}
    for i in range(1, dim + 1):
        if i not in imp_dict:
            d_false, d_true = copy.copy(imp_dict), copy.copy(imp_dict)
            d_false[i] = False
            d_true[i] = True
            return _covered_by_dict(d_false, dim).union(_covered_by_dict(d_true, dim))

    out = ["1" if imp_dict[i] else "0" for i in range(1, dim + 1)]
    return {"".join(out)}


def impst_covered_minterms(imp_st, dim):
    return _covered_by_dict(impst_to_dict(imp_st), dim)


def impn_covered_minterms(impn, dim):
    d = impn_to_dict(impn)
    return _covered_by_dict(d, dim)


def parse_dim(in_st):
    no_space = "".join(in_st.split(" "))
    imp_sts = no_space.split("+")
    return max([_implicant_dim(t) for t in imp_sts])


def parse_xst_to_minterms(bool_st):
    no_space = "".join(bool_st.split(" "))
    imp_sts = no_space.split("+")
    dim = max([_implicant_dim(t) for t in imp_sts])
    out = set()
    for s in imp_sts:
        out = out.union(impst_covered_minterms(s, dim))
    return out

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
        return impn_set_tost(essential)
    return petrick(c_minterm_coveredby,essential)


def min_bits(n):
    i=1
    while 2**i-1<n:
        i+=1
    return i

def dec_to_bst(n,dim):
    st= str(bin(n))
    st=st.split("b")[1]
    n_add=dim-len(st)
    return "0"*n_add+st

def parse_mst(mst):
    start,end=mst.find("("),mst.find(")")
    assert start!=-1 and end !=-1
    comma_nums = mst[start+1:end]

    nums = filter(lambda c: c!="", comma_nums.split(","))
    nums = [int(c) for c in nums]
    dim = min_bits(max(nums))
    return set(dec_to_bst(n,dim) for n in nums),dim


need_petrick="m(0,1,2,5,6,7)"
if __name__ == "__main__":
    st = need_petrick
    if "x" in st:
        minterms= parse_xst_to_minterms(st)
        dim = parse_dim(st)
    else:
        minterms,dim = parse_mst(st)

    primes = get_prime_implicants(minterms)
    x=get_min_implicants(minterms,primes,dim)
    print(x)
