import DiffHell_prog
import Shamir_prog
import random

def generation_c_d(lenKeys,p,g):
    while True:
        c = random.randint(10 ** (lenKeys - 1), 10 ** lenKeys)
        if c < p - 1 and Shamir_prog.egcd(c, p - 1)[0]:
            d = DiffHell_prog.modular_pow(g, c, p)
            break
    return c, d

def calculated_r_e(text,g,p,d):
    k = random.randint(1, p - 2)
    r = DiffHell_prog.modular_pow(g, k, p)
    e = (text * DiffHell_prog.modular_pow(d, k, p)) % p
    return k, r, e

def get_m(e,r,p,c):
    return (e * DiffHell_prog.modular_pow(r, (p - 1) - c, p)) % p
