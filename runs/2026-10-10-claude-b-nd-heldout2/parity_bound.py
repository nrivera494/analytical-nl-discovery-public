"""Parity bound (C-20261010-claude-a-03) on the held-out set 2 points (claude-b, T-20261010-claude-interactive-05).
Same construction as runs/2026-10-10-claude-b-nd-oracle/parity_bound.py. Writes parity_bound.json."""
import json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.expanduser("~/analytical-nl-discovery-data/2026-10-10-claude-b-nd-heldout2")
H = json.load(open(os.path.join(HERE, "summary.json")))
rows = {json.loads(l)["tag"]: json.loads(l) for l in open(os.path.join(RAW, "rows.jsonl"))}
out = {}
for tag in ("N16_zr0.5", "N24_zr1.25", "N12_zr2.5"):
    r = rows[tag]
    d = np.load(os.path.join(RAW, tag + ".npz"))
    C, nb, keep, w = d["C"], d["nbar"], d["keep"], d["w"]
    kk = np.rint(w[keep] / (2 * np.pi / r["TW"])).astype(int)
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
    Fb = H[tag]["P6_binary_gap"]["F_bin"]
    out[tag] = dict(lam_gen=r["lam_gen"], lam_odd=lo, lam_even=le, F_par=Fp, F_bin=Fb,
                    dB_bin_over_Fpar=10 * np.log10(Fb / Fp), dB_Fpar_over_gen=10 * np.log10(Fp / r["lam_gen"]))
    print(tag, {k: round(v, 4) for k, v in out[tag].items()})
json.dump(out, open(os.path.join(HERE, "parity_bound.json"), "w"), indent=1)
