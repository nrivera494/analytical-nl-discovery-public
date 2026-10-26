"""Size of the Weyl-ordering term T_qs = sum_p R_pqps that the large-n truncated-Wigner runs omit (dA_q/dz gains -i g sum_s T_qs A_s).
Only its mode-dependent part matters (a common diagonal shift is a global phase). Output: ordering_term.txt."""
import numpy as np, resonant_model as rm, grin_model as gm
lines = []
for name, (gr, ep, u, S, R) in [('toy K=4 (M=10), resonant_model.build(4, 400, 0)', rm.build(4, 400, 0)), ('GRIN K=5 (M=15), grin_model.build(5, 0, 0)', gm.build(5, 0, 0))]:
    T = np.einsum('pqps->qs', R); d = np.diag(T); off = T - np.diag(d)
    lines.append(f"{name}: T_qq in [{d.min():.3f}, {d.max():.3f}], spread {d.max()-d.min():.3f}; max |T_qs| (q != s) {np.abs(off).max():.3f}")
lines.append("Phase from the mode-dependent part: spread * z / n (z in L_NL, n photons per cell): toy n = 1e5, z = 4000 -> %.3f rad; GRIN n = 1e6, z = 1500 -> %.4f rad"
             % (0.826*4000/1e5, 2.0*1500/1e6))
open('ordering_term.txt', 'w').write('\n'.join(lines) + '\n'); print('\n'.join(lines))
