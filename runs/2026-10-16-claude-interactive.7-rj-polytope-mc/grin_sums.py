# GRIN (one polarization) closed forms for the condensed-regime microcanonical statistics.
# groups k=0..K-1, degeneracy k+1, eps'_k = k*kappa (kappa=1).
import numpy as np
from math import log
gE = 0.5772156649015329
for K in [3,4,5,8,10,15,20,40,100,1000]:
    k = np.arange(1, K); g = k+1
    D = g.sum(); S1 = np.sum(g/k); S2 = np.sum(g/k**2)
    rel = D*(S2 - S1**2/D)/((D+1)*S1**2)       # Var(N_ex)/<N_ex>^2
    asym = (log(K) + gE + np.pi**2/6 - 2)/K**2  # large-K estimate (with S1 ~ K, D ~ K^2/2)
    harm = D/S1                                  # sign-change energy (units of kappa)
    print(f"K={K:5d} M={D+1:7d} g2_exc={2-2/(D+1):.4f} relVar(Nex)={rel:.3e} asym={asym:.3e} harmonic-mean eps'={harm:.3f} (K/2={K/2:.1f})")
