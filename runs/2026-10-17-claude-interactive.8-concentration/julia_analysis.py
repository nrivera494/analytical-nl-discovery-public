"""Compare the agents' Julia solver (b9fa957) with the verifier's Python solver on case A3, and apply the
verifier's own diagnostics (E, Q, rho from the continuum identity, F(Q)) to the Julia fields."""
import json, os
import numpy as np
from scipy import fft as sfft

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.expanduser("~/analytical-nl-discovery-data/2026-10-17-claude-interactive.8-concentration")
t = np.fromfile(os.path.join(RAW, "julia_A3_t_f64.bin"), dtype=np.float64) * 1e-12   # s
Nt = t.size
A = np.fromfile(os.path.join(RAW, "julia_A3_field_c128.bin"), dtype=np.complex128).reshape((Nt, -1), order="F")
nz = A.shape[1]
dt = t[1] - t[0]
tau1, tau2, fR, n2, Aeff = 12.2e-15, 32e-15, 0.18, 2.6e-20, 80e-12
a, b = 1 / tau2, 1 / tau1
k = a * a + b * b
kappa = n2 * fR * k / (2 * 299792458.0 * Aeff)
Om = -2 * np.pi * sfft.fftfreq(Nt, dt)
H = k / ((a - 1j * Om) ** 2 + b * b)
W = Om * np.imag(H)
coefE = n2 * fR / (299792458.0 * Aeff)
z = np.linspace(0, 0.25, nz)
rows = []
for j in range(nz):
    I = np.abs(A[:, j]) ** 2
    E = I.sum() * dt
    Q = (I * I).sum() * dt / E**2
    If = sfft.fft(I) * dt
    dEdz = -coefE * np.sum(W * np.abs(If) ** 2) / (Nt * dt)
    rho = -dEdz / (kappa * E * E)
    F = 2 / np.pi * np.arctan(np.pi * tau2 * Q / 2)
    rows.append((z[j], E, Q, rho, F))
rows = np.array(rows)
py = np.load(os.path.join(RAW, "A3_sampled_dt1.npz"))
pya = np.load(os.path.join(RAW, "A3.npz"))
E_py = np.interp(z, py["z"], py["E"]) / py["E"][0]
E_pya = np.interp(z, pya["z"], pya["E"]) / pya["E"][0]
Ej = rows[:, 1] / rows[0, 1]
out = {"planes": int(nz), "julia_E0_J": float(rows[0, 1]), "python_E0_J": float(py["E"][0]),
       "julia_retention": float(Ej[-1]), "python_sampled_retention": float(E_py[-1]),
       "python_analytic_retention": float(E_pya[-1]),
       "max_abs_diff_Ez_julia_vs_python_sampled": float(np.max(np.abs(Ej - E_py))),
       "max_abs_diff_Ez_julia_vs_python_analytic": float(np.max(np.abs(Ej - E_pya))),
       "julia_max_rho_over_F": float(np.max(rows[:, 3] / rows[:, 4])),
       "python_max_rho_over_F_on_same_planes": float(np.max(np.interp(z, pya["z"], pya["ratio"]))),
       "julia_violations": int(np.sum(rows[:, 3] > rows[:, 4] * (1 + 1e-6))),
       "julia_max_tau2Q": float(np.max(tau2 * rows[:, 2])),
       "julia_retention_energy_only_bound": float(1 / (1 + kappa * rows[0, 1] * 0.25)),
       "julia_retention_Qmax_bound": float(1 / (1 + kappa * rows[0, 1] * 0.25 *
                                              2 / np.pi * np.arctan(np.pi * tau2 * rows[:, 2].max() / 2)))}
json.dump(out, open(os.path.join(HERE, "summary_julia.json"), "w"), indent=1)
print(out)
