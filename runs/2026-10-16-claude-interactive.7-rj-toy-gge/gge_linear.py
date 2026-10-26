"""Linear-response (fluctuation-response) GGE: Delta<I_0> = Cov_RJ(I_0, H_res)/Var_RJ(H_res) * (h_in - <H_res>_RJ),
moments over the exact condensed-regime RJ ensemble (Dirichlet intensities x uniform phases). Compared with the GGE shell
Monte Carlo and the disorder-free toy runs. Also a closed-form leading-order estimate of the slope:
  Cov(I_0, H) ~ -Cov(N_ex, W),  W = sum_m c_m I_m,  c_m = <I_0>(2 S_00mm - S_0000),
  Var(H) = Var(Hbar(I)) + E[Var_phase(H | I)]."""
import numpy as np, json, warnings
warnings.filterwarnings('ignore')
import resonant_model as rm
rng = np.random.default_rng(21)
cases = [(4, 0.9, 'dephased', 0.4216, 0.4228), (5, 0.9, 'dephased', 0.4539, 0.4578), (4, 0.9, 'focused', 0.5593, 0.5488),
         (4, 0.6, 'focused', 0.6783, 0.6713), (5, 0.9, 'focused', 0.5829, 0.5831), (4, 0.6, 'dephased', 0.6197, 0.6165),
         (4, 0.3, 'dephased', 0.8012, 0.8117)]
out = []
for K, Ep, launch, toy, shell in cases:
    groups, eps, u, S, R = rm.build(K, 400, 0)
    M = len(groups); D = M-1; R2 = R.reshape(M, -1)
    def H(A):
        v = np.einsum('qb,rb,sb->qrsb', A.conj(), A, A).reshape(M**3, -1)
        return 0.5*np.real(np.einsum('pb,pb->b', A.conj(), R2 @ v))
    I0 = np.zeros(M); a = Ep/3.; i1 = groups==1; i2 = groups==2
    I0[i1] = a/i1.sum(); I0[i2] = a/i2.sum(); I0[0] = 1-I0.sum()
    if launch == 'dephased':
        ph = np.random.default_rng(1).uniform(0, 2*np.pi, M)
    else:
        jstar = np.argmax(np.abs(u.T @ np.sqrt(I0))); ph = np.where(u[:, jstar] >= 0, 0.0, np.pi)
    h_in = H((np.sqrt(I0)*np.exp(1j*ph))[:, None])[0]
    B = 60000
    x = rng.dirichlet(np.ones(D), size=B).T
    I = np.zeros((M, B)); I[1:] = Ep*x/eps[1:, None]; I[0] = 1 - I[1:].sum(0)
    A = np.sqrt(I)*np.exp(1j*rng.uniform(0, 2*np.pi, (M, B)))
    hs = H(A)
    slope = np.cov(I[0], hs)[0, 1]/hs.var()
    N0_RJ = I[0].mean()
    lin = N0_RJ + slope*(h_in - hs.mean())
    # closed-form leading-order slope: c_m = <I_0>(2 S_00mm - S_0000); Cov(N_ex, W) and Var(W) from Dirichlet covariances;
    # Var(H) approximated by the sampled total variance (phase part not in closed form here)
    S00 = np.einsum('ppqq->pq', S)[0]
    c = N0_RJ*(2*S00[1:] - S00[0])
    w = 1/eps[1:]
    def dcov(av, bv):   # Cov(sum a_m I_m, sum b_m I_m) for the Dirichlet ensemble
        return Ep**2/(D**2*(D+1))*(D*np.sum(av*bv*w**2) - np.sum(av*w)*np.sum(bv*w))
    cov_closed = -dcov(np.ones(D), c)
    slope_closed = cov_closed/hs.var()
    lin_closed = N0_RJ + slope_closed*(h_in - hs.mean())
    r = dict(K=K, Eprime=Ep, launch=launch, h_in=float(h_in), H_RJ_mean=float(hs.mean()), H_RJ_std=float(hs.std()),
             z=float((h_in-hs.mean())/hs.std()), N0_RJ=float(N0_RJ), slope=float(slope), N0_linear=float(lin),
             slope_closed_cov=float(slope_closed), N0_linear_closedcov=float(lin_closed), N0_shell=shell, N0_toy=toy)
    out.append(r)
    print(f"K={K} E'={Ep} {launch:8s} z={r['z']:+.2f}  N0: RJ {N0_RJ:.4f}  linear {lin:.4f}  linear(closed Cov) {lin_closed:.4f}  shell {shell:.4f}  toy {toy:.4f}")
json.dump(out, open('gge_linear.json', 'w'), indent=1)
