"""Independent extraction-window and shooting-resolution audit. gpt-c/gpt-6-astra/gpt."""
import json
from pathlib import Path
import numpy as np
from scipy.fft import fft,ifft,fftfreq
from independent import RAW,zs_root,beta2_local,carrier_beta2,W0,GAMMA,write_json,census
HERE=Path(__file__).resolve().parent
out={'agent':'gpt-c','model':'gpt-6-astra','family':'gpt','cases':[]}
names=['bw_N3_T25','bw_N3_T50','bw_N4_T200','bw_N6_T400','bw_N4.5_T240',
             'measured_hc_s1_N3_T25','measured_hc_s1_N3_T50','measured_hc_s1_N3_T140',
             'measured_hc_s1_N4_T200','measured_hc_s1_N6_T400']
for name,zn in [(name,4) for name in names]+[('conv_fine_N12_T1176',2),('conv_fine_N16_T1875',2)]:
    path=HERE/(name+'.json')
    if not path.exists():continue
    r=json.loads(path.read_text());case=r['case'];N=case['N'];T=case['T0_fs']
    cp=next(c for c in r['checkpoints'] if c['zN']==zn)
    data=np.load(RAW/(name+'_zN'+str(zn)+'.npz'));t=data['t'];q=data['q'];dt=t[1]-t[0]
    lead=census(t,q,case)['leading'];j=lead['index'];wc=lead['red_w'];b=lead['local_beta2_ratio'];g=lead['local_gamma_ratio']
    qd=q*np.exp(-1j*wc*(t-t[j]))*np.sqrt(g/b)
    half0=(lead['bounds'][1]-lead['bounds'][0])/2
    rows=[]
    for fac in [.5,.75,1,1.5,2]:
        mask=abs(t-t[j])<half0*fac
        for pts in [1024,2048,4096]:
            z=zs_root(t[mask]-t[j],qd[mask],guess=[lead['zs']['real'],lead['zs']['eta']],points=pts)
            frac=4*z['eta']*b/g/(2*N*N)
            rows.append({'halfwidth_factor':fac,'halfwidth_T0':half0*fac,'points':pts,'zs':z,'f_zs':frac,
                         'f_temporal_gate':float(np.trapezoid(abs(q[mask])**2,t[mask])/(2*N*N))})
    I=abs(q)**2;dq=ifft(1j*2*np.pi*fftfreq(len(t),dt)*fft(q));mask=(t>=lead['bounds'][0])&(t<=lead['bounds'][1])
    corewc=float(np.sum(I[mask]*np.imag(q[mask].conj()*dq[mask]))/np.sum(I[mask]**2))
    out['cases'].append({'case':name,'zN':zn,'leading':lead,'core_weighted_red_w':corewc,
                         'fractional_centroid_difference':corewc/wc-1,'variations':rows})
    print(name,'f',lead['f_zs'],'variations',[(x['halfwidth_factor'],x['f_zs']) for x in rows if x['points']==4096],flush=True)
write_json(HERE/'extraction_checks.json',out)
