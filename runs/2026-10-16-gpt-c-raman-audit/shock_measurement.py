"""Compare the claim's unscaled ZS observable with local energy. gpt-c/gpt-6-astra/gpt."""
from pathlib import Path
import json
import numpy as np
from scipy.fft import fft,fftfreq
from independent import RAW,W0,zs_root,write_json

HERE=Path(__file__).resolve().parent
out=dict(agent='gpt-c',model='gpt-6-astra',family='gpt',rows=[])
for N,T in [(3,100),(3,140),(4,200),(6,400)]:
    name=f'shock_bw_N{N}_T{T}'
    path=HERE/(name+'.json')
    if not path.exists():continue
    r=json.loads(path.read_text())
    ref=json.loads((HERE/f'bw_N{N}_T{T}.json').read_text())
    for cp in r['checkpoints']:
        if cp['zN'] not in [3,4]:continue
        d=np.load(RAW/(name+'_zN'+str(cp['zN'])+'.npz'));t=d['t'];q=d['q']
        p=cp['leading'];a,b=p['bounds'];mask=(t>=a)&(t<=b)
        tc=t[mask]-p['t_peak'];qd=q[mask]*np.exp(-1j*p['red_w']*tc)
        unscaled=zs_root(tc,qd,points=8192)
        scaled=zs_root(tc,qd*np.sqrt(p['local_gamma_ratio']),points=8192)
        g=p['local_gamma_ratio'];unscaled_f=4*unscaled['eta']/(2*N*N)
        scaled_f=4*scaled['eta']/g/(2*N*N)
        w=2*np.pi*fftfreq(len(t),t[1]-t[0]);carrier=1-w/(W0*T);positive=carrier>0
        gate=np.where(mask,q,0);v=fft(gate);v0=fft(N/np.cosh(t))
        photon=float(np.sum(abs(v[positive])**2/carrier[positive])/np.sum(abs(v0[positive])**2/carrier[positive]))
        base=next(c for c in ref['checkpoints'] if c['zN']==cp['zN'])['leading']
        item=dict(N=N,T0_fs=T,zN=cp['zN'],case=name,carrier_ratio=g,
            unscaled_zs_fraction=unscaled_f,local_zs_energy_fraction=scaled_f,
            gate_energy_fraction=p['f_window'],gate_photon_fraction=photon,
            reference_zs_fraction=base['f_zs'],reference_gate_fraction=base['f_window'],
            unscaled_photon_relative_to_reference=unscaled_f/g/base['f_zs']-1,
            local_zs_photon_relative_to_reference=scaled_f/g/base['f_zs']-1,
            gate_photon_relative_to_reference=photon/base['f_window']-1,
            ideal_sech_unscaled_to_energy_ratio=2*np.sqrt(g)-g,
            unscaled_zs=unscaled,scaled_zs=scaled)
        out['rows'].append(item)
        print(N,T,cp['zN'],'relative photon:',item['unscaled_photon_relative_to_reference'],
              item['local_zs_photon_relative_to_reference'],item['gate_photon_relative_to_reference'],flush=True)
write_json(HERE/'shock_measurement.json',out)
