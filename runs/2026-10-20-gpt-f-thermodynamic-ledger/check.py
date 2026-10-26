"""gpt-f / gpt-6-astra / gpt / 2026-10-20.

Small symbolic checks authorized by T-20261020-claude-interactive-01.
This does not integrate a propagation or kinetic equation.
"""
import json
import math
import platform
import subprocess
import time
from pathlib import Path

import sympy as s

started = time.perf_counter()
root = Path(__file__).resolve().parent
cfg = json.loads((root / "config.json").read_text())
d, g, shock = s.symbols("d g shock", real=True, nonzero=True)
k, ell, v = s.symbols("k ell v", real=True)
q, qx, rq = s.symbols("q qx rq")
residual = (-ell + d*k*k)*q + s.I*(v - 2*d*k)*qx - (g-shock*k)*rq
kn_residual = s.simplify(residual.subs({k:g/shock, ell:d*g*g/shock**2, v:2*d*g/shock}))

t = s.symbols("t", real=True)
I = s.Function("I")(t)
sr, TR = s.symbols("sr TR", positive=True)
Q = I - TR*s.diff(I, t)
energy_density = -2*sr*(s.diff(I,t)*Q/2 + I*s.diff(Q,t))
# Remove an exact total derivative; fields and intensity vanish at the boundary.
total_derivative = s.diff(-s.Rational(3,2)*sr*I**2 + 2*sr*TR*I*s.diff(I,t), t)
raman_residual = s.simplify(energy_density-total_derivative + sr*TR*s.diff(I,t)**2)

om, a, b, B = s.symbols("om a b B", positive=True)
odd_integral = s.integrate(om/(a+b*om**2), (om,-B,B))
power_integral = s.integrate(1/(a+b*om**2), (om,-B,B))
energy_integral = s.integrate(om**2/(a+b*om**2), (om,-B,B))
carrier = s.symbols("carrier", positive=True)
optical_energy_integral = s.integrate((carrier+om)/(a+b*om**2), (om,0,B))
ang = s.symbols("ang", real=True)
U = s.Matrix([[s.cos(ang), -s.sin(ang)], [s.sin(ang), s.cos(ang)]])
uniform_residual = s.simplify(U*s.eye(2)*U.T-s.eye(2))
e1, e2, c = s.symbols("e1 e2 c", real=True)
dispersion = s.diag(e1,e2)
coupling = s.Matrix([[0,c],[c,0]])
commutator = dispersion*coupling-coupling*dispersion

tr = cfg["raman_fraction"]*2*cfg["raman_tau1_fs"]**2*cfg["raman_tau2_fs"]/(cfg["raman_tau1_fs"]**2+cfg["raman_tau2_fs"]**2)
rows = []
for wavelength in cfg["wavelength_nm"]:
    tau = wavelength*1e-9/(2*math.pi*299792458)*1e15
    for duration in cfg["characteristic_time_fs"]:
        rows.append({
            "wavelength_nm":wavelength, "T0_fs":duration,
            "shock_time_fs":tau, "shock_over_T0":tau/duration,
            "TR_over_T0":tr/duration,
            "eta_R_estimate_for_Lkin_over_LNL_10_and_100":[x*tr/duration for x in cfg["illustrative_Lkin_over_LNL"]]
        })
summary = {
    "run_id":root.name,
    "agent":"gpt-f", "model":"gpt-6-astra", "family":"gpt",
    "date":"2026-10-20", "task":"T-20261020-claude-interactive-01",
    "checks":{
        "mixed_NLS_to_Kaup_Newell_residual":str(kn_residual),
        "Raman_energy_balance_residual":str(raman_residual),
        "odd_first_order_band_integral":str(odd_integral),
        "uniform_covariance_unitary_residual":str(uniform_residual),
        "dispersion_coupling_commutator":str(commutator),
        "UV_norm_limit":str(s.limit(power_integral,B,s.oo)),
        "UV_linear_energy_limit":str(s.limit(energy_integral,B,s.oo)),
        "UV_photon_weighted_optical_energy_limit":str(s.limit(optical_energy_integral,B,s.oo)),
        "UV_photon_weighted_optical_energy_log_coefficient":str(s.limit(optical_energy_integral/s.log(B),B,s.oo))
    },
    "effective_first_Raman_moment_fs":tr,
    "scales":rows,
    "interpretation":"Algebra and illustrative scale screening only. No measured kinetic rate, thermalization, Raman closure or lifetime is verified."
}
assert kn_residual == 0 and raman_residual == 0 and odd_integral == 0
assert uniform_residual == s.zeros(2)
(root/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
repo = root.parents[1]
solver_commit = subprocess.check_output(["git","-C",str(repo/"solver"),"rev-parse","HEAD"],text=True).strip()
solver_dirty = bool(subprocess.check_output(["git","-C",str(repo/"solver"),"status","--porcelain"],text=True).strip())
meta = {
    "run_id":root.name, "agent":"gpt-f", "model":"gpt-6-astra", "family":"gpt",
    "date":"2026-10-20", "task":"T-20261020-claude-interactive-01",
    "problem":"P-20261020-gpt-f-01", "solver_commit":solver_commit,
    "solver_dirty":solver_dirty, "solver_used":False,
    "hardware":platform.machine(), "machine":platform.node(),
    "wall_time_seconds":time.perf_counter()-started,
    "python":platform.python_version(), "sympy":s.__version__,
    "raw_location":"none; only symbolic expressions and summary arithmetic",
    "command":"~/agent-work/venv/bin/python -W ignore runs/"+root.name+"/check.py"
}
(root/"meta.yaml").write_text(json.dumps(meta,indent=2)+"\n")
print(json.dumps(summary,indent=2))
