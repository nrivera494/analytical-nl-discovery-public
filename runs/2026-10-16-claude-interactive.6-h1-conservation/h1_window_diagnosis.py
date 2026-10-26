"""H1(g) diagnosis: does the solver's fixed blue-edge damping window explain its photon drift?
numpy run of the h1 case with the Julia window (damped_freq_window, copied below) applied to the Kerr prefactor."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "2026-10-16-claude-interactive.6-lwir-common"))
import numpy as np
from lwir import *


def damped_freq_window(nt):
    """Port of FastDifferentiableMMNLO src/backend/fft_utils.jl damped_freq_window (FFT order)."""
    f = np.fft.ifftshift(np.arange(1, nt + 1)).astype(float)
    fc_idx = nt // 2 + 1
    fc = float(fc_idx)
    ffwhm = nt * 0.85
    f0 = ffwhm / (2 * np.sqrt(np.log(2)))
    window = np.exp(-((f - fc) ** 40) / (2 * f0 ** 40)) ** 20
    window[fc_idx - 1:] = 1.0      # Julia window[fc_idx:end] .= 1 (1-based)
    return window


fib = StepIndexFiber("SiO2", 4.1, 0.14, n=600, n2=2.6e-20)
wp = wl_to_w(1.55); wg = wl_to_w(1.75)
g = Grid(2 ** 13, 0.003, wg)
aeff0 = float(fib.aeff_um2(np.array([wp]))[0])
b2 = abs(fib.beta2(np.array([wp]))[0]); gam = fib.n2 * wp / C_M_PS / (aeff0 * 1e-12)
P0 = 9 * b2 / (gam * 0.0567 ** 2)
A0 = sech_pulse(g, P0, 0.0567, W_off=wp - wg)
win = damped_freq_window(g.nt)
res = {"window_min": float(win.min()), "window_lt_0.99_from_lambda_um": float(w_to_wl(g.w[win < 0.99].min()))}
for name, wnd, dz in [("window_dz0.25", win, 2.5e-4), ("window_dz0.125", win, 1.25e-4)]:
    sim = GNLSE(g, fib.beta, fib.n2, lambda w: np.full_like(np.asarray(w, float), aeff0), aeff0,
                raman=OscillatorRaman(0.18, 0.0122, 0.032), w_ref=wg, window=wnd)
    out = sim.run(A0, 1.0, dz, n_save=4, callback=lambda z, Aw: sim.photons(Aw))
    N = np.array(out["diag"])
    res[name] = {"rel_photon_drift": float((N[-1] - N[0]) / N[0]),
                 "photon_fraction_in_damped_band_final": float(sim.photons(out["Aw"], win < 0.99) / N[-1])}
    print(name, res[name], flush=True)
json.dump(res, open(os.path.join(HERE, "summary_window_diagnosis.json"), "w"), indent=1)
