"""Run all polytope-ensemble checks and write summary.json (run 2026-10-16-claude-interactive.7-rj-polytope-mc)."""
import json, subprocess, sys, io, contextlib, runpy, numpy as np
out = {}
for name in ['check_dirichlet.py', 'check_bspline.py', 'grin_sums.py', 'check_degenerate.py', 'quantum_partitions.py']:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        runpy.run_path(name, run_name='__main__')
    out[name] = buf.getvalue().splitlines()
json.dump(out, open('summary.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
