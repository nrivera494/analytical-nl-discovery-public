"""Compute and score held-out set 3 (claude-b, T-20261010-claude-interactive-05; predictions frozen in d6ab3a9).
Usage: python run.py -> summary.json"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-10-claude-b-nd-oracle"))
import run_points as rp
import refine_binary as rb

RUN = "2026-10-10-claude-b-nd-heldout3"
RAW = os.path.expanduser(f"~/analytical-nl-discovery-data/{RUN}")
if __name__ == "__main__":
    c = json.load(open(os.path.join(HERE, "cases.json")))[0]
    rp.run_case(RUN, c)
    r = [json.loads(l) for l in open(os.path.join(RAW, "rows.jsonl"))][-1]
    p = json.load(open(os.path.join(HERE, "predictions.json")))
    d = np.load(os.path.join(RAW, c["tag"] + ".npz"))
    C, nb, keep, w = d["C"], d["nbar"], d["keep"], d["w"]
    Fnn, wnn, (Fr, Tr, name) = rb.refine(C, nb, d["Tbest"], d["evec"], np.random.default_rng(9))
    F_bin = min(Fr, r["F_best"])
    n = np.abs(d["alpha"]) ** 2
    wb = (n * w).sum() / n.sum()
    Fc = 0.5 / ((n * (w - wb) ** 2).sum() / n.sum())
    kk = np.rint(w[keep] / (2 * np.pi / c["TW"])).astype(int)
    ks = set(kk)
    inB = np.array([(-k in ks) for k in kk])
    Cb, nbb, kb = C[np.ix_(inB, inB)], nb[inB], kk[inB]
    idx = {k: i for i, k in enumerate(kb)}
    perm = np.array([idx[-k] for k in kb])
    A = Cb / np.sqrt(nbb)[:, None] / np.sqrt(nbb)[None, :]
    m = len(nbb)
    P = np.zeros((m, m)); P[np.arange(m), perm] = 1
    ue, se, _ = np.linalg.svd((np.eye(m) + P) / 2); Be = ue[:, se > 0.5]
    uo, so, _ = np.linalg.svd((np.eye(m) - P) / 2); Bo = uo[:, so > 0.5]
    le = float(np.linalg.eigvalsh(Be.T @ A @ Be)[0]); lo = float(np.linalg.eigvalsh(Bo.T @ A @ Bo)[0])
    Fpar = 0.5 * (lo + le) if lo <= le else le
    s = dict(Z=r["N"] * r["xi"], lam_min=r["lam_min"], lam_pass=r["lam_pass"], lam_2=r["lam_2"], lam_gen=r["lam_gen"],
             F_centroid=Fc, F_par=Fpar, lam_odd=lo, lam_even=le, F_bin=F_bin)
    s["P1_lam_min"] = dict(rel_err=r["lam_min"] / p["lam_min_formula"] - 1,
                           pass_=bool(p["lam_min_lo"] <= r["lam_min"] <= p["lam_min_formula"]))
    s["P2_centroid"] = dict(rel_err=Fc / p["F_centroid"] - 1, gen_dB_below=10 * np.log10(Fc / r["lam_gen"]),
                            pass_=bool(abs(Fc / p["F_centroid"] - 1) <= 0.01 and 0 <= 10 * np.log10(Fc / r["lam_gen"]) <= 1.0))
    s["P3_Fpar_over_gen_dB"] = dict(value=10 * np.log10(Fpar / r["lam_gen"]), pass_=bool(10 * np.log10(Fpar / r["lam_gen"]) >= 7.0))
    s["P4_bin_over_Fpar_dB"] = dict(value=10 * np.log10(F_bin / Fpar), pass_=bool(2.0 <= 10 * np.log10(F_bin / Fpar) <= 6.5))
    json.dump(s, open(os.path.join(HERE, "summary.json"), "w"), indent=1, default=float)
    print(json.dumps(s, indent=1, default=float))
