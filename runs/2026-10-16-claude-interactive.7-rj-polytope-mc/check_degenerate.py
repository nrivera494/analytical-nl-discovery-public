"""Degenerate fundamental (two polarizations, d0 = 2 modes at eps = 0), only N and E' conserved:
prediction: excitations x_m = eps_m I_m / E' ~ Dirichlet(1^D) tilted by (N - N_ex)^(d0-1). Monte Carlo of the full polytope
vs (a) untilted Dirichlet and (b) tilted Dirichlet (importance-weighted)."""
import numpy as np
rng = np.random.default_rng(4)
eps = np.array([0., 0., 1., 1., 2., 2.])   # 2 polarizations x 3 spatial modes (eps 0, 1, 2)
N, E = 1.0, 0.8
M = len(eps); D = int(np.sum(eps > 0)); exc = eps > 0
out = []
while len(out) < 30000:
    x = rng.dirichlet(np.ones(M), size=400000)*N; e = x @ eps
    out.extend(x[np.abs(e-E) < 0.003*E])
X = np.array(out[:30000]); Iex = X[:, exc]
g2_mc = np.mean((Iex**2).mean(0)/Iex.mean(0)**2)
Nex_mc = Iex.sum(1).mean()
# Dirichlet (untilted) and tilted predictions by sampling
xs = rng.dirichlet(np.ones(D), size=400000); I = E*xs/eps[exc]; Nex = I.sum(1)
g2_d = np.mean((I**2).mean(0)/I.mean(0)**2)
w = (N - Nex); w = w/w.mean()
mt = (I*w[:, None]).mean(0); g2_t = np.mean(((I**2)*w[:, None]).mean(0)/mt**2)
print(f"D={D}: g2 excited  MC {g2_mc:.4f}   Dirichlet {g2_d:.4f} (2D/(D+1)={2*D/(D+1):.4f})   tilted {g2_t:.4f}")
print(f"<N_ex>  MC {Nex_mc:.4f}   Dirichlet {Nex.mean():.4f}   tilted {(Nex*w).mean():.4f}")
