"""Extra cases for run 2026-10-04-claude-b-manakov-deviation-edge-scan (claude-b, T-20261004-claude-b-06).

mode "shifted": p2 = 0.3, delta = 0.942, mode-resolved readout in which the LP01 band is |k| <= kmax and the LP02
    band follows the trapped minority's carrier at -delta, |k + 6| <= kmax (delta = 6 grid units). F_tot is the
    variance of the sum of the two filtered counts. Also records the spectral centroid of the mean LP02 output,
    to check where the trapped light sits.
mode "p2_0.15": p2 = 0.15, delta in {0, 0.942}, fixed band |k| <= kmax on both modes (as config.py).
kmax in {3, 4, 5, 6, 7}; zeta from the command line. F_s (LP01 reference) is recomputed at each edge.
Usage: python config_extra.py <mode> <zeta>   ->  summary_<mode>_zeta<zeta>.json
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-04-claude-b-manakov-deviation-scan"))
import twomode_lib as lib
from twomode_lib import noise, propagate, t, w, TW

DZ = 2e-3
C_GRIN = [[1, 1], [1, 0.5]]
UNIT = 2 * np.pi / TW
K_D = 6


def launch(p2):
    p1 = 1 - p2
    S = C_GRIN[0][0] * p1 * p1 + 2 * C_GRIN[0][1] * p1 * p2 + C_GRIN[1][1] * p2 * p2
    sech = 1 / np.cosh(t)
    return np.sqrt(p1 / S) * sech + 0j, np.sqrt(p2 / S) * sech + 0j


def main(mode, z):
    sech = 1 / np.cosh(t)
    k = np.round(w / UNIT)
    out = {"mode": mode, "zeta": z, "dz": DZ, "grid": {"N": len(t), "T_window": TW}, "cases": []}
    for kmax in (3, 4, 5, 6, 7):
        edge = (kmax + 0.5) * UNIT
        maskA = (np.abs(k) <= kmax).astype(float)
        Fs = noise(sech + 0j, 0 * sech + 0j, z, DZ, C_GRIN, 0.0, maskA, maskA)["Fa"]
        if mode == "shifted":
            a0, b0 = launch(0.3)
            maskB = (np.abs(k + K_D) <= kmax).astype(float)
            d = K_D * UNIT
            r = noise(a0, b0, z, DZ, C_GRIN, d, maskA, maskB)
            am, bm = propagate(a0[None], b0[None], z, DZ, C_GRIN, d)
            Sb = np.abs(np.fft.fft(bm[0])) ** 2
            centroid = float(np.sum(w * Sb) / np.sum(Sb))
            peak = float(w[np.argmax(Sb)])
            dB = 10 * np.log10(r["Ftot"]) - 10 * np.log10(Fs)
            out["cases"].append({"kmax": kmax, "edge": edge, "p2": 0.3, "delta": d, "band_b_center": -d, "Fs_LP01": Fs,
                                 "computed": r, "Ftot_dB_minus_Fs_dB": dB, "lp02_spectral_centroid": centroid, "lp02_spectral_peak": peak})
            print(f"shifted zeta={z} edge={edge:.3f}: Fs={Fs:.5f} Ftot={r['Ftot']:.5f} dB={dB:+.4f} rho={r['rho']:+.4f} "
                  f"LP02 centroid={centroid:+.3f} peak={peak:+.3f}", flush=True)
        else:
            a0, b0 = launch(0.15)
            for kd in (0, K_D):
                d = kd * UNIT
                r = noise(a0, b0, z, DZ, C_GRIN, d, maskA, maskA)
                dB = 10 * np.log10(r["Ftot"]) - 10 * np.log10(Fs)
                out["cases"].append({"kmax": kmax, "edge": edge, "p2": 0.15, "delta": d, "Fs_LP01": Fs, "computed": r, "Ftot_dB_minus_Fs_dB": dB})
                print(f"p2=0.15 zeta={z} edge={edge:.3f} delta={d:.3f}: Fs={Fs:.5f} Ftot={r['Ftot']:.5f} dB={dB:+.4f}", flush=True)
    with open(os.path.join(HERE, f"summary_{mode}_zeta{z:g}.json"), "w") as fh:
        json.dump(out, fh, indent=1, default=float)


if __name__ == "__main__":
    main(sys.argv[1], float(sys.argv[2]))
