"""Analysis of the clamp runs: group fractions (lam = 0), lam-odd and lam-even parts of group photon numbers,
local z-exponents, and the no-Kerr multimode Langmuir reference with the exact discrete kernel.
usage: python analyze_clamp.py [tag]
"""
import json
import os
import sys

import numpy as np
import scipy.fft as sfft

from mmfieldM import ModelM

RUN_ID = "2026-10-20-claude-interactive.21-raman-clamp"
RAW = os.path.expanduser("~/analytical-nl-discovery-data/" + RUN_ID)
tag = sys.argv[1] if len(sys.argv) > 1 else "main"
cfg = json.load(open("config.json"))
c = dict(cfg["main"]); c.update(cfg.get(tag, {}))
G, R = c["G"], c["R_base"]
m = ModelM(G=G, N=c["N"], dt=c["dt_ps"], gamma=c["gamma_perWm"], fR=c["fR"], tau1=c["tau1_ps"], tau2=c["tau2_ps"],
           omega0=c["omega0_radps"], dbeta=c["dbeta_perm"], beta2=c["beta2_ps2perm"], s=c["s"], lam=1.0, Dd=0.0)
grp = m.grp
z = np.arange(c["nsteps"] // c["save_every"] + 1) * c["save_every"] * c["dz_m"]


def load(lam):
    f = os.path.join(RAW, "%s_lam%g_photon.npy" % (tag, lam))
    if not os.path.exists(f):
        return None
    x = np.load(f)
    return np.stack([x[:, :, grp == k].sum(-1) for k in range(G)], axis=-1)   # (nz, 2R, G)


def pair(x):
    return 0.5 * (x[:, :R] + x[:, R:])


out = {"tag": tag, "z_m": z.tolist()}
n0 = load(0.0)
if n0 is not None:
    fr = n0 / n0.sum(-1, keepdims=True)
    out["lam0_group_fractions_mean"] = fr.mean(1).tolist()
    out["lam0_group_fractions_se"] = (fr.std(1, ddof=1) / np.sqrt(fr.shape[1])).tolist()
p, mm = load(1.0), load(-1.0)
if p is not None and mm is not None and n0 is not None:
    odd = 0.5 * (pair(p) - pair(mm))
    even = 0.5 * (pair(p) + pair(mm)) - pair(n0)
    out["odd_mean"] = odd.mean(1).tolist()
    out["odd_maxabs_rel"] = float(np.max(np.abs(odd.mean(1)) / pair(n0).mean(1)))
    out["even_mean"] = even.mean(1).tolist()
    out["even_se"] = (even.std(1, ddof=1) / np.sqrt(R)).tolist()
    E0 = even.mean(1)[:, 0]
    with np.errstate(divide="ignore", invalid="ignore"):
        loc = np.gradient(np.log(np.abs(E0[1:])), np.log(z[1:]))
    out["even0_local_exponent"] = loc.tolist()

# no-Kerr Langmuir reference with the exact discrete kernel, launched spectra, same z grid
def langmuir():
    W = m.W
    b = np.zeros((m.M, m.N))
    for q in range(m.M):
        g = np.exp(-W ** 2 / (2 * c["sigma_radps"] ** 2)); g[m.N // 2] = 0
        b[q] = c["powers_W"][q] * g / g.sum()
    S = np.array([[m.S[p_, q, p_, q] for q in range(m.M)] for p_ in range(m.M)])
    res = {}
    for lam in (1.0, -1.0):
        FH = np.fft.fft(lam * m.H.imag)
        bb = b.copy()
        f = lambda x: -2 * c["gamma_perWm"] * c["fR"] * x * (S @ np.real(np.fft.ifft(FH[None, :] * np.fft.fft(x, axis=-1), axis=-1)))
        rec = [bb.sum(-1)]
        cen = [(bb * W).sum(-1) / bb.sum(-1)]
        for n in range(c["nsteps"]):
            dz = c["dz_m"]
            k1 = f(bb); k2 = f(bb + 0.5 * dz * k1); k3 = f(bb + 0.5 * dz * k2); k4 = f(bb + dz * k3)
            bb = bb + dz / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
            if (n + 1) % c["save_every"] == 0:
                rec.append(bb.sum(-1))
                cen.append((bb * W).sum(-1) / bb.sum(-1))
        res[lam] = np.array(rec)
        res[("c", lam)] = np.array(cen)
    ev = 0.5 * (res[1.0] + res[-1.0]) - b.sum(-1)[None, :]
    cc, pp = res[("c", 1.0)], res[1.0]
    w1 = pp[:, grp == 1]
    dc = cc[:, 0] - (cc[:, grp == 1] * w1).sum(-1) / w1.sum(-1)
    global LANG_DC
    LANG_DC = dc
    return np.stack([ev[:, grp == k].sum(-1) for k in range(G)], axis=-1)

# operational L_kin (pre-registered definition) from the lam = 0 group-1 fraction
if n0 is not None:
    lg = c.get("lkin_group", 1)
    f1 = (n0 / n0.sum(-1, keepdims=True)).mean(1)[:, lg]
    target = c["lkin_target"] if "lkin_target" in c else f1[-5:].mean()
    lvl = f1[0] + (1 - np.exp(-1)) * (target - f1[0])
    idx = np.where((f1 - lvl) * np.sign(target - f1[0]) >= 0)[0]
    out["Lkin_m"] = float(z[idx[0]]) if len(idx) else None
    out["group1_fraction_plateau"] = float(target)

# energy centroids: C0 and the lambda-odd inter-group offset Delta c_01
def loadc(lam):
    f = os.path.join(RAW, "%s_lam%g_centroid.npy" % (tag, lam))
    return np.load(f) if os.path.exists(f) else None
c0, cp, cm = loadc(0.0), loadc(1.0), loadc(-1.0)
def dc01(cent, phot):
    w1 = phot[:, :, grp == 1]
    cg1 = (cent[:, :, grp == 1] * w1).sum(-1) / w1.sum(-1)
    return cent[:, :, 0] - cg1                     # (nz, 2R)
if c0 is not None:
    raw0 = np.load(os.path.join(RAW, "%s_lam0_photon.npy" % tag))
    out["C0_max_abs_pair_centroid_lam0"] = float(np.max(np.abs(0.5 * (c0[:, :R] + c0[:, R:]).mean(1))))
if cp is not None and cm is not None:
    rawp = np.load(os.path.join(RAW, "%s_lam1_photon.npy" % tag))
    rawm = np.load(os.path.join(RAW, "%s_lam-1_photon.npy" % tag))
    dp, dm = dc01(cp, rawp), dc01(cm, rawm)
    odd_dc = 0.5 * (0.5 * (dp[:, :R] + dp[:, R:]) - 0.5 * (dm[:, :R] + dm[:, R:]))   # (nz, R)
    out["dc01_odd_mean"] = odd_dc.mean(1).tolist()
    out["dc01_odd_se"] = (odd_dc.std(1, ddof=1) / np.sqrt(R)).tolist()
    a = np.abs(odd_dc.mean(1))
    with np.errstate(divide="ignore", invalid="ignore"):
        out["dc01_local_exponent"] = np.gradient(np.log(a[1:]), np.log(z[1:])).tolist()

EL = langmuir()
out["langmuir_even_noKerr"] = EL.tolist()
out["langmuir_dc01_noKerr"] = LANG_DC.tolist()
json.dump(out, open("results/summary_%s.json" % tag, "w"), indent=1)
print("z:", np.round(z, 2))
if "lam0_group_fractions_mean" in out:
    for i in range(0, len(z), 3):
        print("z=%.1f m fractions %s" % (z[i], np.round(out["lam0_group_fractions_mean"][i], 4)))
print("L_kin (operational):", out.get("Lkin_m"), " group-1 plateau:", out.get("group1_fraction_plateau"))
print("C0 max |pair-averaged centroid| at lam=0:", out.get("C0_max_abs_pair_centroid_lam0"))
if "dc01_odd_mean" in out:
    for i in range(0, len(z), 3):
        print("z=%.1f  dc01_odd %.5f +- %.5f  (Langmuir no Kerr %.5f)  local exp %s" % (z[i], out["dc01_odd_mean"][i],
              out["dc01_odd_se"][i], LANG_DC[i], np.round(out["dc01_local_exponent"][i - 1], 2) if i > 0 else "-"))
if "even_mean" in out:
    print("max |odd| / N:", out["odd_maxabs_rel"])
    for i in range(0, len(z), 3):
        print("z=%.1f E_g %s +- %s ; Langmuir %s ; local exp %s" % (z[i], np.round(out["even_mean"][i], 3),
              np.round(out["even_se"][i], 3), np.round(EL[i], 3),
              np.round(out["even0_local_exponent"][i - 1], 2) if i > 0 else "-"))
