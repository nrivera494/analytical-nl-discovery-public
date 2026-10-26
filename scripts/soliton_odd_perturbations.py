#!/usr/bin/env python3
"""Parity/order checks for shock and beta3 in the scalar soliton lane.

agent: gpt-b; model: gpt-6-astra; family: gpt.
Uses the RK4IP discrete pullback independently checked against the native
solver. No Raman kernel or reservoir is constructed in this evaluator.
"""
import argparse
import json
from pathlib import Path
import time
import numpy as np
from soliton_batch_adjoint import ScalarRK, fw, bw, score, checks


def evaluate(s,delta,n=256,window=40.,z=3.,steps=600):
    rk=ScalarRK.__new__(ScalarRK)
    rk.cfg=dict(nsteps=steps,z_over_LD=z);rk.n=n;rk.window=window
    rk.x=(np.arange(n)-n//2)*window/n;rk.k=2*np.pi*np.fft.fftfreq(n,window/n)
    rk.R=np.ones(n,complex);rk.S=np.zeros(n);rk.shock=1+s*rk.k
    rk.p=1+s*rk.k;rk.delta3=delta;rk.h=z/steps
    rk.D=np.exp(1j*(-.5*rk.k**2+delta*rk.k**3)*rk.h/2)
    history=np.empty((steps+1,n),complex);history[0]=rk.launch()
    start=time.monotonic()
    for j in range(steps):history[j+1]=rk.stages(history[j])[0]
    final=fw(history[-1]);selected=np.flatnonzero(abs(rk.k)<=6)
    selected=selected[np.argsort(rk.k[selected])]
    fs=final[selected]/np.sqrt(rk.p[selected]);m=len(selected)
    terminal=np.zeros((n,2*m),complex);phase=np.exp(1j*np.angle(fs))
    terminal[selected,np.arange(m)]=phase/np.sqrt(rk.p[selected])
    terminal[selected,m+np.arange(m)]=1j*phase/np.sqrt(rk.p[selected])
    lam=bw(terminal)
    for j in range(steps-1,-1,-1):lam=rk.pullback(rk.stages(history[j])[1],lam)
    lw=fw(lam)
    with np.errstate(over='ignore',invalid='ignore',divide='ignore'):
        v=(lw.conj().T@(rk.p[:,None]*lw)).real
    mask,row=score(v,fs,rk.k[selected])
    edge=(abs(rk.k[selected])<.7368).astype(float)
    readout=np.r_[abs(fs)*edge,np.zeros(m)]
    with np.errstate(over='ignore',invalid='ignore',divide='ignore'):
        fedge=float(readout@v@readout/(abs(fs)**2@edge))
    power=abs(history[-1])**2;spec=abs(final)**2
    row.update(s=s,delta3=delta,n=n,window=window,z_over_LD=z,nsteps=steps,
        centered_fixed_edge_F=fedge,mean_x=float(rk.x@power/power.sum()),
        mean_k=float(rk.k@spec/spec.sum()),predicted_first_order_x=(s+delta)*z,
        wall_time_s=time.monotonic()-start,validation=checks(rk))
    return row


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True)
    args=ap.parse_args();out=dict(agent='gpt-b',model='gpt-6-astra',family='gpt',points=[])
    cases=[(0.,0.)]
    for value in [.001,.002,.004,.008]:
        cases.extend([(value,0.),(-value,0.),(0.,value),(0.,-value)])
    for s,delta in cases:
        row=evaluate(s,delta);out['points'].append(row)
        Path(args.output).write_text(json.dumps(out,indent=2))
        print(json.dumps({k:v for k,v in row.items() if not k.endswith('indices')}),flush=True)


if __name__=='__main__':main()
