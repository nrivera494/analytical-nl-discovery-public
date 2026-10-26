"""gpt-e / gpt-6-astra / gpt. Independent finite-volume ASE covariance.

Discretizes d_x[(1-x^2)d_x] with zero boundary flux, obtains numerical
eigenvectors, and integrates the Lyapunov equation. No proposer code imported.
State is (exp(tau/3)*n, exp(-tau/3)*epsilon*p), tau=log(power gain).
"""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[key]='1'
import argparse,json,time
from pathlib import Path
import numpy as np
from scipy.linalg import eigh_tridiagonal
from scipy.integrate import solve_ivp
from scipy.special import eval_legendre

HERE=Path(__file__).resolve().parent
RAW=Path('~/analytical-nl-discovery-data')/HERE.name
RAW.mkdir(parents=True,exist_ok=True)

def covariance(Gamma=np.sqrt(18),nsp=1.,cells=256,modes=8,launch='asymptotic',
               last=30.,epsilon=.05,phase_noise=False,edge_cutoff=0.,rtol=2e-10):
    start=time.time();dx=2/cells;x=-1+(np.arange(cells)+.5)*dx
    faces=np.linspace(-1,1,cells+1);wfaces=1-faces**2
    diagonal=-(wfaces[:-1]+wfaces[1:])/dx**2;off=wfaces[1:-1]/dx**2
    vals,vec=eigh_tridiagonal(diagonal,off,select='i',select_range=(cells-modes,cells-1))
    vals=vals[::-1];vec=vec[:,::-1]
    ph=np.array([np.sqrt((2*l+1)/2)*eval_legendre(l,x) for l in range(5)])
    # The claim is about an orthonormal projection. Raw midpoint Legendre
    # quadrature leaks a tiny energy component into shape modes, which dominates
    # a decaying shape at sufficiently high gain. QR removes that artefact.
    orth,R=np.linalg.qr(np.sqrt(dx)*ph.T)
    orth*=np.sign(np.diag(R))[None,:]
    Q=orth.T@vec
    B=4/3*(vec.T*(1-x*x))@vec
    BP=epsilon**2/3*(vec.T/np.maximum(1-x*x,edge_cutoff))@vec if phase_noise else np.zeros_like(B)
    initial=np.zeros((2*modes,2*modes));initial[:modes,:modes]=B;initial[modes:,modes:]=BP
    if launch=='asymptotic':A0=(18/Gamma**2)**(1/3);rate0=1/3
    elif launch=='unchirped':A0=1.;rate0=0.
    elif launch=='chirped':A0=1.;rate0=Gamma/3/Gamma
    else:raise ValueError(launch)
    y0=np.r_[A0,rate0,0.,initial.ravel()]
    def rhs(tau,state):
        A,rate,theta=state[:3];C=state[3:].reshape(2*modes,2*modes)
        mat=np.zeros_like(C)
        mat[:modes,:modes]=np.eye(modes)/3
        mat[modes:,modes:]=-np.eye(modes)/3
        mat[:modes,modes:]=np.diag(vals)/(Gamma*A*A)
        mat[modes:,:modes]=np.eye(modes)/(Gamma*A)
        D=np.zeros_like(C)
        D[:modes,:modes]=(2*nsp-1)*np.exp(-tau/3)*B
        D[modes:,modes:]=(2*nsp-1)*np.exp(-5*tau/3)*BP
        dc=mat@C+C@mat.T+D
        return np.r_[(rate-1/3)*A,2/(Gamma**2*A**3)-rate*rate,np.exp(2*tau/3)/(Gamma*A),dc.ravel()]
    taus=np.unique(np.r_[np.arange(.25,last+.001,.25),[1.,2.,4.,6.,12.,15.,18.,last]])
    taus=taus[taus<=last]
    sol=solve_ivp(rhs,(0,last),y0,method='DOP853',rtol=rtol,atol=rtol*.02,t_eval=taus)
    if not sol.success:raise RuntimeError(sol.message)
    rows=[]
    for tau,state in zip(sol.t,sol.y.T):
        A,rate,theta=state[:3];C=state[3:].reshape(2*modes,2*modes);C=(C+C.T)/2
        # In a common exp(-tau/3) spectral prefactor, which cancels in ratios.
        read=np.column_stack([Q,Q@np.diag(vals)/(Gamma*A*A*rate)])
        spec=read@C@read.T;se=np.linalg.eigvalsh(spec)
        n0=np.r_[Q[0]/np.sqrt(2),np.zeros(modes)]
        pbar=np.r_[np.zeros(modes),Q[0]/np.sqrt(2)-Q[2]/np.sqrt(10)]
        vn=n0@C@n0;vp=pbar@C@pbar;cross=n0@C@pbar
        deficit=1-cross*cross/(vn*vp)
        # Numerical-mode versus orthonormal-Legendre projection is tested by
        # the grid and mode-count sweeps, not assumed identical.
        nn=np.diag(Q@C[:modes,:modes]@Q.T)
        pp=np.diag(Q@C[modes:,modes:]@Q.T)
        row=dict(tau=float(tau),A_scaled=float(A),width=float(A*np.exp(tau/3)),width_rate=float(rate),
            theta=float(theta),Phi_NL=float(theta/epsilon),spectral_ratio=float(se[-2]/se[-1]),
            phase_energy_deficit=float(deficit),scaled_intensity_variances=nn[2:5].tolist(),
            scaled_phase_variances=pp[2:5].tolist(),
            photon_intensity_variances=(np.exp(tau/3)*nn[2:5]).tolist(),
            photon_phase_variances=(np.exp(5*tau/3)*pp[2:5]/epsilon**2).tolist(),
            n0_variance=float(np.exp(-2*tau/3)*vn),
            n2_variance=float(2.5*np.exp(-2*tau/3)*nn[2]),
            p2_variance=float(2.5*np.exp(2*tau/3)*pp[2]/epsilon**2),
            matched_phase_variance=float(np.exp(2*tau/3)*vp/epsilon**2),
            CAA=float(2.25*np.exp(tau/3)*vn),
            CPP=float(4*np.exp(5*tau/3)*vp/epsilon**2),
            CAP=float(3*np.exp(tau)*cross/epsilon))
        rows.append(row)
    arr=np.array([[r['tau'],*r['photon_intensity_variances'],*r['photon_phase_variances'],r['spectral_ratio'],r['phase_energy_deficit']] for r in rows])
    fit=(arr[:,0]>=12)&(arr[:,0]<=18)
    slopes=np.polyfit(arr[fit,0],np.log(arr[fit,1:]),1)[0].tolist()
    late=arr[:,0]>=12
    # Envelopes bounded after the exact power is removed, not convergence of
    # each prefactor. Record extrema and oscillation amplitude.
    normalized=arr[:,1:]*np.exp(-arr[:,0,None]*np.array([1/3]*3+[5/3]*3+[-2/3]*2))
    result=dict(Gamma=Gamma,nsp=nsp,cells=cells,modes=modes,launch=launch,last=last,epsilon=epsilon,
        phase_noise=phase_noise,edge_cutoff=edge_cutoff,rtol=rtol,eigenvalues=vals.tolist(),
        slopes_12_18=slopes,late_normalized_min=normalized[late].min(axis=0).tolist(),
        late_normalized_max=normalized[late].max(axis=0).tolist(),seconds=time.time()-start,
        rows=rows)
    fname=f'g{Gamma:.12g}_sp{nsp}_c{cells}_m{modes}_{launch}_p{phase_noise}_e{edge_cutoff}_r{rtol}_end{last:.12g}_qr'
    np.savez_compressed(RAW/(fname+'.npz'),tau=sol.t,states=sol.y,x=x,eigenvectors=vec)
    dense=RAW/(fname+'.json');dense.write_text(json.dumps(result,indent=2)+'\n')
    result['raw_curve_location']=str(dense)
    checkpoints=[1.,2.,4.,6.,12.,15.,18.,24.,last]
    result['rows']=[r for r in rows if any(abs(r['tau']-t)<1e-10 for t in checkpoints)]
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument('--suite',default='main');a=p.parse_args()
    if a.suite=='main':
        cases=[dict(Gamma=g,launch=launch) for g in [.5,1.,np.sqrt(18),10.,12.] for launch in ['asymptotic','unchirped']]
        cases += [dict(nsp=2.),dict(nsp=1.5)]
    elif a.suite=='checks':
        cases=[dict(cells=512),dict(cells=1024),dict(modes=16),dict(rtol=1e-11),
               dict(phase_noise=True,edge_cutoff=.01),dict(phase_noise=True,edge_cutoff=.001),
               dict(phase_noise=True,cells=1024,edge_cutoff=.001)]
    else:raise ValueError(a.suite)
    rows=[]
    for kw in cases:
        result=covariance(**kw);rows.append(result)
        print(json.dumps({k:v for k,v in result.items() if k!='rows'}),flush=True)
        (HERE/f'reduced-{a.suite}.json').write_text(json.dumps(rows,indent=2)+'\n')
if __name__=='__main__':main()
