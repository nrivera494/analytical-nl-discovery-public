"""POST-FREEZE summary for run 2026-10-10-claude-b.6-solver-nd-check.

Written after summary.json was hashed (sha256 3c6879c7...4803, 11:11:49 EDT). It
(1) collects the post-freeze solver points (results_postfreeze.jsonl: self-steepening
dynamics with photon counting uniform in frequency, s = 1/121.526 and s = 0.0082), and
(2) compares the frozen solver numbers with claude-b's numpy covariance matrices in
~/analytical-nl-discovery-data/2026-10-10-claude-b-nd-oracle/*.npz (read-only), which were
opened for the first time after the freeze. F_numpy = 1^T C_T 1 / sum(nbar_T) over the
filter bins, with bins identified as k = round(w / (2pi/40)) on claude-b's numpy fftfreq axis.

Convention: claude-b's spectrum is numpy fft(u) (coefficient of exp(+i w t)), the solver's is
ifft (coefficient of exp(-i Omega t)), and both time-domain equations carry self-steepening
as (1 + i s d/dtau)(|u|^2 u). Hence claude-b's bin k is the solver's bin -k ("mirror").

Usage (repository root):
  ~/agent-work/venv/bin/python runs/2026-10-10-claude-b.6-solver-nd-check/summarize_postfreeze.py
"""
import json
import os
import numpy as np

RUN_ID = "2026-10-10-claude-b.6-solver-nd-check"
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(os.path.expanduser("~"), "analytical-nl-discovery-data", RUN_ID)
ORACLE = os.path.join(os.path.expanduser("~"), "analytical-nl-discovery-data",
                      "2026-10-10-claude-b-nd-oracle")
FN = ("best_binary_bins", "best_interval_bins")

frozen = json.load(open(os.path.join(HERE, "summary.json")))
filters = json.load(open(os.path.join(HERE, "filters_for_solver.json")))
post = [json.loads(l) for l in open(os.path.join(RAW, "results_postfreeze.jsonl")) if l.strip()]


def pick(stage, fname, mirror):
    out = [r for r in post if r["stage"] == stage and r["filter"] == fname and r["mirror"] == mirror]
    return out[-1]["F"] if out else None


def numpy_F(npz, key, fname, mirror):
    d = np.load(os.path.join(ORACLE, npz))
    dk = 2 * np.pi / 40
    kb = np.round(d["w"][d["keep"]] / dk).astype(int)
    assert np.max(np.abs(d["w"][d["keep"]] - kb * dk)) < 1e-9
    bins = np.array(filters[key][fname]) * (-1 if mirror else 1)
    sel = np.isin(kb, bins)
    missing = int(len(bins) - sel.sum())
    F = float(d["C"][np.ix_(sel, sel)].sum() / d["nbar"][sel].sum())
    return F, missing


out = {"run_id": RUN_ID, "status": "POST-FREEZE; not part of the hashed summary.json",
       "convention": "claude-b numpy bin k == solver bin -k (solver 'mirror')"}

# (1) post-freeze solver points
ss = {}
for fname in FN:
    ss[fname] = {
        "s_1_over_121.526": {"solver_filter(+k)": pick("post_B", fname, False),
                             "solver_mirror(-k)": pick("post_B", fname, True),
                             "dz_halved_change_filter": (pick("post_B_conv_n8000", fname, False)
                                                         - pick("post_B", fname, False)),
                             "dz_halved_change_mirror": (pick("post_B_conv_n8000", fname, True)
                                                         - pick("post_B", fname, True))},
        "s_0.0082": {"solver_filter(+k)": pick("post_B_s0082", fname, False),
                     "solver_mirror(-k)": pick("post_B_s0082", fname, True)}}
out["B_selfsteepening_uniform_photon_weights"] = ss

# (2) comparison with claude-b's numpy covariances
cmp = {}
for npz, key in (("N10_zr0.7.npz", "N10_zr0.7"), ("N20_zr0.3.npz", "N20_zr0.3")):
    for fname in FN:
        Fn, miss = numpy_F(npz, key, fname, False)
        Fs = frozen["case_A"][key][fname]["F_s0"]
        cmp[f"A/{key}/{fname}"] = {"numpy_bins_as_given": Fn, "missing_bins": miss,
                                   "solver_F_s0": Fs, "numpy_minus_solver": Fn - Fs}
for fname in FN:
    for mirror in (False, True):
        Fn, miss = numpy_F("N10_zr0.7_ss0.0082.npz", "N10_zr0.7", fname, mirror)
        # numpy bins as given (mirror=False) correspond to solver mirror (-k)
        Fs = pick("post_B", fname, not mirror)
        Fs2 = pick("post_B_s0082", fname, not mirror)
        cmp[f"B_ss_uniform/{fname}/numpy_{'mirror' if mirror else 'as_given'}"] = {
            "numpy": Fn, "missing_bins": miss,
            "solver_same_physical_bins_s=1/121.526": Fs, "numpy_minus_solver": Fn - Fs,
            "solver_same_physical_bins_s=0.0082": Fs2, "numpy_minus_solver_s0082": Fn - Fs2}
out["comparison_with_claude_b_numpy"] = cmp

with open(os.path.join(HERE, "summary_postfreeze.json"), "w") as f:
    json.dump(out, f, indent=1)
print(json.dumps(out, indent=1))
