"""Frozen physical and convergence controls. gpt-c / gpt-6-astra / gpt."""
import json,math
from pathlib import Path
from make_cases import make
from independent import carrier_beta2,BETA3,W0,measured_beta2
HERE=Path(__file__).resolve().parent

def dump(name,cases):
    (HERE/(name+'.json')).write_text(json.dumps(cases,indent=2)+'\n')
def main():
    cs=[]
    for N,center in [(3,135),(4,210),(6,375)]:
        for f in [.8,.9,1.,1.1,1.2]:
            c=make(N,center*f,'hc',split='physical',suffix='_smf',dispersion='measured',shock=True,loss_db_km=.2)
            c['zN']=[3,4,5];cs.append(c)
    b0=carrier_beta2('measured')
    for T in [150,160,175,200,250,300,400,500]:
        N=math.sqrt(3e6*.0013*T/(2*b0))
        c=make(N,T,'hc',split='constrained',suffix='_E3nJ_L2m',dispersion='measured',shock=True,loss_db_km=.2)
        c['zN']=[2*b0*N/T**2];c['constraint']={'E_launch_nJ':3,'L_m':2,'Pmax_W':10000,'T0_interval_fs':[150,500]};cs.append(c)
    dump('physical_cases',cs)
    cs=[]
    for N,T in [(4,200),(8,620),(16,1875)]:
        base=make(N,T,split='control',suffix='_baseline')
        if N==4:base.update(n=16384,width=160,zN=[3,4])
        if N==8:base.update(n=32768,width=100,zN=[1.5,2,2.5])
        if N==16:base.update(n=32768,width=45,zN=[1.1,1.25,1.4])
        cs.append(base)
        for mode in ['fine','wide','tight']:
            c=dict(base);c['id']=base['id'].replace('_baseline','_'+mode)
            if mode=='fine':c['n']*=2
            if mode=='wide':c['n']*=2;c['width']*=2
            if mode=='tight':c['tol']/=16
            c['convergence_justification']=mode+' check of production peak; larger grid used only as a convergence control.'
            cs.append(c)
    for h in [.0004,.0002,.0001,.00005]:
        c=make(4,200,split='control',suffix=f'_step{h:g}',fixed_step=h)
        c.update(n=16384,width=96,zN=[3]);cs.append(c)
    for n in [8192,16384,32768]:
        for sampling in ['analytic','sampled_normalized']:
            c=make(4,200,split='control',suffix=f'_kernel{sampling}_n{n}')
            c.update(n=n,width=96,zN=[3])
            if sampling!='analytic':c['raman_sampling']=sampling
            cs.append(c)
    for N in [4,8]:
        for f in [.7,.85,1.,1.15,1.4]:
            cs.append(make(N,21*N**1.62*f,'bw_damped',split='calibration'))
    c=make(4,400,'bw',split='control',suffix='_times2',raman_scale=2.)
    c.update(n=32768,width=160,zN=[3,4]);cs.append(c)
    c=make(4,200,'bw','gaussian',split='control',fixed_step=.0001,shock=True,solver_filter=True,raman_sampling='sampled_raw')
    c.update(id='library_matched_gaussian_N4_T200',n=16384,width=96,zN=[3],
             convergence_justification='Matched sampled response, shock and library filter; compares Gaussian field against agents solver.')
    cs.append(c)
    dump('control_cases',cs)
    print('physical',len(json.loads((HERE/'physical_cases.json').read_text())),'controls',len(cs),'measured beta2',-b0/1000)
if __name__=='__main__':main()
