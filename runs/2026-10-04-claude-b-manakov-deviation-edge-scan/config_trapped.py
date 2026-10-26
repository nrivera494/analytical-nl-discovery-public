"""Trapped-carrier readout for run 2026-10-04-claude-b-manakov-deviation-edge-scan (claude-b, T-20261004-claude-b-06).

With walk-off delta the two components trap: momentum conservation (N_a w_a + N_b w_b = 0) and equal group velocity
(w_a - w_b = delta) put the carriers at w_a = +p2 delta and w_b = -p1 delta (trapping_check.py measures the centroids).
Mode-resolved readout with each band centred on its trapped carrier, rounded to the nearest grid bin:
LP01 |k - 2| <= kmax (centre +0.314; p2 delta = 0.283), LP02 |k + 4| <= kmax (centre -0.628; -p1 delta = -0.659).
p2 = 0.3, delta = 0.942, kmax in {3, 4, 5, 6, 7}, zeta from the command line. F_s is the LP01 soliton with the
centred band |k| <= kmax (as in config.py), so the comparison is at equal band width.
Usage: python config_trapped.py <zeta>  ->  summary_trapped_zeta<zeta>.json
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-04-claude-b-manakov-deviation-scan"))
from twomode_lib import noise, t, w, TW

DZ = 2e-3
C_GRIN = [[1, 1], [1, 0.5]]
UNIT = 2 * np.pi / TW
KA, KB, KD = 2, -4, 6


def main(z):
    p2 = 0.3; p1 = 1 - p2
    S = p1 * p1 + 2 * p1 * p2 + 0.5 * p2 * p2
    sech = 1 / np.cosh(t)
    a0, b0 = np.sqrt(p1 / S) * sech + 0j, np.sqrt(p2 / S) * sech + 0j
    k = np.round(w / UNIT)
    d = KD * UNIT
    out = {"mode": "trapped", "zeta": z, "p2": p2, "delta": d, "band_centres": [KA * UNIT, KB * UNIT], "cases": []}
    for kmax in (3, 4, 5, 6, 7):
        edge = (kmax + 0.5) * UNIT
        m0 = (np.abs(k) <= kmax).astype(float)
        Fs = noise(sech + 0j, 0 * sech + 0j, z, DZ, C_GRIN, 0.0, m0, m0)["Fa"]
        mA = (np.abs(k - KA) <= kmax).astype(float)
        mB = (np.abs(k - KB) <= kmax).astype(float)
        r = noise(a0, b0, z, DZ, C_GRIN, d, mA, mB)
        dB = 10 * np.log10(r["Ftot"]) - 10 * np.log10(Fs)
        out["cases"].append({"kmax": kmax, "half_width": edge, "Fs_LP01": Fs, "computed": r, "Ftot_dB_minus_Fs_dB": dB})
        print(f"trapped zeta={z} half-width={edge:.3f}: Fs={Fs:.5f} Ftot={r['Ftot']:.5f} dB={dB:+.4f} rho={r['rho']:+.4f}", flush=True)
    with open(os.path.join(HERE, f"summary_trapped_zeta{z:g}.json"), "w") as fh:
        json.dump(out, fh, indent=1, default=float)


if __name__ == "__main__":
    main(float(sys.argv[1]))
