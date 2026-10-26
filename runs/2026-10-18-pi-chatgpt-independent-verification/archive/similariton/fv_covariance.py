#!/usr/bin/env python3
"""Independent similariton calculation: conservative real-space finite volumes.

No repository code is imported.  Discretize d_x[(1-x^2)d_x] on midpoint
cells with zero endpoint flux. Its low eigenvectors are found numerically;
Legendre polynomials set their signs only, not the generator or readout.
Propagate the covariance by a differential Lyapunov equation, including
distributed amplifier diffusion.  This is a discretization of the
hydrodynamic core, NOT a full NLSE or a sharp-edge quantum state.

Both quadratures can be included at a finite grid cutoff. eps=0 keeps the
leading intensity source of the claim; eps>0 includes phase vacuum and ASE.
Normalization: all state covariances multiplied by input photon number N0.
State u=e^(tau/3)n, w=eps*e^(-tau/3)p; tau=g*z.

Run: python fv_covariance.py --output results_fv.json
Requires numpy, scipy; makes no network calls.
"""
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import eigh_tridiagonal
from scipy.special import eval_legendre


def finite_volume(cells=128, modes=8):
    h = 2.0 / cells
    x = -1 + (np.arange(cells) + 0.5) * h
    faces = -1 + np.arange(cells + 1) * h
    f = 1 - x*x
    ff = np.maximum(0., 1 - faces*faces)
    # -D is positive and symmetric, natural no-flux endpoints.
    diag = (ff[:-1] + ff[1:]) / h**2
    off = -ff[1:-1] / h**2
    eig, U = eigh_tridiagonal(diag, off, select='i',
                              select_range=(0, modes-1))
    # Conservative flux differences annihilate constants exactly.
    # Remove only roundoff in that known null eigenvalue.
    eig[0] = 0.
    for l in range(modes):
        if np.dot(U[:, l], eval_legendre(l, x)) < 0:
            U[:, l] *= -1
    F0 = h * f.sum()
    # Coefficients refer to orthonormal grid functions U/sqrt(h).
    Cn = F0 * (U.T @ (f[:, None] * U))
    Cp = (F0/4) * (U.T @ (U/f[:, None]))
    # Read out in the solver's own orthonormal eigenbasis. Midpoint
    # quadrature against continuous P_l leaks O(h^2) of the energy mode
    # into l=2; this is nonuniform in gain and eventually masks decay.
    # The numerical eigenfunctions converge to normalized Legendre modes.
    proj = np.eye(5, modes)
    energy = np.sqrt(h) * U.sum(axis=0) / F0
    phase_mean = np.sqrt(h) * (f @ U) / F0
    return eig, Cn, Cp, proj, energy, phase_mean


def simulate(cells=128, modes=8, eps=0., gamma=np.sqrt(18.),
             launch='asymptotic', nsp=1., end=26., samples=None):
    eig, Cn, Cp, proj, energy, pm = finite_volume(cells, modes)
    A = (18/gamma**2)**(1/3)
    if launch == 'asymptotic':
        s0, v0 = 1., 0.
    elif launch == 'unchirped':
        s0, v0 = 1/A, -1/(3*A)
    else:
        raise ValueError(launch)
    M = modes
    C0 = np.zeros((2*M, 2*M))
    C0[:M, :M] = Cn
    C0[M:, M:] = eps**2 * Cp
    y0 = np.r_[s0, v0, 0., C0.ravel()]
    def rhs(t, y):
        s, v, theta = y[:3]
        B = np.zeros((2*M, 2*M))
        B[:M, :M] = np.eye(M)/3
        B[M:, M:] = -np.eye(M)/3
        B[:M, M:] = -np.diag(eig)/(gamma*A*A*s*s)
        B[M:, :M] = np.eye(M)/(gamma*A*s)
        C = y[3:].reshape(2*M, 2*M)
        dC = B@C + C@B.T
        dC[:M, :M] += (2*nsp-1)*np.exp(-t/3)*Cn
        dC[M:, M:] += (2*nsp-1)*eps**2*np.exp(-5*t/3)*Cp
        return np.r_[v, -2*v/3-s/9+1/(9*s*s),
                     np.exp(2*t/3)/(gamma*A*s), dC.ravel()]
    if samples is None:
        samples = np.linspace(0, end, int(end*20)+1)
    sol = solve_ivp(rhs, (0, end), y0, t_eval=samples,
                    method='DOP853', rtol=2e-12, atol=2e-13)
    if not sol.success:
        raise RuntimeError(sol.message)
    rows = []
    for t, y in zip(sol.t, sol.y.T):
        s, v, theta = y[:3]
        C = y[3:].reshape(2*M, 2*M)
        C = (C+C.T)/2
        a = A*np.exp(t/3)*s
        ap = gamma*A*np.exp(t/3)*(v+s/3)
        en = np.r_[np.exp(-t/3)*energy, np.zeros(M)]
        ph = np.r_[np.zeros(M), np.exp(t/3)*pm]
        ve, vp, cp = en@C@en, ph@C@ph, en@C@ph
        n2 = np.r_[np.exp(-t/3)*proj[2], np.zeros(M)]
        p2 = np.r_[np.zeros(M), np.exp(t/3)*proj[2]]
        vn, vq = n2@C@n2, p2@C@p2
        if abs(ap) > 1e-12:
            H = np.c_[np.exp(-t/3)*proj,
                      -np.exp(t/3)/(a*ap)*(proj*eig[None, :])]
            spec = H@C@H.T
            ev = np.linalg.eigvalsh((spec+spec.T)/2)[::-1]
            ratio = ev[1]/ev[0]
        else:
            ev, ratio = np.full(5, np.nan), np.nan
        deficit = 1-cp*cp/(ve*vp) if vp>0 else np.nan
        rows.append(dict(tau=float(t), width=float(a), theta=float(theta),
                         energy_relative_variance_N0=float(ve),
                         density_shape_variance_N0=float(vn),
                         phase_shape_variance_eps2_N0=float(vq),
                         density_photon_variance=float(np.exp(t)*vn),
                         phase_photon_variance_eps2=float(np.exp(t)*vq),
                         matched_phase_Cpp_eps2=float(4*np.exp(t)*vp),
                         phase_energy_deficit=float(deficit),
                         spectral_ratio=float(ratio),
                         spectral_eigenvalues_N0=ev.tolist()))
    return dict(method='midpoint finite-volume + differential Lyapunov',
                cells=cells, modes=modes, eps=eps, Gamma=float(gamma),
                launch=launch, nsp=nsp, grid_eigenvalues=eig.tolist(),
                energy_check_max_abs=float(max(abs(r['energy_relative_variance_N0']-
                   (1+(2*nsp-1)*(1-np.exp(-r['tau'])))) for r in rows)),
                rows=rows)


def run(output):
    base_times=np.array([0.,2.,4.,6.,9.,12.,15.,18.,21.,24.,26.])
    records=[]
    for cells in [32,64,128,256,512,1024]:
        r=simulate(cells=cells, samples=base_times)
        records.append(r)
        print('FV',cells,'energy error',r['energy_check_max_abs'],flush=True)
    # Finite physical phase cutoff. Its logarithmic divergence under grid
    # refinement is intentional, exposing the sharp-edge domain problem.
    for cells in [64,128,256]:
        records.append(simulate(cells=cells,eps=.05,samples=base_times))
    for gamma in [np.sqrt(18.),1.]:
        records.append(simulate(cells=1024,gamma=gamma,launch='unchirped',
                                end=6.,samples=np.array([0.,2.,4.,6.])))
    dense=simulate(cells=512,end=26.)
    # Fit over several oscillations; additional period-matched slopes are
    # insensitive to the l=2 covariance's nonconstant oscillatory envelope.
    rr=dense['rows']; t=np.array([r['tau'] for r in rr])
    mask=(t>=12)&(t<=26)
    slopes={k:float(np.polyfit(t[mask],np.log(np.array([r[k] for r in rr])[mask]),1)[0])
            for k in ['density_photon_variance','phase_photon_variance_eps2',
                      'matched_phase_Cpp_eps2','spectral_ratio','phase_energy_deficit']}
    period=3*np.pi/np.sqrt(2)
    pair=simulate(cells=512,end=18+2*period,samples=np.array([18.,18+2*period]))
    a,b=pair['rows']
    periodic_slopes={k:float(np.log(b[k]/a[k])/(b['tau']-a['tau']))
                     for k in ['density_photon_variance','phase_photon_variance_eps2',
                               'phase_energy_deficit']}
    result=dict(records=records,dense=dense,regression_slopes_12_26=slopes,
                period_matched_l2_slopes=periodic_slopes,
                period_matched_l2=dict(variance_period=float(period),
                                      rows=pair['rows']),
                scope='Hydrodynamic core only; no full NLSE edge-error certification.')
    Path(output).write_text(json.dumps(result,indent=2,allow_nan=True)+'\n')
    print('SLOPES',slopes,flush=True)
    print('PERIOD-MATCHED',periodic_slopes,flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default='results_fv.json')
    run(p.parse_args().output)
