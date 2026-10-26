#!/usr/bin/env python3
"""Constructive binary filters from the stationary-phase picture (Kerr, dispersionless, Gaussian).
Leading-order squeezing needs real weights g(w) that are piecewise linear through w = 0 (g - w g' = 0). A binary filter
can realize a weight density d(w) in [0,1] by error-diffusion dithering over the fine spectral bins; the dither error is
high-'quefrency', i.e. it maps to large delays where the field is dark, so it adds vacuum noise d(1-d) per photon.
Prediction:  F_bin ~= 1 - (1 - F_d) <d^2>/<d>,  F_d = smooth-weight Fano factor of d,  <.> = average over nbar.
Shapes: 'V' d = min(1, |w|/wc); 'one' d = min(1, w/wc) for w > 0, 0 otherwise.
Usage: python dither_ramp.py out.json [Phis]"""
import json, sys, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
from dlfano import build_model, covariance, spectral, lam_gen, fano_of, gaussian_p, binary_search4

def dither(d, order):
    T = np.zeros_like(d); e = 0.0
    for i in order:
        e += d[i]
        if e >= 0.5:
            T[i] = 1.0; e -= 1.0
    return T

out = sys.argv[1] if len(sys.argv) > 1 else "dither_ramp.json"
Phis = [float(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else [5.0, 10.0, 20.0, 30.0]
rows = []
for Phi in Phis:
    t0 = time.time()
    dt = min(0.04, 0.8 / Phi); t = np.arange(-7, 7, dt); p = gaussian_p(t)
    m = build_model(p, dt, Phi); V = covariance(m)
    nb, Va, idx, w = spectral(m, V, pad=8, thr=1e-6)
    lg = lam_gen(Va)
    wmax = np.sqrt(2) * Phi * np.exp(-0.5)            # max instantaneous frequency of the SPM chirp (Gaussian)
    order = np.argsort(w)
    s = np.sqrt(nb)
    best = None
    for shape in ("V", "one"):
        for frac in (0.4, 0.55, 0.7, 0.8, 0.9, 1.0, 1.1, 1.25, 1.5, 2.0, 3.0):
            wc = frac * wmax
            d = np.minimum(1.0, np.abs(w) / wc) if shape == "V" else np.where(w > 0, np.minimum(1.0, w / wc), 0.0)
            y = d * s
            Fd = float(y @ Va @ y / (y @ y))
            ratio = float((d * d * nb).sum() / (d * nb).sum())
            pred = 1 - (1 - Fd) * ratio
            T = dither(d, order)
            Fb = fano_of(T, nb, Va)
            r = {"Phi": Phi, "shape": shape, "wc_over_wmax": frac, "F_smooth_d": Fd, "d2_over_d": ratio,
                 "F_pred": pred, "F_binary_dithered": Fb, "n_selected": int(T.sum()), "n_bins": int(len(nb)),
                 "lam_gen": lg}
            rows.append(r)
            print(json.dumps({k: (round(v, 5) if isinstance(v, float) else v) for k, v in r.items()}), flush=True)
            if best is None or Fb < best[0]:
                best = (Fb, T.copy(), shape, frac)
    # polish the best dithered filter with the same tabu machinery used elsewhere (seeded start)
    rb = binary_search4(nb, Va, w, extra_starts=(best[1],))
    r = {"Phi": Phi, "shape": "best_dither_then_tabu", "seed_shape": best[2], "seed_frac": best[3],
         "F_seed": best[0], "F_after_search": rb["F"], "lam_gen": lg, "wall_s": round(time.time() - t0, 1)}
    rows.append(r); print(json.dumps(r), flush=True)
    json.dump({"rows": rows}, open(out, "w"), indent=1)
