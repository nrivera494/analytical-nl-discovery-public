"""Independent algebra/quadrature check, not a propagation simulation.

agent: gpt-b; model: gpt-6-astra; family: gpt
Run from the repository root with the session Python environment.
"""
import json
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.integrate import quad

RUN = Path(__file__).resolve().parent
RAW = Path.home() / "analytical-nl-discovery-data" / RUN.name
RAW.mkdir(parents=True, exist_ok=True)
s = sp.symbols("s", nonnegative=True)
# Angular averages of products relative to phi_01^4, with s = r^2.
polynomials = {
    "S01_02": (1-s)**2,
    "S01_11": s,
    "S02_02": (1-s)**4,
    "S11a_11a": sp.Rational(3, 2)*s**2,
    "S11a_11b": s**2/2,
    "S01_03": (1-2*s+s**2/2)**2,
    "S01_03_02_02": (1-2*s+s**2/2)*(1-s)**2,
}
ratios = {k: str(2*sp.integrate(p*sp.exp(-2*s), (s, 0, sp.oo)))
          for k, p in polynomials.items()}
captures = []
for delta in (0, 0.25, 0.5, 1, 2, 3):
    a, error = quad(lambda t: np.cos(delta*t)/np.cosh(t)**2,
                    -40, 40, epsabs=1e-13, epsrel=1e-13)
    formula = 1.0 if delta == 0 else (np.pi*delta/(2*np.sinh(np.pi*delta/2)))**2
    captures.append(dict(delta=delta, quadrature=(a/2)**2, formula=formula,
                         quadrature_error_bound=error))
t = sp.symbols("t", real=True)
b = sp.sech(t)
bound_residual = sp.simplify(sp.diff(b, t, 2)/2 + b**3-b/2)
result = dict(agent="gpt-b", model="gpt-6-astra", family="gpt",
              kind="symbolic and quadrature only", overlaps_over_S0101=ratios,
              bound_eigenfunction_residual=str(bound_residual), capture=captures,
              max_capture_absolute_error=max(abs(x["formula"]-x["quadrature"]) for x in captures))
text = json.dumps(result, indent=2)+"\n"
(RAW/"calculation.json").write_text(text)
(RUN/"summary.json").write_text(text)
print(text)
