"""Compute and score held-out set 2 (claude-b, T-20261010-claude-interactive-05).
Oracle per case: run_points.run_case of run 2026-10-10-claude-b-nd-oracle (same code; bound_chain now also returns
lambda_2), then the second binary search stage (refine_binary.refine). Scores predictions.json (frozen in commit
cdb6951) and writes summary.json. Usage: python run.py
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-10-claude-b-nd-oracle"))
import run_points as rp
import refine_binary as rb

RUN = "2026-10-10-claude-b-nd-heldout2"
RAW = os.path.expanduser(f"~/analytical-nl-discovery-data/{RUN}")

if __name__ == "__main__":
    cases = json.load(open(os.path.join(HERE, "cases.json")))
    for c in cases:
        rp.run_case(RUN, c)
    rows = {json.loads(l)["tag"]: json.loads(l) for l in open(os.path.join(RAW, "rows.jsonl"))}
    pred = json.load(open(os.path.join(HERE, "predictions.json")))
    rng = np.random.default_rng(5)
    out = {}
    for c in cases:
        tag = c["tag"]
        r, p = rows[tag], pred[tag]
        d = np.load(os.path.join(RAW, tag + ".npz"))
        Fnn, wnn, (Fb, Tb, name) = rb.refine(d["C"], d["nbar"], d["Tbest"], d["evec"], rng)
        F_bin = min(Fb, r["F_best"])
        n = np.abs(d["alpha"]) ** 2
        w = d["w"]
        wb = (n * w).sum() / n.sum()
        Fc = 0.5 / ((n * (w - wb) ** 2).sum() / n.sum())
        wc = w[d["keep"]] - wb
        Fc_cov = float(wc @ d["C"] @ wc / (wc @ (d["nbar"] * wc)))
        s = dict(Z=r["N"] * r["xi"])
        s["P1_lam_min"] = dict(actual=r["lam_min"], formula=p["lam_min"]["formula"], rel_err=r["lam_min"] / p["lam_min"]["formula"] - 1,
                               c_measured=(1 - r["lam_min"] / p["lam_min"]["formula"]) * p["Phi"] ** 2,
                               pass_=bool(p["lam_min"]["lo"] <= r["lam_min"] <= p["lam_min"]["hi"]))
        s["P2_lam_pass"] = dict(actual=r["lam_pass"], formula=p["lam_pass"]["formula"], rel_err=r["lam_pass"] / p["lam_pass"]["formula"] - 1,
                                pass_=bool(p["lam_pass"]["lo"] <= r["lam_pass"] <= p["lam_pass"]["hi"]))
        s["P3_lam_pass_eq_lam_2"] = dict(rel=r["lam_pass"] / r["lam_2"] - 1, pass_=bool(abs(r["lam_pass"] / r["lam_2"] - 1) <= 1e-6))
        s["P4_F_centroid"] = dict(actual=Fc, pred=p["F_centroid"]["pred"], rel_err=Fc / p["F_centroid"]["pred"] - 1,
                                  momentum_check=Fc_cov / Fc, pass_=bool(abs(Fc / p["F_centroid"]["pred"] - 1) <= 0.01))
        s["P5_lam_gen"] = dict(actual=r["lam_gen"], ratio_to_F_centroid=r["lam_gen"] / Fc, gap_dB=10 * np.log10(Fc / r["lam_gen"]),
                               pass_=bool(10 ** -0.1 <= r["lam_gen"] / Fc <= 1.0))
        s["P6_binary_gap"] = dict(F_bin=F_bin, gap_dB_over_lam_gen=10 * np.log10(F_bin / r["lam_gen"]),
                                  pass_=bool(10 * np.log10(F_bin / r["lam_gen"]) >= 10.0))
        s["F_nonneg_heuristic"] = Fnn
        s["gaps_dB"] = dict(bin_vs_formula=10 * np.log10(F_bin / p["lam_min"]["formula"]), bin_vs_gen=10 * np.log10(F_bin / r["lam_gen"]),
                            bin_vs_min=10 * np.log10(F_bin / r["lam_min"]), bin_vs_pass=10 * np.log10(F_bin / r["lam_pass"]))
        out[tag] = s
        print(tag, json.dumps(s, default=float), flush=True)
    json.dump(out, open(os.path.join(HERE, "summary.json"), "w"), indent=1, default=float)
