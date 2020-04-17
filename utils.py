

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
    return "+".join(out)