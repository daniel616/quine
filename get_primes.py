import copy
from collections import defaultdict

def merge_implicants(implicants):
    merged_imps = defaultdict(lambda: set())
    used = set()
    for i in implicants:
        chrs = list(i)
        for idx, c in enumerate(chrs):
            cpy = copy.copy(chrs)
            if c == "0":
                cpy[idx] = "1"
            else:
                cpy[idx] = "0"
            n_st = "".join(cpy)
            if n_st in implicants:
                m_cpy = copy.copy(chrs)
                m_cpy[idx] = "_"
                merged = "".join(m_cpy)
                merged_imps[merged].add(n_st)
                merged_imps[merged].add(i)
                used.add(n_st)
                used.add(i)
    return merged_imps, implicants - used


def get_prime_implicants(implicants):
    primes = set()
    cur_implicants = implicants
    while True:
        merged_imp_dict, unmerged = merge_implicants(cur_implicants)
        merged_imps = set(merged_imp_dict.keys())
        primes = primes.union(unmerged)
        cur_implicants = merged_imps
        if not merged_imps:
            return primes