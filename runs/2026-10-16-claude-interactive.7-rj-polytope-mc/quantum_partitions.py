"""Quantum microcanonical statistics of Q excitation quanta above a condensate in an ideal GRIN fibre (one polarization):
group k (k = 1..K-1) has k+1 modes of energy k (units of kappa); the noninteracting quantum microcanonical ensemble is uniform
over occupation configurations with sum_m k_m n_m = Q. Exact integer partition counting (generating functions).
Outputs, vs Q: <n> and g2 of a group-1 and a group-2 mode, <N_ex> and Var(N_ex); compared with the classical Dirichlet (RJ)
values at E' = Q kappa (same K): <n_m> = Q/(D k_m), g2 = 2D/(D+1)."""
import numpy as np, json
from fractions import Fraction
K = 10; QMAX = 60
groups = [k for k in range(1, K) for _ in range(k+1)]          # energies of excited modes
D = len(groups)
def poly_mul_geom(p, k, mult=1):
    # multiply series p (list of ints, length QMAX+1) by (1 - q^k)^(-mult)
    for _ in range(mult):
        for i in range(k, QMAX+1):
            p[i] += p[i-k]
    return p
# full generating function G(q) = prod_k (1-q^k)^{-(k+1)}
G = [1] + [0]*QMAX
for k in range(1, K):
    G = poly_mul_geom(G, k, k+1)
def stats_mode(k):
    # P(n_m = j) = G_{-m}(Q - j k)/G(Q), with G_{-m} = G * (1 - q^k)
    Gm = [G[i] - (G[i-k] if i >= k else 0) for i in range(QMAX+1)]
    res = []
    for Q in range(1, QMAX+1):
        m1 = sum(j*Gm[Q-j*k] for j in range(1, Q//k+1)); m2 = sum(j*(j-1)*Gm[Q-j*k] for j in range(2, Q//k+1))
        n = Fraction(m1, G[Q]); f2 = Fraction(m2, G[Q])
        res.append((Q, float(n), float(f2/n**2) if n > 0 else float('nan')))
    return res
# N_ex statistics: bivariate generating function prod_k (1 - t q^k)^{-(k+1)}; track moments in t via derivatives:
# use series in q with coefficients being polynomials in t truncated at degree QMAX (N_ex <= Q)
B = np.zeros((QMAX+1, QMAX+1), dtype=object); B[0, 0] = 1   # B[Q, n]
for k in range(1, K):
    for _ in range(k+1):
        for Q in range(k, QMAX+1):
            for n in range(1, QMAX+1):
                B[Q, n] += B[Q-k, n-1]
nex = []
for Q in range(1, QMAX+1):
    tot = sum(B[Q, :]); m1 = sum(n*B[Q, n] for n in range(QMAX+1)); m2 = sum(n*n*B[Q, n] for n in range(QMAX+1))
    mean = Fraction(m1, tot); var = Fraction(m2, tot) - mean**2
    nex.append((Q, float(mean), float(var)))
g1 = stats_mode(1); g2m = stats_mode(2)
S1 = sum(1/k for k in groups); S2 = sum(1/k**2 for k in groups)
out = []
for i, Q in enumerate(range(1, QMAX+1)):
    T = Q/D
    out.append(dict(Q=Q, n_group1=g1[i][1], g2_group1=g1[i][2], n_group2=g2m[i][1], g2_group2=g2m[i][2],
                    Nex_mean=nex[i][1], Nex_var=nex[i][2],
                    classical_n_group1=T/1, classical_n_group2=T/2, classical_g2=2*D/(D+1),
                    classical_Nex_mean=T*S1, classical_Nex_var=T**2*D*(S2 - S1**2/D)/(D+1)))
json.dump(dict(K=K, D=D, rows=out), open('quantum_partitions.json', 'w'), indent=1)
print(f"K={K} D={D} (classical g2 = {2*D/(D+1):.3f})")
print("  Q   <n1>   g2_1   <n2>   g2_2  <Nex>  Var(Nex) | classical <n1> <Nex> Var(Nex)")
for r in out:
    if r['Q'] in (1, 2, 3, 5, 8, 10, 15, 20, 30, 40, 50, 60):
        print(f"{r['Q']:3d} {r['n_group1']:6.3f} {r['g2_group1']:6.3f} {r['n_group2']:6.3f} {r['g2_group2']:6.3f} {r['Nex_mean']:6.2f} {r['Nex_var']:7.2f} |   {r['classical_n_group1']:6.3f} {r['classical_Nex_mean']:6.2f} {r['classical_Nex_var']:7.2f}")
