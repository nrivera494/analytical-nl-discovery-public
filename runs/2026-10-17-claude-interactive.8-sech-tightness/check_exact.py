"""C-20261017-gpt-d-01: closed form vs two independent quadratures, asymptotic exponents.

Run after predictions.json was committed (freeze commit f784fed).
"""
import json, time
import mpmath as mp
import numpy as np
from ramanlib import (rho_closed, rho_spectral, rho_time, rho_long_lead, rho_long_two,
                      osc_moment, q_diff)

mp.mp.dps = 40
t0 = time.time()
pred = json.load(open("predictions.json"))
out = {"run_id": "2026-10-17-claude-interactive.8-sech-tightness", "freeze_commit": "f784fed"}

# ---------------------------------------------------------------- 0. Laplace transform of q (derivation step)
lap = []
for s in [mp.mpf("0.3"), mp.mpf(2), mp.mpc(0.38125, -1) * 3, mp.mpc(5, -1) * 0.2, mp.mpc(0.1, -1) * 40]:
    num = mp.quad(lambda v: mp.exp(-s * v) * q_diff(v), [0, 1, 5, 20, 80])
    cf = (1 - s) / 2 + s**2 / 4 * mp.psi(1, 1 + s / 2)
    lap.append({"s": str(s), "quad": mp.nstr(num, 20), "closed": mp.nstr(cf, 20),
                "absdiff": float(abs(num - cf))})
out["laplace_q"] = lap
out["q_first_moment"] = float(mp.quad(lambda v: v * q_diff(v), [0, 1, 5, 20, 80]))  # should be 1/2

# ---------------------------------------------------------------- 1. held-out exact formula
rows = []
for e in pred["exact_formula"]:
    r, x = e["r"], e["x"]
    rc = mp.mpf(e["rho_claim"])
    rs = rho_spectral(r, x)
    rt = rho_time(r, x) if x <= 40 else None   # time-domain form oscillatory for long pulses
    rows.append({"r": r, "x": x, "rho_claim": float(rc), "rho_spectral": float(rs),
                 "rel_spec": float(abs(rs - rc) / rc),
                 "rho_time": None if rt is None else float(rt),
                 "rel_time": None if rt is None else float(abs(rt - rc) / rc)})
out["heldout_exact"] = rows
out["heldout_max_rel_spec"] = max(r_["rel_spec"] for r_ in rows)
out["heldout_max_rel_time"] = max(r_["rel_time"] for r_ in rows if r_["rel_time"] is not None)
out["heldout_exact_pass"] = bool(out["heldout_max_rel_spec"] < 1e-9 and out["heldout_max_rel_time"] < 1e-9)

# ---------------------------------------------------------------- 2. long-pulse exponents
def slope(xs, ys):
    p = np.polyfit(np.log(np.asarray(xs, float)), np.log(np.abs(np.asarray(ys, float))), 1)
    return float(p[0])

xl = [float(v) for v in np.geomspace(50, 400, 8)]
long_rows = []
for r in [0.1, 0.2275, 0.45, 1.0, 2.5, 5.0]:
    lead_err, two_err, decay = [], [], []
    for x in xl:
        rc = rho_closed(r, x)
        lead_err.append(float((rc - rho_long_lead(r, x)) / rc))
        two_err.append(float((rc - rho_long_two(r, x)) / rc))
        decay.append(float(rc))
    # coefficient extrapolation: rho x^3 = C3 (1 + c x^-2 + ...); fit vs x^-2 at the 3 largest x
    X = np.array(xl[-3:]) ** -2.0
    Y = np.array([float(rho_closed(r, x) * mp.mpf(x) ** 3) for x in xl[-3:]])
    C3_fit = float(np.polyfit(X, Y, 2)[-1])
    C3_ex = 16 * r / (15 * (1 + r * r) ** 2)
    row = {"r": r, "decay_slope": slope(xl, decay), "lead_relerr_slope": slope(xl, lead_err),
           "two_relerr_slope": slope(xl, two_err), "C3_extrapolated": C3_fit, "C3_claim": C3_ex,
           "C3_rel": abs(C3_fit - C3_ex) / C3_ex, "lead_relerr_at_400": lead_err[-1],
           "two_relerr_at_400": two_err[-1]}
    if r == 1.0:
        row["pass"] = abs(row["lead_relerr_slope"] + 4) <= 0.15
    else:
        row["pass"] = abs(row["lead_relerr_slope"] + 2) <= 0.05 and abs(row["two_relerr_slope"] + 4) <= 0.15
    long_rows.append(row)
out["long"] = long_rows

# general-response remainder bound check (oscillator): |R| <= 16 mu5abs/(225 k T^7)
rem_rows = []
for r in [0.2275, 1.0, 5.0]:
    a, b = mp.mpf(r), mp.mpf(1)
    k = a * a + b * b
    mu1, mu3 = osc_moment(1, a, b), osc_moment(3, a, b)
    h = lambda t: k / b * mp.exp(-a * t) * mp.sin(b * t)
    mu5abs = mp.quad(lambda t: t**5 * abs(h(t)), [mp.pi * j for j in range(0, 400)] + [mp.inf])
    for x in [3.0, 10.0, 30.0]:
        T = mp.mpf(x)
        R = rho_closed(r, x) - (8 * mu1 / (15 * k * T**3) - 16 * mu3 / (63 * k * T**5))
        bound = 16 * mu5abs / (225 * k * T**7)
        rem_rows.append({"r": r, "x": x, "R": float(R), "bound": float(bound),
                         "R_over_bound": float(R / bound), "ok": bool(abs(R) <= bound)})
    # mu1, mu3 closed forms vs quadrature
out["remainder_bound"] = rem_rows
out["moments_check"] = []
for r in [0.2275, 2.5]:
    a, b = mp.mpf(r), mp.mpf(1)
    k = a * a + b * b
    h = lambda t: k / b * mp.exp(-a * t) * mp.sin(b * t)
    for j in [1, 3]:
        q = mp.quad(lambda t: t**j * h(t), [mp.pi * i for i in range(0, 200)] + [mp.inf])
        out["moments_check"].append({"r": r, "j": j, "quad": float(q), "closed": float(osc_moment(j, a, b))})

# ---------------------------------------------------------------- 3. short-pulse exponents
xs = [float(v) for v in np.geomspace(1e-4, 1e-2, 8)]
short_rows = []
for r in [0.1, 0.2275, 0.45, 1.0, 2.5, 5.0]:
    rr = mp.mpf(r)
    c2 = mp.pi**2 * (3 * rr**2 - 1) / 12
    c3 = 2 * rr * (1 - rr**2) * mp.zeta(3)
    gap_ratio, res3, res4 = [], [], []
    for x in xs:
        X = mp.mpf(x)
        rc = rho_closed(r, x)
        gap_ratio.append(float((1 - rc) / (2 * rr * X) - 1))
        res3.append(float(1 - rc - 2 * rr * X + c2 * X**2))   # 1-rho = 2rx - c2 x^2 - c3 x^3
        res4.append(float(1 - rc - 2 * rr * X + c2 * X**2 + c3 * X**3))
    row = {"r": r, "gap_ratio_slope": slope(xs, gap_ratio), "cubic_residual_slope": slope(xs, res3),
           "quartic_residual_slope": slope(xs, res4),
           "c3_measured": float(mp.mpf(res3[0]) / -(mp.mpf(xs[0]) ** 3)), "c3_claim": float(c3)}
    ok1 = abs(row["gap_ratio_slope"] - 1) <= 0.05
    ok2 = abs(row["cubic_residual_slope"] - (4 if r == 1.0 else 3)) <= (0.15 if r == 1.0 else 0.1)
    row["pass"] = bool(ok1 and ok2)
    short_rows.append(row)
out["short"] = short_rows

# short-limit exact value check against quadrature at very small x (adds an independent number)
out["short_quadrature"] = []
for r in [0.45, 5.0]:
    for x in [1e-3, 1e-2]:
        rs, rc = rho_spectral(r, x), rho_closed(r, x)
        out["short_quadrature"].append({"r": r, "x": x, "one_minus_rho_spec": float(1 - rs),
                                        "one_minus_rho_closed": float(1 - rc),
                                        "rel_gap_diff": float(abs((1 - rs) - (1 - rc)) / (1 - rc))})

out["wall_time_s"] = time.time() - t0
json.dump(out, open("summary_static.json", "w"), indent=1)
print(json.dumps({k: out[k] for k in ["heldout_max_rel_spec", "heldout_max_rel_time", "heldout_exact_pass",
                                       "q_first_moment"]}, indent=1))
for row in long_rows: print("long", row)
for row in short_rows: print("short", row)
for row in rem_rows: print("rem", row)
print(out["moments_check"]); print(out["laplace_q"]); print(out["short_quadrature"])
print("wall", out["wall_time_s"])
