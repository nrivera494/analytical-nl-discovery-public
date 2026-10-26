"""Peak brackets and diagnostic gates. gpt-c / gpt-6-astra / gpt."""
import json,math,sys
from pathlib import Path
from collections import defaultdict
import numpy as np
from independent import write_json,shape_integral,carrier_beta2,GAMMA
HERE=Path(__file__).resolve().parent
IDENT={'agent':'gpt-c','model':'gpt-6-astra','family':'gpt'}

def gate(z,c):
    bad=[];p=z.get('leading')
    if p is None:return ['no-leading-pulse']
    for key in ['max_time_edge_fraction','max_spectral_edge_fraction','time_edge_fraction','spectral_edge_fraction']:
        if z[key]>1e-6:bad.append(key)
    if not p['zs']['success'] or p['zs']['residual']>1e-8:bad.append('ZS-root')
    if p['boundary_intensity_ratio']>1e-3:bad.append('gate-overlap')
    if abs(p['zs_window_ratio']-1)>.05:bad.append('ZS-gate-disagreement')
    if z.get('largest_share') and p['f_zs']<.99*z['largest_share']['f_zs']:bad.append('reddest-not-largest')
    loss=c.get('loss_db_km',0)*np.log(10)/10/1000*z['length_m']
    inv=(1+z['photon_drift'])*np.exp(loss)-1 if c.get('shock') else z['mass_drift']
    if abs(inv)>1e-5:bad.append('invariant')
    if c.get('shock') and z['nonpositive_frequency_fraction']>1e-8:bad.append('nonpositive-frequency')
    return bad

def all_rows():
    rows=[]
    for f in sorted(HERE.glob('*.json')):
        x=json.loads(f.read_text())
        if not isinstance(x,dict) or 'case' not in x:continue
        c=x['case'];prior=None
        for z in x['checkpoints']:
            p=z.get('leading');bad=gate(z,c)
            if p is None:continue
            rel=None if prior is None else abs(p['f_zs']/prior['f_zs']-1)
            row=dict(case=c['id'],response=c.get('raman','bw'),shape=c.get('shape','sech'),N=c['N'],T0_fs=c['T0_fs'],
                     zN=z['zN'],split=c.get('split','control'),f1=p['f_zs'],scaled_share=np.sqrt(c['N'])*p['f_zs'],
                     y=c['N']**2*(15.5 if c.get('raman')=='as2s3' else 12.2)/c['T0_fs'],
                     f_gate=p['f_window'],energy_nJ=p['energy_zs_nJ'],gate_energy_nJ=z['energy_launch_nJ']*p['f_window'],
                     launch_energy_nJ=z['energy_launch_nJ'],photon_fraction=p['f_photon_window']/z['initial_photon_energy_equivalent_ratio'],
                     launch_photon_energy_equivalent_ratio=z['initial_photon_energy_equivalent_ratio'],
                     area_width_fs=p['area_width_fs'],fit_width_fs=p['fit_width_fs'],fwhm_width_fs=p['fwhm_width_fs'],
                     sech_fit_relative_l2=p['sech_fit_relative_l2'],lambda_nm=p['lambda_nm'],length_m=z['length_m'],
                     plateau_relative_change=rel,invalid=bad,dt_fs=z['dt_fs'],n=c['n'],width=c['width'],
                     max_time_edge_fraction=z['max_time_edge_fraction'],max_spectral_edge_fraction=z['max_spectral_edge_fraction'],
                     mass_drift=z['mass_drift'],photon_drift=z['photon_drift'],
                     global_spectral_fraction_1200_2300nm=z['global_spectral_fraction_1200_2300nm'],
                     leading_spectral_fraction_1200_2300nm=p['spectral_fraction_1200_2300nm'],
                     local_beta2_ratio=p['local_beta2_ratio'],local_gamma_ratio=p['local_gamma_ratio'],relative_dispersion_variation_one_rms=p['relative_dispersion_variation_one_rms'],
                     dispersion=c.get('dispersion','constant'),shock=c.get('shock',False),loss_db_km=c.get('loss_db_km',0))
            rows.append(row)
            prior=p if not bad else None
    return rows

def peakfit(points):
    points=sorted(points,key=lambda r:r['T0_fs']);k=int(np.argmax([p['f1'] for p in points]));winner=points[k]
    if k in [0,len(points)-1]:return {'bracketed':False,'best':winner,'sample_count':len(points)}
    tri=points[k-1:k+2];T=np.array([p['T0_fs'] for p in tri]);f=np.array([p['f1'] for p in tri]);u=np.log(T/winner['T0_fs'])
    cs=np.polyfit(u,f,2);us=-cs[1]/(2*cs[0]);Ts=float(winner['T0_fs']*np.exp(us));fs=float(np.polyval(cs,us))
    qs=np.polyfit(T/winner['T0_fs']-1,f,2);v=-qs[1]/(2*qs[0]);Tlin=float(winner['T0_fs']*(1+v))
    if cs[0]>=0 or not T[0]<Ts<T[-1]:return {'bracketed':False,'best':winner,'sample_count':len(points),'interpolation_failure':True}
    out=dict(N=winner['N'],response=winner['response'],shape=winner['shape'],split=winner['split'],zN=winner['zN'],
             bracketed=True,T0_fs=Ts,f1=fs,scaled_share=float(fs*np.sqrt(winner['N'])),y=winner['N']**2*(15.5 if winner['response']=='as2s3' else 12.2)/Ts,
             T_bracket_fs=[float(T[0]),float(T[-1])],sample_T0_fs=winner['T0_fs'],sample_f1=winner['f1'],
             interpolation_T_difference_fs=abs(Ts-Tlin),interpolation_share_difference=abs(fs-float(np.polyval(qs,v))),
             cases=[p['case'] for p in tri],curvature_logT=float(2*cs[0]),sample_count=len(points),
             max_plateau_relative_change=max([p['plateau_relative_change'] or 0 for p in tri]),
             plateau_complete=all(p['plateau_relative_change'] is not None for p in tri),
             dispersion=winner['dispersion'],shock=winner['shock'])
    for key in ['fit_width_fs','area_width_fs','fwhm_width_fs','energy_nJ','gate_energy_nJ','launch_energy_nJ','photon_fraction','launch_photon_energy_equivalent_ratio','length_m','lambda_nm','f_gate','global_spectral_fraction_1200_2300nm','leading_spectral_fraction_1200_2300nm','sech_fit_relative_l2']:
        out[key]=float(np.interp(Ts,T,[p[key] for p in tri])) if all(p[key] is not None for p in tri) else None
    b0=carrier_beta2(winner['dispersion']);S=shape_integral(winner['shape'])
    out['length_m']=winner['zN']/winner['N']*Ts*Ts/b0
    out['launch_energy_nJ']=S*winner['N']**2*b0/(GAMMA*Ts)*1e-6
    out['energy_nJ']=fs*out['launch_energy_nJ']
    out['gate_energy_nJ']=out['f_gate']*out['launch_energy_nJ']
    if winner['dispersion']=='constant' and not winner['shock']:
        out['area_width_fs']=2*Ts/(S*winner['N']**2*fs)
    out['global_spectral_support_min_in_bracket']=min(p['global_spectral_fraction_1200_2300nm'] for p in tri)
    out['leading_spectral_support_min_in_bracket']=min(p['leading_spectral_fraction_1200_2300nm'] for p in tri)
    out['bracket_values']=[{'T0_fs':p['T0_fs'],'scaled_share':p['scaled_share'],'fit_width_fs':p['fit_width_fs'],'area_width_fs':p['area_width_fs']} for p in tri]
    return out

def main():
    rows=all_rows();groups=defaultdict(list)
    for r in rows:
        if r['split'] not in ['calibration','heldout','physical','constrained','matched_shape']:continue
        if r['invalid']:continue
        groups[(r['response'],r['shape'],r['N'],r['zN'],r['dispersion'],r['shock'])].append(r)
    fits=[]
    for key,rs in groups.items():
        # Multiple controls at the same duration do not alter production fit.
        unique={r['T0_fs']:r for r in rs}
        if len(unique)>=3:fits.append(peakfit(list(unique.values())))
    preferred=[]
    gg=defaultdict(list)
    for p in fits:
        if p.get('bracketed'):
            gg[(p['response'],p['shape'],p['N'],p['dispersion'],p['shock'])].append(p)
    for key,ps in gg.items():
        latest=max(ps,key=lambda p:p['zN'])
        if latest['plateau_complete'] and latest['max_plateau_relative_change']<=.005:
            preferred.append(latest)
    out=dict(IDENT,run_id=HERE.name,status='completed' if '--final' in sys.argv else 'in-progress',rows=rows,peak_fits=fits,preferred_peaks=preferred)
    write_json(HERE/'summary.json',out)
    print('cases',len(set(r['case'] for r in rows)),'rows',len(rows),'preferred peaks',len(preferred))
    for p in sorted(preferred,key=lambda x:(x['response'],x['shape'],x['N'])):
        print(p['response'],p['shape'],p['N'],'T*',round(p['T0_fs'],3),'a',round(p['scaled_share'],6),'bracket',p['T_bracket_fs'],'zN',p['zN'])
if __name__=='__main__':main()
