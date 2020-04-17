from utils import impst_covered_minterms, to_dim_and_not

def dec_to_bst(n,dim):
    st= str(bin(n))
    st=st.split("b")[1]
    n_add=dim-len(st)
    return "0"*n_add+st


def min_bits(n):
    i=1
    while 2**i-1<n:
        i+=1
    return i



def parse_mst(mst):
    def get_bracketed_minterms_dim(mst):
        start, end = mst.find("("), mst.find(")")
        assert start != -1 and end != -1
        comma_nums = mst[start + 1:end]

        nums = filter(lambda c: c != "", comma_nums.split(","))
        return [int(c) for c in nums]

    if "D" in mst:
        care,dcare = mst.split("D")
        minterm_ns=get_bracketed_minterms_dim(care)
        dcareterm_ns=get_bracketed_minterms_dim(dcare)
        largest = max(max(minterm_ns),max(dcareterm_ns))
        dim=min_bits(largest)

        minterms=set(dec_to_bst(n,dim) for n in minterm_ns)
        dcareterms=set(dec_to_bst(n,dim) for n in dcareterm_ns)
        return minterms,dim,dcareterms
    else:
        minterm_ns = get_bracketed_minterms_dim(mst)
        dim=min_bits(max(minterm_ns))
        minterms=set(dec_to_bst(n,dim) for n in minterm_ns)
        return minterms, dim, set()



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

def parse(st):
    if "x" in st:
        minterms= parse_xst_to_minterms(st)
        dim = parse_dim(st)
        return minterms,dim, set()
    else:
        return parse_mst(st)