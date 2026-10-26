"""Numerical error orders and alternative integrator. gpt-c / gpt-6-astra / gpt."""
import json,time,resource,hashlib
from pathlib import Path
import numpy as np
from scipy.fft import fft,ifft,fftfreq
from independent import RAW,write_json,response,census
from material import time_response
from run_serial import guard
HERE=Path(__file__).resolve().parent

def main():
    guard();out={'agent':'gpt-c','model':'gpt-6-astra','family':'gpt','controls':[],
                'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    for p in HERE.glob('control_*.json'):
        x=json.loads(p.read_text())
        if not isinstance(x,dict) or 'case' not in x:continue
        c=x['case'];bid=c.get('control_reference')
        if not bid:continue
        b=json.loads((HERE/(bid+'.json')).read_text())
        for v in x['checkpoints']:
            if v['zN']!=4:continue
            a=next(s for s in b['checkpoints'] if s['zN']==4)
            q,pulse=v['leading'],a['leading']
            ds={k:float(q[k]/pulse[k]-1) for k in ['f_zs','f_window','fit_width_fs','area_width_fs']}
            out['controls'].append({'id':c['id'],'base':bid,'dt_fs':v['dt_fs'],
                'relative_changes':ds,'pass':max(abs(ds[k]) for k in ['f_zs','f_window'])<.002 and
                max(abs(ds[k]) for k in ['fit_width_fs','area_width_fs'])<.01})
    fields=[]
    for h in [4e-4,2e-4,1e-4,5e-5]:
        name=f'control_fixed_h{h:g}';p=RAW/(name+'_zN2.0.npz')
        if p.exists():fields.append((h,np.load(p)['q'].copy()))
    if len(fields)==4:
        diff=[float(np.linalg.norm(a[1]-b[1])/np.linalg.norm(b[1])) for a,b in zip(fields[:-1],fields[1:])]
        orders=[float(np.log2(a/b)) for a,b in zip(diff[:-1],diff[1:])]
        out['rk4ip']={'steps':[x[0] for x in fields],'successive_field_differences':diff,
                      'orders':orders,'pass':all(3.5<p<4.5 for p in orders)}
    out['kernel']=[]
    for dt in [3.,1.5,.75,.375]:
        t=np.arange(32768)*dt;w=2*np.pi*fftfreq(len(t),dt)
        h=time_response(t);H=fft(h)*dt;norm=float(H[0].real);H/=norm
        exact,_=response(w,1,'zblan');band=abs(w)<.3
        out['kernel'].append({'dt_fs':dt,'integral_before_normalizing':norm,
            'max_error_below_0p3_rad_fs':float(max(abs(H[band]-exact[band])))})
    err=[x['max_error_below_0p3_rad_fs'] for x in out['kernel']]
    out['kernel_orders']=[float(np.log2(a/b)) for a,b in zip(err[:-1],err[1:])]
    out['kernel_pass']=all(1.8<p<2.2 for p in out['kernel_orders'][-2:])
    peaks=json.loads((HERE/'analysis.json').read_text())['peaks'];out['shooting']=[]
    for N in [3,6]:
        p=next(x for x in peaks if x['N']==N and x['model']=='physical' and x['bracketed'])
        name=p['best_sample'];r=json.loads((HERE/(name+'.json')).read_text());raw=np.load(RAW/(name+'_zN4.0.npz'))
        rows=[]
        for n in [1024,2048,4096,8192]:
            c=dict(r['case'],zs_points=n);v=census(raw['t'],raw['q'],c)['leading']
            rows.append({'points':n,'f1':v['f_zs'],'residual':v['zs']['residual']})
        diff=[abs(a['f1']-b['f1']) for a,b in zip(rows[:-1],rows[1:])]
        orders=[float(np.log2(a/b)) for a,b in zip(diff[:-1],diff[1:])]
        out['shooting'].append({'case':name,'rows':rows,'successive_differences':diff,'orders':orders,
                                'pass':all(1.8<p<2.2 for p in orders)})
    if len(fields)==4:
        guard();base=json.loads((HERE/'control_fixed_h5e-05.json').read_text())['case']
        n=base['n'];dt=base['width']/n;t=(np.arange(n)-n//2)*dt;w=2*np.pi*fftfreq(n,dt)
        H,fR=response(w,base['T0_fs'],'zblan');strang=[];start=time.monotonic()
        for h in [4e-4,2e-4,1e-4]:
            q=base['N']/np.cosh(t);end=2/base['N'];steps=int(round(end/h));h=end/steps
            half=np.exp(-.25j*w*w*h)
            for j in range(steps):
                q=ifft(half*fft(q));I=abs(q)**2
                q=q*np.exp(1j*h*((1-fR)*I+fR*ifft(H*fft(I)).real))
                q=ifft(half*fft(q))
            strang.append((h,q));np.savez(RAW/f'strang_h{h:g}.npz',t=t,q=q)
        diff=[float(np.linalg.norm(a[1]-b[1])/np.linalg.norm(b[1])) for a,b in zip(strang[:-1],strang[1:])]
        order=float(np.log2(diff[0]/diff[1]));error=float(np.linalg.norm(strang[-1][1]-fields[-1][1])/np.linalg.norm(fields[-1][1]))
        out['strang']={'steps':[x[0] for x in strang],'differences':diff,'order':order,
                       'relative_field_error_to_rk4ip':error,'pass':1.8<order<2.2 and error<1e-3,
                       'wall_seconds':time.monotonic()-start}
    out['peak_rss_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    lib=RAW/'library_zblan_N4_T200_zN2.csv';py=RAW/'control_library_matched_zN2.0.npz'
    if lib.exists() and py.exists():
        v=np.loadtxt(lib,delimiter=',');q=v[:,1]+1j*v[:,2];r=np.load(py)
        error=float(np.linalg.norm(q-r['q'])/np.linalg.norm(r['q']))
        out['library']={'relative_field_error':error,'time_grid_error':float(max(abs(v[:,0]-r['t']))),
                        'pass':error<1e-6,'solver_commit':'b9fa957f922b9cae20b2a2e4c4ff45c1bc8768aa',
                        'details':(RAW/'library_crosscheck.txt').read_text()}
    write_json(HERE/'accuracy.json',out)
    print(json.dumps({k:v for k,v in out.items() if k!='controls'},indent=2))
    print('Physical controls:',sum(x['pass'] for x in out['controls']),'/',len(out['controls']))
if __name__=='__main__':main()
