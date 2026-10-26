"""Exploration T-20261004-claude-b-06: deviation of the filtered Fano factor of a finite-fraction GRIN LP01/LP02
launch from the LP01 (Manakov-limit) value, in the pure-Kerr two-mode NLS (no Raman, no FWM).

Run id: 2026-10-04-claude-b-manakov-deviation-scan (agent claude-b).
Model and noise method: twomode_lib.py (same code as run 2026-10-04-claude-b-reduction-selfcheck, where the
Manakov rotation formulas were reproduced to 1e-9 and the walk-off gauge to 1e-8).
Launch: a = sqrt(p1/S) sech(t), b = sqrt(p2/S) sech(t), S = sum C_mn p_m p_n  (the card's gamma_eff energy),
C = [[1,1],[1,1/2]] (ideal parabolic LP01/LP02). Readout: hard bandpass |w| < 0.8 on both modes (fixed, not shifted),
all-mode count (F_tot) and mode-resolved counts (F_a, F_b, rho). Reference: scalar LP01 soliton a = sech, same z.
Manakov prediction at d = 0: F_tot = F_s, F_a = cos^2 F_s + sin^2, F_b = sin^2 F_s + cos^2, rho = cos sin (F_s-1)/sqrt(F_a F_b),
with tan^2(theta) = p2/p1.
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from twomode_lib import noise, t, w, TW

DZ, WF = 2e-3, 0.8
C_GRIN = [[1, 1], [1, 0.5]]
UNIT = 2 * np.pi / TW            # frequency-grid spacing; walk-offs are multiples of it


def launch(p2):
    p1 = 1 - p2
    S = C_GRIN[0][0] * p1 * p1 + 2 * C_GRIN[0][1] * p1 * p2 + C_GRIN[1][1] * p2 * p2
    sech = 1 / np.cosh(t)
    return np.sqrt(p1 / S) * sech + 0j, np.sqrt(p2 / S) * sech + 0j, S


def manakov_pred(Fs, p2):
    th = np.arctan(np.sqrt(p2 / (1 - p2)))
    c2, s2 = np.cos(th)**2, np.sin(th)**2
    Fa, Fb = c2 * Fs + s2, s2 * Fs + c2
    return dict(Ftot=Fs, Fa=Fa, Fb=Fb, rho=float(np.cos(th) * np.sin(th) * (Fs - 1) / np.sqrt(Fa * Fb)))


def main():
    mask = (np.abs(w) < WF).astype(float)
    out = {"model": "pure-Kerr two-mode NLS, C=[[1,1],[1,1/2]], gamma_eff launch, hard bandpass |w|<0.8 on both modes",
           "dz": DZ, "grid": {"N": 256, "T_window": TW}, "cases": []}
    plan = [(2.0, p2, k) for p2 in (0.05, 0.15, 0.30) for k in (0, 3, 6)] + [(5.0, p2, k) for p2 in (0.15, 0.30) for k in (0, 6)]
    Fs_cache = {}
    for z, p2, k in plan:
        if z not in Fs_cache:
            sech = 1 / np.cosh(t)
            Fs_cache[z] = noise(sech + 0j, 0 * sech + 0j, z, DZ, C_GRIN, 0.0, mask, mask)["Fa"]
        Fs = Fs_cache[z]
        a0, b0, S = launch(p2)
        d = k * UNIT
        r = noise(a0, b0, z, DZ, C_GRIN, d, mask, mask)
        pred = manakov_pred(Fs, p2)
        case = {"zeta": z, "p2": p2, "delta": d, "S_gamma_eff": S, "Fs_LP01": Fs, "computed": r, "manakov_pred_delta0": pred,
                "Ftot_minus_Fs": r["Ftot"] - Fs, "Ftot_over_Fs": r["Ftot"] / Fs,
                "Ftot_dB_minus_Fs_dB": 10 * np.log10(r["Ftot"]) - 10 * np.log10(Fs)}
        out["cases"].append(case)
        print(f"zeta={z} p2={p2:.2f} delta={d:.3f}: Ftot={r['Ftot']:.5f} (Fs={Fs:.5f}, dB diff {case['Ftot_dB_minus_Fs_dB']:+.3f}) "
              f"Fa={r['Fa']:.4f} Fb={r['Fb']:.4f} rho={r['rho']:+.4f} | Manakov: Fa={pred['Fa']:.4f} Fb={pred['Fb']:.4f} rho={pred['rho']:+.4f} "
              f"| Nb/(Na+Nb)={r['Nb']/(r['Na']+r['Nb']):.3f}", flush=True)
    out["Fs_LP01"] = Fs_cache
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "summary.json"), "w") as fh:
        json.dump(out, fh, indent=1, default=float)


if __name__ == "__main__":
    main()
