"""Phase mismatch of the leading intermodal four-wave-mixing processes and the walk-off parameter in nominal GIF625
(ideal parabolic GRIN) at 1550 nm, against pulse width (claude-b, T-20261008-claude-b-01, claim C-20261008-claude-b-01).

Uses beta(omega, order) of run 2026-10-04-claude-b-gif625-walkoff unchanged (analytic GRIN propagation constant of the
solver with the Malitson silica index, a = 31.25 um, NA = 0.275; order = 2p + |l|):
  dbeta(02+02 -> 01+03) = beta(0) + beta(4) - 2 beta(2)       (l = 0 sector, the one relevant to an LP01+LP02 launch)
  dbeta(11+11 -> 01+21) = beta(0) + beta(2) - 2 beta(1)       (relevant to an LP01+LP11a launch)
  delta_m = dbeta1_m T0 / |beta2|, with dbeta1 and beta2 from that run's summary at 1550 nm.
The cross-phase-only two-mode model needs |dbeta| L_D >~ 10, L_D = T0^2 / |beta2|. Writes summary.json.
"""
import importlib.util, json, os
import mpmath as mp
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "2026-10-04-claude-b-gif625-walkoff")
spec = importlib.util.spec_from_file_location("gw", os.path.join(SRC, "config.py"))
gw = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gw)
w0 = 2 * mp.pi * gw.C / (mp.mpf(1550) * mp.mpf("1e-9"))
b = {o: gw.beta(w0, o) for o in (0, 1, 2, 4)}
d0203 = float(b[0] + b[4] - 2 * b[2])
d1121 = float(b[0] + b[2] - 2 * b[1])
prev = json.load(open(os.path.join(SRC, "summary.json")))
s1550 = prev["1550"] if "1550" in prev else prev
beta2 = 0.02809   # |beta2| of LP01 at 1550 nm in ps^2/m, run 2026-10-04-claude-b-gif625-walkoff (-28.09 ps^2/km)
db1 = {"LP11": 0.0727, "LP02": 0.1508}  # ps/m, same run
# propagation-constant offsets; kappa = dbeta0 L_D sets the residual of the averaged coherent intermodal terms
# (about 0.095 / kappa in F at zeta = 2, p2 = 0.3, kmax = 5: run 2026-10-08-claude-b.5-solver-twomode-check)
dbeta0_01_02 = float(b[0] - b[2])
dbeta0_01_11 = float(b[0] - b[1])
rows = []
for T0 in (0.03, 0.05, 0.1, 0.15, 0.2, 0.227, 0.3, 0.5):
    LD = T0 ** 2 / beta2
    rows.append(dict(T0_ps=T0, L_D_m=LD, dbeta_0203_LD=d0203 * LD, dbeta_1121_LD=d1121 * LD,
                     kappa_LP02=dbeta0_01_02 * LD, kappa_LP11=dbeta0_01_11 * LD,
                     delta_LP02=db1["LP02"] * T0 / beta2, delta_LP11=db1["LP11"] * T0 / beta2))
out = dict(dbeta0_LP01_LP02_per_m=dbeta0_01_02, dbeta0_LP01_LP11_per_m=dbeta0_01_11,
           dbeta_02_02_to_01_03_per_m=d0203, dbeta_11_11_to_01_21_per_m=d1121,
           coeff_dbeta0203_LD_per_T0sq_ps=d0203 / beta2, coeff_dbeta1121_LD_per_T0sq_ps=d1121 / beta2,
           delta_LP02_per_T0_ps=db1["LP02"] / beta2, delta_LP11_per_T0_ps=db1["LP11"] / beta2,
           delta_LP02_at_dbetaLD_10=(db1["LP02"] / beta2) * (10 / abs(d0203 / beta2)) ** 0.5,
           delta_LP11_at_dbetaLD_10=(db1["LP11"] / beta2) * (10 / abs(d1121 / beta2)) ** 0.5,
           rows=rows, inputs=dict(beta2_ps2_per_m=beta2, dbeta1_ps_per_m=db1, source_run="2026-10-04-claude-b-gif625-walkoff"))
json.dump(out, open(os.path.join(HERE, "summary.json"), "w"), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "rows"}, indent=1))
