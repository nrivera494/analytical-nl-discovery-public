# Monte Carlo predictions of the uniform-polytope (N, E') ensemble for the GRIN-like K-group spectrum.
import numpy as np, json, sys
def predict(K, Eprime, N=1.0, nsamp=40000, seed=11, tol=0.003):
    rng = np.random.default_rng(seed)
    eps = np.concatenate([[k]*(k+1) for k in range(K)]).astype(float); M = len(eps)
    out = []
    while len(out) < nsamp:
        x = rng.dirichlet(np.ones(M), size=400000)*N; e = x @ eps
        out.extend(x[np.abs(e-Eprime) < tol*N])
    X = np.array(out[:nsamp]); m = X.mean(0)
    return dict(K=K, Eprime=Eprime, mean=m.tolist(), g2=((X**2).mean(0)/m**2).tolist(), var_N0=float(X[:,0].var()))
if __name__ == '__main__':
    res = [predict(K, E) for K, E in [(4,1.5),(4,2.0)]]
    json.dump(res, open('polytope_pred.json','w'))
    for r in res: print(r['K'], r['Eprime'], 'N0', round(r['mean'][0],4), 'varN0 %.3e'%r['var_N0'], 'g2 exc mean', round(float(np.mean(r['g2'][1:])),3))
