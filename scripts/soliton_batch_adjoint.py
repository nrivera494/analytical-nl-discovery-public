#!/usr/bin/env python3
"""Batch scalar RK4IP discrete adjoints for the soliton lane only.

agent: gpt-b; model: gpt-6-astra; family: gpt.
Independent scalar evaluator; checked against the pinned public solver.
Raman kernels/symmetrized spectra are exported by soliton_native_check.jl.
Output covariance is restricted to a declared spectral band; convergence
of that restriction is required before interpreting its lowest eigenvalue.
"""
import argparse
import json
import os
from pathlib import Path
import time
os.environ.setdefault('OPENBLAS_NUM_THREADS','2')
os.environ.setdefault('VECLIB_MAXIMUM_THREADS','2')
os.environ.setdefault('OMP_NUM_THREADS','2')
import numpy as np
from scipy.fft import fft, ifft
from scipy.linalg import eigh, null_space
try:
    import tomllib
except ImportError:
    import tomli as tomllib
from soliton_fano_theory import search_binary
FFT_WORKERS=max(1,min(2,int(os.environ.get('SOLITON_FFT_WORKERS','2'))))


def fw(u):
    return ifft(u,axis=0,norm='ortho',workers=FFT_WORKERS)


def bw(u):
    return fft(u,axis=0,norm='ortho',workers=FFT_WORKERS)


class ScalarRK:
    def __init__(self,cfg):
        self.cfg=cfg
        kernels=np.loadtxt(Path(cfg['raw_location'])/'native_kernels.csv',delimiter=',')
        self.k=kernels[:,0];self.R=kernels[:,1]+1j*kernels[:,2]
        self.S=kernels[:,3];self.shock=kernels[:,4]
        self.n=len(self.k);self.window=cfg['window_over_T0']
        self.x=(np.arange(self.n)-self.n//2)*self.window/self.n
        omega0=2*np.pi*2.99792458e-4/(cfg['lambda0_nm']*1e-9)
        if cfg.get('suppress_shock',False):omega0=1e12
        self.p=1+self.k/(cfg['T0_ps']*omega0)
        self.delta3=cfg['beta3_ps3_per_m']/(6*abs(cfg['beta2_ps2_per_m'])*cfg['T0_ps'])
        self.h=cfg['z_over_LD']/cfg['nsteps']
        self.D=np.exp(1j*(-.5*self.k**2+self.delta3*self.k**3)*self.h/2)

    def mult(self,u,symbol):
        return bw(symbol[:,None]*fw(u)) if u.ndim==2 else bw(symbol*fw(u))

    def nonlinear(self,u):
        response=self.mult(abs(u)**2,self.R).real
        return self.mult(u*response,1j*self.shock)

    def vjp(self,u,lam):
        response=self.mult(abs(u)**2,self.R).real
        y=self.mult(lam,-1j*self.shock)
        source=(u.conj()[:,None]*y).real
        back=self.mult(source,self.R.conj()).real
        return response[:,None]*y+2*u[:,None]*back

    def stages(self,u):
        a=self.mult(u,self.D)
        k1=self.mult(self.nonlinear(u),self.D)
        s2=a+self.h/2*k1;k2=self.nonlinear(s2)
        s3=a+self.h/2*k2;k3=self.nonlinear(s3)
        s4=self.mult(a+self.h*k3,self.D)
        k4=self.nonlinear(s4)
        out=self.mult(a+self.h/6*(k1+2*k2+2*k3),self.D)+self.h/6*k4
        return out,(u,s2,s3,s4)

    def pullback(self,stages,lam):
        u,s2,s3,s4=stages;h=self.h
        dl=self.mult(lam,self.D.conj())
        ba=dl.copy();bk1=h/6*dl;bk2=h/3*dl;bk3=h/3*dl
        bs4=self.vjp(s4,h/6*lam)
        bt4=self.mult(bs4,self.D.conj());ba+=bt4;bk3+=h*bt4
        bs3=self.vjp(s3,bk3);ba+=bs3;bk2+=h/2*bs3
        bs2=self.vjp(s2,bk2);ba+=bs2;bk1+=h/2*bs2
        return self.mult(ba,self.D.conj())+self.vjp(u,self.mult(bk1,self.D.conj()))

    def launch(self):
        if self.cfg.get('launch','sech')=='gaussian':
            q=np.exp(-self.x**2/2)
        else:q=1/np.cosh(self.x)
        return self.cfg.get('N',1.)*q.astype(complex)

    def source_gram(self,u,lam):
        shocked=self.mult(lam,self.shock)
        b=-(shocked.conj()*u[:,None]).imag
        bf=fw(b)
        # Relative to coherent Re/Im covariance q/4, the bath covariance is 4S.
        with np.errstate(over='ignore',divide='ignore',invalid='ignore'):
            result=4*(bf.conj().T@(self.S[:,None]*bf)).real
        if not np.all(np.isfinite(result)):raise FloatingPointError('source covariance')
        return result


def checks(rk):
    rng=np.random.default_rng(1010);u=rk.launch()
    v=(rng.normal(size=rk.n)+1j*rng.normal(size=rk.n))/np.sqrt(rk.n)
    lam=(rng.normal(size=rk.n)+1j*rng.normal(size=rk.n))/np.sqrt(rk.n)
    out,stages=rk.stages(u)
    adj=rk.pullback(stages,lam[:,None])[:,0]
    h=1e-5
    fd=(rk.stages(u+h*v)[0]-rk.stages(u-h*v)[0])/(2*h)
    left=np.vdot(lam,fd).real;right=np.vdot(adj,v).real
    return {'discrete_adjoint_dot_relative_error':float(abs(left-right)/max(abs(left),abs(right),1e-12))}


def score(v,fs,k,seed=20261010):
    n=len(fs)
    vamp=v[:n,:n]
    lmin=float(eigh(v,eigvals_only=True,subset_by_index=[0,0])[0])
    lgen=float(eigh(vamp,eigvals_only=True,subset_by_index=[0,0])[0])
    # Coordinates are locally rotated by the output mean phase: i*mean has
    # zero amplitude block and the positive mean magnitude in its phase block.
    globalphase=np.r_[np.zeros(n),abs(fs)]
    basis=null_space(globalphase.reshape(1,-1))
    lpass=float(eigh(basis.T@v@basis,eigvals_only=True,subset_by_index=[0,0])[0])
    mask,res=search_binary(vamp,fs,seed=seed)
    res.update(lambda_min=lmin,lambda_gen=lgen,lambda_pass=lpass)
    for key in ('lambda_min','lambda_gen','lambda_pass','best_binary_found','best_interval'):
        res[key+'_dB']=float(10*np.log10(res[key]))
    res['gap_gen_to_binary_dB']=res['best_binary_found_dB']-res['lambda_gen_dB']
    res['gap_min_to_binary_dB']=res['best_binary_found_dB']-res['lambda_min_dB']
    return mask,res


def main():
    ap=argparse.ArgumentParser();ap.add_argument('config')
    ap.add_argument('--band',type=float,default=6.);ap.add_argument('--source-stride',type=int,default=4)
    ap.add_argument('--output-suffix',default='batch');ap.add_argument('--check-only',action='store_true')
    ap.add_argument('--no-bath',action='store_true');ap.add_argument('--amplitude-only',action='store_true')
    ap.add_argument('--bin-width',type=float,default=0.,help='Optional constant-filter spectral cells in dimensionless k; eigenvalues are Ritz values in this basis.')
    ap.add_argument('--omit-adjoint',action='store_true')
    args=ap.parse_args();cfg=tomllib.loads(Path(args.config).read_text());dest=Path(cfg['raw_location'])
    rk=ScalarRK(cfg);validation=checks(rk);print(validation,flush=True)
    if args.check_only:return
    started=time.monotonic()
    mean=np.empty((cfg['nsteps']+1,rk.n),complex);mean[0]=rk.launch()
    for j in range(cfg['nsteps']):mean[j+1]=rk.stages(mean[j])[0]
    print('forward done',time.monotonic()-started,flush=True)
    native=dest/'native_mean.csv'
    if native.exists():
        data=np.loadtxt(native,delimiter=',');native_mean=data[:,1]+1j*data[:,2]
        validation['native_mean_relative_error']=float(np.linalg.norm(native_mean-mean[-1])/np.linalg.norm(native_mean))
    fullfs=fw(mean[-1])
    power=abs(fullfs)**2
    center=float(rk.k@power/power.sum())
    selected=np.flatnonzero((abs(rk.k-center)<=args.band)&(rk.p>0))
    selected=selected[np.argsort(rk.k[selected])]
    p=rk.p[selected];finefs=fullfs[selected]/np.sqrt(p)
    phase=np.exp(1j*np.angle(finefs))
    if args.bin_width>0:
        labels=np.floor((rk.k[selected]-center)/args.bin_width).astype(int)
        _,groups=np.unique(labels,return_inverse=True)
        m=int(groups.max()+1)
        group_power=np.bincount(groups,weights=abs(finefs)**2,minlength=m)
        fs=np.sqrt(group_power).astype(complex)
        weights=abs(finefs)/np.sqrt(group_power[groups])
    else:
        groups=np.arange(len(selected));m=len(selected);fs=finefs;weights=np.ones(m)
    columns=m if args.amplitude_only else 2*m
    terminal=np.zeros((rk.n,columns),complex)
    terminal[selected,groups]=phase/np.sqrt(p)*weights
    if not args.amplitude_only:terminal[selected,m+groups]=1j*phase/np.sqrt(p)*weights
    lam=bw(terminal)
    raman=np.zeros((columns,columns))
    source_on=not args.no_bath and np.max(rk.S)>0
    lastsource=rk.source_gram(mean[-1],lam) if source_on else None
    lastindex=cfg['nsteps']
    for j in range(cfg['nsteps']-1,-1,-1):
        _,stages=rk.stages(mean[j]);lam=rk.pullback(stages,lam)
        if source_on and (j%args.source_stride==0 or j==0):
            source=rk.source_gram(mean[j],lam)
            raman+=(lastindex-j)*rk.h*(source+lastsource)/2
            lastsource=source;lastindex=j
        if j%max(1,cfg['nsteps']//10)==0:
            print('adjoint',j,'/',cfg['nsteps'],'elapsed',time.monotonic()-started,flush=True)
    lw=fw(lam)
    with np.errstate(over='ignore',divide='ignore',invalid='ignore'):
        vac=(lw.conj().T@(np.maximum(rk.p,0)[:,None]*lw)).real
    total=(vac+raman);total=(total+total.T)/2
    if not np.all(np.isfinite(total)):raise FloatingPointError('output covariance')
    if args.amplitude_only:
        mask,res=search_binary(total,fs)
    else:mask,res=score(total,fs,rk.k[selected])
    readout=np.r_[abs(fs)*mask,np.zeros(columns-m)]
    den=float(sum(abs(fs)**2*mask))
    allread=np.r_[abs(fs),np.zeros(columns-m)]
    with np.errstate(over='ignore',divide='ignore',invalid='ignore'):
        res['best_binary_Raman_part']=float(readout@raman@readout/den)
        res['best_binary_vacuum_part']=float(readout@vac@readout/den)
        res['full_selected_F']=float(allread@total@allread/(abs(fs)**2).sum())
    res.update(agent='gpt-b',model='gpt-6-astra',family='gpt',
        output_band_halfwidth=args.band,output_band_center=center,output_bins=m,
        underlying_output_bins=len(selected),filter_cell_width=args.bin_width,
        output_mean_fraction=float(np.sum(power[selected])/np.sum(power)),
        n=cfg['nt'],dt_fs=cfg['window_over_T0']*cfg['T0_ps']/cfg['nt']*1000,
        nsteps=cfg['nsteps'],source_stride=args.source_stride,
        wall_time_s=time.monotonic()-started,validation=validation,
        eigenvalues_are_for_declared_output_band=True,config=cfg)
    arrays=dict(V=total,Vvac=vac,VR=raman,mean=mean[-1],selected=selected,
                k=rk.k[selected],fs=fs,finefs=finefs,groups=groups,mask=mask)
    if not args.omit_adjoint:arrays['input_adjoint']=lam
    np.savez_compressed(dest/(args.output_suffix+'.npz'),**arrays)
    (dest/(args.output_suffix+'.json')).write_text(json.dumps(res,indent=2))
    # Native masks are centered frequency ordered; preserve the exact bin pattern.
    fullmask=np.zeros(rk.n);fullmask[selected]=mask[groups]
    edge=(abs(rk.k)<cfg.get('edge',.7368)).astype(float)
    np.savetxt(dest/(args.output_suffix+'_masks.csv'),np.fft.fftshift(np.column_stack([np.ones(rk.n),edge,fullmask]),axes=0),delimiter=',')
    print(json.dumps({k:v for k,v in res.items() if not k.endswith('indices')}),flush=True)


if __name__=='__main__':main()
