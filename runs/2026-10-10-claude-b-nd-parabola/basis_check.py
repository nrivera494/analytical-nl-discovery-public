"""Basis-truncation check for the odd-sector difference in the parabola cross-check (claude-b, T-20261010-claude-interactive-05):
reduced numerics at N = 50 (Nt 2048, 40 T0) with M = 160 and M = 240 Hermite functions at zeta = 1 and 2. Writes basis_check.json."""
import json, os
from parabola import reduced_curve, legendre_sigma, HERE
out = {"legendre": [legendre_sigma(z) for z in (1.0, 2.0)]}
for M in (160, 240):
    out[f"M{M}"] = reduced_curve(50, 2048, M, 0.02, [1.0, 2.0])
    print(M, out[f"M{M}"], flush=True)
json.dump(out, open(os.path.join(HERE, "basis_check.json"), "w"), indent=1)
