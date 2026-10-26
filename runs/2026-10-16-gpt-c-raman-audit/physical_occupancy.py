"""Band-support and loss-corrected invariant checks. gpt-c/gpt-6-astra/gpt."""
from pathlib import Path
import json
import numpy as np
from scipy.fft import fft,ifft,fftfreq
from independent import RAW,W0,K,write_json,beta2_local
HERE=Path(__file__).resolve().parent
out=dict(agent='gpt-c',model='gpt-6-astra',family='gpt',rows=[])
for path in sorted(HERE.glob('*.json')):
    r=json.loads(path.read_text())
    if not isinstance(r,dict) or 'checkpoints' not in r or 'case' not in r:continue
    c=r['case']
    if c.get('dispersion') not in ['smf','measured','tod'] and not c.get('shock'):continue
    for cp in r['checkpoints']:
        data=np.load(RAW/(c['id']+'_zN'+str(cp['zN'])+'.npz'))
        t,q=data['t'],data['q'];dt=t[1]-t[0]
        w=2*np.pi*fftfreq(len(q),dt);power=abs(fft(q))**2;omega=W0-w/c['T0_fs']
        fractions={}
        positive=omega>0
        power0=abs(fft(c['N']/np.cosh(t)))**2
        photon0=float(np.sum(power0[positive]*W0/omega[positive]))
        fractions['initial_photon_energy_equivalent_ratio']=photon0/float(np.sum(power0))
        if cp['leading'] is not None:
            a,b=cp['leading']['bounds'];mask=(t>=a)&(t<=b);gate=q*mask;gpower=abs(fft(gate))**2
            fractions['leading_photon_fraction_exact']=float(np.sum(gpower[positive]*W0/omega[positive])/photon0)
            carrier_ratio=1-cp['leading']['red_w']/(W0*c['T0_fs'])
            fractions['leading_photon_fraction_centroid_zs']=cp['leading']['f_zs']/carrier_ratio/fractions['initial_photon_energy_equivalent_ratio'] if carrier_ratio>0 else None
            wc=cp['leading']['red_w'];dq=ifft(1j*w*fft(q))
            rms=float(np.sqrt(np.trapezoid(abs(dq[mask]-1j*wc*q[mask])**2,t[mask])/np.trapezoid(abs(q[mask])**2,t[mask])))
            b0=cp['leading']['local_beta2_ratio'];disp=c.get('dispersion','constant')
            bp,bm=[beta2_local(wc+v*rms,c['T0_fs'],disp) for v in [-1,1]]
            fractions['leading_rms_frequency_from_bulk_gradient']=rms
            fractions['relative_dispersion_variation_bulk_gradient']=float(max(abs(bp-b0),abs(bm-b0))/b0) if np.isfinite(bp) and np.isfinite(bm) else None
        for lo,hi in [(1200,2300),(1260,2300),(800,3000)]:
            mask=(omega>=K/hi)&(omega<=K/lo)
            fractions[f'global_spectral_fraction_{lo}_{hi}nm']=float(np.sum(power[mask])/np.sum(power))
        alpha=c.get('loss_db_km',0)*np.log(10)/10/1000
        invariant='photon_drift' if c.get('shock') else 'mass_drift'
        out['rows'].append(dict(case=c['id'],zN=cp['zN'],length_m=cp['length_m'],
              invariant=invariant,loss_corrected_drift=float((1+cp[invariant])*np.exp(alpha*cp['length_m'])-1),
              nonpositive_frequency_fraction=float(np.sum(power[omega<=0])/np.sum(power)),**fractions))
write_json(HERE/'physical_occupancy.json',out)
print('physical checkpoints',len(out['rows']))
