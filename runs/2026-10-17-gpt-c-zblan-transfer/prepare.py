"""Response-only computations and frozen design; never propagates. gpt-c / gpt-6-astra / gpt."""
import json
from pathlib import Path
import numpy as np
from scipy.integrate import simpson,quad
from scipy.optimize import minimize_scalar
from material import response,time_response,TABLE
HERE=Path(__file__).resolve().parent

def overlap(T,n=8193):
    x=np.linspace(1e-8,18,n)
    return float(np.pi/2*simpson(x**3*(-response(x/T).imag)/np.sinh(np.pi*x/2)**2,x=x))

def main():
    scan=np.geomspace(2,300,150); vals=np.array([overlap(t,4097) for t in scan]);j=np.argmax(vals)
    opt=minimize_scalar(lambda t:-overlap(t),bounds=(scan[j-1],scan[j+1]),method='bounded',options={'xatol':1e-9})
    fine=minimize_scalar(lambda t:-overlap(t,16385),bounds=(scan[j-1],scan[j+1]),method='bounded',options={'xatol':1e-9})
    w=np.linspace(0,.25,10001); jg=np.argmax(-response(w).imag)
    gain=minimize_scalar(lambda a:response(a).imag,bounds=(w[jg-1],w[jg+1]),method='bounded',options={'xatol':1e-12})
    tau=1/gain.x
    data={'agent':'gpt-c','model':'gpt-6-astra','family':'gpt','response_table':TABLE.tolist(),
      'overlap_max_fs':float(opt.x),'overlap_max_quadrature_fine_fs':float(fine.x),'Rmax':float(-opt.fun),
      'overlap_bracket_fs':[float(scan[j-1]),float(scan[j+1])],
      'gain_peak_rad_fs':float(gain.x),'gain_inverse_angular_frequency_fs':float(tau),
      'raman_fraction':.24,'raman_first_moment_fs':float(.24*quad(lambda t:t*time_response(t),0,10000,epsabs=1e-9)[0]),
      'response_norm':float(quad(lambda t:time_response(t),0,10000,epsabs=1e-10)[0]),
      'predictions':[]}
    cases=[]
    for N in [3,4,5,6]:
        T=1.70*tau*N**1.62; a=1.29; E=2*N*N*18900/(.0021*T)*1e-6*a/np.sqrt(N)
        data['predictions'].append({'N':N,'T0_fs':T,'T0_relative_tolerance':.30,'scaled_share':a,
          'scaled_share_relative_tolerance':.10,'energy_nJ':E,'energy_relative_tolerance':.45,
          'exit_width_null_fs':float(opt.x),'exit_width_null_relative_tolerance':.15})
        for physical in [True,False]:
            for fac in [.4,.55,.7,.85,1.,1.2,1.5,2.,2.7]:
                t=T*fac;n=2**int(np.ceil(np.log2(max(8192,96*t/2.5))))
                if n>32768:raise ValueError('grid budget')
                cases.append({'id':f"{'physical' if physical else 'reference'}_N{N}_r{fac:g}",
                  'N':N,'T0_fs':t,'n':n,'width':96.,'tol':2e-9,'raman':'zblan','shape':'sech',
                  'dispersion':'tod' if physical else 'constant','shock':physical,
                  'loss_db_km':50 if physical else 0,'zN':[2.,3.,4.], 'heldout':True})
    (HERE/'response_only.json').write_text(json.dumps(data,indent=2)+'\n')
    (HERE/'cases.json').write_text(json.dumps(cases,indent=2)+'\n')
    print(json.dumps({k:v for k,v in data.items() if k!='response_table'},indent=2))
if __name__=='__main__':main()
