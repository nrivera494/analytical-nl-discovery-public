#!/usr/bin/env python3
"""Independent full gain-NLSE with tangent/adjoint noise analysis.

The exact lens change of variables removes expansion and quadratic chirp:
 psi=sqrt(exp(tau)/a)*U(x/a)*exp[i Phi-i(a'/a)x^2/(2 eps)], tau=g*z.
 U_tau=-i eps/(2 Gamma a^2) U_xixi
       +i exp(tau)/(Gamma eps a) (|U|^2+xi^2-1)U.
a(tau) is the *coordinate choice* obeying the hydrodynamic width equation;
the U equation retains all second derivatives (quantum pressure).

The solver uses symmetric split flows with exact cubic tangent maps.
The same discrete flow is reversed to compute its exact real adjoint.
Vacuum/ASE covariances use adjoint complex L2 Gram matrices, automatically
including both field quadratures; this is not a reduced density-source model.
ASE diffusion is integrated with a second-order weighted trapezoidal rule.
The flat-gain energy variance provides an exact normalization benchmark.

Run: OPENBLAS_NUM_THREADS=1 python lens_nlse.py --output results_nlse.json
"""
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import eval_legendre


def setup(eps, end, ngrid, dt, launch, gamma, box, smooth):
    steps=int(np.ceil(end/dt));dt=end/steps
    t=np.arange(steps+1)*dt
    x=np.linspace(-box,box,ngrid,endpoint=False);dx=2*box/ngrid
    k=2*np.pi*np.fft.fftfreq(ngrid,d=dx)
    A=(18/gamma**2)**(1/3)
    s0=1. if launch=='asymptotic' else 1/A
    v0=0. if launch=='asymptotic' else -1/(3*A)
    def width_rhs(t,y):
        s,v=y
        return [v,-2*v/3-s/9+1/(9*s*s)]
    sol=solve_ivp(width_rhs,(0,end),[s0,v0],dense_output=True,
                  rtol=1e-12,atol=1e-13,method='DOP853')
    mids=t[:-1]+dt/2
    sm,vm=sol.sol(mids)
    am=A*np.exp(mids/3)*sm
    # Midpoint evaluation gives a symmetric, second-order nonautonomous step.
    kinetic=eps*dt/(4*gamma*am**2)
    cubic=np.exp(mids)*dt/(gamma*eps*am)
    sl,vl=sol.sol(end)
    al=A*np.exp(end/3)*sl
    apl=gamma*A*np.exp(end/3)*(vl+sl/3)
    f=1-x*x
    if smooth>0:
        delta=smooth*eps**(2/3)
        rho=delta*np.logaddexp(0.,f/delta)
    else:
        rho=np.maximum(f,0.)
    # Fixed input photon number/energy for all smoothings and grids.
    rho*=(4/3)/(dx*rho.sum())
    U=np.sqrt(rho).astype(complex)
    return x,dx,k,t,kinetic,cubic,U,al,apl


def kinetic_map(U,coeff,k2):
    phase=np.exp(1j*coeff*k2)
    if U.ndim==2:phase=phase[:,None]
    return np.fft.ifft(np.fft.fft(U,axis=0)*phase,axis=0)


def simulate(eps=.05,end=4.,ngrid=2048,dt=.002,launch='asymptotic',
             gamma=np.sqrt(18.),box=2.,smooth=.25,do_cov=True):
    x,dx,k,t,ks,cs,U,al,apl=setup(eps,end,ngrid,dt,launch,gamma,box,smooth)
    U0=U.copy();E0=dx*np.vdot(U,U).real;k2=k*k
    # Finite-energy phase perturbations, eps*p_l(0)=1, no singular density kick.
    modes=[2,3,4]
    P=np.array([eval_legendre(l,x) for l in modes]).T
    dU=1j*U[:,None]*P/eps
    dU0=dU.copy()
    samples=[]
    stride=max(1,len(ks)//120)
    def record(i):
        drho=2*np.real(U.conj()[:,None]*dU)
        nn=np.array([(2*l+1)/2*dx*np.dot(eval_legendre(l,x),drho[:,j])
                     for j,l in enumerate(modes)])
        samples.append({'tau':float(t[i]),'n_from_unit_eps_phase':nn.tolist()})
    record(0)
    for i,(kin,cub) in enumerate(zip(ks,cs)):
        U=kinetic_map(U,kin,k2);dU=kinetic_map(dU,kin,k2)
        phase=np.exp(1j*cub*(abs(U)**2+x*x-1))
        drho=2*np.real(U.conj()[:,None]*dU)
        dU=phase[:,None]*(dU+1j*cub*U[:,None]*drho)
        U=phase*U
        U=kinetic_map(U,kin,k2);dU=kinetic_map(dU,kin,k2)
        if (i+1)%stride==0 or i+1==len(ks):record(i+1)
    energy_error=dx*np.vdot(U,U).real/E0-1
    out=dict(eps=eps,tau=end,ngrid=ngrid,steps=len(ks),dt=float(t[1]-t[0]),
             Gamma=float(gamma),launch=launch,box=box,smooth=smooth,
             energy_error=float(energy_error),width=float(al),samples=samples,
             edge_mass_fraction=float(dx*np.sum(abs(U[abs(x)>.9*box])**2)/E0))
    if not do_cov:return out
    # Output observables. A and P are matched mean-field quadratures.
    adj=[U/np.sqrt(E0),1j*U/np.sqrt(E0)]
    chirp=al*apl/eps
    carrier=np.exp(-.5j*chirp*x*x)
    V=carrier*U
    spec=np.fft.fft(V)
    for l in range(5):
        filt=np.where(abs(k)<chirp,eval_legendre(l,k/chirp),0.)
        # Orthonormal Legendre coefficient of deltaS, not raw coefficients.
        adj.append(np.sqrt((2*l+1)/2)*carrier.conj()*
                   np.fft.ifft(filt*spec))
    h=np.array(adj).T
    tangent_output_pairing=dx*np.real(h.conj().T@dU)
    def gram(h):return dx*np.real(h.conj().T@h)
    gend=gram(h);ase=np.zeros_like(gend)
    comm_end=float(dx*np.imag(np.vdot(h[:,0],h[:,1])))
    comm_ase=0.
    UL=U.copy()
    for i in range(len(ks)-1,-1,-1):
        kin,cub=ks[i],cs[i]
        U=kinetic_map(U,-kin,k2);h=kinetic_map(h,-kin,k2)
        phase=np.exp(-1j*cub*(abs(U)**2+x*x-1))
        U=phase*U
        hrot=phase[:,None]*h
        h=hrot+2*cub*U[:,None]*np.imag(U.conj()[:,None]*hrot)
        U=kinetic_map(U,-kin,k2);h=kinetic_map(h,-kin,k2)
        gstart=gram(h)
        comm_start=float(dx*np.imag(np.vdot(h[:,0],h[:,1])))
        # Exact exponential weight; exact for constant Gram (energy mode).
        ase+=(np.exp(-t[i])-np.exp(-t[i+1]))*(gstart+gend)/2
        comm_ase+=(np.exp(-t[i])-np.exp(-t[i+1]))*(comm_start+comm_end)/2
        gend=gstart
        comm_end=comm_start
    inp=gram(h)
    C=np.exp(end)*(inp+ase)  # nsp=1; generalized ASE factor is 2*nsp-1.
    Clo=C[:2,:2]
    # spectral covariance has different global scale, irrelevant to ratio.
    es=np.linalg.eigvalsh((inp+ase)[2:,2:])[::-1]
    out.update(input_gram=inp.tolist(),ase_gram=ase.tolist(),
               matched_LO_covariance=Clo.tolist(),
               matched_LO_min=float(np.linalg.eigvalsh(Clo)[0]),
               matched_LO_determinant=float(np.linalg.det(Clo)),
               phase_energy_deficit=float(1-Clo[0,1]**2/(Clo[0,0]*Clo[1,1])),
               energy_noise_relative_error=float(Clo[0,0]/(2*np.exp(end)-1)-1),
               spectral_ratio=float(es[1]/es[0]),
               reverse_error=float(np.sqrt(dx*np.sum(abs(U-U0)**2)/E0)),
               commutator_relative_error=float(np.exp(end)*(comm_end-comm_ase)-1),
               tangent_adjoint_pairing_relative_error=float(np.linalg.norm(
                   dx*np.real(h.conj().T@dU0)-tangent_output_pairing)/
                   max(np.linalg.norm(tangent_output_pairing),1e-30)),
               Nyquist_over_chirp_edge=float(np.max(abs(k))/chirp))
    return out


def run(output):
    cases=[]
    configs=[
        # Short-time, complete-quantum-noise counterexample to 'no squeezing'.
        dict(end=.02,eps=.05,ngrid=512,dt=.0002),
        dict(end=.02,eps=.05,ngrid=1024,dt=.0001),
        # Moderate gain and step/grid refinement, including quantum pressure.
        dict(end=4.,eps=.1,ngrid=1024,dt=.002),
        dict(end=4.,eps=.1,ngrid=2048,dt=.001),
        dict(end=4.,eps=.05,ngrid=2048,dt=.002),
        dict(end=4.,eps=.05,ngrid=4096,dt=.001),
    ]
    for c in configs:
        r=simulate(**c);cases.append(r)
        print({k:r[k] for k in ['eps','tau','ngrid','steps','energy_error',
              'energy_noise_relative_error','matched_LO_min','spectral_ratio',
              'phase_energy_deficit','reverse_error']},flush=True)
        Path(output).write_text(json.dumps({'cases':cases},indent=2)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default='results_nlse.json')
    run(p.parse_args().output)
