"""Independent check of the parity-bound numbers reported on the -04 branch (C-20261010-claude-a-03: F_par = 0.152, 0.144,
0.061 at Phi = 20 for B = {nbar >= 1e-6, 1e-9, 1e-12 nbar_max}; unverified WIP read at 13:34) with this run's
dispersionless oracle (claude-b, T-20261010-claude-interactive-05). Gaussian p = exp(-t^2/T0^2), pure SPM, Nt = 2048 over
40 T0 (bins 2 pi/40). Writes parity_phi20.json."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-10-claude-b-nd-oracle"))
import nd_cov as nd
Phi = 20.0
g = nd.Grid(2048, 40.0)
eps = 1e-6; Nt = g.Nt; D = 2 * Nt
u0 = np.exp(-g.t ** 2 / 2) + 0j
dirs = np.zeros((D, Nt), complex)
dirs[:Nt] = np.eye(Nt) * (eps / np.sqrt(g.dt)); dirs[Nt:] = np.eye(Nt) * (1j * eps / np.sqrt(g.dt))
spm = lambda u: u * np.exp(1j * Phi * np.abs(u) ** 2)
o = nd.output_spectrum(g, spm(np.concatenate([u0[None] + dirs, u0[None] - dirs])))
d = (o[:D] - o[D:]) / (2 * eps)
J = np.concatenate([d.real.T, d.imag.T], axis=0)
alpha = nd.output_spectrum(g, spm(u0[None]))[0]
nall = np.abs(alpha) ** 2
G = 2 * (alpha.real[:, None] * J[:Nt] + alpha.imag[:, None] * J[Nt:])
out = {}
for thr in (1e-6, 1e-9, 1e-12):
    sel = np.where(nall >= thr * nall.max())[0]
    k = np.rint(g.w[sel] / (2 * np.pi / 40)).astype(int)
    ks = set(k)
    sel = sel[np.array([(-kk in ks) for kk in k])]
    k = np.rint(g.w[sel] / (2 * np.pi / 40)).astype(int)
    idx = {kk: i for i, kk in enumerate(k)}
    perm = np.array([idx[-kk] for kk in k])
    C = 0.25 * G[sel] @ G[sel].T
    nb = nall[sel]
    A = C / np.sqrt(nb)[:, None] / np.sqrt(nb)[None, :]
    n = len(nb)
    P = np.zeros((n, n)); P[np.arange(n), perm] = 1
    ue, se, _ = np.linalg.svd((np.eye(n) + P) / 2); Be = ue[:, se > 0.5]
    uo, so, _ = np.linalg.svd((np.eye(n) - P) / 2); Bo = uo[:, so > 0.5]
    le = float(np.linalg.eigvalsh(Be.T @ A @ Be)[0]); lo = float(np.linalg.eigvalsh(Bo.T @ A @ Bo)[0])
    Fp = 0.5 * (lo + le) if lo <= le else le
    out[str(thr)] = dict(n_bins=n, lam_odd=lo, lam_even=le, F_par=Fp, lam_gen=float(min(lo, le)))
    print(thr, {kk: (round(v, 5) if isinstance(v, float) else v) for kk, v in out[str(thr)].items()}, flush=True)
json.dump(out, open(os.path.join(HERE, "parity_phi20.json"), "w"), indent=1)
