"""Largest Lyapunov exponent of the GRIN resonant model (exact Hermite-Gauss Kerr tensor, S_0000 = 1, z in L_NL) against the number
of mode groups K = 4..8 (M = 10..36 modes) at a FIXED thermal condensate fraction: E' chosen per K so that the Dirichlet
<I_0> = 1 - (E'/D) S_1 equals 0.70. Weak intra-group disorder sigma = 0.3 (dis_seed 7), random fixed launch phases
(phase_seed 1 and 2), shadow-trajectory estimate renormalized every L_NL (grin_model.run), z up to 2000.
Question: does scrambling get faster with more modes at fixed f0 (z_E = ln(n/F_in)/(2 lambda_1) for real fibres)?"""
import json, time, warnings, numpy as np, sys
warnings.filterwarnings('ignore')
import grin_model as gm
F0 = 0.70
out = []
for K in [4, 5, 6, 7, 8]:
    groups = np.concatenate([[k]*(k+1) for k in range(K)]); ex = groups[groups > 0].astype(float); D = len(ex); S1 = np.sum(1/ex)
    Ep = (1 - F0)*D/S1
    for ps in ([1, 2] if K in (5, 8) else [1]):
        t0 = time.time()
        o = gm.run(K=K, J=0, seed=0, Eprime=Ep, launch='dephased', zmax=2000., zburn=500., dz=0.05, sigma=0.3, phase_seed=ps, dis_seed=7)
        r = dict(K=K, M=int(len(groups)), D=int(D), Eprime=float(Ep), phase_seed=ps, lyapunov=o['lyapunov'], wall_s=time.time() - t0,
                 I0_mean=o['mean_N0'], g2_exc_mean=o['g2_exc_mean'], g2_dirichlet=2*D/(D + 1))
        out.append(r); json.dump(out, open('lyap_modecount.json', 'w'), indent=1)
        print(f"K={K} M={len(groups)} E'={Ep:.4f} phase_seed={ps}: lambda_1 L_NL = {o['lyapunov']:.4f}; <I0>(z>500) = {r['I0_mean']:.3f} (Dirichlet {F0}); mean excited g2 {r['g2_exc_mean']:.3f} (Dirichlet {2*D/(D+1):.3f}); wall {time.time()-t0:.0f}s", flush=True)
