"""Frozen observable extraction and peak scoring. gpt-c / gpt-6-astra / gpt."""
import json
from pathlib import Path
import numpy as np
from independent import write_json
HERE=Path(__file__).resolve().parent

def quality(c,s):
    p=s.get('leading'); bad=[]
    if p is None:return ['no leading soliton']
    if max(s[k] for k in ['max_time_edge_fraction','max_spectral_edge_fraction',
                         'time_edge_fraction','spectral_edge_fraction'])>1e-6:bad.append('edge')
    if p['zs']['residual']>1e-8:bad.append('ZS residual')
    if p['boundary_intensity_ratio']>1e-3:bad.append('gate boundary')
    if abs(p['zs_window_ratio']-1)>.05:bad.append('gate/ZS disagreement')
    if p['index']!=s['largest_share']['index']:bad.append('reddest is not largest')
    alpha=c.get('loss_db_km',0)*np.log(10)/10000
    drift=(1+s['photon_drift'])*np.exp(alpha*s['length_m'])-1
    if abs(drift)>1e-5:bad.append('invariant')
    if c.get('shock') and s['nonpositive_frequency_fraction']>1e-8:bad.append('negative absolute frequency')
    return bad

def records():
    rows=[]
    for path in HERE.glob('*.json'):
        r=json.loads(path.read_text())
        if not isinstance(r,dict) or 'case' not in r or 'checkpoints' not in r:continue
        c=r['case']
        for s in r['checkpoints']:
            p=s.get('leading');bad=quality(c,s)
            if p is None:continue
            rows.append({'id':c['id'],'N':c['N'],'T0_fs':c['T0_fs'],'zN':s['zN'],
                'model':'physical' if c.get('shock') else 'reference','qualified':not bad,'rejections':bad,
                'f_zs':p['f_zs'],'a':p['f_zs']*np.sqrt(c['N']),'f_gate':p['f_window'],
                'E_zs_nJ':p['energy_zs_nJ'],'E_gate_nJ':p['f_window']*s['energy_launch_nJ'],
                'T1_fit_fs':p['fit_width_fs'],'T1_area_fs':p['area_width_fs'],
                'photon_fraction':p['f_photon_window']/s['initial_photon_energy_equivalent_ratio'],
                'centroid_nm':p['lambda_nm'],'length_m':s['length_m'],'dt_fs':s['dt_fs'],
                'time_edge':max(s['max_time_edge_fraction'],s['time_edge_fraction']),
                'spectral_edge':max(s['max_spectral_edge_fraction'],s['spectral_edge_fraction']),
                'invariant_quantity':'photons' if c.get('shock') else 'energy',
                'loss_corrected_invariant_drift':(1+s['photon_drift'])*np.exp(c.get('loss_db_km',0)*np.log(10)/10000*s['length_m'])-1,
                'global_support_1200_4000nm':s['global_spectral_fraction_1200_4000nm'],
                'leading_support_1200_4000nm':p['spectral_fraction_1200_4000nm'],
                'global_support_1500_3000nm':s['global_spectral_fraction_1500_3000nm'],
                'leading_support_1500_3000nm':p['spectral_fraction_1500_3000nm'],
                'gate_boundary_ratio':p['boundary_intensity_ratio'],'ZS_gate_ratio':p['zs_window_ratio'],
                'local_dispersion_variation_one_rms':p['relative_dispersion_variation_one_rms'],
                'sech_fit_relative_l2':p['sech_fit_relative_l2'],
                'nonpositive_frequency_fraction':s['nonpositive_frequency_fraction'],
                'case':c})
    return rows

def parabola(x,y):
    z=np.polyfit(x,y,2)
    if z[0]>=0:return None
    xp=-z[1]/(2*z[0])
    if not min(x)<xp<max(x):return None
    return float(xp),float(np.polyval(z,xp))

def score(value,interval,pred,tol):
    lo,hi=pred*(1-tol),pred*(1+tol)
    status='pass' if interval[0]>=lo and interval[1]<=hi else ('fail' if interval[1]<lo or interval[0]>hi else 'unresolved bracket')
    return {'prediction':pred,'tolerance_relative':tol,'prediction_interval':[lo,hi],
        'measured':value,'measurement_interval':interval,'relative_error':value/pred-1,'verdict':status}

def main():
    rs=records(); pars=json.loads((HERE/'response_only.json').read_text()); peaks=[]
    for model in ['physical','reference']:
        for N in [3,4,5,6]:
            r=sorted([x for x in rs if x['model']==model and x['N']==N and x['zN']==4 and x['qualified'] and not x['id'].startswith('control')],key=lambda x:x['T0_fs'])
            if len(r)<3:continue
            j=int(np.argmax([x['a'] for x in r])); pred=next(x for x in pars['predictions'] if x['N']==N)
            if j in [0,len(r)-1]:
                peaks.append({'model':model,'N':N,'bracketed':False,'best':r[j]['id'],'edge':'lower' if j==0 else 'upper'});continue
            tri=r[j-1:j+2];T=np.array([x['T0_fs'] for x in tri]);a=np.array([x['a'] for x in tri])
            fit=parabola(np.log(T),a);ordinary=parabola(T,a)
            if fit is None:continue
            tp,ap=np.exp(fit[0]),fit[1]
            # Full neighbors retained for location uncertainty; fit-coordinate
            # sensitivity plus frozen convergence allowance for peak height.
            au=max(abs(ap-(ordinary[1] if ordinary else max(a))),.002*ap)
            bracket=[float(min(T)),float(max(T))]
            def interp(k):return float(np.interp(np.log(tp),np.log(T),[x[k] for x in tri]))
            ep=2*N*N*18900/(.0021*tp)*1e-6*ap/np.sqrt(N)
            ei=[min(x['E_zs_nJ'] for x in tri)*.998,max(x['E_zs_nJ'] for x in tri)*1.002]
            p={'model':model,'N':N,'bracketed':True,'bracket_ids':[x['id'] for x in tri],
               'best_sample':r[j]['id'],'T0_fs':float(tp),'T0_bracket_fs':bracket,'scaled_share':ap,
               'scaled_share_interval':[ap-au,ap+au],'ordinary_T_fit':ordinary,
               'energy_nJ':ep,'energy_interval_nJ':ei,'share':ap/np.sqrt(N),
               'fit_width_fs':interp('T1_fit_fs'),'area_width_fs':interp('T1_area_fs'),
               'length_m':float(4*tp*tp/(N*18900)),
               'launch_energy_nJ':float(2*N*N*18900/(.0021*tp)*1e-6),
               'gated_share':interp('f_gate'),'gated_energy_nJ':interp('E_gate_nJ'),
               'photon_fraction':interp('photon_fraction'),'centroid_nm':interp('centroid_nm'),
               'y_gain':N*N*pars['gain_inverse_angular_frequency_fs']/tp,
               'scores':{'share':score(ap,[ap-au,ap+au],pred['scaled_share'],.10),
                         'position':score(float(tp),bracket,pred['T0_fs'],.30),
                         'energy':score(ep,ei,pred['energy_nJ'],.45)}}
            for k,field in [('width_fit','T1_fit_fs'),('width_area','T1_area_fs')]:
                iv=[min(x[field] for x in tri)*.99,max(x[field] for x in tri)*1.01]
                p['scores'][k]=score(interp(field),iv,pars['overlap_max_fs'],.15)
            peaks.append(p)
    write_json(HERE/'analysis.json',{'agent':'gpt-c','model':'gpt-6-astra','family':'gpt','rows':rs,'peaks':peaks})
    for p in peaks:print(p['model'],p['N'],p.get('T0_fs'),p.get('scaled_share'),{k:v['verdict'] for k,v in p.get('scores',{}).items()})
if __name__=='__main__':main()
