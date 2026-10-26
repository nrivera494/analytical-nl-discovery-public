"""Compare independent and repository forward maps. gpt-c/gpt-6-astra/gpt."""
from pathlib import Path
import numpy as np
from scipy.interpolate import CubicSpline
from independent import RAW,census,write_json

HERE=Path(__file__).resolve().parent
data=np.loadtxt(RAW/'library_N4_T200_zN3.csv',delimiter=',')
t=data[:,0];q=data[:,1]+1j*data[:,2]
case={'N':4,'T0_fs':200,'width':96,'n':16384,'shock':True,'raman':'bw'}
reference=np.load(RAW/'library_python_N4_T200_zN3_zN3.npz')
qpy=CubicSpline(reference['t'],reference['q'])(t)
phase=np.angle(np.vdot(qpy,q))
res={'agent':'gpt-c','model':'gpt-6-astra','family':'gpt','case':case,
     'solver_commit':'b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa',
     'relative_field_error':float(np.linalg.norm(q-qpy)/np.linalg.norm(qpy)),
     'phase_aligned_field_error':float(np.linalg.norm(q*np.exp(-1j*phase)-qpy)/np.linalg.norm(qpy)),
     'library':census(t,q,case),'independent':census(t,qpy,case),
     'library_step_LD':1e-4,'library_stats':(RAW/'library_crosscheck.txt').read_text()}
res['leading_fraction_difference']=res['library']['leading']['f_zs']-res['independent']['leading']['f_zs']
res['kernel_sampling_comparisons']=[]
for variant in ['sampled_raw','sampled_normalized']:
    name='library_python_'+variant+'_N4_T200_zN3'
    path=RAW/(name+'_zN3.npz')
    if not path.exists():continue
    data=np.load(path);qv=CubicSpline(data['t'],data['q'])(t)
    ph=np.angle(np.vdot(qv,q));measured=census(t,qv,case)
    res['kernel_sampling_comparisons'].append(dict(case=name,
        relative_field_error=float(np.linalg.norm(q-qv)/np.linalg.norm(qv)),
        phase_aligned_field_error=float(np.linalg.norm(q*np.exp(-1j*ph)-qv)/np.linalg.norm(qv)),
        leading_fraction_difference=res['library']['leading']['f_zs']-measured['leading']['f_zs'],
        independent=measured))
tt=np.arange(len(t))*(t[1]-t[0])*200;a,b=1/32.,1/12.2
res['sampled_kernel_dc_before_normalization']=float((tt[1]-tt[0])*np.sum((a*a+b*b)/b*np.exp(-a*tt)*np.sin(b*tt)))
write_json(HERE/'library_comparison.json',res)
print({k:v for k,v in res.items() if k not in ['library','independent','library_stats','kernel_sampling_comparisons']})
print([{k:v for k,v in r.items() if k!='independent'} for r in res['kernel_sampling_comparisons']])
