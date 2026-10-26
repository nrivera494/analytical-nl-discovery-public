"""Parity bound (C-20261010-claude-a-03) on the Raman-reservoir covariances of this run (claude-b,
T-20261010-claude-interactive-05). The reservoir spectrum is even and the deterministic response is not included, so the
problem stays parity-symmetric. Writes parity_raman.json."""
import json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.expanduser("~/analytical-nl-discovery-data/2026-10-10-claude-b-nd-raman")
S = json.load(open(os.path.join(HERE, "summary.json")))["points"]
out = {}
for tag, p in S.items():
    Nt = p["Nt"]
    w = 2 * np.pi * np.fft.fftfreq(Nt, d=40.0 / Nt)
    for T0, r in p["by_T0"].items():
        d = np.load(os.path.join(RAW, f"{tag}_T0_{int(float(T0))}.npz"))
        C, nb, keep = d["C"], d["nbar"], d["keep"]
        kk = np.rint(w[keep] / (2 * np.pi / 40)).astype(int)
        ks = set(kk)
        inB = np.array([(-k in ks) for k in kk])
        C, nb, kk = C[np.ix_(inB, inB)], nb[inB], kk[inB]
        idx = {k: i for i, k in enumerate(kk)}
        perm = np.array([idx[-k] for k in kk])
        A = C / np.sqrt(nb)[:, None] / np.sqrt(nb)[None, :]
        n = len(nb)
        P = np.zeros((n, n)); P[np.arange(n), perm] = 1
        ue, se, _ = np.linalg.svd((np.eye(n) + P) / 2); Be = ue[:, se > 0.5]
        uo, so, _ = np.linalg.svd((np.eye(n) - P) / 2); Bo = uo[:, so > 0.5]
        le = float(np.linalg.eigvalsh(Be.T @ A @ Be)[0]); lo = float(np.linalg.eigvalsh(Bo.T @ A @ Bo)[0])
        Fp = 0.5 * (lo + le) if lo <= le else le
        out[f"{tag}_T0_{T0}"] = dict(lam_gen=r["lam_gen"], lam_odd=lo, lam_even=le, F_par=Fp, F_bin=r["F_bin"],
                                      dB_bin_over_Fpar=10 * np.log10(r["F_bin"] / Fp), dB_Fpar_over_gen=10 * np.log10(Fp / r["lam_gen"]))
        o = out[f"{tag}_T0_{T0}"]
        print(f"{tag} T0={T0}: gen {o['lam_gen']:.4f} odd {lo:.4f} even {le:.4f} F_par {Fp:.4f} F_bin {o['F_bin']:.4f} | bin/F_par {o['dB_bin_over_Fpar']:.2f} dB, F_par/gen {o['dB_Fpar_over_gen']:.2f} dB")
json.dump(out, open(os.path.join(HERE, "parity_raman.json"), "w"), indent=1)
