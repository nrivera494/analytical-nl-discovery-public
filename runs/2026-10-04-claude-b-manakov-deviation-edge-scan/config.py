"""Exploration T-20261004-claude-b-06, follow-up: filter-edge dependence of the deviation of a finite-fraction GRIN
LP01/LP02 launch from the LP01 filtered Fano factor (pure-Kerr two-mode NLS, no Raman, no FWM).

Run id: 2026-10-04-claude-b-manakov-deviation-edge-scan (agent claude-b).
Uses twomode_lib.py from run 2026-10-04-claude-b-manakov-deviation-scan unchanged (N = 256 over 40 T0).
The hard bandpass is set by bin count, |k| <= kmax with w = k * 2pi/40, so the effective edge (kmax + 1/2) 2pi/40
is controlled exactly; kmax = 5 is the scan's filter (|w| < 0.8, effective edge 0.864) and reproduces it.
Cases: p2 = 0.3, delta in {0, 6 * 2pi/40 = 0.942}, kmax in {3, 4, 5, 6, 7}, zeta given on the command line.
Output: summary_zeta<zeta>.json in this folder.
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-04-claude-b-manakov-deviation-scan"))
from twomode_lib import noise, t, w, TW

DZ = 2e-3
C_GRIN = [[1, 1], [1, 0.5]]
UNIT = 2 * np.pi / TW


def main(z):
    p2 = 0.3
    p1 = 1 - p2
    S = C_GRIN[0][0] * p1 * p1 + 2 * C_GRIN[0][1] * p1 * p2 + C_GRIN[1][1] * p2 * p2
    sech = 1 / np.cosh(t)
    a0, b0 = np.sqrt(p1 / S) * sech + 0j, np.sqrt(p2 / S) * sech + 0j
    out = {"zeta": z, "p2": p2, "dz": DZ, "grid": {"N": len(t), "T_window": TW}, "cases": []}
    for kmax in (3, 4, 5, 6, 7):
        mask = (np.abs(np.round(w / UNIT)) <= kmax).astype(float)
        edge = (kmax + 0.5) * UNIT
        Fs = noise(sech + 0j, 0 * sech + 0j, z, DZ, C_GRIN, 0.0, mask, mask)["Fa"]
        for k in (0, 6):
            d = k * UNIT
            r = noise(a0, b0, z, DZ, C_GRIN, d, mask, mask)
            dB = 10 * np.log10(r["Ftot"]) - 10 * np.log10(Fs)
            out["cases"].append({"kmax": kmax, "edge": edge, "delta": d, "Fs_LP01": Fs, "computed": r, "Ftot_dB_minus_Fs_dB": dB})
            print(f"zeta={z} edge={edge:.3f} delta={d:.3f}: Fs={Fs:.5f} Ftot={r['Ftot']:.5f} dB={dB:+.4f} rho={r['rho']:+.4f}", flush=True)
    with open(os.path.join(HERE, f"summary_zeta{z:g}.json"), "w") as fh:
        json.dump(out, fh, indent=1, default=float)


if __name__ == "__main__":
    main(float(sys.argv[1]))
