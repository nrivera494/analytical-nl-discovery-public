"""H1b part 2: the program value on the frequency window actually used in the TL card-grid simulations
(W = pi/dt of run 2026-10-16-claude-b-dw-oracle, yield_cardA/B.json), compared with the simulated TL yields."""
import numpy as np, json
from program import launch_invariants, windowed_value
rows = []
for f in ['../2026-10-16-claude-b-dw-oracle/yield_cardA.json', '../2026-10-16-claude-b-dw-oracle/yield_cardB.json']:
    try:
        data = json.load(open(f))
    except FileNotFoundError:
        continue
    for r in data:
        N, d3, Nt, TW = r['N'], r['d3'], r['Nt'], r['TW']
        W = np.pi*Nt/TW
        inv = launch_invariants('gauss', N, d3)
        (val, v, supp), _ = windowed_value(inv, d3, W, M=2001, nv=100)
        eta = r['h2']['eta_B']['2']
        rows.append(dict(N=N, d3=d3, W=W, program=val, eta_TL=eta, ratio=val/eta))
        print(N, d3, 'W', round(W, 1), 'program', round(val, 4), 'eta_TL', '%.3e' % eta, 'program/eta_TL', round(val/eta, 1), flush=True)
json.dump(rows, open('summary_simwindow.json', 'w'), indent=1, default=float)
