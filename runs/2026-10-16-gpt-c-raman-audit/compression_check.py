"""Check the claim's integrable first-compression premise. gpt-c/gpt-6-astra/gpt."""
from pathlib import Path
import sys
import numpy as np
from scipy.fft import fft,fftfreq
from independent import propagate,write_json
from run_audit import guard
HERE=Path(__file__).resolve().parent
out=dict(agent='gpt-c',model='gpt-6-astra',family='gpt',rows=[])
for N in ([int(x) for x in sys.argv[1:]] or [2,3,4,6,8]):
    guard()
    checkpoints=np.linspace(.1,3.5,171).tolist()
    case=dict(N=N,T0_fs=200,raman='off',n=16384,width=80,tol=1e-9,zN=checkpoints)
    rows=[]
    def cb(t,q,s):
        I=abs(q)**2;j=int(np.argmax(I));a=b=j
        while a>0 and I[a]>I[j]/2:a-=1
        while b<len(t)-1 and I[b]>I[j]/2:b+=1
        rows.append(dict(zN=s['zN'],peak_amplitude=float(abs(q[j])),peak_t_over_T0=float(t[j]),
             central_amplitude=float(abs(q[len(t)//2])),FWHM_T0=float(t[b]-t[a]),
             mass_drift=s['mass_drift'],max_spectral_edge_fraction=s['max_spectral_edge_fraction']))
    propagate(case,cb)
    # This finite interval contains the first compression; identify its first local maximum.
    js=[j for j in range(1,len(rows)-1) if rows[j]['peak_amplitude']>rows[j-1]['peak_amplitude'] and rows[j]['peak_amplitude']>=rows[j+1]['peak_amplitude']]
    first=rows[js[0]] if js else None
    item=dict(N=N,case=case,checkpoints=rows,first_compression=first,
        claimed_peak_amplitude=N*N,maximum_sampled=max(rows,key=lambda x:x['peak_amplitude']))
    if first is not None:
        guard()
        fine_case=dict(case,n=32768,tol=1e-10,zN=np.linspace(first['zN']-.04,first['zN']+.04,81).tolist())
        rows=[]
        propagate(fine_case,cb)
        item['fine_case']=fine_case;item['fine_checkpoints']=rows
        item['fine_compression']=max(rows,key=lambda x:x['peak_amplitude'])
    out['rows'].append(item)
    write_json(HERE/'compression_check.json',out)
    print(N,first,flush=True)
