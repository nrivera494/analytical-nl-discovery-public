"""Evaluate the Gaussian ceiling that the Lean library proves (even exponents only) and compare it
with the claim's real-p ceiling and with the TL leading eigenvalue measured by claude-interactive.9.

Lean (canonical_gaussian_ceiling), for q0 = N exp(-t^2/2) and every n >= 1:
    (2n)^(2n) eta^(2n-1) J_(2n) <= 2 (2n-1)^(2n-1) N^(2n) sqrt(pi/n),  J_(2n) = int_{-1}^{1} (1-s^2)^(n-1) ds.
This script is numerical (mpmath, 30 digits); it is not a Lean certificate.
Agent: claude-interactive (claude-opus-5-5, family claude). Task: T-20261018-claude-interactive-04.
"""
import json
import pathlib
from mpmath import mp, mpf, sqrt, pi, gamma, quad, findroot, diff

mp.dps = 30
HERE = pathlib.Path(__file__).resolve().parent
TL = HERE.parent / "2026-10-18-claude-interactive.9-mask-adversary" / "summary.json"


def J(p):
    return sqrt(pi) * gamma(mpf(p) / 2) / gamma(mpf(p + 1) / 2)


def C(p):
    return mpf(p) ** p / mpf(p - 1) ** (p - 1) * J(p) / 2


def eta_ceiling(N, p):  # [int |q0|^p / C_p]^(1/(p-1)) with int (N e^{-t^2/2})^p = N^p sqrt(2 pi / p)
    return (N ** p * sqrt(2 * pi / p) / C(p)) ** (1 / (mpf(p) - 1))


def main():
    # check the integral form used in Lean against the Gamma closed form
    for n in (1, 2, 4, 8):
        assert abs(quad(lambda s: (1 - s * s) ** (n - 1), [-1, 1]) - J(2 * n)) < mpf(10) ** -25
    tl = {h["case"]: h["TL_eta_verified"] for h in json.loads(TL.read_text())["headline"]
          if h["case"].startswith("gauss")}
    out = {}
    for case, eta_tl in sorted(tl.items(), key=lambda kv: float(kv[0].split("=")[1])):
        N = mpf(case.split("=")[1])
        M0 = N ** 2 * sqrt(pi)
        n_best = min(range(1, 60), key=lambda n: eta_ceiling(N, 2 * n))
        e_even = eta_ceiling(N, 2 * n_best)
        f = lambda p: eta_ceiling(N, p)
        p_star = findroot(lambda p: diff(f, p), 2 * n_best)
        e_real = f(p_star) if p_star > 2 else f(mpf(2))
        out[case] = {
            "TL_eta_claude9": eta_tl,
            "TL_f1": float(4 * mpf(eta_tl) / M0),
            "lean_even_best_2n": 2 * n_best,
            "lean_even_f1_ceiling": float(4 * e_even / M0),
            "lean_even_rel_headroom_over_TL": float(e_even / mpf(eta_tl) - 1),
            "realp_p_star": float(p_star),
            "realp_f1_ceiling_not_formalized": float(4 * e_real / M0),
            "realp_rel_headroom_over_TL": float(e_real / mpf(eta_tl) - 1),
        }
    (HERE / "gaussian_even_ceiling.json").write_text(json.dumps(out, indent=2) + "\n")
    for k, v in out.items():
        print(k, json.dumps(v))


if __name__ == "__main__":
    main()
