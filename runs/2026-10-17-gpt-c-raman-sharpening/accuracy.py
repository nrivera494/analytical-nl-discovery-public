"""Convergence and cross-solver summaries. gpt-c / gpt-6-astra / gpt."""
import json
from pathlib import Path
import numpy as np
from independent import RAW,write_json,census
HERE=Path(__file__).resolve().parent
IDENT={'agent':'gpt-c','model':'gpt-6-astra','family':'gpt'}
def case(name):
    p=HERE/(name+'.json');return json.loads(p.read_text()) if p.exists() else None

def main():
    out=dict(IDENT,run_id=HERE.name,grid_window_tolerance=[],fixed_step={},shooting=[],kernel=[],library={},response_specific=[],raman_time_scaling=[],physical_specific=[],wide_window_late_drift=[])
    for N,T in [(4,200),(8,620),(16,1875)]:
        prefix=f'bw_sech_N{N}_T{T:.3f}'
        base=case(prefix+'_baseline')
        if not base:continue
        for mode in ['fine','wide','tight']:
            other=case(prefix+'_'+mode)
            if not other:continue
            for z in base['checkpoints']:
                match=[v for v in other['checkpoints'] if v['zN']==z['zN']]
                if not match:continue
                v=match[0];p=z['leading'];q=v['leading']
                out['grid_window_tolerance'].append({'N':N,'T0_fs':T,'zN':z['zN'],'mode':mode,
                    'f1_difference':q['f_zs']-p['f_zs'],'scaled_share_difference':float(np.sqrt(N)*(q['f_zs']-p['f_zs'])),
                    'fit_width_difference_fs':q['fit_width_fs']-p['fit_width_fs'],
                    'max_edge':max(z['max_time_edge_fraction'],z['max_spectral_edge_fraction'],v['max_time_edge_fraction'],v['max_spectral_edge_fraction']),
                    'cases':[base['case']['id'],other['case']['id']]})
    for file in list(HERE.glob('*_response_fine.json'))+list(HERE.glob('*_response_wide.json')):
        other=json.loads(file.read_text());base=case(other['case']['base_case'])
        if not base:continue
        for z in base['checkpoints']:
            vv=[v for v in other['checkpoints'] if v['zN']==z['zN']]
            if not vv:continue
            v=vv[0];p=z['leading'];q=v['leading']
            out['response_specific'].append(dict(response=base['case']['raman'],shape=base['case']['shape'],N=base['case']['N'],
                zN=z['zN'],control='wide' if file.stem.endswith('_wide') else 'fine',relative_share_change=q['f_zs']/p['f_zs']-1,
                scaled_share_difference=float(np.sqrt(base['case']['N'])*(q['f_zs']-p['f_zs'])),
                relative_fit_width_change=q['fit_width_fs']/p['fit_width_fs']-1,
                max_edge=max(z['max_time_edge_fraction'],z['max_spectral_edge_fraction'],v['max_time_edge_fraction'],v['max_spectral_edge_fraction']),
                cases=[base['case']['id'],other['case']['id']]))
        if file.stem.endswith('_wide'):
            clean=[z for z in other['checkpoints'] if max(z['max_time_edge_fraction'],z['max_spectral_edge_fraction'])<1e-6 and z.get('leading')]
            if len(clean)>=2:
                a,b=clean[-2:]
                out['wide_window_late_drift'].append(dict(case=other['case']['id'],zN_pair=[a['zN'],b['zN']],
                    relative_share_change=b['leading']['f_zs']/a['leading']['f_zs']-1,
                    relative_fit_width_change=b['leading']['fit_width_fs']/a['leading']['fit_width_fs']-1))
    for file in HERE.glob('*_physical_fine.json'):
        other=json.loads(file.read_text());base=case(other['case']['base_case'])
        if not base:continue
        for z in base['checkpoints']:
            vv=[v for v in other['checkpoints'] if v['zN']==z['zN']]
            if not vv:continue
            v=vv[0];p=z['leading'];q=v['leading']
            rs=q['f_zs']/p['f_zs']-1;rg=q['f_window']/p['f_window']-1
            out['physical_specific'].append(dict(N=base['case']['N'],T0_fs=base['case']['T0_fs'],zN=z['zN'],
                relative_ZS_energy_change=rs,relative_gated_energy_change=rg,
                prediction_0p2pct_pass=max(abs(rs),abs(rg))<.002,
                max_edge=max(z['max_time_edge_fraction'],z['max_spectral_edge_fraction'],v['max_time_edge_fraction'],v['max_spectral_edge_fraction']),
                cases=[base['case']['id'],other['case']['id']]))
    fields=[]
    for h in [.0004,.0002,.0001,.00005]:
        name=f'bw_sech_N4_T200.000_step{h:g}'
        p=RAW/(name+'_zN3.npz')
        if p.exists():
            a=np.load(p);fields.append((h,a['q'].copy(),name))
    if len(fields)>=3:
        diffs=[float(np.linalg.norm(a[1]-b[1])/np.linalg.norm(b[1])) for a,b in zip(fields[:-1],fields[1:])]
        out['fixed_step']={'steps':[v[0] for v in fields],'successive_field_differences':diffs,
            'observed_orders':[float(np.log2(a/b)) for a,b in zip(diffs[:-1],diffs[1:])],'cases':[v[2] for v in fields]}
    for n in [8192,16384,32768]:
        a=case(f'bw_sech_N4_T200.000_kernelanalytic_n{n}');b=case(f'bw_sech_N4_T200.000_kernelsampled_normalized_n{n}')
        if a and b and a['checkpoints'] and b['checkpoints']:
            x=a['checkpoints'][-1];y=b['checkpoints'][-1]
            out['kernel'].append({'n':n,'dt_fs':x['dt_fs'],'share_difference':y['leading']['f_zs']-x['leading']['f_zs'],'cases':[a['case']['id'],b['case']['id']]})
    for name,zn in [('bw_sech_N4_T200.000_baseline',4),('bw_sech_N16_T1875.000_fine',1.4)]:
        r=case(name);raw=RAW/(name+'_zN'+str(zn)+'.npz')
        if not r or not raw.exists():continue
        a=np.load(raw);cs=[]
        for points in [1024,2048,4096,8192]:
            c=dict(r['case'],zs_points=points);v=census(a['t'],a['q'],c)['leading'];cs.append({'points':points,'f1':v['f_zs']})
        d=[abs(a['f1']-b['f1']) for a,b in zip(cs[:-1],cs[1:])]
        out['shooting'].append({'case':name,'zN':zn,'results':cs,'successive_differences':d,'observed_orders':[float(np.log2(a/b)) for a,b in zip(d[:-1],d[1:])]})
    base=case('bw_sech_N4_T200.000_baseline');scaled=case('bw_sech_N4_T400.000_times2')
    if base and scaled:
        for z in base['checkpoints']:
            vv=[v for v in scaled['checkpoints'] if v['zN']==z['zN']]
            if not vv:continue
            v=vv[0];a=z['leading'];b=v['leading']
            raw1=RAW/(base['case']['id']+'_zN'+str(z['zN'])+'.npz');raw2=RAW/(scaled['case']['id']+'_zN'+str(z['zN'])+'.npz')
            x=np.load(raw1)['q'];y=np.load(raw2)['q'][::2]
            out['raman_time_scaling'].append(dict(zN=z['zN'],share_difference=b['f_zs']-a['f_zs'],
                fitted_width_ratio=b['fit_width_fs']/a['fit_width_fs'],area_width_ratio=b['area_width_fs']/a['area_width_fs'],
                common_grid_field_relative_error=float(np.linalg.norm(x-y)/np.linalg.norm(x)),
                cases=[base['case']['id'],scaled['case']['id']]))
    p=RAW/'library_gaussian_N4_T200_zN3.csv';r=case('library_matched_gaussian_N4_T200')
    if p.exists() and r and r['checkpoints']:
        arr=np.loadtxt(p,delimiter=',');q=arr[:,1]+1j*arr[:,2]
        b=np.load(RAW/'library_matched_gaussian_N4_T200_zN3.npz');ref=b['q'];t=b['t']
        variants={'direct':q,'reversed':q[(-np.arange(len(q)))%len(q)],'conjugated':q.conj()}
        errors={k:float(np.linalg.norm(v-ref)/np.linalg.norm(ref)) for k,v in variants.items()};best=min(errors,key=errors.get)
        c=r['case'];measure=census(t,variants[best],c)['leading'];lead=r['checkpoints'][-1]['leading']
        out['library']={'variant_errors':errors,'matched_variant':best,'relative_field_error':errors[best],
                        'independent_share':lead['f_zs'],'library_share':measure['f_zs'],'share_difference':measure['f_zs']-lead['f_zs'],
                        'solver_commit':'b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa','details':(RAW/'library_crosscheck.txt').read_text()}
    write_json(HERE/'accuracy.json',out)
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
