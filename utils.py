import copy

def impn_to_dict(impn):
    out = {}
    for _, c in enumerate(impn):
        idx = _ + 1
        if c=="_":continue
        assert c=="1" or c=="0"
        out[idx] = True if c == "1" else False
    return out

def impn_to_impst(impn):
    out=[]
    for _, c in enumerate(impn):
        idx = _+1
        if c=="1":
            out.append(f"x{idx}")
        elif c=="0":
            out.append(f"x{idx}'")
        else:
            assert c=="_"
    return "".join(out)


def impn_set_tost(impn_set):
    out=list(map(lambda impn:impn_to_impst(impn),impn_set ))
    return " + ".join(out)

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


def to_dim_and_not(imp_st):
    dim_and_not = imp_st.split("x")
    dim_and_not = list(filter(lambda t: t, dim_and_not))
    return dim_and_not


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