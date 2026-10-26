"""Helpers to turn contract.jl JSON outputs into the normalized quantities of R6-R10."""
import json, math
import numpy as np


def load(path):
    with open(path) as f:
        return json.load(f)


def block(d, a, b):
    i, j = d["names"].index(a), d["names"].index(b)
    return np.array([d["C_in"][i][j], d["C_ase"][i][j]])


def collective(d):
    """Returns N0-scaled (in, ase) pairs for VarTc, VarWc, Cov, VarTcomp, plus D_c."""
    N0 = d["N0"]
    TT, WW, TW = block(d, "Tc", "Tc"), block(d, "Wc", "Wc"), block(d, "Tc", "Wc")
    o = d["output"]
    Dc = -o["cov"] / o["varW"]
    comp = TT + 2 * Dc * TW + Dc ** 2 * WW
    return dict(VarTc=N0 * TT, VarWc=N0 * WW, Cov=N0 * TW, VarTcomp=N0 * comp, Dc=Dc)


def r7_closed(U):
    G3 = math.exp(-U / 3)
    return dict(VarWc=(1.0, 3 * (1 - G3)), VarTc=((1 + U / 3) ** 2, 3 + U * U / 3 - 3 * G3),
                VarTcomp=(U * U / 9, U * U / 3 - 2 * U + 6 * (1 - G3)))


def r7_sim(d):
    c = collective(d)
    s = d["seed"]
    g, b2 = d["params"]["g"], d["params"]["b2"]
    sT2 = s["varT"]
    sW2 = (g / (3 * b2)) ** 2 * sT2
    return dict(VarWc=c["VarWc"] / sW2, VarTc=c["VarTc"] / sT2, VarTcomp=c["VarTcomp"] / sT2,
                VarWc_actual_seed_bw=c["VarWc"] / s["varW"])


def energy(d):
    N0, NL = d["N0"], d["NL"]
    return N0 * block(d, "N", "N") / NL ** 2


def matched_lo(d):
    """C_AA, C_PP in output shot-noise units (Var/(1/4)), and r (n_sp = 1)."""
    NL = d["NL"]
    NN, PP, NP = block(d, "N", "N"), block(d, "XP", "XP"), block(d, "N", "XP")
    CAA = NN / NL  # Var(N)/(4 N (1/4)) = Var(N)/N
    CPP = 4 * PP
    tot = lambda x: x[0] + x[1]
    r = tot(NP) / math.sqrt(tot(NN) * tot(PP))
    return dict(CAA=CAA, CPP=CPP, r=r, one_minus_r2=1 - r * r)


def spectral(d, metric="L2"):
    names = [f"s{l}" for l in range(5)]
    idx = [d["names"].index(n) for n in names]
    Cin = np.array(d["C_in"])[np.ix_(idx, idx)] * d["N0"]
    Cas = np.array(d["C_ase"])[np.ix_(idx, idx)] * d["N0"]
    C = Cin + Cas  # n_sp = 1
    if metric == "L2":
        Gh = np.diag([math.sqrt(2 / (2 * l + 1)) for l in range(5)])
        M = Gh @ C @ Gh
    else:
        M = C
    ev = np.sort(np.linalg.eigvalsh(M))[::-1]
    return dict(var_in=np.diag(Cin), var_ase=np.diag(Cas), ratio=ev[1] / ev[0], eig=ev)
