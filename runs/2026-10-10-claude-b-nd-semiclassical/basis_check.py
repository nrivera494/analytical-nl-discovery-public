"""Basis-truncation check of the Gaussian reduced curve (claude-b, T-20261010-claude-interactive-05): N = 50, Nt = 2048,
M = 160, records every 0.5 in Z to 3.3 (plus the oracle Z values), to compare with curve_N50.json (M = 80). Writes
curve_N50_M160.json."""
import json, os
from lambda_curve import run, HERE
out = run(50, 2048, 160, 0.02, Zmax=3.3, rec_dZ=0.5)
json.dump(out, open(os.path.join(HERE, "curve_N50_M160.json"), "w"), indent=1)
print("done", out["wall"])
