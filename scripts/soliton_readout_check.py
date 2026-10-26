#!/usr/bin/env python3
"""Selected-mask convergence using the exact scalar RK4IP pullback.
agent: gpt-b; model: gpt-6-astra; family: gpt.
"""
import argparse,json,time
from pathlib import Path
import numpy as np
try:
    import tomllib
except ImportError:
    import tomli as tomllib
from soliton_batch_adjoint import ScalarRK,fw,bw,checks


def main():
    ap=argparse.ArgumentParser();ap.add_argument('config');ap.add_argument('--masks')
    ap.add_argument('--nsteps',type=int);ap.add_argument('--stride',type=int,default=1)
    ap.add_argument('--output',required=True);ap.add_argument('--columns',nargs='+',type=int)
    args=ap.parse_args();cfg=tomllib.loads(Path(args.config).read_text())
    if args.nsteps:cfg['nsteps']=args.nsteps
    rk=ScalarRK(cfg);start=time.monotonic()
    validation=checks(rk)
    history=np.empty((cfg['nsteps']+1,rk.n),complex);history[0]=rk.launch()
    for j in range(cfg['nsteps']):history[j+1]=rk.stages(history[j])[0]
    finefs=fw(history[-1]);maskpath=args.masks or cfg['mask_file']
    masks=np.loadtxt(maskpath,delimiter=',',ndmin=2)
    if args.columns:masks=masks[:,np.array(args.columns)-1]
    masks=np.fft.ifftshift(masks,axes=0);masks[rk.p<=0,:]=0
    invp=np.divide(1.,rk.p,out=np.zeros(rk.n),where=rk.p>0)
    den=(abs(finefs)**2*invp)@masks
    terminal=finefs[:,None]*invp[:,None]*masks/np.sqrt(den)[None,:]
    lam=bw(terminal);bath=np.zeros((masks.shape[1],masks.shape[1]))
    last=rk.source_gram(history[-1],lam);lastj=cfg['nsteps']
    for j in range(cfg['nsteps']-1,-1,-1):
        lam=rk.pullback(rk.stages(history[j])[1],lam)
        if j%args.stride==0:
            source=rk.source_gram(history[j],lam)
            bath+=(lastj-j)*rk.h*(last+source)/2;last=source;lastj=j
    lw=fw(lam);vac=np.sum(abs(lw)**2*np.maximum(rk.p,0)[:,None],axis=0)
    rows=[dict(column=(args.columns[i] if args.columns else i+1),F_vacuum=float(vac[i]),
               F_Raman=float(bath[i,i]),F_total=float(vac[i]+bath[i,i]),
               dB=float(10*np.log10(vac[i]+bath[i,i]))) for i in range(len(vac))]
    out=dict(agent='gpt-b',model='gpt-6-astra',family='gpt',config=cfg,mask_path=maskpath,
        nsteps=cfg['nsteps'],source_stride=args.stride,wall_time_s=time.monotonic()-start,
        validation=validation,rows=rows)
    Path(args.output).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))


if __name__=='__main__':main()
