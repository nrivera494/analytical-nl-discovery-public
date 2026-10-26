"""Analysis of P3, P3s05 and convergence runs; Langmuir comparisons. Writes summary.json.
usage: python analyze.py
"""
import json
import os

import numpy as np

from mmfield import Model, launch

RUN_ID = "2026-10-20-claude-interactive.21-raman-parity"
RAW = os.path.expanduser("~/analytical-nl-discovery-data/" + RUN_ID)
cfg = json.load(open("config.json"))
c3 = cfg["P3"]
R = c3["R_base"]


def load(tag, s, lam):
    f = os.path.join(RAW, "%s_s%g_lam%g_photon.npy" % (tag, s, lam))
    return np.load(f) if os.path.exists(f) else None   # shape (nsave+1, 2R, 3)


def pair(x):
    """average over each base realization and its mirror: (nz, 2R, 3) -> (nz, R, 3)"""
    return 0.5 * (x[:, :R] + x[:, R:])


def mse(x):
    return x.mean(axis=1), x.std(axis=1, ddof=1) / np.sqrt(x.shape[1])


def decompose(tag, s, lam):
    p, m, o = load(tag, s, lam), load(tag, s, -lam), load(tag, s, 0.0)
    out = {}
    if p is None or m is None:
        return None
    odd_pair = 0.5 * (pair(p) - pair(m))
    out["odd_pair_mean"], out["odd_pair_se"] = [a.tolist() for a in mse(odd_pair)]
    odd_base = 0.5 * (p[:, :R] - m[:, :R])
    out["odd_base_mean"], out["odd_base_se"] = [a.tolist() for a in mse(odd_base)]
    out["odd_pair_maxabs_rel"] = float(np.max(np.abs(odd_pair.mean(axis=1)) / pair(p).mean(axis=1)))
    if o is not None:
        even_pair = 0.5 * (pair(p) + pair(m)) - pair(o)
        out["even_pair_mean"], out["even_pair_se"] = [a.tolist() for a in mse(even_pair)]
        out["N0_initial"] = pair(o)[0].mean(axis=0).tolist()
    return out


def langmuir_exact(s, nsteps, dz):
    """Mean-field multimode Langmuir equation with the exact discrete Raman kernel, no Kerr:
    db_p/dz = -2 gamma fR lam w b_p sum_q S_pqpq (ImH (*) b_q), integrated by RK4, for lam = +-1;
    returns the lam-even part of the photon number of each mode at the saved z (post hoc)."""
    B = cfg["base"]
    res = {}
    for lam in (1.0, -1.0, 0.0):
        m = Model(N=B["N"], dt=B["dt_ps"], gamma=B["gamma_perWm"], fR=B["fR"], tau1=B["tau1_ps"],
                  tau2=B["tau2_ps"], omega0=B["omega0_radps"], dbeta=B["dbeta_perm"], beta2=B["beta2_ps2perm"],
                  b1=0.0, s=s, lam=1.0 if lam == 0 else lam, Dd=0.0)
        _, b = launch(np.random.default_rng(0), 1, m.N, m.dt, c3["powers_W"], c3["sigma_radps"], c3["centre_radps"])
        ImH = m.H.imag * (0 if lam == 0 else 1)
        FH = np.fft.fft(ImH)
        S = np.array([[m.S[p, q, p, q] for q in range(3)] for p in range(3)])

        def f(b):
            conv = np.real(np.fft.ifft(FH[None, :] * np.fft.fft(b, axis=-1), axis=-1))
            return -2 * B["gamma_perWm"] * B["fR"] * m.w[None, :] * b * (S @ conv)
        rec = [np.sum(b / m.w, axis=-1)]
        for n in range(nsteps):
            k1 = f(b); k2 = f(b + 0.5 * dz * k1); k3 = f(b + 0.5 * dz * k2); k4 = f(b + dz * k3)
            b = b + dz / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
            if (n + 1) % (nsteps // c3["nsave"]) == 0:
                rec.append(np.sum(b / m.w, axis=-1))
        res[lam] = np.array(rec)
    even = 0.5 * (res[1.0] + res[-1.0]) - res[0.0]
    odd = 0.5 * (res[1.0] - res[-1.0])
    return even, odd


def langmuir_lineargain_second_order(z):
    """Pre-registered estimate: dN_p/N_p = (g1^2 z^2/2)[sig_p^2 s_p^2 - sum_q S_pq P_q sig_q^2 s_q]."""
    B = cfg["base"]
    tau1, tau2 = B["tau1_ps"], B["tau2_ps"]
    T1 = 2 * tau1 ** 2 * tau2 / (tau1 ** 2 + tau2 ** 2)
    g1 = 2 * B["gamma_perWm"] * B["fR"] * T1
    P = np.array(c3["powers_W"], float)
    sig = np.array(c3["sigma_radps"], float)
    from mmfield import hg_overlaps
    S4 = hg_overlaps()
    S = np.array([[S4[p, q, p, q] for q in range(3)] for p in range(3)])
    sp = S @ P
    rel = (g1 ** 2 * z ** 2 / 2) * (sig ** 2 * sp ** 2 - S @ (P * sig ** 2 * sp))
    return (rel * P).tolist(), rel.tolist()


summary = {"run_id": RUN_ID}
for k in ("P1", "P2"):
    f = "results/%s.json" % k
    if os.path.exists(f):
        summary[k] = json.load(open(f))
summary["P2_predictions"] = json.load(open("predictions.json"))
zs = (np.arange(c3["nsave"] + 1) * (c3["nsteps"] // c3["nsave"]) * c3["dz_m"]).tolist()
summary["z_m"] = zs
P3 = {}
for s in (0, 1):
    for lam in (1.0, 0.5):
        d = decompose("P3", s, lam)
        if d:
            P3["s%g_lam%g" % (s, lam)] = d
d = decompose("P3s05", 0.5, 1.0)
if d:
    P3["s0.5_lam1"] = d
summary["P3"] = P3
conv = {}
for tag in ("conv_dz", "conv_dt", "conv_window"):
    d = decompose(tag, 1, 1.0)
    if d:
        conv[tag] = d
summary["convergence"] = conv
summary["langmuir_lineargain_prereg_W_and_rel_at_0.2m"] = langmuir_lineargain_second_order(0.2)
ev, od = langmuir_exact(0, c3["nsteps"], c3["dz_m"])
summary["langmuir_exactkernel_s0_even_W"] = ev.tolist()
ev1, od1 = langmuir_exact(1, c3["nsteps"], c3["dz_m"])
summary["langmuir_exactkernel_s1_even_W"] = ev1.tolist()
summary["langmuir_exactkernel_s1_odd_W"] = od1.tolist()
json.dump(summary, open("summary.json", "w"), indent=1)

# compact printout
print("z (m):", ["%.2f" % z for z in zs])
for k, d in P3.items():
    print("== P3", k)
    print("  odd(pair) mode0 mean/se at z=0.2:", d["odd_pair_mean"][-1][0], d["odd_pair_se"][-1][0],
          " max|odd|/N:", d["odd_pair_maxabs_rel"])
    print("  odd(base) mode0 mean/se at z=0.2:", d["odd_base_mean"][-1][0], d["odd_base_se"][-1][0])
    if "even_pair_mean" in d:
        print("  even(pair) modes at z=0.2:", d["even_pair_mean"][-1], "se", d["even_pair_se"][-1])
for k, d in conv.items():
    print("== conv", k, "odd0", d["odd_pair_mean"][-1][0], "+-", d["odd_pair_se"][-1][0],
          "even0", d.get("even_pair_mean", [[None]])[-1][0])
print("Langmuir linear-gain prereg (W, rel):", summary["langmuir_lineargain_prereg_W_and_rel_at_0.2m"])
print("Langmuir exact kernel s=0 even at 0.2 m:", ev[-1], " s=1 even:", ev1[-1], " s=1 odd:", od1[-1])
