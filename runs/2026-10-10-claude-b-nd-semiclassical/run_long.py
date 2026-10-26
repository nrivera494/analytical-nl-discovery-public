"""Long-distance reduced curve (claude-b, T-20261010-claude-interactive-05): N = 50, Nt = 4096 over 80 T0, M = 80,
record every 0.1 in Z up to Z = 10 (about 9.4 z_wb), to locate where (if anywhere) Lambda(Z) stops being N-independent.
Usage: python run_long.py -> curve_N50_long.json"""
import json, os
from lambda_curve import run, HERE
out = run(50, 4096, 80, 0.02, Zmax=10.0, rec_dZ=0.1, TW=80.0, partial_path=os.path.join(HERE, "curve_N50_long.partial.json"))
json.dump(out, open(os.path.join(HERE, "curve_N50_long.json"), "w"), indent=1)
print("done", out["wall"])
