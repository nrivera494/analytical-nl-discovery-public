#!/usr/bin/env python3
"""agent: gpt-b; model: gpt-6-astra; family: gpt. Coherence and scaling analysis."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'evaluator'))
from thermalized_light import *
from scipy.optimize import curve_fit
RUN=Path(__file__).resolve().parent;DATA=RAW/RUN.name

def observables(blocks,n):
    B=32*len(blocks);o=blocks.mean(axis=0);M=o.shape[1]//6
    mean=o[:,:M]+1j*o[:,M:2*M];I=o[:,2*M:3*M];I2=o[:,3*M:4*M]
    photons=I-.5/n
    coherent=(B*abs(mean)**2-I)/(B-1)
    coh=coherent/np.maximum(photons,1e-30)
    # These legacy "relative_variance" fields are normally ordered excess
    # g2-1, NOT photon-number relative variance. See variance_clocks.json.
    g2=(I2-2*I/n+.5/n**2)/np.maximum(photons**2,1e-60)
    batch_cross=blocks[:,:,4*M:5*M]+1j*blocks[:,:,5*M:6*M]
    cross=batch_cross.mean(axis=0)
    nb=len(blocks)
    cross2=(nb*abs(cross)**2-np.mean(abs(batch_cross)**2,axis=0))/(nb-1)
    relative_coherence=cross2/np.maximum(photons[:,:1]*photons,1e-60)
    return dict(coherence=coh.mean(axis=1),weighted=coherent.sum(axis=1)/photons.sum(axis=1),
        relative_coherence=relative_coherence[:,1:].mean(axis=1),
        relative_variance=np.median(g2[:,1:]-1,axis=1),
        launched_relative_variance=np.median(g2[:,1:6]-1,axis=1),mean_I0=photons[:,0])

def crossing(z,y,target=.5,start=10,down=True):
    for j in range(1,len(z)):
        if z[j]<start:continue
        if (y[j]<=target<y[j-1]) if down else (y[j]>=target>y[j-1]):
            return float(z[j-1]+(z[j]-z[j-1])*(target-y[j-1])/(y[j]-y[j-1]))
    return None

def main():
    records=[json.loads(s) for s in (DATA/'records.jsonl').read_text().splitlines()]
    rows=[]
    for r in records:
        b=np.load(r['raw_file'])['moments'];o=observables(b,r['n']);z=np.arange(len(o['coherence']))*r['sample']
        model=Model(5);a=model.launch(.6,4101);rng=np.random.default_rng(9301);initial=[]
        for _ in range(8):
            if r['dephased']:x=abs(a)*np.exp(2j*np.pi*rng.random((32,model.M)))
            else:x=np.broadcast_to(a,(32,model.M)).copy()
            x+=(rng.normal(size=x.shape)+1j*rng.normal(size=x.shape))/(2*np.sqrt(r['n']))
            initial.append(x)
        before=abs(np.array(initial))**2;after=abs(np.load(r['raw_file'])['final'])**2
        checks=dict(max_final_N_drift=float(np.max(abs(after.sum(axis=2)-before.sum(axis=2)))),
                    max_final_E_drift=float(np.max(abs(np.sum(after*model.q,axis=2)-np.sum(before*model.q,axis=2)))))
        if r['dephased']:
            target=13/30
            first=crossing(z,o['relative_variance'],target,start=.2,down=False)
            launched=crossing(z,o['launched_relative_variance'],target,start=.2,down=False)
            left=bool(o['relative_variance'][1]>=target)
            jk=[]
            for j in range(len(b)):
                oo=observables(np.delete(b,j,axis=0),r['n'])
                val=crossing(z,oo['launched_relative_variance'],target,start=.2,down=False)
                if val is not None:jk.append(val)
            row=dict(r,fluctuation_onset=first,launched_modes_onset=launched,**checks,
                variance_definition='legacy diagnostic: normally ordered g2-1; not photon-number relative variance',
                onset_left_censored_at_first_nonzero_sample=left,
                first_nonzero_sample_relative_variance=float(o['relative_variance'][1]),
                launched_onset_se=float(np.sqrt((len(jk)-1)*np.var(jk))) if len(jk)>1 else None,
                mean_I0_at_lengths={str(t):float(o['mean_I0'][round(t/r['sample'])]) for t in [2,10,50,100,200]})
        else:
            length=crossing(z,o['coherence']);weighted=crossing(z,o['weighted'])
            jk=[]
            for i in range(len(b)):
                val=crossing(z,observables(np.delete(b,i,axis=0),r['n'])['coherence'])
                if val is not None:jk.append(val)
            se=float(np.sqrt((len(jk)-1)*np.var(jk))) if len(jk)>1 else None
            row=dict(r,crossing=length,crossing_se=se,weighted_crossing=weighted,
                relative_phase_crossing=crossing(z,o['relative_coherence']),**checks,
                jackknife_crossings=jk,thermal_variance_crossing=crossing(z,o['relative_variance'],13/30,start=10,down=False),
                scaled_dephasing={str(t):float(r['n']*(-np.log(max(o['coherence'][round(t/r['sample'])],1e-100))))
                                  for t in [10,25,50,100]})
        rows.append(row)
    fits=[]
    lyap=json.loads((RUN/'lyapunov_summary.json').read_text())['rows']
    for seed in [7501,7502]:
        rr=sorted([r for r in rows if not r['dephased'] and r['dt']==.04 and r['disorder_seed']==seed and r['n']>=1e6],key=lambda r:r['n'])
        if len(rr)!=5 or any(r['crossing'] is None for r in rr):continue
        x=np.log([r['n'] for r in rr]);y=np.array([r['crossing'] for r in rr])
        train=np.array([r['n'] not in [1e7,1e12] for r in rr])
        coef,cov=np.polyfit(x[train],y[train],1,cov=True)
        ref=next(r for r in lyap if r['seed']==seed and r['epsilon']==1e-7)
        residuals=y-np.polyval(coef,x)
        jkcoef=[];jkresidual=[]
        for j in range(8):
            if any(len(r['jackknife_crossings'])!=8 for r in rr):break
            jy=np.array([r['jackknife_crossings'][j] for r in rr])
            jc=np.polyfit(x[train],jy[train],1);jkcoef.append(jc);jkresidual.append(jy-np.polyval(jc,x))
        slope_jk_se=float(np.sqrt(7*np.var(np.array(jkcoef)[:,0]))) if len(jkcoef)==8 else None
        # Diagnostic free exponent with an intercept; uncertainty is from fit curvature.
        try:
            power,pcov=curve_fit(lambda xx,a,b,p:b+a*xx**p,x,y,p0=[coef[0],coef[1],1],maxfev=20000)
            exponent=float(power[2]);exponent_se=float(np.sqrt(pcov[2,2]))
        except (ValueError,RuntimeError):exponent=None;exponent_se=None
        fits.append(dict(disorder_seed=seed,slope=float(coef[0]),intercept=float(coef[1]),
            slope_se=float(np.sqrt(cov[0,0])),lambda1=ref['lambda1'],predicted_slope=ref['predicted_slope'],
            slope_shot_jackknife_se=slope_jk_se,
            residual_shot_jackknife_se=np.sqrt(7*np.var(jkresidual,axis=0)) if len(jkresidual)==8 else None,
            slope_ratio=float(coef[0]/ref['predicted_slope']),residuals=residuals,n=[r['n'] for r in rr],
            held_out=[r['n'] in [1e7,1e12] for r in rr],free_log_power=exponent,free_log_power_se=exponent_se,
            free_log_power_fit_role='post-hoc diagnostic using all five points; not a held-out test',
            pass_slope=bool(abs(coef[0]/ref['predicted_slope']-1)<=.3),
            pass_held_out=bool(all(abs(residuals[i])<=max(30,3*(r['crossing_se'] or 0))
                                  for i,r in enumerate(rr) if r['n'] in [1e7,1e12]))))
    save_json(RUN/'summary.json',dict(**IDENTITY,rows=rows,fits=fits,lyapunov=lyap,
                                     exact=json.loads((RUN/'exact_summary.json').read_text()),
                                     variance_clock_correction=json.loads((RUN/'variance_clocks.json').read_text())))
    for f in fits:print(f)
    for r in rows:
        if r['dephased']:print('dephased',r['n'],r['fluctuation_onset'],r['launched_modes_onset'])

if __name__=='__main__':main()
