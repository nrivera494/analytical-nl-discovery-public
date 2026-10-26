# Check: for x uniform on the simplex Delta_M restricted to sum eps x = e, the marginal of x_p is
#   P(x_p=s) = (M-1)(1-s)^(M-3) Mspl((e-eps_p s)/(1-s); eps_{-p}) / Mspl(e; eps)
# with Mspl(y; t) = (n-1) * sum_i (t_i - y)_+^(n-2) / prod_{j!=i}(t_i - t_j)  (Curry-Schoenberg, distinct knots).
import numpy as np
from scipy.integrate import quad
rng = np.random.default_rng(3)
def Mspl(y, t):
    t = np.asarray(t, float); n = len(t); s = 0.0
    for i in range(n):
        s += max(t[i]-y, 0.0)**(n-2)/np.prod([t[i]-t[j] for j in range(n) if j != i])
    return (n-1)*s
eps = np.array([0.0, 0.7, 1.1, 1.6, 2.3, 3.0]); M = len(eps); e = 1.3   # non-condensed: e > eps_1
# Monte Carlo (thin slab rejection)
out = []
while len(out) < 60000:
    x = rng.dirichlet(np.ones(M), size=400000); ee = x @ eps
    out.extend(x[np.abs(ee-e) < 0.004])
X = np.array(out[:60000])
# check the B-spline itself: density of sum eps x at e
x = rng.dirichlet(np.ones(M), size=2000000); ee = x @ eps
print("B-spline density at e: formula %.4f  MC %.4f" % (Mspl(e, eps), np.mean(np.abs(ee-e)<0.01)/0.02))
for p in range(M):
    em = np.delete(eps, p)
    f = lambda s: (M-1)*(1-s)**(M-3)*Mspl((e-eps[p]*s)/(1-s), em)/Mspl(e, eps)
    hi = min(1.0, e/eps[p]) if eps[p] > 0 else 1.0
    # support: need (e-eps_p s)/(1-s) within [min eps_-p, max eps_-p]
    Z = quad(f, 0, hi*0.999999, limit=200)[0]
    m1 = quad(lambda s: s*f(s), 0, hi*0.999999, limit=200)[0]
    m2 = quad(lambda s: s*s*f(s), 0, hi*0.999999, limit=200)[0]
    print(f"p={p} eps={eps[p]}: norm {Z:.4f}  <x> formula {m1:.4f} MC {X[:,p].mean():.4f}  g2 formula {m2/m1**2:.3f} MC {np.mean(X[:,p]**2)/X[:,p].mean()**2:.3f}")
