"""Build summary.json for run 2026-10-08-claude-b.5-solver-twomode-check.

Reads ~/analytical-nl-discovery-data/2026-10-08-claude-b.5-solver-twomode-check/results.jsonl
(one JSON object per computed (point, kmax), written by run_twomode.jl) and
writes summary.json next to this script.

Usage: ~/agent-work/venv/bin/python runs/2026-10-08-claude-b.5-solver-twomode-check/summarize.py
"""
import json
import math
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
RUN_ID = "2026-10-08-claude-b.5-solver-twomode-check"
RAW = os.path.expanduser(f"~/analytical-nl-discovery-data/{RUN_ID}")
KALL = [3, 4, 5, 6, 7]
W0 = 1.0e6


def load():
    recs = []
    with open(os.path.join(RAW, "results.jsonl")) as fh:
        for line in fh:
            line = line.strip()
            if line:
                recs.append(json.loads(line))
    return recs


def close(a, b, rel=1e-12):
    return abs(a - b) <= rel * max(1.0, abs(a), abs(b))


def pick(recs, **kw):
    out = []
    for r in recs:
        ok = True
        for k, v in kw.items():
            rv = r.get(k)
            if isinstance(v, float) and isinstance(rv, (int, float)) and not isinstance(rv, bool):
                if not close(float(rv), v):
                    ok = False
                    break
            elif rv != v:
                ok = False
                break
        if ok:
            out.append(r)
    return out


def F_of(recs, **kw):
    m = pick(recs, **kw)
    return m[-1]["F"] if m else None


def git(*args):
    return subprocess.run(["git", "-C", os.path.join(HERE, "..", "..", "solver"), *args],
                          capture_output=True, text=True).stdout.strip()


def main():
    recs = load()
    S = {
        "run_id": RUN_ID,
        "agent": "claude-b.5",
        "model": "claude-opus-5-5",
        "family": "claude",
        "task": "T-20261008-claude-b-01",
        "solver_commit": git("rev-parse", "HEAD"),
        "solver_dirty": bool(git("status", "--porcelain")),
        "model_equations": "i a_z + a_tt/2 + (|a|^2+|b|^2) a = 0; i b_z + i delta b_t + b_tt/2 + (|a|^2 + C22 |b|^2) b = 0 (normalized soliton units)",
        "launch": "a = sqrt(p1/Sigma) sech(tau), b = sqrt(p2/Sigma) sech(tau), p1 = 1 - p2, Sigma = p1^2 + 2 p1 p2 + C22 p2^2",
        "readout": "N = sum_m sum_{|k|<=kmax} |A_m(Omega_k)|^2 (photon units, both modes, same hard bandpass), Omega_k = k 2pi/(40 T0); F = Var(N)/<N> from linearized vacuum noise of coherent inputs, Var(N) = sum |dN/dconj(B(0))|^2 with the discrete RK4IP adjoint",
        "conventions": {
            "T0_ps": 1.0, "beta2_ps2_per_m": -1.0, "L_D_m": 1.0, "gamma_per_W_per_m": 1.0,
            "P0_W": 1.0, "window_T0": 40.0, "Nt": 256,
            "frequency_bins": "solver frequency_axis is centered with a bin at Omega = 0; k = round(Omega T0/(2pi/40)), checked max |Omega - k dOmega| < 1e-9 dOmega",
            "omega0T0_production": W0,
            "self_steepening_parameter_s": 1.0 / W0,
            "adjoint_mode": "discrete_rk4ip (checkpoint_stride :auto)",
            "forward_method": "RK4IP fixed step, Float64, CPU (solve_mmgnlse default)",
            "raman": "NoRaman()",
            "exact_tensor": "symmetric_S = false: S[1,2,2,1] = S[2,1,1,2] = 0, other two-1/two-2 elements S0/2; removes the coherent A2^2 A1^* and A1^2 A2^* terms exactly, so the solver integrates the incoherent XPM model itself; kappa = 0; dz = 5e-4 L_D",
            "specified_tensor": "symmetric_S = true: all two-1/two-2 elements S0/2; coherent FWM suppressed by kappa = Delta beta0 L_D on mode 2; dz = 0.1/kappa L_D (2 kappa dz = 0.2)",
        },
    }

    def ex(label, p2, C22, zeta, delta, k, stage="exact_main"):
        return F_of(recs, stage=stage, symmetric_S=False, label=label, p2=float(p2),
                    C22=float(C22), zeta=float(zeta), delta=float(delta), kmax=k)

    def ref2(k):
        return ex("case2", 0.0, 0.5, 2.0, 0.0, k)

    # ---------------- case 1 ----------------
    c1 = {"description": "C22 = 1, delta = 0, zeta = 2: all-mode F at p2 = 0.3 versus scalar (p2 = 0)"}
    rows, maxrel = {}, 0.0
    for k in KALL:
        f0, f3 = ex("case1", 0.0, 1.0, 2.0, 0.0, k), ex("case1", 0.3, 1.0, 2.0, 0.0, k)
        if f0 is None or f3 is None:
            continue
        rel = (f3 - f0) / f0
        maxrel = max(maxrel, abs(rel))
        rows[str(k)] = {"F_scalar_p2_0": f0, "F_p2_0.3": f3, "rel_diff": rel}
    c1["exact_tensor"] = {"per_kmax": rows, "max_abs_rel_diff": maxrel}
    sym_rows = {}
    for kap in (1.0e3, 2.0e3):
        sub, mr = {}, 0.0
        for k in KALL:
            f0 = ex("case1", 0.0, 1.0, 2.0, 0.0, k)
            fs = F_of(recs, stage="sym_case1", symmetric_S=True, p2=0.3, C22=1.0, zeta=2.0,
                      kappa=kap, kmax=k)
            if f0 is None or fs is None:
                continue
            rel = (fs - f0) / f0
            mr = max(mr, abs(rel))
            sub[str(k)] = {"F_p2_0.3": fs, "rel_diff_vs_scalar": rel}
        if sub:
            sym_rows[f"kappa_{kap:.0f}"] = {"per_kmax": sub, "max_abs_rel_diff": mr}
    if sym_rows:
        c1["specified_tensor"] = sym_rows
    small = {}
    for z in (0.001, 0.01, 0.1):
        for p2 in (0.0, 0.3):
            for k in KALL:
                v = F_of(recs, stage="exact_smallzeta", p2=float(p2), zeta=float(z), kmax=k)
                if v is not None:
                    small.setdefault(f"zeta_{z:g}", {}).setdefault(f"p2_{p2}", {})[str(k)] = {
                        "F": v, "F_minus_1": v - 1.0}
    c1["small_zeta_exact_tensor"] = small
    S["case1"] = c1

    # ---------------- tables ----------------
    def ftable(label, p2s, C22, zeta, delta=0.0, ref=None):
        F, dF = {}, {}
        for k in KALL:
            f0 = ref(k) if ref is not None else ex(label, 0.0, C22, zeta, 0.0, k)
            for p2 in p2s:
                v = f0 if p2 == 0.0 else ex(label, p2, C22, zeta, delta, k)
                F.setdefault(f"p2_{p2}", {})[str(k)] = v
                if v is not None and f0 is not None:
                    dF.setdefault(f"p2_{p2}", {})[str(k)] = v - f0
        return F, dF

    def symtable(stage, label, p2s, C22, zeta, delta_list, ref, exact_lookup):
        out = {}
        for kap in (1.0e3, 2.0e3):
            for d in delta_list:
                for p2 in p2s:
                    for k in KALL:
                        v = F_of(recs, stage=stage, symmetric_S=True, label=label, p2=float(p2),
                                 C22=float(C22), zeta=float(zeta), delta=float(d), kappa=kap, kmax=k)
                        if v is None:
                            continue
                        key = f"p2_{p2}" if len(delta_list) == 1 else f"delta_{d}"
                        f0 = ref(k)
                        fe = exact_lookup(p2, d, k)
                        out.setdefault(f"kappa_{kap:.0f}", {}).setdefault(key, {})[str(k)] = {
                            "F": v, "dF": (v - f0) if f0 is not None else None,
                            "F_minus_exact_tensor": (v - fe) if fe is not None else None}
        if "kappa_1000" in out and "kappa_2000" in out:
            rich = {}
            for key, rws in out["kappa_2000"].items():
                for k, r2 in rws.items():
                    r1 = out["kappa_1000"].get(key, {}).get(k)
                    if r1 is None:
                        continue
                    FR = 2.0 * r2["F"] - r1["F"]
                    f0 = ref(int(k))
                    rich.setdefault(key, {})[k] = {
                        "F": FR, "dF": (FR - f0) if f0 is not None else None,
                        "F_minus_exact_tensor": (FR - (r2["F"] - r2["F_minus_exact_tensor"]))
                        if r2["F_minus_exact_tensor"] is not None else None}
            out["richardson_2F(2kappa)-F(kappa)"] = rich
            mx = {}
            for kk in ("kappa_1000", "kappa_2000", "richardson_2F(2kappa)-F(kappa)"):
                vals = [abs(r["F_minus_exact_tensor"]) for rws in out[kk].values() for r in rws.values()
                        if r["F_minus_exact_tensor"] is not None]
                if vals:
                    mx[kk] = max(vals)
            out["max_abs_F_minus_exact_tensor"] = mx
        return out

    F2, dF2 = ftable("case2", [0.0, 0.1, 0.2, 0.3], 0.5, 2.0)
    c2 = {"description": "zeta = 2, delta = 0, C22 = 0.5", "exact_tensor": {"F": F2, "dF": dF2}}
    s2 = symtable("sym_case2", "case2", [0.1, 0.2, 0.3], 0.5, 2.0, [0.0], ref2,
                  lambda p2, d, k: ex("case2", p2, 0.5, 2.0, 0.0, k))
    if s2:
        c2["specified_tensor"] = s2
    S["case2"] = c2

    ref4 = lambda k: ex("case4", 0.0, 0.5, 5.0, 0.0, k)
    F4, dF4 = ftable("case4", [0.0, 0.15, 0.3], 0.5, 5.0)
    c4 = {"description": "zeta = 5, delta = 0, C22 = 0.5", "exact_tensor": {"F": F4, "dF": dF4}}
    s4 = symtable("sym_case4", "case4", [0.15, 0.3], 0.5, 5.0, [0.0], ref4,
                  lambda p2, d, k: ex("case4", p2, 0.5, 5.0, 0.0, k))
    if s4:
        c4["specified_tensor"] = s4
    S["case4"] = c4

    c5 = {"description": "zeta = 2, C22 = 1 (Manakov overlaps), p2 = 0.5, delta in {0.1, 0.2}; dF relative to the scalar p2 = 0 value at zeta = 2 (the case-2 p2 = 0 point; with b = 0 the result does not depend on C22 or delta)"}
    F5, dF5 = {"p2_0_reference": {str(k): ref2(k) for k in KALL}}, {}
    for d in (0.1, 0.2):
        for k in KALL:
            v = ex("case5", 0.5, 1.0, 2.0, d, k)
            F5.setdefault(f"delta_{d}", {})[str(k)] = v
            if v is not None and ref2(k) is not None:
                dF5.setdefault(f"delta_{d}", {})[str(k)] = v - ref2(k)
    c5["exact_tensor"] = {"F": F5, "dF": dF5}
    s5 = symtable("sym_case5", "case5", [0.5], 1.0, 2.0, [0.1, 0.2], ref2,
                  lambda p2, d, k: ex("case5", 0.5, 1.0, 2.0, d, k))
    if s5:
        c5["specified_tensor"] = s5
    S["case5"] = c5

    F6, dF6 = ftable("case6", [0.0, 0.1, 0.3], 0.75, 2.0, ref=ref2)
    c6 = {"description": "zeta = 2, C22 = 0.75, delta = 0; p2 = 0 reference is the case-2 p2 = 0 point",
          "exact_tensor": {"F": F6, "dF": dF6}}
    s6 = symtable("sym_case6", "case6", [0.1, 0.3], 0.75, 2.0, [0.0], ref2,
                  lambda p2, d, k: ex("case6", p2, 0.75, 2.0, 0.0, k))
    if s6:
        c6["specified_tensor"] = s6
    S["case6"] = c6

    # ---------------- convergence (exact tensor) ----------------
    conv = {}
    exc = {}
    variants = ("dz_x2", "dz_half", "Nt_x2", "w0T0_1e7")
    for (label, p2, C22, zeta, delta) in (("case2", 0.0, 0.5, 2.0, 0.0), ("case2", 0.3, 0.5, 2.0, 0.0),
                                          ("case4", 0.3, 0.5, 5.0, 0.0), ("case5", 0.5, 1.0, 2.0, 0.2)):
        key = f"{label}_p2_{p2}_delta_{delta}_zeta_{zeta}"
        for v in variants:
            row = {}
            for k in KALL:
                base = ex(label, p2, C22, zeta, delta, k)
                var = ex(label, p2, C22, zeta, delta, k, stage="exact_conv_" + v)
                if base is None or var is None:
                    continue
                row[str(k)] = {"F_variant": var, "change_in_F": var - base}
            if row:
                row["max_abs_change"] = max(abs(r["change_in_F"]) for r in row.values())
                exc.setdefault(key, {})[v] = row
    ddf = {}
    for v in variants:
        row = {}
        for k in KALL:
            b3, b0 = ex("case2", 0.3, 0.5, 2.0, 0.0, k), ex("case2", 0.0, 0.5, 2.0, 0.0, k)
            v3 = ex("case2", 0.3, 0.5, 2.0, 0.0, k, stage="exact_conv_" + v)
            v0 = ex("case2", 0.0, 0.5, 2.0, 0.0, k, stage="exact_conv_" + v)
            if None in (b3, b0, v3, v0):
                continue
            row[str(k)] = (v3 - v0) - (b3 - b0)
        if row:
            ddf[v] = row
    exc["case2_change_in_dF_p2_0.3"] = ddf
    kap_rows = {}
    for kap in (1.0e3, 2.0e3):
        row = {}
        for k in KALL:
            base = ex("case2", 0.3, 0.5, 2.0, 0.0, k)
            v = F_of(recs, stage="exact_kappa", symmetric_S=False, p2=0.3, kappa=kap, kmax=k)
            if base is None or v is None:
                continue
            row[str(k)] = {"F": v, "change_in_F_vs_kappa_0": v - base}
        if row:
            kap_rows[f"kappa_{kap:.0f}"] = row
    exc["case2_p2_0.3_Delta_beta0_on_exact_tensor"] = kap_rows
    ss = {}
    for r in pick(recs, stage="exact_selfsteep"):
        key = f"{r['label']}_p2_{r['p2']}_delta_{r['delta']}_kmax_{r['kmax']}"
        ss.setdefault(key, {})[f"{r['omega0T0']:.6g}"] = r["F"]
    exc["self_steepening_scan_F_vs_omega0T0"] = ss
    fd = [{"tag": r["tag"], "direction": r["direction"], "dN_fd": r["dN_fd"],
           "dN_adjoint": r["dN_adjoint"], "rel_diff": r["rel_diff"]} for r in pick(recs, stage="fd_check")]
    exc["finite_difference_check_of_adjoint"] = fd
    sol = [{k: r[k] for k in ("Nt", "dz_LD", "max_abs_peak_dev", "max_abs_width_dev", "z_LD",
                              "rms_width_over_T0", "rms_width_sech_exact")}
           for r in pick(recs, stage="soliton_check")]
    exc["scalar_soliton_check_zeta_0_to_5"] = sol
    conv["exact_tensor"] = exc

    # ---------------- convergence (specified tensor), case 2, p2 = 0.3, kmax = 5 ----------------
    sc = {}
    fe = ex("case2", 0.3, 0.5, 2.0, 0.0, 5)
    f0 = ref2(5)
    sc["F_exact_tensor"] = fe
    for kap in (1.0e3, 2.0e3):
        base = F_of(recs, stage="sym_case2", symmetric_S=True, p2=0.3, kappa=kap, kmax=5)
        half = F_of(recs, stage="sym_conv_dz_half", symmetric_S=True, p2=0.3, kappa=kap, kmax=5)
        if base is not None and half is not None:
            sc[f"dz_half_at_kappa_{kap:.0f}"] = {"F_base": base, "F_dz_half": half,
                                                 "change_in_F": half - base,
                                                 "change_in_dF": half - base}
    base = F_of(recs, stage="sym_case2", symmetric_S=True, p2=0.3, kappa=1.0e3, kmax=5)
    nt2 = F_of(recs, stage="sym_conv_Nt_x2", symmetric_S=True, p2=0.3, kappa=1.0e3, kmax=5)
    if base is not None and nt2 is not None:
        sc["Nt_x2_at_kappa_1000"] = {"F_base": base, "F_Nt_512": nt2, "change_in_F": nt2 - base,
                                     "change_in_dF": nt2 - base}
    b1 = F_of(recs, stage="sym_case2", symmetric_S=True, p2=0.3, kappa=1.0e3, kmax=5)
    b2 = F_of(recs, stage="sym_case2", symmetric_S=True, p2=0.3, kappa=2.0e3, kmax=5)
    if b1 is not None and b2 is not None:
        sc["kappa_doubled_1000_to_2000"] = {"change_in_F": b2 - b1, "change_in_dF": b2 - b1}

    def kscan(stage, values):
        rows = {}
        for kap, tagk in values:
            v = F_of(recs, stage=stage, symmetric_S=True, p2=0.3, kappa=kap, kmax=5) if stage else None
            if v is None:
                continue
            rows[tagk] = {"kappa": kap, "F": v, "F_minus_exact_tensor": v - fe,
                          "kappa_times_F_minus_exact": kap * (v - fe)}
        return rows

    unlocked = {}
    for kap, st in ((1.0e3, "sym_case2"), (2.0e3, "sym_case2"), (4.0e3, "sym_conv_kappa"),
                    (8.0e3, "sym_conv_kappa")):
        v = F_of(recs, stage=st, symmetric_S=True, p2=0.3, kappa=kap, kmax=5)
        if v is not None:
            unlocked[f"{kap:.0f}"] = {"kappa": kap, "end_phase_2kappa_zeta_mod_2pi": (4 * kap) % (2 * math.pi),
                                      "F": v, "F_minus_exact_tensor": v - fe,
                                      "kappa_times_F_minus_exact": kap * (v - fe)}
    sc["kappa_scan_unlocked_end_phase"] = unlocked
    locked = {}
    for r in pick(recs, stage="sym_kscan_locked", kmax=5):
        locked[f"{r['kappa']:.4f}"] = {"kappa": r["kappa"], "F": r["F"], "F_minus_exact_tensor": r["F"] - fe,
                                       "kappa_times_F_minus_exact": r["kappa"] * (r["F"] - fe)}
    if locked:
        ks = sorted(locked.values(), key=lambda x: x["kappa"])
        exps = {}
        for a, b in zip(ks[:-1], ks[1:]):
            da, db = a["F_minus_exact_tensor"], b["F_minus_exact_tensor"]
            if da * db > 0:
                exps[f"{a['kappa']:.1f}->{b['kappa']:.1f}"] = math.log(abs(db / da)) / math.log(b["kappa"] / a["kappa"])
        rich = {}
        for a, b in zip(ks[:-1], ks[1:]):
            FR = (b["kappa"] * b["F"] - a["kappa"] * a["F"]) / (b["kappa"] - a["kappa"])
            rich[f"{a['kappa']:.1f}&{b['kappa']:.1f}"] = {"F_extrapolated": FR, "minus_exact_tensor": FR - fe}
        sc["kappa_scan_locked_end_phase"] = {"note": "kappa = m pi/2 so that 2 kappa zeta = 0 mod 2pi at zeta = 2",
                                             "points": locked, "local_exponents": exps,
                                             "richardson_1_over_kappa_pairs": rich}
    osc = {}
    b1v = F_of(recs, stage="sym_case2", symmetric_S=True, p2=0.3, kappa=1.0e3, kmax=5)
    if b1v is not None:
        osc["j0"] = {"kappa": 1.0e3, "F": b1v, "F_minus_exact_tensor": b1v - fe}
    for r in pick(recs, stage="sym_osc", kmax=5):
        j = round((r["kappa"] - 1.0e3) / (math.pi / 8))
        osc[f"j{j}"] = {"kappa": r["kappa"], "F": r["F"], "F_minus_exact_tensor": r["F"] - fe}
    if len(osc) > 1:
        if all(f"j{j}" in osc for j in range(4)):
            d = [osc[f"j{j}"]["F_minus_exact_tensor"] for j in range(4)]
            mean = sum(d) / 4
            amp = math.hypot((d[0] - d[2]) / 2, (d[1] - d[3]) / 2)
            osc["four_phase_mean_of_F_minus_exact"] = mean
            osc["four_phase_oscillation_amplitude"] = amp
            osc["kappa_times_mean"] = 1.0e3 * mean
            osc["kappa_times_amplitude"] = 1.0e3 * amp
            osc["note"] = ("j shifts the end phase 2 kappa zeta by j pi/2; the four-phase mean is the "
                           "secular part of F - F_exact at kappa = 1e3, the amplitude the end-phase part")
        sc["end_phase_scan_kappa_1000_plus_j_pi_over_8"] = osc
    conv["specified_tensor_case2_p2_0.3_kmax5"] = sc
    S["convergence"] = conv
    S["all_points"] = recs
    with open(os.path.join(HERE, "summary.json"), "w") as fh:
        json.dump(S, fh, indent=1)
    print("wrote", os.path.join(HERE, "summary.json"), "with", len(recs), "records")


if __name__ == "__main__":
    main()
