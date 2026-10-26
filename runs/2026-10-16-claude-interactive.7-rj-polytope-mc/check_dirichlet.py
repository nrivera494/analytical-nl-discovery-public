# Check closed forms for the uniform ("polytope") measure on {I>=0, sum I = N, sum eps' I = E'}
# in the condensed regime E' <= kappa N (fundamental eps'=0, excited eps'_m >= kappa).
import numpy as np, sympy as sp
rng = np.random.default_rng(1)

# --- symbolic Dirichlet(1,...,1) moments with D components
D = sp.symbols('D', positive=True, integer=True)
# E[x^k] for Beta(1, D-1): k! (D-1)!/(D+k-1)!
Ex = 1/D; Ex2 = 2/(D*(D+1)); Exy = 1/(D*(D+1))
print("g2 =", sp.simplify(Ex2/Ex**2), " cross g2 =", sp.simplify(Exy/Ex**2))

# --- Monte Carlo of the exact polytope measure (hit-and-run would be generic; here exact Dirichlet sampler
# is what we want to TEST against an independent rejection sampler on the full polytope)
def rejection_polytope(eps, N, E, nsamp):
    # sample I uniform on simplex {I>=0, sum I=N} and accept if |sum eps I - E| < tol (thin slab)
    M = len(eps); out = []; tol = 0.004*E
    while len(out) < nsamp:
        x = rng.dirichlet(np.ones(M), size=200000)*N
        e = x @ eps
        out.extend(x[np.abs(e-E) < tol])
    return np.array(out[:nsamp])

eps = np.array([0., 1., 1., 2., 2., 2.])   # GRIN-like: groups k=0,1,2 with degeneracy 1,2,3 (kappa=1)
N = 1.0; E = 0.6                             # E' <= kappa N -> condensed-regime exactness condition holds
I = rejection_polytope(eps, N, E, 40000)
Dn = len(eps)-1
print("M =", len(eps), " predicted g2 excited = ", 2-2/len(eps))
for m in range(1, len(eps)):
    g2 = np.mean(I[:,m]**2)/np.mean(I[:,m])**2
    print(f" mode {m} eps'={eps[m]}: <I>={np.mean(I[:,m]):.4f} (RJ T/eps' = {E/Dn/eps[m]:.4f}), g2={g2:.3f}")
g2x = np.mean(I[:,1]*I[:,3])/(np.mean(I[:,1])*np.mean(I[:,3]))
print(" cross g2(1,3) =", round(g2x,3), " predicted", 1-1/len(eps))
S1 = np.sum(1/eps[1:]); S2 = np.sum(1/eps[1:]**2)
varN0_pred = (E/Dn)**2*(Dn*S2 - S1**2)/(Dn+1)
print(" Var(N0): MC", np.var(I[:,0]), " predicted", varN0_pred)
# covariance of condensate with each excited mode: predicted -(E'^2/eps_m)/(D^2(D+1)) [D/eps_m - S1]
for m in (1,3):
    pred = -(E**2/eps[m])/(Dn**2*(Dn+1))*(Dn/eps[m]-S1)
    print(f" Cov(N0, I_{m}): MC {np.cov(I[:,0],I[:,m])[0,1]:.5f}  predicted {pred:.5f}")
